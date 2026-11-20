# UI/UX Workflow Hooks

<!-- metadata:
  version: "1.3.0"
  sync_target: "skills/maxilun-craft/SKILL.md"
  origin: "Maxilun Craft Engine"
-->

The Loop in SKILL.md §2 asks the agent to remember to scan, to measure, and to say `[UNVERIFIED]` when it did not. Agents forget under load. On harnesses that expose lifecycle hooks (session start, before and after a tool call, end of turn), the same Loop can run as events that happen rather than instructions that are hoped for. This reference defines which craft checks belong on which hook, how a design hook must be engineered so it cannot fail silently, and the review cadence that ties per-edit scans to the rendered gates in `measured-design-gates.md`. Hooks are an accelerator, not a dependency: where a harness has none, every step below is executed manually in the Loop.

---

## 1. Hook Map

| Event | Craft job | Cost budget | Speaks when |
|---|---|---|---|
| Session start | Detect the UI stack and the decided things (SKILL.md §2 step 1) and inject one line of context | under 1 s, no network | The project renders UI. Silent otherwise. |
| Before an edit | Blast radius of the target file: token source, global stylesheet, shared primitive, or leaf | under 1 s | The target is shared. Silent on leaf files. |
| After an edit | Static scan (`scripts/slopscan.py`) of the changed file only; record the file in the session ledger | under 2 s | A finding exists. Silent on clean files. |
| End of turn | Block once if a renderable page was edited and has no live measurement receipt | under 1 s, reads the ledger only | An edited page is unmeasured. |

Rendered gates never run inside a per-edit hook. They take seconds per page and need a browser; running them on every keystroke-sized edit trains the agent to batch edits to avoid them. Per edit is static, per turn is the receipt check, per release is the full suite under `maxilun-verify`.

## 2. Engineering Rules for Design Hooks

A hook that crashes and exits 0 is indistinguishable from a codebase with no findings. Every rule below exists to keep a hook from lying by omission.

| Rule | Requirement |
|---|---|
| Parse, do not grep | Read the hook input as JSON with a real parser. Regex extraction of `file_path` from JSON breaks on escaped quotes, Windows backslashes, and key order. |
| Native runtime | Write hooks in the language the skill already ships (Python stdlib here). A bash-plus-`jq` hook does not run on a stock Windows machine, and an absent `jq` must not mean "exit 0, all clear". |
| Fail loud | Wrap the body; on an unexpected exception print `craft-hook error: <message>` to stderr and use the harness's "show to the model" exit code. Silence is reserved for "looked and found nothing". |
| Record first | Append to the edit ledger before running any check, so a crashing check cannot erase the evidence that a page changed. |
| No writes into the repo | Ledgers and receipts go to the OS temp directory keyed by session id. Logs inside the project become noise in diffs and leak paths. |
| One path helper | The writer (after-edit) and the reader (end-of-turn) import the same function that builds the ledger path. Two copies of the formula drift, and a reader that looks in the wrong place reports a clean session forever. |
| Silent on success | Print nothing when nothing is wrong. Every line a hook prints costs context on every edit. |
| Loop guard | An end-of-turn hook that blocks must check the harness's "already continuing because of a stop hook" flag and let the turn end the second time, after recording the state. |
| Clearable | The remediation command a blocking hook prints must be one that, when run, clears that same block. Test this path explicitly; a hook whose advice does not clear it blocks every turn for the rest of the session. |
| Units | Check the harness's timeout unit. Claude Code reads hook `timeout` in seconds; a value written as milliseconds becomes a hook allowed to hang for over an hour. |

## 3. Session Start: Inject What Is Already Decided

Detect, in this order, and emit one line:

1. Framework from the manifest dependencies (`next`, `react`, `vue`, `svelte`, `astro`, or none for plain HTML and Apps Script).
2. Token source: a Tailwind v4 `@theme` block in CSS, a Tailwind v3 config file, a `:root` custom-property block, a DTCG JSON token file, or none.
3. Component library markers (`components.json` for a copy-in library, a `ui/` primitives folder).
4. `docs/DESIGN.md` present or absent; UI language from the `lang` attribute or the locale files.

```
craft: next 15 + tailwind v4 (@theme in app/globals.css) | primitives: components/ui (14) | DESIGN.md: yes | lang: id
```

That line is input to the Brief, not a substitute for reading the files. When the token source is `none`, say so: it means step 4 of the Loop (lock tokens) has not happened yet in this project.

## 4. Before an Edit: Blast Radius

Classify the target and report consumers before the change lands.

| Class | Detection | Message |
|---|---|---|
| Token source | The file found as token source at session start | `token source: N files consume --accent; rendered gates required for every page that uses it` |
| Global stylesheet | Imported by the root layout or linked from every page | `global sheet: affects all routes` |
| Shared primitive | Under the primitives folder, or imported by 3 or more files | `primitive Button: 23 importers; co-located: Button.stories.tsx, Button.test.tsx` |
| Leaf | Anything else | silent |

Count consumers with a literal search for the custom-property name or the import path; do not guess. Co-located stories, tests, and snapshots are listed because a visual change to a primitive that leaves its story stale makes the next review compare against a lie. In a Repair under SKILL.md §5 (Nuclear Redesign), touching the token source and primitives is the plan, so the message is informational and never blocks.

## 5. After an Edit: Static Scan of the Changed File

Minimal hook, stdlib only. The harness sends JSON on stdin; exit code 2 returns stderr to the model in Claude Code.

```python
import json, os, subprocess, sys, tempfile

UI_EXT = {".html", ".htm", ".css", ".scss", ".tsx", ".jsx", ".vue", ".svelte", ".astro"}
SCAN = os.path.join(".claude", "skills", "maxilun-craft", "scripts", "slopscan.py")

def ledger_path(session_id):
    return os.path.join(tempfile.gettempdir(), "maxilun-craft", f"{session_id}.edits")

def main():
    data = json.load(sys.stdin)
    path = (data.get("tool_input") or {}).get("file_path") or ""
    if os.path.splitext(path)[1].lower() not in UI_EXT or not os.path.isfile(path):
        return 0
    led = ledger_path(data.get("session_id", "unknown"))
    os.makedirs(os.path.dirname(led), exist_ok=True)
    with open(led, "a", encoding="utf-8") as f:            # record before checking
        f.write(path + "\n")
    out = subprocess.run([sys.executable, SCAN, path], capture_output=True, text=True)
    if out.returncode == 1:
        sys.stderr.write(out.stdout)
        return 2
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:                                # fail loud, never silent
        sys.stderr.write(f"craft-hook error: {exc}\n")
        sys.exit(2)
```

Registration (project settings, relative path):

```json
{ "hooks": { "PostToolUse": [ { "matcher": "Edit|Write|MultiEdit",
  "hooks": [ { "type": "command", "command": "python .claude/hooks/craft_post_edit.py", "timeout": 10 } ] } ] } }
```

Scope: slopscan errors return to the model; warnings stay out of the per-edit channel and appear in the end-of-turn scan of SKILL.md §7. A per-edit hook that recites every warning on every save is ignored by the third edit.

## 6. End of Turn: No Unmeasured Pages

The end-of-turn hook enforces "never state a number you did not measure" for pages, using the receipts defined in `measured-design-gates.md` §1.

1. Read the ledger. Keep only renderable pages (`.html`, `.htm`, or the route list for a framework app). A stylesheet or component file cannot be rendered alone; demanding a receipt for it adds friction and measures nothing.
2. For each page, find a receipt whose SHA-256 matches the file's current hash and whose exit code was 0. A receipt for an older hash is expired: the page changed after it was measured.
3. No live receipt for some page: block once, naming the pages and the exact gate command that writes a receipt for them.
4. No browser available on the machine: do not block (the demand cannot be met). Require instead that the final report marks those pages `[UNVERIFIED]` per SKILL.md §7.
5. Second stop in the same turn (loop guard set): record the unmeasured state and let the turn end.

## 7. Review Cadence

| Tier | Trigger | Runs | Blocks on |
|---|---|---|---|
| Edit | Every write to a UI file | slopscan on that file | errors |
| Turn | End of each agent turn | Receipt check for touched pages | missing or expired receipts |
| Screen done | Before reporting a screen finished | Rendered gates from `measured-design-gates.md` §2 to §13, both themes | any gate exit 1 or 2 |
| Release | Before merge or deploy | Full suite under `maxilun-verify`, then the adversarial critique of `measured-design-gates.md` §14 | gate failures; critique findings of high severity |

Each tier is cheaper and narrower than the one after it. Do not promote a tier's checks downward to "catch it earlier": a slow per-edit hook gets disabled, and a disabled hook protects nothing.

## 8. Hook Anti-Patterns

| Anti-pattern | Why it fails | Instead |
|---|---|---|
| Regex "contrast checks" on class names (`text-gray-300` near `bg-white`) | Guesses a ratio from tokens it cannot resolve; flags fine pages and misses themed failures | Real ratio from `slopscan.py --contrast` on token values, or §2 of the gates on the render |
| Self-scored rubric (1 to 10 per dimension) produced by the agent after building | The builder grades its own work; numbers carry no measurement | Receipts for measurable claims, severity-ranked findings for the rest |
| Session-start banner recommending a dozen plugins or personas | Spends context, invites scope creep, and is not evidence about the project | One line of detected facts (§3) |
| Hook output decorated with emoji status icons | Breaks the no-emoji rule (`CMP-003`) in the agent's own channel and wastes tokens | Plain `rule  file:line  message` lines |
| Hooks that write log files into the project | Pollutes diffs; logs outlive the session and may record local paths | Session-keyed files in the OS temp directory |
| Hooks that download templates or installers at run time | Network side effects in a lifecycle event; unpinned content | Ship the check with the skill; no network in hooks |
| Per-edit hook that also asks for confirmation on every UI file | Approval fatigue; the user starts approving blind | Ask only for genuinely sensitive targets, inform for shared ones (§4) |
