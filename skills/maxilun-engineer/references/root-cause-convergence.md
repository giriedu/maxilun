# Root-Cause Convergence & Surgical Bug Fixing

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-engineer/SKILL.md"
  origin: "Maxilun Engineer Engine"
-->

How to trace a bug to its root-cause convergence point and fix it there, instead of patching the visible symptom.

---

## 1. Find the Root-Cause Convergence Point

Do not fix a bug by adding `if (data === null) return;` in the UI layer when the root cause is corrupt data in the database query layer.

### 3-Step Protocol:
1. **Trace the data origin (upstream tracing)**:
   - Use the `callsIn:` mapping from `maxilun-knowledge-graph` to walk backward from the point where the error surfaces to the first caller that produced the invalid value.
2. **Identify the broken invariant**:
   - Name the contract that was violated (for example: an empty array treated as an object, an undefined time zone, or a race condition between simultaneous transactions).
3. **Fix exactly at the convergence point**:
   - Place the fix at the deepest point where the data is first created or validated. Every downstream consumer is then protected without dozens of extra defensive checks.

---

## 2. Deterministic Regression Test Invariants

Every bug fix ships with one regression test:

1. **Test fails before the fix (Red)**:
   - Write a unit or integration test that reproduces the error consistently with the input that triggers the bug.
2. **Test passes after the fix (Green)**:
   - Apply the minimal surgical fix and confirm the test passes (*exit code 0*).
3. **Flaky-test prevention**:
   - Do not use `sleep()` with an arbitrary duration. Use a deterministic event-based wait (*await event / condition poll*).
