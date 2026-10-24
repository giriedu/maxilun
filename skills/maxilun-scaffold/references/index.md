# Scaffold Reference Corpus

This directory is a bundled reference library for `maxilun-scaffold`. It provides the 10-document context templates (`references/doc-templates.md`), domain-specific PRD & architecture archetypes (`references/prd-archetypes.md`), and direct integration rules with `../maxilun-craft/references/design-md/index.md` for initializing non-generic `DESIGN.md` and `PRD.md` files.

## Index of Bundled References

| File | Purpose | When to Read |
|---|---|---|
| `references/doc-templates.md` | Full canonical templates for all 10 documents in `docs/` (`PRD.md`, `TECHSTACK.md`, `DESIGN.md`, `SECURITY.md`, `STYLEGUIDE.md`, `TASK.md`, `ARCHITECTURE.md`, `SKILLS.md`, `GLOSSARY.md`, `ONBOARDING.md`) | Always read before generating or updating `docs/` files |
| `references/prd-archetypes.md` | Domain-specific archetypes (Fintech, B2B SaaS, DevTools/AI, Commerce/Booking, Media/Docs) mapping product category to PRD invariants, STRIDE threats, data rules, and `maxilun-craft` design references | Read during Discovery/Generation to populate concrete domain facts instead of generic placeholders |
| `../maxilun-craft/references/design-md/index.md` | 84 Production UI/UX Design Systems (Stripe, Linear, Vercel, Wise, Figma, etc.) | Read when generating `docs/DESIGN.md` and UI constraints in `docs/PRD.md` to seed real OKLCH tokens, typography scales, and component rules |

## Reference Selection & Evidence Contract

1. Determine the product domain from repository scan or user interview.
2. Read `references/prd-archetypes.md` to select the closest domain archetype.
3. Read `../maxilun-craft/references/design-md/index.md` and up to two matching brand analysis files in `../maxilun-craft/references/design-md/` to ground `docs/DESIGN.md` in production-proven visual hierarchy and tokens rather than empty `[TBD]` placeholders.
4. Read `references/doc-templates.md` and generate all 10 files in `docs/` with `[CONFIRMED]`, `[ASSUMED]`, or `[TBD: reason]` markers.
5. Include the `References`, `Applied`, `Rejected`, and `Reason` block inside `docs/DESIGN.md`.
