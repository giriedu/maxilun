# Maxilun Routing Protocol Design

Date: 2026-10-23
Status: Approved and implemented

## Goal

Make the Maxilun orchestrator select specialist skills reliably from natural-language prompts, including mixed-domain requests, ambiguous intent, and environments where companion skills are missing. Keep the routing instructions available in the main `SKILL.md` so they are present whenever the orchestrator skill is loaded.

## Recommended approach

Replace the current keyword-first routing guidance with a short, ordered decision protocol in `maxilun/skills/maxilun/SKILL.md`. Keep the specialist catalog as the source of domain descriptions, and remove duplicated/conflicting routing matrices where the new protocol makes them redundant.

### Decision protocol

1. Honor explicit skill or mode commands first, subject to the user's requested outcome and platform capabilities.
2. Read the whole prompt for the requested outcome, action, artifact, constraints, and relevant context. Route by the requested outcome, not an incidental noun or keyword.
3. Select one primary specialist when one domain clearly owns the outcome. Select a second specialist only for a distinct required part of the deliverable.
4. Use confidence bands based on evidence, not pretend-precise numeric scores:
   - **High:** one specialist clearly owns the requested outcome; proceed.
   - **Medium:** one primary is clear but an adjacent domain affects a required part; use a narrowly scoped companion or split the task into waves.
   - **Low:** two or more materially different outcomes remain plausible, or a required constraint is missing; ask one focused question before dependent work.
5. Add companion skills only when their guidance changes the result. Treat availability as an environment check, not an assumption. If unavailable, continue with the primary skill when possible and state the limitation briefly.
6. If no specialist fits, answer directly with general capability or explain the boundary; do not force a weak match.
7. Keep the existing limit of three active specialists per wave and use sequential waves for dependent work.

## Conflict and boundary rules

- User's explicit requested deliverable outranks words that merely mention another domain.
- Explicit slash-skill invocation outranks inferred routing, unless it conflicts with the requested result or unavailable platform capabilities; explain the conflict and ask only if the outcome is unclear.
- Fast path is for genuinely trivial or conceptual requests and must not bypass specialist routing when the user requests consequential implementation, audit, or verification.
- Companions are conditional recommendations, not blanket mandatory dependencies. Existing quality rules still apply when relevant.
- The skill must not claim that a platform auto-loads or dispatches a skill unless that mechanism is available there.

## Routing examples used as acceptance criteria

| Prompt | Expected route |
|---|---|
| “Query database lambat; cari penyebabnya dan optimalkan” | `msal-insight` for diagnosis, then `msal-data` or `msal-engineer` only for the identified fix |
| “Buat form checkout dengan validasi, Server Action, dan tampilan responsif” | `msal-frontend` for action/data behavior and `msal-craft` for UI; sequence implementation if their decisions depend on each other |
| “Tulis README untuk library ini” | `msal-docsmith`; use `msal-content` only if audience-facing copy needs a separate pass |
| “Buat video promosi dalam MP4 dari data CSV” | `msal-cinecode`; do not route to web `msal-motion` unless interactive motion is also requested |
| “Perbaiki ini” with no artifact or context | Ask one focused clarification; do not guess a specialist |
| “Apa arti HTTP 404?” | Direct answer; no specialist or wave |
| Explicitly requests a specialist that is unavailable | Continue only if the primary task can be handled safely without it; disclose the missing capability |

## Scope of document updates

- Update the routing protocol and related workflow references in `maxilun/skills/maxilun/SKILL.md`.
- Align the skill's displayed/internal version with the repository's published version metadata and README badge; add a concise changelog entry if the repository convention requires it.
- Update `README.id.md` and `README.md` only where they describe routing behavior or version metadata, keeping both languages consistent.
- Do not change specialist skill content or user-level installed copies outside this repository.

## Validation

Review the edited routing instructions against every acceptance example above, check that companion skills are not described as guaranteed to exist, and check that version references agree. Do not add an automated router or claim the model's confidence is mathematically calibrated.
