# Harness Engineering: Autonomous Agent Execution Primitives

Harness Engineering shifts autonomous agents from speculative prompt loops to deterministic, repository-anchored execution. Grounded in empirical harness research (walkinglabs), these five primitives ensure agents maintain context continuity, respect scope boundaries, and never declare premature victory.

---

## 1. Repository as System of Record

An autonomous agent must treat the repository state—not the chat context window—as the single source of truth:
1. **Never Trust Ephemeral Memory**: If an architectural decision, schema contract, or verification result is not committed or written to a state file (`docs/`, `manifest`, or `.maxilun/`), it does not exist.
2. **Context Compaction Resilience**: Long-running tasks lose continuity when LLM context windows roll over. Persisting active goals into a structured state file allows seamless resumption.

---

## 2. Five Core Harness Primitives

### Primitive 1: Feature List State Machine (`feature_list.json`)
Tasks with $\ge 2$ deliverables require a deterministic tracking list:
```json
{
  "features": [
    {
      "id": "FEAT-001",
      "description": "Idempotent webhook signature verification",
      "status": "verified",
      "gate_command": "pytest tests/test_webhook.py -k test_signature",
      "exit_code": 0
    },
    {
      "id": "FEAT-002",
      "description": "Replay window deduplication cache",
      "status": "in_progress",
      "gate_command": "pytest tests/test_webhook.py -k test_replay",
      "exit_code": null
    }
  ]
}
```
- **States**: `todo` $\to$ `in_progress` $\to$ `verified`.
- **Invariance**: An item cannot transition to `verified` without an executable command returning exit code 0. Self-awarded checkmarks are strictly rejected.

### Primitive 2: Two-Phase Initialization
Never start coding immediately in a new workspace or complex task:
- **Phase 1: Environment & Pre-Flight Probe**:
  1. Inspect manifests (`package.json`, `Cargo.toml`, `pyproject.toml`).
  2. Verify tool availability (compilers, test runners, linters).
  3. Run baseline test suite to detect pre-existing failures before introducing edits.
- **Phase 2: Scoped Execution**:
  Proceed only after the pre-flight baseline passes.

### Primitive 3: Scope Surface & Anti-Overreach Gate
Agents naturally suffer from "scope creep" (editing adjacent files, unnecessary formatting, drive-by refactoring):
- **Write-Set Enforcement**: Every delegated task has an explicit `WRITE SET`. Changes outside the write set are rejected on sight.
- **Smallest Possible Diff**: Solve the exact problem at root cause. Do not refactor unrelated utilities.

### Primitive 4: Session Continuity & Handoff Ledger (`handoff.json`)
Before yielding a turn or transitioning between agents, the harness captures:
- Exact `file:line` ranges touched.
- Contracts produced or consumed.
- Passing command outputs and unresolved blockers.
- When resuming, the next agent reads the ledger first, preventing duplicate exploration.

### Primitive 5: Clean-State Exit Gate
Before reporting completion to the user:
1. Revert or remove scratch files, temp logs, and debug prints.
2. Check `git status` to ensure zero unintended modified files.
3. Execute the full verification suite (`test`, `typecheck`, `build`, `slopscan`) with exit code 0.
