# Refactoring, Cutover Discipline & CEFR Evaluation

Engineering playbook for surgical code refactoring, self-obsoleted code purging, CEFR matrix self-audit, and regression-free feature cutovers.

---

## 1. The CEFR Evaluation Matrix

Before submitting or handing over any modified code, evaluate against the four CEFR dimensions:

| Dimension | Verification Question | Concrete Corrective Action |
|---|---|---|
| **Correct** | Does the logic safely handle empty collections, `null`, boundary values, Unicode inputs, async cancellation, and concurrent mutations? | Add explicit boundary checks, propagate `AbortSignal`, and validate inputs at public boundaries. |
| **Efficient** | Is there unintentional $O(N^2)$ algorithmic complexity, serial `await` inside loops, duplicate queries, or memory retention? | Replace nested lookups with `Map`/`Set` indexes; batch queries or use bounded `Promise.all`. |
| **Fit** | Does the code conform to existing repository conventions (naming, error handling, auth, structured logging, dependency injection)? | Align with peer modules; never introduce a competing convention without explicit requirement. |
| **Readable** | Can a peer review the change in a single linear pass with branch nesting depth $\le 3$ and clear intent? | Apply early returns (guard clauses), eliminate ternary nesting, and use domain-accurate symbol names. |

---

## 2. Surgical Discipline: Clean Cutover vs Drive-by Refactoring

Maxilun strictly distinguishes between **required cleanup of self-obsoleted code** and **forbidden drive-by refactoring**:

### Required: Purging Self-Obsoleted Code
When replacing an existing function, parameter, or interface:
1. **Delete the superseded artifact**: Remove unused import statements, old helper functions, obsolete type aliases, and unreferenced constants.
2. **Update all callers**: Use `maxilun-knowledge-graph` (`callsIn:`, `importersOf:`) to migrate every caller to the new contract in the same change.
3. **No dead weight**: Leaving dead code commented out or flagged with `// TODO: remove later` is forbidden.

### Forbidden: Drive-by Refactoring
1. **Do not reformat unrelated files**: Keep diffs tightly focused on lines directly relevant to the task.
2. **Do not rename unchanged public exports**: Changing symbols outside the requested scope breaks downstream consumers unnecessarily.
3. **Do not modernize unrelated dependencies**: Upgrading libraries or rewriting existing working modules that were not part of the task scope introduces uncalibrated blast radius.

---

## 3. The 3-Step Atomic Cutover Protocol

When executing structural changes (e.g. migrating from an old utility module to a unified service):

```text
Step 1: Introduce New Mechanism alongside Old
  ├── Write tests for new implementation (Red -> Green)
  └── Confirm zero regressions in existing test suite

Step 2: Cutover Callers Atomically
  ├── Migrate callers one-by-one or in one cohesive atomic commit
  └── Run verification after each caller group

Step 3: Dismantle Superseded Mechanism
  ├── Delete the old implementation and its dedicated helpers
  └── Verify with build and test suite: Zero unused export warnings
```

---

## 4. Conventional Commits & Delivery Evidence

Structure commits so each commit represents one cohesive, verifiable change:

- `feat(scope): ...` — New user-facing or technical capability.
- `fix(scope): ...` — Root-cause bug fix with regression test.
- `refactor(scope): ...` — Internal code structure improvement with no external behavior shift.
- `test(scope): ...` — Adding or updating test suites.

Always conclude work with factual evidence: changed `file:line`, verification command and exit code, and confirmation that all affected callers were updated.
