# Maxilun Swarm Coordination: Topology, Agreement, Shared State, and Failure

<!-- metadata:
  version: "1.3.0"
  sync_target: "skills/maxilun/SKILL.md"
  origin: "Maxilun Orchestration Engine"
-->

What to do when more than one agent is running at once: which coordination shape is justified, how disagreements are settled, what shared memory may and may not carry, how work is claimed exactly once, what happens when an agent stalls or dies, and how spend is capped. `references/dispatch.md` owns sizing, work units, and the handoff packet; this file owns the runtime behaviour between dispatch and receipt. Nothing here overrides `SKILL.md` §4: a swarm is a tool for Cross-domain work, never a default.

---

## 1. First Question: Is a Swarm Justified at All?

A swarm adds three costs that a single owner never pays: context duplication (every agent re-reads the goal, the contracts, and part of the code), coordination messages, and merge risk. It pays off only when the work is wide, not when it is deep.

| Signal | Verdict |
|---|---|
| Units have disjoint write sets and no unit reads another's output | Parallel agents justified |
| One coherent surface, however large | One owner (`SKILL.md` §3.2); a bigger agent count only dilutes context |
| The hard part is reasoning, not breadth (a subtle bug, a design choice) | One owner plus one critic; more voters do not make a judgement more correct |
| Read-only research over many unrelated locations | Parallel read-only scouts; they may share one checkout |
| Writers would share a file, a manifest, or a lockfile | Sequence the writers, or give the shared file to one integration owner |

Rule of thumb: if the coordination text you would write (packets, merge plan, conflict rules) is longer than the diff, do not start a swarm.

## 2. Topologies and When Each Is Justified

A topology is a statement about who may talk to whom and who holds authority. In an LLM harness the host's subagent dispatcher is the real transport; a topology recorded in a state file but not enforced by that dispatcher is decoration.

| Topology | Authority | Justified when | Failure mode |
|---|---|---|---|
| **Hierarchical (lead + workers)** | The lead owns the plan, the contracts, and the merge; workers own only their write sets | Coding work with a shared contract; default for Maxilun waves | Lead becomes the bottleneck; lead failure stalls everything unless state is on disk |
| **Pipeline (stage chain)** | Each stage owns its artifact and hands a finished artifact to the next | Dependency order is strict: contract, then implementation, then proof (`SKILL.md` §5 waves) | A late stage discovers an early-stage defect; loop back to the stage owner, never patch around it downstream |
| **Mesh (peers talk directly)** | No single owner; peers negotiate | Exploration with no shared write set: independent hypotheses, competing designs, parallel searches | Message volume grows with the square of the agent count; consensus becomes the work; drift because no one holds the goal |
| **Star (hub relays only)** | Hub routes messages but owns no decisions | Fan-out of identical, independent jobs (lint N packages, scan N services) | Hub turns into an unacknowledged lead; make it the lead or remove it |

Decision rules:

1. **Default to hierarchical with at most three workers per wave** (matches `dispatch.md` §3). Drift grows with agent count; a lead that holds the goal is the cheapest anti-drift control there is.
2. **Pipeline is hierarchical over time.** Use it when outputs feed each other; it is what Maxilun waves already are.
3. **Mesh only for read-only or proposal-only work.** Peers may argue; they may not write to shared files. The result is merged by one owner.
4. **Peer messages carry decisions and blockers, not progress.** "Editing X" and "50% done" chatter consumes every recipient's context and produces nothing a reviewer can check.
5. **Mesh connection count must be capped.** A full mesh of `n` agents has `n(n-1)/2` channels: 6 at four agents, 28 at eight. Above four peers, cap each agent's neighbours or switch to a lead.

## 3. Agreement: Consensus, Voting, and Conflict Resolution

Distributed-systems consensus (Raft, PBFT, gossip) solves replicated state among machines that can crash or lie. LLM agents in one session share a host process and a file system; their disagreements are about judgement, not about message loss. Borrowing the protocol names does not borrow the guarantees.

| Mechanism | What it actually guarantees | Use for |
|---|---|---|
| **Contract owner decides** | One accountable decision, traceable to a domain | Default. Structure `maxilun-architect`, rendered surface `maxilun-craft`, schema `maxilun-data`, trust boundary `maxilun-sentinel` (`dispatch.md` §7) |
| **Executable arbiter** | The option that passes the gate wins | Competing implementations: run both against the same test or benchmark; keep the winner, discard the other |
| **Quorum vote** | A count; nothing about correctness | Low-stakes preference ties among proposals of equal evidence |
| **Unanimous / user gate** | Nobody proceeds until all named parties or the user approve | Type 1 decisions (`SKILL.md` §3.1); the council ACC gate (`agent-council.md`) |

Rules:

1. **Evidence beats votes.** A vote is admissible only between options with equal executable evidence. When one option has a passing gate and the other has an argument, there is no vote.
2. **Correlated voters are one voter.** Several agents on the same model, given the same prompt and context, fail the same way. Five agreeing copies are one opinion with five times the cost; a critic must differ in instructions, context, or model to count.
3. **Votes need a roster and a deadline.** Fix who may vote before the question is asked, reject votes from outside the roster, and close at a timeout. A vote counted after the deciding action has run is theatre.
4. **Quorum arithmetic.** For `n` voters: simple majority `floor(n/2) + 1`; two-thirds supermajority `ceil(2n/3)`; tolerating `f` arbitrary (lying) participants needs `n >= 3f + 1`. Stop early when the undecided remainder cannot change the outcome.
5. **Record the losing option and why.** The next unit or the user may need to revisit it; a decision without its rejected alternative is unauditable.

## 4. Shared Memory and Its Consistency Risks

Shared memory (a key-value store, a JSON ledger, a vector index, a scratch directory) is where swarms silently lose work.

| Risk | Mechanism | Control |
|---|---|---|
| **Lost update** | Two agents read the same record, each modifies a copy, the last write erases the first while both report success | Every read-modify-write under one lock, or a compare-and-set on a version field |
| **Stale read** | An agent plans from a snapshot that changed before it acted | Re-read inside the locked section; carry a version and reject writes against an old one |
| **Poisoned fact** | One agent writes a wrong conclusion; later agents treat it as ground truth | Memory entries carry source (`file:line`, command, agent) and confidence; facts without a source are hints, not inputs |
| **Branch merge clobber** | Per-agent copy-on-write branches promoted back with "child wins" semantics | Promote one branch at a time through the integration owner; a key touched by two branches is a conflict, not a merge |
| **Unbounded growth** | Agents append notes forever; retrieval returns noise | Namespace per run, expiry on scratch keys, summaries promoted only through review |

Rules:

1. **The repository is the system of record** (`harness-engineering.md` §1). Shared memory carries coordination state (claims, decisions, pointers to artifacts), not the artifacts themselves. Code lives in files and commits.
2. **Keep the critical section synchronous and short.** Do slow work (a model call, a test run) before taking the lock; inside it, reload, check, apply, save. Holding a lock across a model call serialises the swarm and invites lock timeouts.
3. **Write atomically.** Write to a temporary file in the same directory, then rename over the target. A crashed writer must leave either the old file or the new one, never half of each.
4. **Never wait on a lock you already hold.** File locks are usually not re-entrant; a nested acquire on the same store deadlocks with no error.
5. **One writer per worktree.** Read-only agents may share a checkout; writing agents get either disjoint write sets in one tree (Maxilun default) or isolated worktrees merged by one owner.

```python
# Locked read-modify-write over a JSON store. Standard library only.
import json, os, tempfile, time

def update_store(path, mutate, timeout_s=10.0):
    lock = path + ".lock"
    deadline = time.monotonic() + timeout_s
    while True:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            if time.monotonic() > deadline:
                raise TimeoutError(f"store busy: {lock}")
            time.sleep(0.05)
    try:
        data = {}
        if os.path.exists(path):
            with open(path) as f:
                data = json.load(f)
        result, changed = mutate(data)          # must not block or call a model
        if changed:
            fd_tmp, tmp = tempfile.mkstemp(dir=os.path.dirname(path) or ".")
            with os.fdopen(fd_tmp, "w") as f:
                json.dump(data, f)
            os.replace(tmp, path)                # atomic on the same volume
        return result
    finally:
        os.close(fd)
        os.remove(lock)
```

A lock file left by a crashed holder blocks everyone; pair it with a stale-lock rule (holder id plus timestamp, broken only after a timeout well above the longest critical section).

## 5. Task Claiming and Deduplication

Two agents doing the same unit is the most expensive swarm defect: double spend plus a merge conflict.

1. **Claim is compare-and-set, not check-then-set.** "Look up, see it free, then save my claim" with any await or I/O between the steps lets several agents win. The check and the write happen inside one locked section (§4) or one atomic store operation.
2. **A claim is a lease, not ownership forever.** It carries `owner`, `claimed_at`, `last_heartbeat`, and an expiry. An expired lease may be reclaimed; a live one may not.
3. **A claim coordinates; it does not authorise.** Holding the claim on a unit grants no extra tools, write paths, network, or spend. Authority comes from the packet's write set and the orchestrator.
4. **Reassignment rules are explicit.** Work may move from a stalled owner only when the lease expired, the owner reported blocked, or the owner released it. Protect recent claims with a grace period and protect work with real progress (a pushed diff, a passing partial gate) from being taken.
5. **One handoff at a time.** A unit with a pending handoff cannot be released or re-handed; the receiver accepts or rejects before anything else changes.
6. **Deduplicate by unit key, not by wording.** Key units by artifact and write set (`orders-export-endpoint`, `src/api/orders/export.ts`). Two requests that phrase the same change differently are one unit.
7. **Cap concurrent claims per agent.** An agent holding more units than it can advance is hoarding; low single digits is the working range, and in Maxilun waves one unit per agent is the norm.

## 6. Failure, Timeout, and Stall Handling

| Situation | Detection | Action |
|---|---|---|
| Agent exceeds its time budget | Wall-clock deadline per unit set at dispatch | Cancel, keep its partial diff for inspection, re-dispatch once with the failure noted, then escalate |
| Agent repeats the same failing command | Same normalised command failing several times in a row with no success between | Warn at the third consecutive failure, stop at the fifth; route the unit to `maxilun-insight` |
| Agent returns without its done gate | Return lacks the gate command and real output | Treat as unfinished (`dispatch.md` §6); do not merge |
| Agent edits outside its write set | Diff paths compared with the packet | Revert or explicitly accept and re-verify |
| Lead or orchestrator context is lost | Compaction or crash mid-wave | Resume from the on-disk ledger (`harness-engineering.md` Primitive 4); never from memory of the conversation |
| Dependency cycle between units | Adding an edge that reaches back to its source | Reject the edge at planning time; a cycle means two units are one unit |
| Retry storm | Many units failing on a shared cause | Stop retries globally; diagnose the shared cause once |

Rules:

1. **Retries are bounded and different.** One retry with the failure output attached; a second identical attempt is not a retry, it is a loop. Same defect twice goes to diagnosis (`SKILL.md` §4.8).
2. **Every wait has a deadline.** Waiting on a peer, a vote, a lock, or a subagent without a timeout turns one stall into a frozen swarm.
3. **Do not poll.** Status loops burn turns and context. Use completion delivery from the dispatcher; keep doing independent work until a real dependency blocks.
4. **A partial failure pauses only its dependents.** Independent units keep moving; the failed unit's consumers wait or are re-planned.
5. **Fail loud.** A unit that could not finish says what it tried and the exact blocker; silence is never read as success.

## 7. Cost Control

Agent count multiplies context cost before it multiplies output.

1. **Route by need, cheapest sufficient tool first.** Deterministic transform (a codemod, an AST-based rewrite, a formatter) costs no model tokens and should be used whenever the change is mechanical; a small model for classification and extraction; a strong model only for judgement, architecture, and security. Tiering is a policy the orchestrator applies per unit, not a property agents choose for themselves.
2. **Budget per run, checked before each spawn.** Track spend against a ceiling and act on thresholds: notify around half, warn around three quarters, stop optional spawns near the ceiling, and halt new agents at it. Enforcement must sit where spawns happen; an alert that only prints is advisory.
3. **Pay for discovery once.** The Read plan goes into the packet (`dispatch.md` §4); every agent that re-explores repays the same tokens.
4. **Cap return size.** Returns are bounded (`dispatch.md` §5); transcripts are never forwarded.
5. **Kill early.** A unit that blows its time or token budget is cancelled, not allowed to finish "because it is nearly there".
6. **Measure the counterfactual honestly.** Claimed savings from a swarm need the same task run by one owner as the baseline; savings computed against an imagined worst case are not evidence.

## 8. Autonomous Autoloop State Machine, Decision Cards & Routine Cycles

Synthesized from production autonomous runtime paradigms (`agent-autoloop`, `AnyModelBot`, and `ai-employees`):

1. **Autoloop State Transitions (`agent-autoloop`)**:
   - Background autonomous executions progress through an explicit state machine: `queued → claimed → done / nothing / cancelled`.
   - Temporary network or execution interruptions transition to `claimed → unknown`. An `unknown` state does not signify failure; late execution receipts are accepted, and new scheduled work may proceed without race conditions.
   - Run attempts are strictly bounded ($\le 10$ retry attempts with exponential backoff). Terminated runs cannot be re-queued without a fresh event.

2. **Human-In-The-Loop Decision Cards**:
   - Agents must not block conversational terminals with indefinite waiting loops. When human input is mandatory (e.g. Type 1 irreversible architecture choice or ambiguous requirement), the agent emits an atomic Decision Card (`cards.state`: `open → decided → done` or `open → closed`).
   - Cards present explicit, numbered choices (`1. Option A`, `2. Option B`) rather than unconstrained questions.
   - Once the user resolves a card, the autoloop transitions the task back to `claimed` and resumes execution in the assigned workspace lane.

3. **Persistent Decision Memory (`docs/decisions.md` & `docs/declined.md`)**:
   - To eliminate repetitive questions across separate sessions, whenever a user approves an operational direction, the decision is recorded in `docs/decisions.md` with timestamp, context, and scope.
   - Conversely, when a user rejects a proposal, the refusal is recorded in `docs/declined.md`. Agents must check both ledgers before raising questions; previously decided matters must never be re-asked.

4. **Quota Backoff Invariant (`limitedUntil`)**:
   - When an underlying provider returns a rate-limit or quota exhaustion error, the scheduler records a `limitedUntil` timestamp.
   - The coordinator suspends dispatches to that specific agent until the timestamp expires. No speculative token-burning retries are allowed during quota exhaustion.

5. **Sandboxed Workspace Permission Boundaries (`AnyModelBot`)**:
   - Each agent operates within a declared directory workspace (`cwd`).
   - Any proposed file mutation outside the active project root triggers an explicit confirmation gate. Secrets, auth tokens, and private keys are strictly scrubbed from agent logs and execution receipts (`SEC-BOT-001`).

6. **Enterprise Operational Routine Contracts (`ai-employees`)**:
   - Scheduled autonomous work runs as defined routine contracts with standardized manifests (`WORK-CYCLE.md`, `SCHEDULE.md`, `ROLE.md`).
   - Covers 8 enterprise operational roles: Chief of Staff (fleet reconciliation, decision briefs), Ad Manager, Customer Satisfaction, GTM Engineer, Sales, SEO, Social Media, and Web Dev. Each routine defines inputs, invariants, output dossiers, and an automated verification exit code.

## 9. Claims to Discount When Evaluating Swarm Frameworks

Swarm platforms commonly advertise properties their code does not deliver in the path an agent actually uses. Before adopting one, or before borrowing its vocabulary, verify each claim in code:

1. **"Raft / Byzantine / gossip / CRDT consensus".** Check whether messages cross a process boundary. A common pattern is an in-process event emitter where a node "sends" by emitting locally and synthesises the peer's reply, or a strategy name stored in a state file while the actual decision is a vote tally. Neither tolerates crashes or malicious peers. Mark such claims `[UNVERIFIED]` unless a networked transport is wired in the default path.
2. **"Topology-aware coordination".** Check whether the declared topology changes which agent can message or edit what. If the host dispatcher runs every agent independently and the topology lives only in metadata, it governs nothing.
3. **"Self-learning routing" with an accuracy figure.** Ask for the evaluation set, the baseline, and the script. A percentage with no reproducible harness is marketing.
4. **"Shared memory with bounded conflict".** Check for a lock or compare-and-set around read-modify-write. Lost-update races in JSON or key-value stores are typical and only show under real concurrency.
5. **"Cost savings" or "N times faster".** Check what was compared. Many figures compare against brute force at a size where any index wins, or count a no-model path as an agent result.

## 10. Rejected Patterns

- **Swarm as default.** Starting a multi-agent run for routine work because the tool exists; Maxilun sizes from evidence first (`SKILL.md` §4).
- **Large fixed agent rosters.** Six to eight agents for a feature that has two artifacts; a wave holds at most three units.
- **Coordination calls as proof of work.** Initialising a swarm, recording agents, or posting status is bookkeeping; only diffs and gate output count (`SKILL.md` §6).
- **Consensus vocabulary on single-process votes.** Calling a majority count "Byzantine fault tolerant" misstates the guarantee.
- **Heavy runtime dependencies for coordination.** A file lock, an atomic rename, and the host's subagent dispatcher cover the needs of a single-repository swarm; a vector database or a federation layer is justified only by a measured need.
- **Status chatter between peers.** Progress announcements cost every recipient context and carry no decision.
