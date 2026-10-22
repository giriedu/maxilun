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
