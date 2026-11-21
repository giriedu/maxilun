# Systematic TDD & Four-Phase Root-Cause Debugging Protocol

An engineering discipline protocol for test-driven feature development and surgical bug elimination. Grounded in rigorous software engineering methodologies and autonomous agent harness discipline.

---

## 1. Ironclad Test-Driven Development (TDD)

The central invariant: **No production code may be written or modified without a failing test first.**

```text
1. Write Failing Test (RED) ──> Run Test & Confirm Failure
                                      │
2. Minimal Implementation (GREEN) ──> Run Test & Confirm Exit Code 0
                                      │
3. Surgical Refactor (CLEAN) ───────> Run Full Suite & Confirm No Regression
```

### The Three Steps
1. **Red**: Write a focused unit or integration test representing the new feature or reproducing the bug.
   - Run the test suite and verify the test fails for the expected reason (e.g. `AssertionError`, missing symbol), NOT due to a test syntax error.
2. **Green**: Implement the smallest possible production code necessary to make the failing test pass. Do not speculate on future features.
3. **Refactor**: Clean up implementation, eliminate duplication, and adhere to domain naming while keeping all tests green.

---

## 2. Four-Phase Root-Cause Debugging

When a bug, exception, or failure is reported, **never patch symptoms blindly**. Follow the 4-phase sequence:

### Phase 1: Reproduce
- Create a minimal, deterministic reproduction script or automated test case (`test_repro.py` / `repro.sh`).
- Confirm the script reproduces the exact failure reliably. If it cannot be reproduced, inspect environment variables, database state, or input fixtures.

### Phase 2: Isolate
- Use binary search or caller blast radius analysis (`maxilun-knowledge-graph` / `callsIn:`) to narrow down the boundary where good input turns into bad output.
- Check git history (`git bisect`, `git log -p`) to identify the commit that introduced the anomaly.

### Phase 3: Identify
- Trace the defect to a specific `file:line` and name the underlying logical flaw:
  - Off-by-one boundary condition.
  - Race condition / unhandled async concurrency.
  - Type coercion or null/undefined propagation.
  - Stale cache key or uncommitted database transaction.
- Formulate a falsifiable hypothesis before changing code.

### Phase 4: Verify & Prove
- Run the reproduction test created in Phase 1 to prove the fix works.
- Run the entire test suite and linter to prove zero regressions were introduced.
- Document the root cause in one factual sentence in the commit message or PR handoff.

---

## 3. Adversarial Code Review Protocol

Reviewing code requires technical rigor, not performative agreement:
1. **Never Accept Assertions Without Execution Proof**: Claims like "this should be safe" or "cleanly refactored" must be backed by a terminal command and exit code 0.
2. **Check Invariant Compliance**: Verify changes against security trust boundaries, SQL injection risks, and UI purity rules (`CMP-003`, `LAY-008`, `HDR-001`).
3. **Write-Set Audit**: Ensure the diff touches only files inside the declared scope. Revert any accidental modifications.

---

## 4. The 3-Strike Debugging Review Protocol

When fixing complex bugs or flaky tests, coding agents are prone to "trial-and-error thrashing"—repeating small arbitrary edits that degrade code quality.

1. **Strike 1 (Hypothesis-Driven Fix)**:
   - Formulate a falsifiable hypothesis based on reproduction output.
   - Apply a surgical diff and test.
2. **Strike 2 (Boundary Re-Evaluation)**:
   - If Strike 1 fails, do NOT repeat the same line edit.
   - Expand investigation to caller/callee contracts, type marshaling, or state persistence.
3. **Strike 3 (Full Architectural Escalation Gate)**:
   - **MANDATORY HARD STOP**: If two successive fixes fail to resolve the defect, the agent is strictly forbidden from attempting a third speculative edit.
   - Halt execution and invoke an architectural review (`maxilun-architect` / `maxilun-insight`).
   - Re-examine root assumptions, verify whether the test itself contains invalid assertions, and present findings to the coordinator.

---

## 5. Workspace Isolation via Git Worktrees

For risky refactors, dependency upgrades, or multi-branch spike explorations:
- Never accumulate dirty uncommitted changes on the active branch.
- Use isolated git worktrees (`git worktree add ../scratch-fix -b fix/issue-123`) to conduct isolated experiments with independent build targets.
- Merge back only verified diffs with passing test suites (`exit code 0`).

