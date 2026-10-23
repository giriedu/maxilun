# Maxilun Routing Protocol Implementation Plan

> **For agentic workers:** Implement each document task in order. This plan has no code or automated-test changes.

**Goal:** Make Maxilun routing clearer for natural-language, mixed-domain, ambiguous, and unsupported prompts.

**Architecture:** Keep the routing procedure in the orchestrator entrypoint, with the specialist catalog as its domain map. Use evidence-based confidence bands and conditional companions; update both localized READMEs and version notes to match the documented behavior.

**Tech Stack:** Markdown skill instructions and project documentation.

---

### Task 1: Replace conflicting routing rules with one decision protocol

**Files:**
- Modify: `maxilun/skills/maxilun/SKILL.md`

- [x] Remove blanket mandatory-companion claims and duplicated phrase-only dispatch rules.
- [x] Add ordered routing steps: explicit command, requested outcome and constraints, primary specialist, confidence band, conditional companion, unavailable-skill fallback, and no-match behavior.
- [x] Keep disambiguation and wave coordination that remain useful, but make examples conform to the new rules.

### Task 2: Align public docs and version metadata

**Files:**
- Modify: `maxilun/README.md`
- Modify: `maxilun/README.id.md`
- Modify: `maxilun/CHANGELOG.md`
- Modify: `maxilun/skills/maxilun/SKILL.md`

- [x] Ensure both READMEs describe the actual evidence-based routing and use one consistent release version.
- [x] Update the skill metadata/version label and add a concise changelog entry for the routing improvement.
- [x] Do not edit user-level installed copies outside this repository.

### Task 3: Review documentation consistency

**Files:**
- Review: all files modified in Tasks 1–2
- Review: `docs/superpowers/specs/2026-10-23-maxilun-routing-design.md`

- [x] Check each design acceptance example against the new routing rules.
- [x] Check that unavailable external skills are not promised as auto-loaded.
- [x] Check that the release version agrees across the skill and both READMEs.
- [x] Do not add or run automated tests; the request is for skill/documentation changes and no test run was requested.
