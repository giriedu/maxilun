# Maxilun Purity Gate

The **Maxilun Purity Gate** is an engineering and design constraint applied to skill instructions, code, interfaces, copy, diagrams, and verification reports. It eliminates both raw LLM filler and rigid single-template monoculture.

## Universal rules

- Do not invent facts, metrics, test results, citations, user research, or product claims.
- Do not call a placeholder complete. State assumptions and unverified scope explicitly.
- Do not wrap responses in ceremonial emoji HUD banners or self-checked `PASS/FAIL` checklists.
- Do not use impressive buzzwords where a concrete domain noun or verb is available.
- Do not add a dependency, abstraction, section, diagram, or companion specialist without a real boundary need.
- Do not report a diagnosis without `file:line` or profiling evidence.
- Do not report verification success without the executed command, exit code, or observed runtime behavior.

## Decision & routing rules

- Inspect repository evidence (`package.json`, schema, tokens, routes, tests) before asking questions.
- Execute reversible (Type 2) technical and layout decisions directly using repo conventions; ask at most one batched turn for irreversible (Type 1) or blank-slate product decisions.
- Assign one cohesive primary skill per surface; attach companions only at hard capability boundaries (security/crypto, schema migration, rendered video, automated QA).

## Design rules

- Reject raw AI visual clichés (purple-blue gradients, monotonous center-everything cascades, floating hero badge capsules, fake KPI strips) **and** reject misplaced SaaS monoculture (forcing dark developer-tool Bento grids, slate-indigo palettes, or `Cmd+K` badges onto clinical, editorial, retail, or consumer products).
- Derive color hue, typography, navigation, and layout structure from the product's real subject matter and user workflow, informed by 1–2 matched analyses from `skills/maxilun-craft/references/design-md/`.
- Never apply minor border-radius or color band-aids to a cliché layout when asked to redesign. Rebuild the visual hierarchy around real domain tasks; ask once with 3 genuinely contrasting visual archetypes only if aesthetic direction is completely open.

## Motion & Video rules (`maxilun-motion` · `maxilun-cinecode`)

- **Forbidden**:
  - Static web screenshots, 3-column pricing cards, dead pill buttons, or floating web tag capsules masquerading as video scenes.
  - CSS `transition:` or `setTimeout` inside deterministic frame renders (causes frame-capture drift).
- **Required**:
  - Deterministic frame-driven motion (`useCurrentFrame()`, analytical damped springs) with deliberate visual metaphors, readable canvas typography, and audio beat alignment where applicable.

## Delivery verification

Before yielding, verify ownership cohesion, diff minimalism, factual accuracy, functional states (loading, empty, populated, error), accessibility (`:focus-visible`, contrast, keyboard, `prefers-reduced-motion`), and executed smoke/test proof.
