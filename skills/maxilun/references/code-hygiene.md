<!-- metadata:
  version: "1.0.0"
  last_updated: "2026-11-02"
-->

# Maxilun Code Hygiene Rules

Code cleanliness standards. They apply automatically whenever a Maxilun specialist writes or modifies source code.

## 1. Comment Quality

### Prohibited Comment Patterns
- Decorative divider lines (`// ========= SECTION =========`)
- Restating the code (`// Set count to 0` above `let count = 0`)
- Step narration (`// Step 1:`, `// First validate input, then save`)
- Empty labels (`// Helper functions`, `// Main logic`)
- Vague TODOs with no context or completion condition (`// TODO: fix later`)
- JSDoc/docstrings that only repeat parameter names and add no contract information
- Decorative emoji or block-closing markers (`} // end if`)

### Comments to Keep
- Business invariants and non-obvious domain rules
- Security reasons and trust boundaries
- Performance trade-offs backed by real measurements
- External protocol contracts, byte formats, or workarounds for a specific platform/browser bug

Keep it short: one line per reason. Add a second line only when it carries a new technical fact.

## 2. Naming & Control Structure

- **Functions & Methods**: specific verb + object (`verifyWebhookSignature`, `parseInvoiceCsv`, not `process` or `handleData`).
- **Booleans**: read as a clear predicate (`isExpired`, `hasActiveSubscription`, `canVoidPayment`).
- **State Variables**: named from the domain context (`isSubmittingOrder`, `validationErrors`, not `flag` or `temp`).
- **Flat Control Flow**: use guard clauses and early returns at the top of the function; keep indentation depth at 3 levels or fewer.
- **Explicit Types at Module Boundaries**: avoid `any` and untyped objects in public function signatures and API contracts.

## 3. Markup, CSS & Styling Hygiene

1. **Follow the Repository's Styling System**:
   - If the project uses **Tailwind / utility CSS**, use utilities that match the project's token configuration. Extract a component only when the pattern repeats functionally.
   - If the project uses **CSS Modules / Vanilla CSS**, name classes after the component's role (`.invoice-row`, `.auth-form`), not after meaningless wrappers (`.wrapper-inner-box`).
2. **Semantic HTML First**: use `<main>`, `<nav>`, `<section>`, `<article>`, `<form>`, `<button>`, `<dialog>` before falling back to a generic `<div>`. Do not use `<div onClick>` for interactive controls.
3. **Visual Token Discipline**: reference the project's spacing scale variables, semantic colors, and radii. Avoid arbitrary odd pixel values and raw hex colors, because they break light/dark theme consistency.
4. **Inline Styles**: use them only for dynamic values computed at runtime (e.g. drag coordinates, a progress bar width derived from data). Static properties belong in the stylesheet or in token classes.

## 4. Form & Micro-Interaction Hygiene

- Never block paste (`onPaste` with `preventDefault()`) on password inputs, OTP codes, or forms.
- Set `spellCheck={false}` and `autoCapitalize="none"` on email, username, code, URL, and API token inputs.
- Bind every input to an explicit `<label>` (`htmlFor` or direct wrapping), leaving no dead click gap on checkboxes/radios.
- Add `min-w-0` to flexbox children that truncate text (`truncate` / `text-overflow: ellipsis`) so the layout does not overflow.
- Set `overscroll-behavior: contain` on modals, sheets, and popovers that have their own scroll area.
- Use correct typographic characters in interface text: the ellipsis `…` (not `...`), `text-wrap: balance` on main headings, and `tabular-nums` on numbers that change or align vertically.
