<!-- metadata:
  version: "1.0.0"
  ecosystem: "maxilun"
  last_updated: "2026-11-15"
-->

# Maxilun Dispatch: Decomposition, Handoff, and Synthesis

How the orchestrator turns one request into work units, decides who runs them and in what order, hands each one enough context to start without exploring, and merges the results. `SKILL.md` §4 carries the rules; this file carries the templates, worked examples, and failure patterns.

---

## 1. Sizing the Request

Size is measured from repository evidence (a `locate` Read plan, a `callsIn:` count), never guessed from the wording of the request.

| Size | Evidence | Shape of the work |
|---|---|---|
| **Direct** | One domain, at most 2 files, no contract or schema change | One owner executes inline. No subagent, no wave. Verification still runs. |
| **Scoped** | One domain, 3 to 8 files, or one contract with known callers | One owner plus a proof step. A subagent is justified when the reading would crowd the main context. |
| **Greenfield** | Empty directory, `/maxilun-new`, or "buat aplikasi dari nol" | `maxilun-scaffold` 3-question triage → Dual-scaffold (`docs/` + starter code tree) → Wave 1 Vertical Slice |
| **Cross-domain** | Two or more domains whose outputs feed each other | Waves: contracts, then implementation, then proof. |
| **Unknown cause** | A symptom with no located fault | Diagnose first (`maxilun-insight`, or `maxilun-scout` as an agent). Size again once the fault has a `file:line`. |

A request never jumps a size because it sounds important. A one-line fix to a payment function is still Direct; what its risk adds is a companion (`maxilun-sentinel`) and a stricter done gate, not more agents.

## 2. Work Units

A work unit is the smallest piece that one owner can finish and prove alone. Each has five properties:

1. **One owner.** A specialist skill or an agent, chosen by the artifact that changes (`SKILL.md` §2).
2. **A write set.** The files, or line ranges inside a shared file, that only this unit may change.
3. **Inputs.** The contracts it consumes: a schema, an API type, the Craft Brief and token block, a decision.
4. **A done gate.** One command or artifact that proves it, runnable by someone else.
5. **A return format.** What comes back to the orchestrator, capped in size.

### Splitting rules

- Split by artifact and contract, not by step. "Schema", "endpoint", "form" are units; "plan", "code", "review" are phases of one unit.
- Two units in the same wave never share a write set. When they need the same file, either one owner takes both changes or the units are sequenced.
- Keep producer and consumer of a new contract in different waves, or under one owner. A consumer that starts before the contract exists invents it.
- Do not split below the point where the handoff packet is longer than the work.

## 3. Parallel or Sequential

Run units in parallel only when all three hold:

1. No unit reads an output another unit in the same wave produces.
2. Their write sets are disjoint.
3. The platform has a real parallel dispatcher. Where it does not, run the same units in sequence and say so; do not describe sequential work as parallel.

Everything else is sequential, ordered by dependency: Architect (structure) then Craft (Brief, tokens, markup) then Engineer or Frontend (behaviour, data) then Craft (states, motion) then Verify.

At most three units per wave. A fourth unit is a sign that the wave mixes two layers of the dependency order.

## 4. Discovery Runs Once

The most common waste in multi-agent work is every agent rediscovering the same code.

1. Before dispatch, the orchestrator (or `maxilun-scout` in Wave 1) runs `locate` once per sub-question and `query` for each contract symbol.
2. The resulting Read plan lines go into the handoff packet unchanged.
3. The receiving specialist starts at those ranges. It may extend the map with `query` on the neighbours named in `callers:` and `calls:`, or with one further `locate` for a question the packet did not cover.
4. It does not list directories and open files in order, and it does not re-read ranges whose excerpt is already in the packet.

When a specialist finds the packet's coordinates wrong, it reports that in its return instead of quietly working around it, so the next unit does not inherit the same wrong map.

## 5. Handoff Packet

```text
UNIT        <short name>
OWNER       <specialist or agent>
GOAL        <observable outcome, one sentence>
WRITE SET   <files or file:start-end ranges this unit may change>
OUT OF SCOPE <what must stay untouched, and who owns it>
READ PLAN   <file:start-end lines from locate/query, with the excerpt when short>
CONTRACTS   <schemas, types, Brief and tokens, decisions it must honour, each with file:line>
INVARIANTS  <security, data, accessibility, and purity rules that apply here>
DONE GATE   <exact command or artifact>
RETURN      changed file:line list; commands run with their real result;
            contract changes made; open risks; at most 25 lines
```

A packet missing `WRITE SET`, `READ PLAN`, or `DONE GATE` is not ready to send. Filling them is the orchestrator's work, not the specialist's.

### Example: "add CSV export to the orders table"

```text
UNIT        orders-export-endpoint
OWNER       maxilun-engineer
GOAL        GET /api/orders/export returns the filtered orders as CSV for the signed-in tenant.
WRITE SET   src/api/orders/export.ts (new), src/api/orders/index.ts:12-30
OUT OF SCOPE the orders table markup (maxilun-craft unit), the orders schema
READ PLAN   src/api/orders/list.ts:22-71 listOrders [function]
            src/lib/tenant.ts:8-31 requireTenant [function]
CONTRACTS   OrderFilter at src/api/orders/types.ts:4; tenant scoping through requireTenant
INVARIANTS  tenant filter on every query; stream rows, do not load the full result set
DONE GATE   npm test -- orders/export
RETURN      as specified above
```

The companion unit (`maxilun-craft`, the export button and its loading, empty, and error states) runs in the same wave: it consumes only the route path, which this packet already fixes, and its write set is disjoint.

## 6. Receiving Results

1. **Check the gate, not the summary.** A return without the done-gate command and its real output is unfinished, whatever its prose says.
2. **Check the write set.** Changes outside it are either reverted or explicitly accepted and re-verified.
3. **Propagate contract changes.** When a unit reports that it had to change a contract, every unit that consumed the old one is re-checked before the next wave starts.
4. **Merge once.** The user gets one report: what changed (`file:line`), why, which verification ran, residual risk. Per-agent transcripts are not forwarded.

## 7. Loopback and Escalation

| Situation | Action |
|---|---|
| Proof fails | Return the exact `file:line` defects and the failing output to the unit's owner. Re-run the same gate. |
| The same defect survives two fix attempts | Stop patching. Send it to `maxilun-insight` for a root-cause pass, then re-plan the unit. |
| Two specialists disagree | The owner of the contract decides: structure `maxilun-architect`, rendered surface `maxilun-craft`, schema `maxilun-data`, trust boundary `maxilun-sentinel`. |
| A Type 1 decision appears mid-work | Pause the affected units only, ask the user once (`references/discovery.md`), keep independent units moving. |
| A specialist or tool is missing | Say so in one sentence and execute that unit inline under the Core Rules. |
| The environment cannot run the gate | Report `[UNVERIFIED]` with the exact command that could not run. |

## 8. Failure Patterns

- **Ceremonial fan-out.** Three agents for a change one owner could finish in the time it takes to write three packets.
- **Shared-file collision.** Two units editing one file in the same wave, the second overwriting the first.
- **Rediscovery.** Each agent re-reading the repository because the packet carried a goal but no coordinates.
- **Contract by guess.** An implementer inventing a schema or API shape because its producer ran in the same wave.
- **Summary as proof.** Accepting "tests pass" with no command and no output.
- **Endless loopback.** A third and fourth patch on a defect whose cause was never diagnosed.
