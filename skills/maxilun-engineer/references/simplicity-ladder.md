# The Simplicity Ladder: Operationalizing Minimalist Code

<!-- metadata:
  version: "1.3.0"
  sync_target: "skills/maxilun-engineer/SKILL.md"
  origin: "Maxilun Engineer Engine"
-->

How to apply the *Simplicity Ladder* when writing production logic and performing measured refactors.

---

## 1. The Five Levels of the Simplicity Ladder

Before adding a class, a new abstraction, or a third-party library, evaluate solutions starting from the lowest level:

```text
[Level 5: New External Dependency] ── (Last resort, evaluate maintenance & security)
      ▲
[Level 4: Single Pure Helper Function / Minimal Abstraction]
      ▲
[Level 3: Native Platform Feature] ── (<dialog>, CSS, DB constraints)
      ▲
[Level 2: Standard Library / Built-in Language Feature] ── (stdlib)
      ▲
[Level 1: YAGNI & Reuse Existing Repository Code] ── (Zero new conventions)
```

1. **Level 1 — YAGNI & Reuse existing code**:
   - Check whether the repository already has a helper function, utility, or pattern that solves this. Do not start a second convention. Reject speculative parameters.
2. **Level 2 — Standard library first (stdlib)**:
   - Use built-in language capabilities (such as `structuredClone`, `URLSearchParams`, Web Crypto, Python `itertools`, Go `slices`).
3. **Level 3 — Native platform first**:
   - Use native HTML elements (`<dialog>`, native form validation), standard CSS, or database constraints (`UNIQUE`, `CHECK`, `FOREIGN KEY`) instead of redundant application-level code.
4. **Level 4 — One pure helper function**:
   - Write a single, focused helper with no side effects. Reject single-consumer classes or passthrough wrappers.
5. **Level 5 — New external dependency**:
   - Adding a package is the last option. Evaluate package weight, licensing, and vulnerability history before adding it.


---

## 2. Code Comment Invariants

1. **Explain WHY, not WHAT**:
   - Delete comments that describe code flow that is already readable (*"increment the counter"* or *"check whether the user exists"*).
   - Write comments only for unusual architectural decisions, external specification constraints, or handling of specific hardware/browser quirks.
2. **Delete your own obsolete code**:
   - When you refactor a function, delete every import that is no longer used, leftover variables, and dead branches left behind by your change.
