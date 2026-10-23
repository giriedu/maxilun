#!/usr/bin/env bash
set -euo pipefail

echo "🌑 Maxilun Uninstaller"
echo "──────────────────────────────────────"
echo ""
echo "This will remove all Maxilun skills and rules from your system."
echo ""

read -rp "Are you sure you want to continue? [y/N] " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

removed=()
targets=(
    "Antigravity CLI/IDE:${HOME}/.agents/skills:${HOME}/.agents/rules"
    "Claude Code:${HOME}/.claude/skills:${HOME}/.claude/rules"
    "Codex:${HOME}/.codex/skills:${HOME}/.codex/rules"
    "OpenCode:${HOME}/.config/opencode/skills:${HOME}/.config/opencode/rules"
    "Gemini CLI:${HOME}/.gemini/config/skills:"
    "Cursor:${HOME}/.cursor/skills:"
)

for entry in "${targets[@]}"; do
    IFS=':' read -r name skills_dir rules_dir <<< "$entry"
    
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
