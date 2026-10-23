#!/usr/bin/env bash
set -euo pipefail

echo "🌑 Installing Maxilun Skill Ecosystem (18 Specialist Skills + 4 Always-On Engines)..."
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_SRC="${SCRIPT_DIR}/skills"
if [ ! -d "$SKILLS_SRC" ]; then
    SKILLS_SRC="${SCRIPT_DIR}/.agents/skills"
fi
RULES_SRC="${SCRIPT_DIR}/rules"

installed_to=()
installed_backups=()
python_available=false

# --- Python Dependency Check ---
check_python() {
    local candidates=("python3" "python" "py")
    for cmd in "${candidates[@]}"; do
        if command -v "$cmd" &>/dev/null; then
            local ver
            ver=$("$cmd" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null) || true
            local major minor
            major=$(echo "$ver" | cut -d. -f1)
            minor=$(echo "$ver" | cut -d. -f2)
            if [ -n "$major" ] && [ -n "$minor" ]; then
                if [ "$major" -ge 3 ] && [ "$minor" -ge 8 ]; then
                    python_available=true
                    echo "✅ Python ${major}.${minor} detected ($cmd) — Knowledge Graph visualizer ready."
                    return 0
                fi
            fi
        fi
    done
    echo "⚠️  Python 3.8+ not found. Knowledge Graph visualizer (/graph) will be unavailable."
    echo "   Install Python from https://www.python.org/downloads/ and re-run this installer."
    echo "   Other Maxilun skills work without Python."
    return 1
}
check_python || true

install_target() {
    local platform_name="$1"
    local target_dir="$2"
    local rules_dir="${3:-}"

    # Backup existing skills/rules before overwrite (keep one backup per run)
    if [ -d "$target_dir" ] && [ -n "$(ls -A "$target_dir" 2>/dev/null)" ]; then
        local backup_root
        backup_root="$(dirname "$target_dir")/_maxilun_backup_$(date +%Y%m%d-%H%M%S%N)"
        mkdir -p "$backup_root"
        cp -R "$target_dir" "$backup_root/skills"
        if [ -n "$rules_dir" ] && [ -d "$rules_dir" ]; then
            cp -R "$rules_dir" "$backup_root/rules"
        fi
        installed_backups+=("$platform_name: $backup_root")
    fi

    mkdir -p "$target_dir" 2>/dev/null || true
    cp -R "${SKILLS_SRC}/"* "$target_dir/" 2>/dev/null || true
    if [ -n "$rules_dir" ] && [ -d "$RULES_SRC" ]; then
        mkdir -p "$rules_dir" 2>/dev/null || true
        cp -R "${RULES_SRC}/"* "$rules_dir/" 2>/dev/null || true
    fi
    installed_to+=("$platform_name: $target_dir")
}

# 1. Antigravity / Agent Protocol / Zed (~/.agents/skills/)
install_target "Antigravity CLI/IDE & Zed" "${HOME}/.agents/skills" "${HOME}/.agents/rules"

# 2. Claude Code & Termul (~/.claude/skills/)
install_target "Claude Code & Termul" "${HOME}/.claude/skills" "${HOME}/.claude/rules"

# 3. Codex (~/.codex/skills/)
if [ -d "${HOME}/.codex" ]; then
    install_target "Codex" "${HOME}/.codex/skills" "${HOME}/.codex/rules"
fi

# 4. OpenCode (~/.config/opencode/skills/ or ~/.opencode/skills/)
if [ -d "${HOME}/.config/opencode" ]; then
    install_target "OpenCode" "${HOME}/.config/opencode/skills" "${HOME}/.config/opencode/rules"
elif [ -d "${HOME}/.opencode" ]; then
    install_target "OpenCode" "${HOME}/.opencode/skills" "${HOME}/.opencode/rules"
fi

# 5. Gemini CLI (~/.gemini/config/skills/)
if [ -d "${HOME}/.gemini" ]; then
    install_target "Gemini CLI" "${HOME}/.gemini/config/skills"
fi

# 6. Cursor (~/.cursor/skills/)
if [ -d "${HOME}/.cursor" ]; then
    install_target "Cursor" "${HOME}/.cursor/skills"
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
    echo "   Tip: Use 'npx skills add giriedu/maxilun' for interactive skill & agent installation."
else
    echo "✅ Maxilun installed successfully to:"
    for loc in "${installed_to[@]}"; do
        echo "   → $loc"
    done
fi

echo "🌑 Maxilun ecosystem ready. Type /maxilun or /msal to verify."
echo ""
echo "18 Specialist Skills Installed:"
echo "   1.  maxilun              — Master Orchestrator (/maxilun, /msal)"
echo "   2.  msal-knowledge-graph — Dependency & Repo Graph (AST/Lens)"
echo "   3.  msal-scaffold        — Project Context Scaffolder (docs/)"
echo "   4.  msal-architect       — Architecture & API Design (/msal-think)"
echo "   5.  msal-sentinel        — Security, Auth, & Privacy"
echo "   6.  msal-engineer        — Code, Bugfix, & Refactor"
echo "   7.  msal-data            — Database & Data Layer"
echo "   8.  msal-frontend        — RSC, App Router, & Server Actions"
echo "   9.  msal-verify          — QA, E2E, & Regression"
echo "   10. msal-insight         — Diagnostics & Root Cause"
echo "   11. msal-deploy          — CI/CD, Docker, & Monitoring"
echo "   12. msal-docsmith        — Technical Docs & API Contracts"
echo "   13. msal-craft           — UI/UX & Design Systems"
echo "   14. msal-motion          — Motion Design & Animation"
echo "   15. msal-cinecode        — Programmatic Video & Render Pipeline"
echo "   16. msal-diagrams        — Diagrams & Flow Mapping"
echo "   17. msal-content         — Copywriting & Brand Voice"
echo "   18. msal-seo-audit       — Technical SEO & Web Vitals"
echo ""
echo "4 Always-On Engines Active:"
echo "   ✓ Focus Engine (Executive HUD & Working-Memory Scaffold)"
echo "   ✓ Purity Engine (Purpose Gate & Zero AI Fluff)"
echo "   ✓ Minimalist Engineering Engine (The Simplicity Ladder)"
echo "   ✓ Clarity Engine (High-Density Technical Synthesis)"

# --- Post-Install Verification ---
echo ""
echo "──────────────────────────────────────"
echo "  Post-Install Verification"
echo "──────────────────────────────────────"
verify_ok=true
for loc_entry in "${installed_to[@]}"; do
    target_dir="${loc_entry#*: }"
    platform_label="${loc_entry%%:*}"
    skill_count=$(find "$target_dir" -maxdepth 2 \( -path "*/maxilun/SKILL.md" -o -path "*/msal-*/SKILL.md" \) 2>/dev/null | wc -l)
    if [ "$skill_count" -ge 18 ]; then
        echo "  ✅ ${platform_label}: ${skill_count}/18 skills verified"
    else
        echo "  ❌ ${platform_label}: Only ${skill_count}/18 skills found — reinstall recommended"
        verify_ok=false
    fi
done
if $python_available; then
    kg_cli=""
    for loc_entry in "${installed_to[@]}"; do
        candidate="${loc_entry#*: }/msal-knowledge-graph/cli.py"
        if [ -f "$candidate" ]; then
            kg_cli="$candidate"
            break
        fi
    done
    if [ -n "$kg_cli" ]; then
        echo "  ✅ Knowledge Graph CLI: Found at $kg_cli"
    else
        echo "  ⚠️  Knowledge Graph CLI: cli.py not found in installed skills"
        verify_ok=false
    fi
else
    echo "  ⏭️  Knowledge Graph CLI: Skipped (Python not available)"
fi
echo ""
if $verify_ok; then
    echo "  🎉 All checks passed. Maxilun is fully operational."
else
    echo "  ⚠️  Some checks failed. Review output above and re-run installer if needed."
    exit 1
fi
echo ""
