# Evidence-First Discovery & Decision Triage Protocol

Use this protocol only when a request leaves room for interpretation that materially affects architecture, data contracts, or product identity. It replaces passive one-question-at-a-time interviews with **repository investigation first, then one grouped clarification sized by decision cost**.

---

## 1. Triage Order Before Asking

Run these 3 steps internally before asking the user a single question:

1. **Inspect Repository Evidence**:
   - **Check root context documents and docs/**: First look for the repository's single source of truth: either the document set in `docs/` (`PRD.md`, `TECHSTACK.md`, `SECURITY.md`, `DESIGN.md`) or the 4 fast-context files at the repository root (`Security.md`, `Code-Style.md`, `Database.md`, `API-Guide.md`). Read these files before touching code so you stop guessing the schema, auth model, endpoints, or naming conventions.
   - Read the manifest (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`), the folder structure, the DB schema, the example environment variables, and existing CSS tokens/components.
   - **Never ask again** for a fact that is visible in the repository or in those context documents.
2. **Measure the Cost of Reversing the Decision (*Reversibility Check*)**:
   - **Type 2 (cheap to reverse)**: internal component structure, local naming, a single-page layout on an existing design system, performance/bug fixes, or standard CRUD endpoints.
   - **Type 1 (expensive to reverse)**: splitting a database/service, financial/multi-tenant schemas, breaking changes to a public API contract, removing an existing feature, or creating a visual identity system from scratch with no reference at all.
3. **Choose the Action**:
   - **Type 2 → Execute directly.** Pick the most standard option that fits the repo's conventions, write one sentence stating the assumption when relevant, then finish the work.
   - **Type 1 → At most 1 grouped clarification turn** (2–4 crucial points that actually change the design, each with concrete options and a recommended default).

---

## 2. Four Dimensions That Must Be Clear Before a Large Implementation

If the prompt plus the repository read already answer all four dimensions, **do not run a question-and-answer session**:

| Dimension | What to Look For | Primary Source |
|---|---|---|
| **1. User Outcome** | Which real workflow change must the user be able to perform? | User prompt + existing routes/features |
| **2. Hard Constraints** | Stack, data schema, security boundaries, performance targets, backward compatibility | Repo manifest, CI configuration, DB schema |
| **3. Scope Boundary (Non-goals)** | Which adjacent parts are deliberately left untouched in this iteration? | YAGNI principle + the prompt's explicit scope |
| **4. Proof Criteria** | Which test command, interaction flow, or metric proves the task is done? | Repo test suite + feature acceptance flow |

---

## 3. Clarification Rules When Truly Needed (Type 1)

1. **One Grouped Turn, Not a Drip-Fed Interrogation**:
   - Do not hold up the work for 3–4 consecutive question rounds. Group at most 2–3 unanswered key decisions into one short message.
2. **Present Substantively Different Options + a Recommendation**:
   - Avoid empty questions such as *"Can you explain in more detail?"* or *"What should the UI look like?"* with no anchor.
   - Give 2–3 real choices with their short consequences, and mark the recommended one.
3. **Interface Design Only: Feature Addition vs Redesign**:
   - **Feature addition on a healthy system**: If the repository already has a healthy token/component system that fits the domain, **follow and reinforce the existing system** without asking.
   - **Redesign / UI UX replacement request**: If the user asks for a redesign, **do NOT keep old tokens, CSS variables (:root), or layout wrappers that lock the look into something dull and generic**. Perform a *Clean Cutover*: detect the 5 Design System Locks (`SYS-001` .. `SYS-005` in `purity-catalog.md`), delete/replace the old root variables, open up the constraining layout containers, and install a new visual foundation that fits the domain.
   - **Style direction not stated**: If the project is truly new (*greenfield*) or the user asks for a *total redesign* without naming a style direction, offer **3 visual archetypes that genuinely contrast** and fit the product domain (see `../maxilun-craft/SKILL.md` and `../maxilun-craft/references/design-md/index.md`) — for example *Warm Editorial* vs *Bright Precise Operational* vs *High-Contrast Minimalist* — not three similar dark-dashboard variations.
   - If the user answers *"up to you / overhaul it fully"* ("terserah / rombak maksimal"), pick the one direction most authentic to that product's audience, state the choice and its reason in 2–3 sentences, and build it completely right away.
---

## 4. Bad Pattern vs Maxilun Pattern

### Case A: Feature in an Existing Repository
**Prompt**: *"Add a patient appointment scheduling feature to this clinic app."*

- **Passive pattern (rejected)**: Stop working and drip-feed 4 question turns (*"Who uses it?"*, *"Which stack?"*, *"What are the non-goals?"*) wrapped in empty emoji banner blocks.
- **Active evidence-based pattern (required)**:
  1. Read the repo: Next.js App Router detected, Prisma (`Patient`, `Doctor` already exist in `schema.prisma`), separate authentication for reception staff and the patient portal, and a clean light palette in `globals.css`.
  2. Only 1 Type 1 decision is not written in the schema: the cancellation / slot *double-booking* rule and external calendar sync.
  3. If `.env.example` shows no external integration, build the booking flow directly on a unique database constraint (`doctor_id, slot_start`) with the explicit assumption of no external payment gateway. Ask 1 focused clarification only if a half-finished Google Calendar stub is found.

### Case B: Complaint "It Still Looks Like Generic AI, Replace the UI/UX, or Redesign"
- **Patchwork & locked pattern (rejected)**: Change only `border-radius` or margins in leaf JSX while the generic gray `:root` variables, the narrow layout container, and the old wrappers keep locking the look. The UI/UX stays the same as before.
- **Structural overhaul & clean unlock pattern (required)**:
  1. Identify the structural defects and the **Design System Locks** that lock the UI (for example: pale slate tokens in `globals.css`, a rigid `max-w-5xl` wrapper in `layout.tsx`, old buttons/cards with uniform corners, every section center-aligned).
  2. Unlock the foundation: replace the `:root` tokens with an OKLCH color ladder taken from the product's physical domain, open the layout container so the spatial rhythm has room, and update primitive components to the concentric formula.
  3. Set the visual direction from the domain (for example: *Calm Clinical Operational* for a clinic — clean light surfaces, high contrast, queue and schedule focus in <3 steps; or a concrete reference from `../maxilun-craft/references/design-md/`). State the principles applied and rejected (DDR), then rebuild the components completely and delete the obsolete styling code (*clean cutover*).
