# Test Matrix Orchestration: Deterministic Verification Engineering

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-verify/SKILL.md"
  origin: "Maxilun Verify Engine"
-->

How to orchestrate a deterministic test matrix, run container-based integration tests, and eliminate *flaky tests*.

---

## 1. The Measured Test Matrix Pyramid

The test pyramid is ordered by the ratio of execution speed to isolation level:

```text
       [End-to-End Playwright (Critical Only, < 10%)]
                        ▲
          [Integration & API Contract Tests (20-30%)]
                        ▲
           [Unit & Deterministic State Tests (60-70%)]
```

1. **Unit Tests**:
   - Test pure functions, state machines, and data transformations.
   - They must run in memory with no real network or disk I/O ($< 5\text{ms}$ per test).
2. **Integration / Contract Tests**:
   - Test the interaction between handler code and a real database or message queue.
   - Use a temporary database (*ephemeral database* / Testcontainers) instead of fake mocks, which hide SQL type inconsistencies.
3. **End-to-End (E2E) Tests**:
   - Use Playwright to test the *critical user journeys*: account sign-up, the payment transaction flow, and form submission.
   - Run headless, with *trace recording* active only when a failure occurs.

---

## 2. Anti-Flakiness Invariants

1. **No arbitrary time waits (`sleep`)**:
   - Every assertion must wait on an explicit state (for example: `waitForSelector`, `await expect(...).toBeVisible()`).
2. **State isolation between tests**:
   - Every test case must start from a *clean fixture*. Never rely on side effects or mutations left behind by an earlier test case.
3. **Failure screenshots & traces**:
   - Store screenshots and browser console logs only for failed tests, so they do not fill CI/CD artifact storage.
