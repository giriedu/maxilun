# Contributing to Maxilun

Thank you for your interest in contributing to Maxilun. This document covers how to add skills, where shared rules live, testing requirements, and code style conventions.

## Adding a New Specialist Skill

### 1. Create the skill directory

```
skills/maxilun-<name>/SKILL.md
```

### 2. Frontmatter template

Every SKILL.md must start with this YAML frontmatter:

```yaml
---
name: maxilun-<name>
description: >
  One-paragraph description of what this specialist does.
  Include trigger keywords in natural language.
metadata:
  version: "1.0.0"
  ecosystem: maxilun
  author: Maxilun Architecture
  license: Free-to-Use
  platforms:
    - claude-code
    - opencode
    - antigravity-cli
    - antigravity-ide
    - cursor
    - codex
    - zed
    - gemini-cli
---
```

### 3. Core Rules block + domain deltas

Every SKILL.md must contain the canonical `CORE-RULES` block, copied verbatim from `skills/maxilun/SKILL.md` (between the `<!-- CORE-RULES:START -->` and `<!-- CORE-RULES:END -->` markers). CI compares the block across all 18 skills and fails on drift.

After the block, declare only domain deltas:

```markdown
## 1. Engine Overrides

Delta domain terhadap Core Rules di atas. Override <name>:

- **Purity**: ...
- **Minimalist**: ...
```

Do not restate the engines. If a rule must change for everyone, change the canonical block in the orchestrator, then propagate it to all skills.

Shared detail lives in `skills/maxilun/references/` (`engines.md`, `discovery.md`, `purity-catalog.md`, `code-hygiene.md`). Reference it as `../maxilun/references/<file>.md`; CI resolves every such path and fails if the file is missing.

### 4. Register in orchestrator

Update the routing matrix in `skills/maxilun/SKILL.md` so the orchestrator can dispatch to your new specialist.

### 5. Update docs

Add the new skill row to `docs/SKILLS.md`.

### 6. Register in test suite

Add the new skill name to `EXPECTED_SKILLS` list in `scripts/test-suite.py`. PRs that add a skill without updating the test suite will fail CI.

## Adding or Changing a Shared Rule

There is no `rules/` directory. Shared material lives inside the orchestrator skill so it survives `npx skills add`, which copies skill folders only.

1. Rule applies to every skill → edit the `CORE-RULES` block in `skills/maxilun/SKILL.md`, then copy it verbatim into the other 17 skills.
2. Rule needs explanation longer than the block → add or edit a file in `skills/maxilun/references/` and link it from the block or from the relevant section.
3. Rule applies to one domain only → put it in that skill's `## 1. Engine Overrides` section.

Never create a rule file outside a skill folder: agents cannot see it, and the test suite will not install it.

## Testing Requirements

**Run the test suite before submitting any PR:**

```bash
python scripts/test-suite.py
```

The test suite validates:
- Frontmatter delimiters and required name, description, version, and license fields
- All 18 skills present and loadable
- Purity engine compliance (no banned cliches)
- Installer integrity
- Cross-platform script validity

PRs that fail the test suite will not be merged.

## Code Style

- **Body text**: Indonesian (Bahasa Indonesia) for SKILL.md content and user-facing documentation.
- **Technical terms**: English (e.g., "Server Components", "ORM", "CI/CD", "frontmatter").
- **Code blocks**: English identifiers, comments in Indonesian only when explaining non-obvious logic.
- **Naming**: `msal-<noun>` for specialists, kebab-case throughout.
- **Comments**: Explain *why*, never *what*. Delete commented-out code.

## Changelog

Update `CHANGELOG.md` under the appropriate section (`Added`, `Changed`, `Fixed`, `Removed`) following [Keep a Changelog](https://keepachangelog.com/) format.

## License Acceptance

By submitting a contribution, you agree that your work will be licensed under the project's current license. Ensure all submitted code is original or properly attributed.
