#!/usr/bin/env bash
set -euo pipefail

VERSION="1.1.0"
PROJECT_MODE=false
for arg in "$@"; do
    case "$arg" in
        --project|-p|-Project)
            PROJECT_MODE=true
            ;;
    esac
done

echo "🌑 Installing Maxilun ${VERSION} (25 skills + 13 autonomous agents)"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_SRC="${SCRIPT_DIR}/skills"
if [ ! -d "$SKILLS_SRC" ]; then
    SKILLS_SRC="${SCRIPT_DIR}/.agents/skills"
fi
AGENTS_SRC="${SCRIPT_DIR}/agents"

installed_to=()
installed_backups=()
python_available=false

# --- Python Dependency Check (Knowledge Graph) ---
check_python() {
    local candidates=("python3" "python" "py")
    for cmd in "${candidates[@]}"; do
        if command -v "$cmd" &>/dev/null; then
            local ver major minor
            ver=$("$cmd" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null) || true
            major=$(echo "$ver" | cut -d. -f1)
            minor=$(echo "$ver" | cut -d. -f2)
            if [ -n "$major" ] && [ -n "$minor" ] && [ "$major" -ge 3 ] && [ "$minor" -ge 8 ]; then
                python_available=true
                echo "✅ Python ${major}.${minor} detected ($cmd) — Knowledge Graph visualizer ready."
                return 0
            fi
        fi
    done
    echo "⚠️  Python 3.8+ not found. Knowledge Graph visualizer will be unavailable."
    echo "   Install Python from https://www.python.org/downloads/ and re-run this installer."
    echo "   All other Maxilun skills work without Python."
    return 1
}
check_python || true

# Remove v1 rule files left outside the skill folder. Only files carrying Maxilun markers.
clean_legacy_rules() {
    local rules_dir="$1"
    [ -d "$rules_dir" ] || return 0
    local removed=0
    for rule in always-on.md maxilun-global.md code-hygiene.md purity-catalog.md; do
        local f="${rules_dir}/${rule}"
        [ -f "$f" ] || continue
        if grep -Eq '^(# Maxilun|# Four Always-On Engines|# Aturan Global Maxilun)' "$f" 2>/dev/null; then
            rm -f -- "$f"
            removed=$((removed + 1))
        fi
    done
    [ "$removed" -gt 0 ] && echo "   cleaned ${removed} legacy rule file(s) from ${rules_dir}"
    return 0
}

# Remove legacy msal-* skill folders (superseded by maxilun-*)
clean_legacy_skills() {
    local target_dir="$1"
    [ -d "$target_dir" ] || return 0
    local removed=0
    for d in "${target_dir}"/msal-*; do
        [ -d "$d" ] || continue
        if [ -f "${d}/SKILL.md" ] && grep -Eq '^  ecosystem:\s*maxilun\s*$' "${d}/SKILL.md" 2>/dev/null; then
            rm -rf -- "$d"
            removed=$((removed + 1))
        fi
    done
    [ "$removed" -gt 0 ] && echo "   cleaned ${removed} legacy msal-* directory/directories from ${target_dir}"
    return 0
}

install_target() {
    local platform_name="$1"
    local target_dir="$2"
    local legacy_rules_dir="${3:-}"
    local agents_dir="${4:-}"
    local existing_maxilun=()
    if [ -d "$target_dir" ]; then
        while IFS= read -r -d '' d; do
            if [ -f "${d}/SKILL.md" ] && grep -Eq '^  ecosystem:\s*maxilun\s*$' "${d}/SKILL.md" 2>/dev/null; then
                existing_maxilun+=("$d")
            fi
        done < <(find "$target_dir" -mindepth 1 -maxdepth 1 -type d \( -name "maxilun" -o -name "maxilun-*" -o -name "msal-*" \) -print0 2>/dev/null)
    fi

    if [ ${#existing_maxilun[@]} -gt 0 ]; then
        local ts
        ts=$(date +%Y%m%d-%H%M%S 2>/dev/null || date +%s)
        local backup_root
        backup_root="$(dirname "$target_dir")/_maxilun_backup_${ts}"
        mkdir -p "$backup_root/skills"
        for d in "${existing_maxilun[@]}"; do
            cp -R "$d" "$backup_root/skills/"
            rm -rf -- "$d"
        done
        installed_backups+=("$platform_name: $backup_root")
    fi

    clean_legacy_skills "$target_dir"
    mkdir -p "$target_dir" 2>/dev/null || true
    cp -R "${SKILLS_SRC}/"* "$target_dir/" 2>/dev/null || true

    # Never ship bytecode or local scan caches
    find "$target_dir" -type d \( -name __pycache__ -o -name .maxilun -o -name maxilun-out \) -prune -exec rm -rf {} + 2>/dev/null || true
    find "$target_dir" -type f -name '*.pyc' -delete 2>/dev/null || true
    [ -n "$legacy_rules_dir" ] && clean_legacy_rules "$legacy_rules_dir"

    if [ -n "$agents_dir" ] && [ -d "$AGENTS_SRC" ]; then
        mkdir -p "$agents_dir" 2>/dev/null || true
        cp -R "${AGENTS_SRC}/"* "$agents_dir/" 2>/dev/null || true
    fi

    installed_to+=("$platform_name: $target_dir")
}

if [ "$PROJECT_MODE" = true ]; then
    CURRENT_DIR="$(pwd)"
    install_target "Universal / Antigravity / Zed (Project)" "${CURRENT_DIR}/.agents/skills" "${CURRENT_DIR}/.agents/rules" "${CURRENT_DIR}/.agents/agents"
    install_target "[CC] / Termul (Project)" "${CURRENT_DIR}/.claude/skills" "${CURRENT_DIR}/.claude/rules" "${CURRENT_DIR}/.claude/agents"
    install_target "Trae (Project)" "${CURRENT_DIR}/.trae/skills"
    install_target "Windsurf (Project)" "${CURRENT_DIR}/.windsurf/skills"
    install_target "CodeBuddy (Project)" "${CURRENT_DIR}/.codebuddy/skills"
else
    install_target "Antigravity CLI/IDE & Zed" "${HOME}/.agents/skills" "${HOME}/.agents/rules" "${HOME}/.agents/agents"
    install_target "[CC] & Termul" "${HOME}/.claude/skills" "${HOME}/.claude/rules" "${HOME}/.claude/agents"

    if [ -d "${HOME}/.codex" ]; then
        install_target "Codex" "${HOME}/.codex/skills" "${HOME}/.codex/rules"
    fi
    if [ -d "${HOME}/.config/opencode" ]; then
        install_target "OpenCode" "${HOME}/.config/opencode/skills" "${HOME}/.config/opencode/rules" "${HOME}/.config/opencode/agents"
    elif [ -d "${HOME}/.opencode" ]; then
        install_target "OpenCode" "${HOME}/.opencode/skills" "${HOME}/.opencode/rules" "${HOME}/.opencode/agents"
    fi
    if [ -d "${HOME}/.gemini" ]; then
        install_target "Gemini CLI" "${HOME}/.gemini/config/skills"
    fi
    if [ -d "${HOME}/.cursor" ]; then
        install_target "Cursor" "${HOME}/.cursor/skills"
    fi
    if [ -d "${HOME}/.trae" ]; then
        install_target "Trae" "${HOME}/.trae/skills"
    fi
    if [ -d "${HOME}/.windsurf" ]; then
        install_target "Windsurf" "${HOME}/.windsurf/skills"
    fi
    if [ -d "${HOME}/.codebuddy" ]; then
        install_target "CodeBuddy" "${HOME}/.codebuddy/skills"
    fi
fi

echo ""
if [ ${#installed_backups[@]} -gt 0 ]; then
    echo "⚠️  Previous versions backed up to:"
    for loc in "${installed_backups[@]}"; do
        echo "   → $loc"
    done
fi
echo ""
if [ ${#installed_to[@]} -eq 0 ]; then
    echo "⚠️  No supported AI CLI/IDE detected automatically."
    echo "   Tip: use 'npx skills add giriedu/maxilun' for interactive installation."
else
    echo "✅ Maxilun installed to:"
    for loc in "${installed_to[@]}"; do
        echo "   → $loc"
    done
fi

echo ""
echo "──────────────────────────────────────"
echo "  Post-Install Verification"
echo "──────────────────────────────────────"
verify_ok=true
for loc_entry in "${installed_to[@]}"; do
    target_dir="${loc_entry#*: }"
    platform_label="${loc_entry%%:*}"
    skill_count=$(find "$target_dir" -maxdepth 2 \( -path "*/maxilun/SKILL.md" -o -path "*/maxilun-*/SKILL.md" -o -path "*/msal-*/SKILL.md" \) 2>/dev/null | wc -l | tr -d ' ')
    if [ "$skill_count" -ge 18 ]; then
        echo "  ✅ ${platform_label}: ${skill_count}/18 skills"
    else
        echo "  ❌ ${platform_label}: only ${skill_count}/18 skills — reinstall recommended"
        verify_ok=false
    fi
    if [ -f "${target_dir}/maxilun/references/engines.md" ]; then
        echo "     ✅ rules bundled inside skill (references/)"
    else
        echo "     ❌ references/engines.md missing — skill would run without core rules"
        verify_ok=false
    fi
    if find "$target_dir" -type d -name __pycache__ -print -quit 2>/dev/null | grep -q .; then
        echo "     ⚠️  __pycache__ present in install"
    fi
done
if $python_available; then
    kg_cli=""
    for loc_entry in "${installed_to[@]}"; do
        candidate="${loc_entry#*: }/maxilun-knowledge-graph/cli.py"
        if [ -f "$candidate" ]; then
            kg_cli="$candidate"
            break
        fi
    done
    if [ -n "$kg_cli" ]; then
        echo "  ✅ Knowledge Graph CLI: ${kg_cli}"
    else
        echo "  ⚠️  Knowledge Graph CLI: cli.py not found"
        verify_ok=false
    fi
else
    echo "  ⏭️  Knowledge Graph CLI: skipped (Python not available)"
fi
echo ""
if $verify_ok; then
    echo "  🎉 All checks passed. Maxilun ${VERSION} is operational."
else
    echo "  ⚠️  Some checks failed. Review output above and re-run the installer."
    exit 1
fi
echo ""
