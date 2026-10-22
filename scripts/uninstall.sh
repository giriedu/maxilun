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
        maxilun_skills=$(find "$skills_dir" -maxdepth 1 -type d \( -name "maxilun*" -o -name "msal*" \) 2>/dev/null)
        if [ -n "$maxilun_skills" ]; then
            for skill_path in $maxilun_skills; do
                rm -rf "$skill_path"
            done
            removed+=("$name (skills): $skills_dir")
            echo "  Removed Maxilun/MSAL skills from: $skills_dir"
        fi
    fi
    
    if [ -n "$rules_dir" ] && [ -d "$rules_dir" ]; then
        maxilun_rules=$(find "$rules_dir" -maxdepth 1 -name "*maxilun*" -o -name "always-on.md" -o -name "code-hygiene.md" -o -name "purity-catalog.md" 2>/dev/null)
        if [ -n "$maxilun_rules" ]; then
            for rule_file in $maxilun_rules; do
                if grep -qi "maxilun" "$rule_file" 2>/dev/null; then
                    rm -f "$rule_file"
                fi
            done
            removed+=("$name (rules): $rules_dir")
            echo "  Removed Maxilun rules from: $rules_dir"
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
