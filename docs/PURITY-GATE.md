# Maxilun Purity Gate

The **Maxilun Purity Gate** is an engineering delivery constraint, not a writing style. It applies to skill instructions, generated artifacts, code, copy, diagrams, and verification reports.

## Universal rules

- Do not invent facts, metrics, test results, citations, user research, or product claims.
- Do not call a placeholder complete. Label drafts and unresolved assumptions.
- Do not use impressive wording where a concrete noun or verb is available.
- Do not add a dependency, abstraction, section, diagram, or specialist without a stated purpose.
- Do not report a diagnosis without evidence.
- Do not report PASS without the command, observation, or artifact that supports it.
- Do not silently change scope, naming, platform assumptions, or acceptance criteria.
- Do not duplicate the same deliverable across two skill owners.

## Routing rules

- Select one primary skill per deliverable.
- Companions must contribute a named artifact or validation step.
- Prefer a standalone workflow when the user installed only one skill.
- Reuse inherited discovery or design context instead of repeating it.

## Design rules

- Avoid default purple-blue gradients, generic glass panels, unexplained pill controls, decorative glow, and clone layouts.
- Use the bundled design corpus as evidence for principles, never as a copy source.
- Every major visual choice needs a one-line reason tied to audience, task, brand, or platform.

## Motion & Video rules (maxilun-motion · maxilun-cinecode)

- **FORBIDDEN (AI Slop Motion Patterns)**:
  - Rendering static website screenshots, 3-column pricing tables, or static cards as "motion scenes".
  - Full-screen blueprint or wireframe grid paper covering the entire background.
  - Floating uppercase capsule badges (pill shape + glowing border + status dot) floating like web tags in a video.
  - Dead pill buttons with `→` arrows inside video frames.
  - Static slides with crossfades masquerading as motion graphics.
  - CSS `transition:` or `setTimeout` inside deterministic frame renders (causes frame drift).
- **REQUIRED (Studio Motion Standards)**:
  - Continuous kinetic rhythm: every second has deliberate primary or secondary motion (camera drift, line trace, kinetic typography).
  - Graphic visual metaphors instead of literal web pages (e.g. geometric logo assembly, vector path tracing, spatial depth planes).
  - True kinetic typography using analytical damped springs and masked slide reveals.
  - Audio beat alignment: scene transitions locked to musical beats ($\text{Frames/Beat} = \text{round}(\text{FPS} \times 60 / \text{BPM})$).

## Delivery gate

Before delivery, check: ownership, evidence, scope, factual accuracy, functional completeness, accessibility, and whether the result would remain useful if the product name were removed.
