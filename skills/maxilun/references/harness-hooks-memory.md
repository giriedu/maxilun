# Harness Hooks, Memory, and Context Budget

<!-- metadata:
  version: "1.3.0"
  sync_target: "skills/maxilun/SKILL.md"
  origin: "Maxilun Harness Engine"
-->

How Maxilun turns its rules into mechanisms that run whether or not the model remembers them: lifecycle hooks as enforcement points, a bounded memory that survives context loss, a context budget that decides when to checkpoint, and a rule-layering order that keeps specific guidance from eroding the Core Rules. `harness-engineering.md` defines the ledgers and gates; this file defines where and when the harness enforces them.

---

## 1. Prose, Hook, or CI: Where a Rule Lives

A rule written only in a prompt is a request. A rule the harness executes is a guarantee. Put each rule at the cheapest layer that can actually enforce it.

| The rule... | Layer | Why |
|---|---|---|
| Needs judgment (naming, design trade-offs, scope) | Prose in `SKILL.md` / references | No script can decide it |
| Is a deterministic predicate on one tool call (forbidden flag, protected file, secret pattern) | Pre-tool hook, blocking | Stops the damage before it happens |
| Is a deterministic predicate on the edited result (format, types, debug statements) | Post-tool accumulate, Stop-time batch check | One run per turn instead of one per edit |
| Must hold for every contributor, human or agent | CI and the repository's own git hooks | Hooks are local and can be disabled; CI cannot be skipped by the agent |
| Concerns session continuity (state, checkpoints) | Session-start, pre-compact, stop hooks | Fire exactly at the moments context is created or destroyed |

Rules:

1. A rule that keeps getting violated in prose and is mechanically checkable gets promoted to a hook. A hook that needs judgment to avoid false positives gets demoted back to prose.
2. Hooks never replace `maxilun-verify` proof. A green hook is a filter; the evidence gate in `SKILL.md` §6 still requires the real test or build output.
3. One rule, one enforcement point. The same check in a hook, a skill, and CI with three slightly different patterns is three sources of drift.

## 2. Lifecycle Event Map

| Event | Allowed work | Blocking? | Must not |
|---|---|---|---|
| Session start | Load a bounded excerpt of the previous checkpoint and lessons; detect the toolchain from manifests | No | Inject unbounded history; scan the home directory; call the network |
| Prompt submit | Measure context occupancy; inject a one-time checkpoint order above the hard threshold | No (guidance only) | Rewrite the user's words; re-nag every turn |
| Pre-tool | Guards: forbidden flags, protected files, secret patterns, first-edit evidence gate | Yes, on a deterministic match | Run slow checks (type checker, test suite) |
| Post-tool | Record the edited path to a session-scoped list; cheap observation | No | Format or typecheck per edit; mutate files the agent did not touch |
| Pre-compact | Write the checkpoint file before the window is summarized | No | Depend on the model to remember to do it |
| Stop | Batch format/typecheck over the accumulated paths; debug-statement audit; persist the ledger | Yes, when the batch check fails | Send notifications or telemetry by default |
| Session end | Clean up session-scoped temp files; final ledger flush | No | Delete anything outside the session's own files |

Exit semantics stay uniform across every hook: success allows, a dedicated block code stops the tool call and returns a reason to the model, anything written to stderr without the block code is a warning. A block message always states what was detected, why it is blocked, and the allowed alternative, in one short paragraph; a bare "denied" teaches the model to retry blindly.

## 3. Hook Runtime Discipline

Hooks run on every tool call with the user's privileges. Treat them as production code on the hot path.

1. **Latency budget.** Pre-tool guards finish in well under a second. Anything slower moves to Stop or to an asynchronous post-tool job.
2. **Bounded input.** Read the event payload from stdin with a byte cap and an idle timeout. A hook that waits forever on an unclosed stdin stalls the whole session.
3. **Fail mode is a declared property, not an accident.**
   - Safety guards (protected config, bypass flags, secret write) fail **closed**: if the payload is truncated or unparseable, block and say why.
   - Advisory and observation hooks fail **open**: an error is logged and the tool call proceeds.
4. **Profiles and per-hook switches.** Ship hooks in profiles (`minimal`, `standard`, `strict`) and give every hook a stable ID that can be disabled individually through configuration. Disabling one guard must never silently disable its siblings.
5. **Sanitize identifiers.** A session ID or path embedded in a temp filename is reduced to `[A-Za-z0-9_-]` and length-capped; temp files live in the OS temp directory or `.maxilun/`, never in the project root.
6. **Idempotent installation.** Installed hook entries carry stable IDs so reinstalling updates in place and uninstalling removes only Maxilun-owned entries, leaving the user's own hooks intact. If hook metadata lives beside the executable config, a validation step fails the build when the two drift.
7. **Concurrency.** Hooks for parallel tool calls run concurrently. Append-only writes of one line per record are safe; read-modify-write of a shared JSON file is not without a lock.

## 4. Pre-Action Guards Worth Having

### 4.1 Evidence-before-edit gate

Self-assessment ("are you sure this is safe?") reliably returns "yes". Asking for facts that can only be obtained by looking forces the look. On the **first** edit of a given file in a session, the gate denies once and asks for:

1. The importers of the file (from `maxilun-knowledge-graph` `importersOf:` or a precise search).
2. The public symbols the change affects.
3. The shape of any data file the code reads or writes, with synthetic values.
4. The user's current instruction, quoted.

For a new file the questions become: who calls it, and proof that no existing file already serves the purpose. After the facts are presented, the same file is allowed for the rest of the session. This is the mechanical form of "Locate, then read" in `SKILL.md` §3; when a handoff packet already carries a Read plan covering the file, the gate accepts the packet as the evidence. Cap the gate at one denial per file so it cannot loop.

### 4.2 Protected configuration

Agents under pressure to make a check pass edit the check instead of the code: relaxing a lint rule, widening a type-checker exclusion, skipping a test file in the runner config. Block modification of existing lint, formatter, type-checker, and test-runner configuration files unless the unit's `WRITE SET` names them explicitly. Creating such a file in a project that has none is allowed.

### 4.3 Bypass flags

Block flags whose only purpose is to skip the repository's own safety net: commit or push with verification disabled, overriding the git hooks path inline, force-pushing a protected branch. A static scan of the command string catches the usual spellings; it cannot catch a bypass assembled at run time (variables, decoding, generated scripts). State that limit in the hook's own documentation rather than claiming completeness.

### 4.4 What not to guard in pre-tool

Style preferences, file naming, documentation placement, "consider using a terminal multiplexer" reminders. These are advisory at best; as blocking hooks they train the model to route around the harness, and as warnings on every call they are noise that consumes context.

## 5. Accumulate, Then Verify Once

Per-edit formatting and type checking multiply latency by the number of edits and fight with in-progress multi-file changes that are temporarily inconsistent. The pattern:

1. Post-tool: append the edited path to a session-scoped list (one line, append-only).
2. Stop: deduplicate the list, group by toolchain, and run each formatter or checker once over its group.
3. On failure, return the exact diagnostics with `file:line` to the model as a block reason, so the next turn fixes them before yielding.

```python
# stop_batch_check.py: run once per turn over files edited this turn
import json, os, subprocess, sys, tempfile, re

payload = json.loads(sys.stdin.read(1_000_000) or "{}")
sid = re.sub(r"[^A-Za-z0-9_-]", "_", str(payload.get("session_id", "default")))[:64]
ledger = os.path.join(tempfile.gettempdir(), f"maxilun-edited-{sid}.txt")
if not os.path.exists(ledger):
    sys.exit(0)
with open(ledger, encoding="utf-8") as fh:
    paths = sorted({p.strip() for p in fh if p.strip() and os.path.exists(p.strip())})
os.remove(ledger)  # consume: next turn starts with an empty list

py = [p for p in paths if p.endswith(".py")]
if py:
    run = subprocess.run(["ruff", "check", *py], capture_output=True, text=True)
    if run.returncode != 0:
        sys.stderr.write(run.stdout[-4000:])
        sys.exit(2)  # block: diagnostics go back to the model
```

The ledger is consumed on read so a failure is reported once per turn, not forever. The output is tail-capped so a large diagnostic dump does not flood the context.

### Continuous verification cadence

| Moment | Check |
|---|---|
| Every turn that edited files | Stop-time batch format/lint/typecheck over edited files only |
| A work unit reaches its done gate | The unit's own `DONE GATE` command (`dispatch.md` §5) |
| Before a wave transition | Contract consumers re-checked; changed-file list compared with the write set |
| Before reporting to the user | Full suite plus the clean-state exit gate (`harness-engineering.md` Primitive 5) |

Local proof and target-environment proof are reported separately. Passing locally says nothing about staging or production; when the target was not checked, say so and name the next permitted check.

## 6. Context Budget

### 6.1 Measure the right signal

Tool-call count is a weak proxy: three large file reads can fill a window, and fifty small greps can leave it nearly empty. Use the harness's reported token usage for the last turn (input plus cached input) divided by the real window size. When the window size is unknown, say so and fall back to the count, labelled as a proxy.

For "how much context is left", point to the harness's native meter command and stop; do not scan files to estimate it. A static audit of installed skills and rules is a separate, opt-in task that reports **eager** overhead (descriptions, always-loaded rule files, tool schemas) apart from **on-demand** bodies, and labels every number as an estimate.

### 6.2 Thresholds

| Occupancy | Action |
|---|---|
| Below about 60% | Work normally |
| About 60-80% | Prefer compaction at the next phase boundary (6.3); do not start a new exploratory sweep |
| About 80-90% | Write the checkpoint now; finish the current unit to a clean stop |
| Above about 90% | One-time order: checkpoint immediately, hand the user a one-line resume instruction, stop |

The high-threshold action fires **once** with a complete protocol. Repeating "should we pause here?" every turn pushes a decision the harness can make onto the user and wastes the scarce context it is trying to save. If the platform auto-compacts below the hard threshold, the threshold must sit under the auto-compact point or it never fires.

### 6.3 Compact at phase boundaries, not mid-unit

| Transition | Compact? | Reason |
|---|---|---|
| Exploration finished, Read plan written | Yes | The plan is the distilled output; raw reads are dead weight |
| Plan written to a file, implementation starts | Yes | Implementation needs room for code |
| Mid-implementation of one unit | No | Paths, partial edits, and variable names are expensive to rebuild |
| Debugging finished, next unit unrelated | Yes | Stack traces pollute unrelated work |
| An approach failed and was abandoned | Yes | Remove dead-end reasoning before retrying |

What survives compaction: files on disk, git state, project rule files, the checkpoint. What does not: file contents read earlier, intermediate reasoning, verbal preferences the user gave but nobody wrote down, and any in-chat task list on platforms where the list tool is absent. **Write before compacting**, every time.

## 7. Session Memory

Two stores, never mixed:

| Store | Scope | Lifetime | Content |
|---|---|---|---|
| **Checkpoint** (`handoff.json`, `harness-engineering.md` Primitive 4) | One task | Until the task is done | Goal, write set, touched `file:line`, last gate output, next step, open blockers |
| **Lessons** (`.maxilun/lessons.jsonl`) | One repository | Until disproven or stale | Repository-specific facts learned the hard way |

Checkpoint rules:

1. Written by the pre-compact hook and at the 80% threshold, and by the agent at every unit boundary. A checkpoint written only by the model is a checkpoint that will be forgotten at the worst moment.
2. Stored per session under `.maxilun/` so parallel sessions never overwrite each other and a user's own notes file is never a target.
3. Loaded at session start capped by characters (a few thousand), newest first, with a switch to disable the load entirely.
4. The resume instruction is a proposal; the next session re-runs the last gate before trusting the recorded status.

## 8. Learning Persistence Without Self-Rewriting

A lesson is one trigger, one action, its evidence, a confidence, and a scope:

```json
{"id":"L-014","trigger":"editing db/migrations","action":"run the migration dry-run task before the test suite","evidence":["user correction on 2026-11-02","failed CI run 4812 at db/migrate.ts:88"],"confidence":0.6,"scope":"repo","last_confirmed":"2026-11-18"}
```

1. **Sources rank by strength.** An explicit user correction outranks a failed gate, which outranks an observed repetition. Repetition alone never raises confidence above a tentative level.
2. **Project scope by default.** A lesson moves to a cross-repository scope only when it was independently confirmed in at least two repositories, and only through human review.
3. **Decay.** A lesson not confirmed within a set window loses confidence; one contradicted by repository evidence (a changed manifest, a removed file) is deleted, not argued with. Repository evidence beats memory, always.
4. **Load only matching lessons.** Match the trigger against the current write set and task; never inject the whole file.
5. **No automatic skill evolution.** Clustering lessons into new skills, commands, or agents without review is how a skill set grows into a catalogue. A recurring lesson becomes a proposed edit to the owning specialist's reference file, reviewed like any other code change.
6. **Local only.** Observations and transcripts stay on the machine. Nothing leaves without an explicit, opt-in integration, and observation logs never contain secrets: redact before writing.

## 9. Rule Layering

Precedence, highest first:

1. The user's explicit instruction in this session.
2. Project rule files (`AGENTS.md`, `CLAUDE.md`, a project design-defaults file).
3. The owning specialist's language or framework guidance (for example idiomatic mutation in one language).
4. The Maxilun Core Rules and common references.

Specific overrides general on **convention** (style, idiom, tooling). It never overrides the **floor**: input validation, security, error handling, accessibility, and evidence-gated verification hold at every layer, as the Core Rules state. A layered rule file names the general rule it refines so the override is visible, not silent.

Install layered rule sets as directories under a namespace, never flattened: two layers that both contain a file of the same name will overwrite each other, and a flat install collides with other rule packs.

## 10. Rejected Patterns

| Pattern | Maxilun standard instead |
|---|---|
| A catalogue of hundreds or thousands of narrow skills, each with its own trigger description | 24 cohesive owners with one `SKILL.md` each; depth in references loaded on demand. Every eager description costs context in every session |
| The same skills copied into one directory per agent platform | One source tree; platform adapters generate or link, they do not fork content |
| Auto-generated skills, commands, or agents from observed sessions | Lessons propose edits to an existing owner's reference, under review (§8) |
| Advisory hooks that nag on every call (reminders, style hints, "consider compacting") | Block on deterministic violations; otherwise stay silent; one-time high-context order (§6.2) |
| Desktop notifications, cost telemetry, and remote dashboards enabled by default | Off by default, local only, opt-in per integration |
| A task list in chat treated as durable memory | A checkpoint file on disk (§7) |
| Effectiveness scores for a gate measured by its own authors on their own tasks, quoted as fact | A gate is justified by the failure it blocks in this repository, shown with `file:line`; claimed improvements are `[UNVERIFIED]` until reproduced |
| One-line installers piping a downloaded script into a shell | Pinned release, inspected script, explicit install command |
