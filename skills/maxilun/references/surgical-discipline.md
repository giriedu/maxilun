<!-- metadata:
  version: "1.0.0"
  ecosystem: "maxilun"
  last_updated: "2026-11-02"
-->

# Maxilun Surgical Engineering Discipline

Operating discipline that prevents four classic LLM failure modes when modifying production code: hidden assumptions, bloated abstractions, collateral damage (*collateral diff*), and claiming completion without execution proof.

---

## 1. Pre-flight Reasoning (Investigate Before Editing)

1. **Read repo facts before assuming** — check the symbol's callers (`callsIn:`), data types, error handling patterns, and the existing test suite.
2. **Separate cheap decisions from expensive ones**:
   - Local implementation details that are easy to reverse (*Type 2*): pick the pattern consistent with the codebase, state any assumption that has impact, and do the work immediately.
   - Changes to a public contract, a production data schema, or ambiguous business behavior that are expensive to reverse (*Type 1*): lay out the options with their trade-offs briefly and ask the user to decide in one turn.
3. **Reject plans with hidden risk** — if the user's request could break caller compatibility or open a security hole, show the evidence (`file:line`) and propose a safe path.

### Example
**Request:** *"Make user search faster."*
- **Bad**: Install Redis immediately and write a 180-line caching layer without measuring where the slowness is.
- **Right**: Inspect the actual query → find a full scan on `WHERE LOWER(email) = $1` at `src/users/repo.ts:84` → add the expression index `users (LOWER(email))` and prove the change with `EXPLAIN ANALYZE`.

---

## 2. Radical Simplicity

1. **Build exactly what was asked** — no configuration parameters for the future, no extra "while we're here" features.
2. **No single-use abstractions** — do not create an `Interface`, `Factory`, `Strategy`, or *base class* when only one real implementation exists.
3. **Rewrite bloated code** — if simple logic has grown into 200 lines of wrappers that 40–50 plain lines can solve cleanly, simplify it now.
4. **Do not handle impossible scenarios** — put strict validation at external input boundaries (*trust boundaries*); inside strongly typed internal functions, trust the type invariants already enforced.

---

## 3. Surgical Precision (Change Radius)

1. **No *drive-by refactoring*** — do not change indentation, reorder functions, swap quote styles, or rewrite healthy code outside the task scope.
2. **Single rule for dead-code cleanup**:
   - **Must delete**: imports, variables, helpers, types, or old paths that **became obsolete because of your own change/migration**.
   - **Do not touch silently**: old unused code in other modules entirely unrelated to the task; mention it in one line at the end of the report if it is risky.
3. **Local repository conventions vs redesign scope**:
   - **Regular features & bug fixes**: follow the styling system, ORM, test runner, and naming patterns the project already uses.
   - **Redesign / UI/UX overhaul request**: the old design system that locks the look (dull CSS `:root` variables, obsolete theme tokens, rigid layout wrappers) **is a legitimate change target and must be migrated**. Keeping broken old tokens out of fear of violating conventions is an anti-pattern. Perform a *Clean Cutover*: replace the root tokens, update the layout shell, update the primitive components, and fully delete the old styling that became obsolete.
4. **Diff Trace Test** — every changed hunk must have a direct reason from the user's request or from updating an affected caller.

---

## 4. Verifiable Goal Loop (Real Execution Proof)

Turn every task into a target that can be proven objectively before stopping:

| Task Type | Verification Evidence That Must Be Run |
|---|---|
| Bug fix | Reproduction script/test fails before the edit → passes after the edit |
| Feature / API change | Boundary-behavior and failure-path tests pass + old callers updated |
| Structural refactor | Test suite & typecheck pass with no external behavior change |
| Web interface / CLI | Run the real app/script, observe the rendered result or actual output |

If execution is blocked by an environment factor (e.g. an external database is down), run every static/local verification that is possible and mark the rest honestly with `[UNVERIFIED]`.
