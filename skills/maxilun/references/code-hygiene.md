<!-- metadata:
  version: "1.0.0"
  last_updated: "2026-10-22"
-->

# Maxilun Code Hygiene Rules
# (Aturan Higienitas Kode Maxilun)

Applied automatically when any maxilun-* skill generates or modifies code.
Berlaku otomatis saat skill apapun dalam ekosistem maxilun menghasilkan atau mengubah kode.

## Comment Quality

### Forbidden Comment Patterns
- Decorative separators (`// ========= SECTION =========`)
- Restating the obvious (`// Initialize counter` above `let count = 0`)
- Step narration (`// Step 1:`, `// Step 2:`, `// First...`, `// Next...`)
- Empty labels (`// Main logic`, `// Helper function`, `// Entry point`)
- Vague TODOs (`// TODO: Improve this`, `// TODO: Fix later`)
- Signature echo (JSDoc that only repeats parameter names)
- Decorative emoji (`// ✅ Done`, `// 🚀 Fast`)
- End markers (`} // end if`, `// End of function`)
- Over-explained single facts (4 lines explaining what fits in 1)

### Valuable Comments (Always Keep)
- Business rules and domain logic
- Security constraints and reasoning
- Performance trade-offs with measured data
- API contracts and protocol details
- Workarounds for known platform bugs
- Edge cases and their handling assumptions
- Licensing and legal notices

### Comment Length Rule
One line per comment. Two lines only when the second carries a
genuinely new fact. Never three lines for a single point.

## Naming

- Variables and functions: descriptive, no abbreviations that save
  zero tokens (cfg, impl, req, res, fn — use full words)
- Boolean variables: read as questions (`isValid`, `hasPermission`,
  `canEdit`)
- Functions: verb-first (`validateUser`, `fetchOrders`, `renderCard`)
- Constants: SCREAMING_SNAKE only for true compile-time constants,
  not for every config value

## Structure

- Prefer flat over nested (max 3 levels of indentation before
  extracting a function)
- Early returns over deep nesting
- Guard clauses at function top
- Related code stays together (no "organize by type" when "organize
  by feature" makes more sense)

## CSS & UI Code Purity Rules

### Class Naming
- Forbidden generic names: `container`, `wrapper`, `content`, `section`,
  `box`, `card`, `inner`, `outer`, `left`, `right` without context
- Required contextual naming: `login-form-container`, `invoice-card`,
  `sidebar-nav-section`, `hero-cta-box`
- Component prefix for scoped styles: `.InvoiceCard__header`,
  `.LoginForm__input-group` (BEM or project convention)
- Utility classes allowed only from established system (Tailwind,
  design tokens). No ad-hoc utility classes invented per-component.

### Inline Styles
- Forbidden: inline styles for layout, spacing, colors, typography
- Allowed: dynamic values computed at runtime (position from drag,
  color from user preference, width from data)
- All static visual properties belong in CSS/design tokens

### Component Structure Anti-Patterns
- Forbidden: header + content + footer structure in every component
  without reason. Structure follows content needs, not template.
- Forbidden: wrapping plain text in `<div>` or `<Card>` without
  grouping purpose. Text can exist without container.
- Forbidden: decorative wrapper elements (`<div className="wrapper">`
  that does nothing but add a layer)
- Required: semantic HTML first (`<nav>`, `<main>`, `<article>`,
  `<form>`, `<dialog>`). Generic `<div>` only when no semantic tag fits.

### Design Token Compliance
- Spacing values must reference token scale (4px grid), not magic numbers
- Colors must reference semantic tokens (`--brand-primary`), not raw hex/rgb
- Border radius must follow nested hierarchy (child <= parent)
- Font sizes must follow modular scale, not arbitrary px values
- If design tokens don't exist yet, create them BEFORE writing component CSS

### JavaScript/TypeScript UI Code
- Event handler naming: `onSubmit`, `handleFormSubmit`, not `click`,
  `handleClick` (what happens, not what triggers it)
- State variable naming: `isSubmitting`, `hasError`, `userList`, not
  `loading`, `error`, `data` (specific to context)
- Magic strings forbidden: use constants or enums for status values,
  route paths, event names
- Type definitions: prefer specific interfaces over `any`, `object`,
  `Record<string, unknown>`. Define shape explicitly.
