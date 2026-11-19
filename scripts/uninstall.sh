#!/usr/bin/env bash
set -euo pipefail
PROJECT_MODE=false
for arg in "$@"; do
    case "$arg" in
        --project|-p|-Project)
            PROJECT_MODE=true
            ;;
    esac
done

echo "🌑 Maxilun Uninstaller"
echo "──────────────────────────────────────"
echo "This will remove all Maxilun skills and rules from your system."
echo ""

read -rp "Are you sure you want to continue? [y/N] " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

removed=()
if [ "$PROJECT_MODE" = true ]; then
    CURRENT_DIR="$(pwd)"
    targets=(
        "Universal / Antigravity / Zed (Project):${CURRENT_DIR}/.agents/skills:${CURRENT_DIR}/.agents/rules:${CURRENT_DIR}/.agents/agents"
        "OpenCode (Project):${CURRENT_DIR}/.opencode/skills:${CURRENT_DIR}/.opencode/rules:${CURRENT_DIR}/.opencode/agents"
        "Claude Code (Project):${CURRENT_DIR}/.claude/skills:${CURRENT_DIR}/.claude/rules:${CURRENT_DIR}/.claude/agents"
        "Trae (Project):${CURRENT_DIR}/.trae/skills::"
        "Windsurf (Project):${CURRENT_DIR}/.windsurf/skills::"
        "CodeBuddy (Project):${CURRENT_DIR}/.codebuddy/skills::"
    )
else
    targets=(
        "Antigravity CLI/IDE:${HOME}/.agents/skills:${HOME}/.agents/rules:${HOME}/.agents/agents"
        "Claude Code:${HOME}/.claude/skills:${HOME}/.claude/rules:${HOME}/.claude/agents"
        "Codex:${HOME}/.codex/skills:${HOME}/.codex/rules:"
        "OpenCode (.config):${HOME}/.config/opencode/skills:${HOME}/.config/opencode/rules:${HOME}/.config/opencode/agents"
        "OpenCode:${HOME}/.opencode/skills:${HOME}/.opencode/rules:${HOME}/.opencode/agents"
        "Gemini CLI:${HOME}/.gemini/config/skills::"
        "Cursor:${HOME}/.cursor/skills::"
        "Trae:${HOME}/.trae/skills::"
        "Windsurf:${HOME}/.windsurf/skills::"
        "CodeBuddy:${HOME}/.codebuddy/skills::"
    )
fi

for entry in "${targets[@]}"; do
    IFS=':' read -r name skills_dir rules_dir agents_dir <<< "$entry"
    
    if [ -d "$skills_dir" ]; then
        removed_skills=0
        while IFS= read -r -d '' skill_path; do
            if [ -f "$skill_path/SKILL.md" ] && grep -Eq '^  ecosystem:[[:space:]]*maxilun[[:space:]]*$' "$skill_path/SKILL.md"; then
                rm -rf -- "$skill_path"
                removed_skills=$((removed_skills + 1))
            fi
        done < <(find "$skills_dir" -mindepth 1 -maxdepth 1 -type d \( -name "maxilun" -o -name "maxilun-*" -o -name "msal-*" \) -print0 2>/dev/null)
        if [ "$removed_skills" -gt 0 ]; then
            removed+=("$name (skills): $skills_dir")
            echo "  Removed $removed_skills owned Maxilun skill(s) from: $skills_dir"
        fi
    fi

    if [ -n "${agents_dir:-}" ] && [ -d "$agents_dir" ]; then
        removed_agents=0
        while IFS= read -r -d '' agent_path; do
            rm -f -- "$agent_path"
            removed_agents=$((removed_agents + 1))
        done < <(find "$agents_dir" -mindepth 1 -maxdepth 1 -type f -name "maxilun-*.md" -print0 2>/dev/null)
        if [ "$removed_agents" -gt 0 ]; then
            removed+=("$name (agents): $agents_dir")
            echo "  Removed $removed_agents Maxilun agent definitions from: $agents_dir"
        fi
    fi
    
    if [ -n "$rules_dir" ] && [ -d "$rules_dir" ]; then
        removed_rules=0
        while IFS= read -r -d '' rule_file; do
            case "$(basename "$rule_file")" in
                always-on.md) marker='^# (Tujuh Mesin Wajib Maxilun|Four Always-On Engines and Three Operating Protocols|Maxilun Always-On)' ;;
                maxilun-global.md) marker='^# Aturan Global Maxilun' ;;
                code-hygiene.md) marker='^# Maxilun Code Hygiene Rules' ;;
                purity-catalog.md) marker='^# Maxilun Purity Catalog' ;;
                *) continue ;;
            esac
            if grep -Eq "$marker" "$rule_file" 2>/dev/null; then
                rm -f -- "$rule_file"
                removed_rules=$((removed_rules + 1))
            fi
        done < <(find "$rules_dir" -maxdepth 1 -type f \( -name "always-on.md" -o -name "maxilun-global.md" -o -name "code-hygiene.md" -o -name "purity-catalog.md" \) -print0 2>/dev/null)
        if [ "$removed_rules" -gt 0 ]; then
            removed+=("$name (legacy rules): $rules_dir")
            echo "  Removed $removed_rules legacy Maxilun rule file(s) from: $rules_dir"
        fi
    fi
done

echo ""
if [ ${#removed[@]} -eq 0 ]; then
    echo "No Maxilun installation found."
else
    echo "✅ Maxilun removed from ${#removed[@]} location(s)."
fi
echo ""
