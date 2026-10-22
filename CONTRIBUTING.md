# Contributing to Maxilun

Thank you for your interest in contributing to Maxilun. This document covers how to add skills, rules, testing requirements, and code style conventions.

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
  license: Maxilun-Source-Available-2.0
  platforms:
    - claude-code
    - antigravity-cli
    - antigravity-ide
    - cursor
    - codex
  rules:
    - rules/always-on.md
    - rules/maxilun-global.md
    - rules/code-hygiene.md
    - rules/purity-catalog.md
---
```

### 3. Delta-only engine pattern

Specialists **must not** restate the 4 always-on engines. Instead, declare only overrides:

```markdown
## 1. Engine Overrides

Skill ini beroperasi **delta-only** terhadap `rules/always-on.md`.
Semua aturan global Maxilun berlaku penuh. Override spesifik <name>:

- **Focus**: ...
- **Purity**: ...
```

This saves ~2,500 tokens per session vs full restatement.

### 4. Register in orchestrator

Update the routing matrix in `skills/maxilun/SKILL.md` so the orchestrator can dispatch to your new specialist.

### 5. Update docs

Add the new skill row to `docs/SKILLS.md`.

### 6. Register in test suite

Add the new skill name to `EXPECTED_SKILLS` list in `scripts/test-suite.py`. PRs that add a skill without updating the test suite will fail CI.

## Adding a New Rule

1. Create `rules/<rule-name>.md` with clear, actionable directives.
2. Reference it in relevant SKILL.md frontmatter under `metadata.rules:`.
3. If the rule applies globally, add it to `rules/always-on.md` instead.

## Testing Requirements

**Run the test suite before submitting any PR:**

```bash
python scripts/test-suite.py
```

The test suite validates:
- Frontmatter YAML structure on all SKILL.md files
- All 18 skills present and loadable
- Purity engine compliance (no banned cliches)
- Installer integrity
- Cross-platform script validity

PRs that fail the test suite will not be merged.

## Code Style

- **Body text**: Indonesian (Bahasa Indonesia) for SKILL.md content and user-facing documentation.
- **Technical terms**: English (e.g., "Server Components", "ORM", "CI/CD", "frontmatter").
- **Code blocks**: English identifiers, comments in Indonesian only when explaining non-obvious logic.
- **Naming**: `maxilun-<noun>` for specialists, kebab-case throughout.
- **Comments**: Explain *why*, never *what*. Delete commented-out code.

## Changelog

Update `CHANGELOG.md` under the appropriate section (`Added`, `Changed`, `Fixed`, `Removed`) following [Keep a Changelog](https://keepachangelog.com/) format.

## License Acceptance

By submitting a contribution, you agree that your work will be licensed under the project's current license. Ensure all submitted code is original or properly attributed.
