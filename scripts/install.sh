#!/usr/bin/env bash
set -euo pipefail

VERSION="1.3.0"
PROJECT_MODE=false
for arg in "$@"; do
    case "$arg" in
        --project|-p|-Project)
            PROJECT_MODE=true
            ;;
    esac
done

echo "🌑 Installing Maxilun ${VERSION} (27 skills + 21 autonomous agents)"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_SRC="${SCRIPT_DIR}/skills"
if [ ! -d "$SKILLS_SRC" ]; then
    SKILLS_SRC="${SCRIPT_DIR}/.agents/skills"
fi
AGENTS_SRC="${SCRIPT_DIR}/agents"
expected_skill_count=$(find "$SKILLS_SRC" -maxdepth 2 -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
if [ -z "$expected_skill_count" ] || [ "$expected_skill_count" -le 0 ]; then
    expected_skill_count=27
fi
CURRENT_DIR="$(pwd)"

installed_to=()
installed_agents=()
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
            if [ -n "$major" ] && [ -n "$minor" ] && { [ "$major" -gt 3 ] || { [ "$major" -eq 3 ] && [ "$minor" -ge 8 ]; }; }; then
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
        if [ -f "${d}/SKILL.md" ] && grep -Eq '^  ecosystem:[[:space:]]*maxilun[[:space:]]*$' "${d}/SKILL.md" 2>/dev/null; then
            rm -rf -- "$d"
            removed=$((removed + 1))
        fi
    done
    [ "$removed" -gt 0 ] && echo "   cleaned ${removed} legacy msal-* directory/directories from ${target_dir}"
    return 0
}

# Copy agent definitions (*.md only). Owned maxilun-*.md files are removed first so
# renamed/removed agents never linger. format=omp rewrites frontmatter for OMP:
# drops the `model:` line (OMP model selector) and lowercases tool names.
install_agents() {
    local platform_name="$1"
    local agents_dir="$2"
    local format="${3:-claude}"
    [ -d "$AGENTS_SRC" ] || return 0
    mkdir -p "$agents_dir"
    local f dest
    for f in "$agents_dir"/maxilun-*.md; do
        [ -f "$f" ] || continue
        rm -f -- "$f"
    done
    for f in "$AGENTS_SRC"/*.md; do
        [ -f "$f" ] || continue
        dest="${agents_dir}/$(basename "$f")"
        if [ "$format" = omp ]; then
            awk '
                NR == 1 && /^---/ { fm = 1; print; next }
                fm && /^---/ { fm = 0 }
                fm && /^model:/ { next }
                fm && /^  - (Read|Grep|Glob|Bash|Write|Edit)[[:space:]]*$/ { sub(/- [A-Za-z]+/, "- " tolower($2)) }
                { print }
            ' "$f" > "$dest" || { echo "❌ Failed to write ${dest}" >&2; exit 1; }
        else
            cp -- "$f" "$dest" || { echo "❌ Failed to copy ${f} to ${agents_dir}" >&2; exit 1; }
        fi
    done
    installed_agents+=("$platform_name: $agents_dir")
}

install_target() {
    local platform_name="$1"
    local target_dir="$2"
    local legacy_rules_dir="${3:-}"
    local agents_dir="${4:-}"
    local existing_maxilun=()
    if [ -d "$target_dir" ]; then
        while IFS= read -r -d '' d; do
            if [ -f "${d}/SKILL.md" ] && grep -Eq '^  ecosystem:[[:space:]]*maxilun[[:space:]]*$' "${d}/SKILL.md" 2>/dev/null; then
                existing_maxilun+=("$d")
            fi
        done < <(find "$target_dir" -mindepth 1 -maxdepth 1 \( -type d -o -type l \) \( -name "maxilun" -o -name "maxilun-*" -o -name "msal-*" \) -print0 2>/dev/null)
    fi

    if [ ${#existing_maxilun[@]} -gt 0 ]; then
        local ts parent_dir backup_root b i
        ts=$(date +%Y%m%d-%H%M%S 2>/dev/null || date +%s)
        parent_dir="$(dirname "$target_dir")"
        backup_root="${parent_dir}/_maxilun_backup_${ts}"
        mkdir -p "$backup_root/skills"
        for d in "${existing_maxilun[@]}"; do
            cp -R -- "$d" "$backup_root/skills/" || { echo "❌ Backup of ${d} failed; aborting." >&2; exit 1; }
            rm -rf -- "$d"
        done
        installed_backups+=("$platform_name: $backup_root")
        # Keep at most 2 most recent backups (timestamped names glob in chronological order)
        local backups=()
        for b in "$parent_dir"/_maxilun_backup_*; do
            [ -d "$b" ] && backups+=("$b")
        done
        for ((i = 0; i < ${#backups[@]} - 2; i++)); do
            rm -rf -- "${backups[$i]}"
        done
    fi

    clean_legacy_skills "$target_dir"
    mkdir -p "$target_dir"
    local src name
    for src in "$SKILLS_SRC"/*/; do
        [ -d "$src" ] || continue
        src="${src%/}"
        name="$(basename "$src")"
        cp -R -- "$src" "$target_dir/" || { echo "❌ Failed to copy ${name} to ${target_dir}" >&2; exit 1; }
        # Never ship bytecode or local scan caches (scoped to the skill just copied)
        find "${target_dir}/${name}" -type d \( -name __pycache__ -o -name .maxilun -o -name maxilun-out \) -prune -exec rm -rf {} +
        find "${target_dir}/${name}" -type f -name '*.pyc' -delete
    done
    [ -n "$legacy_rules_dir" ] && clean_legacy_rules "$legacy_rules_dir"

    if [ -n "$agents_dir" ]; then
        install_agents "$platform_name" "$agents_dir"
    fi

    installed_to+=("$platform_name: $target_dir")
}

if [ "$PROJECT_MODE" = true ]; then
    CURRENT_DIR="$(pwd)"
    install_target "Universal / Antigravity / Zed (Project)" "${CURRENT_DIR}/.agents/skills" "${CURRENT_DIR}/.agents/rules" "${CURRENT_DIR}/.agents/agents"
    install_target "OpenCode (Project)" "${CURRENT_DIR}/.opencode/skills" "${CURRENT_DIR}/.opencode/rules" "${CURRENT_DIR}/.opencode/agents"
    install_target "[CC] / Termul (Project)" "${CURRENT_DIR}/.claude/skills" "${CURRENT_DIR}/.claude/rules" "${CURRENT_DIR}/.claude/agents"
    install_agents "OMP (Project)" "${CURRENT_DIR}/.omp/agents" omp
    [ -d "${CURRENT_DIR}/.cursor" ] && install_target "Cursor (Project)" "${CURRENT_DIR}/.cursor/skills"
    install_target "Trae (Project)" "${CURRENT_DIR}/.trae/skills"
    install_target "Windsurf (Project)" "${CURRENT_DIR}/.windsurf/skills"
    install_target "CodeBuddy (Project)" "${CURRENT_DIR}/.codebuddy/skills"
else
    codex_home="${CODEX_HOME:-${HOME}/.codex}"
    xdg_config="${XDG_CONFIG_HOME:-${HOME}/.config}"
    install_target "Antigravity CLI/IDE & Zed" "${HOME}/.agents/skills" "${HOME}/.agents/rules" "${HOME}/.agents/agents"
    install_target "[CC] & Termul" "${HOME}/.claude/skills" "${HOME}/.claude/rules" "${HOME}/.claude/agents"

    if [ -d "${HOME}/.omp" ]; then
        install_agents "OMP" "${HOME}/.omp/agent/agents" omp
    fi
    if [ -d "$codex_home" ]; then
        install_target "Codex" "${codex_home}/skills" "${codex_home}/rules" "${codex_home}/agents"
    fi
    if [ -d "${xdg_config}/opencode" ]; then
        install_target "OpenCode" "${xdg_config}/opencode/skills" "${xdg_config}/opencode/rules" "${xdg_config}/opencode/agents"
    elif [ -d "${HOME}/.opencode" ]; then
        install_target "OpenCode" "${HOME}/.opencode/skills" "${HOME}/.opencode/rules" "${HOME}/.opencode/agents"
    fi
    if [ -d "${HOME}/.gemini/config/skills" ]; then
        install_target "Gemini CLI / Antigravity Config" "${HOME}/.gemini/config/skills"
    fi
    if [ -d "${HOME}/.gemini" ]; then
        install_target "Gemini CLI" "${HOME}/.gemini/skills"
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
if [ ${#installed_agents[@]} -gt 0 ]; then
    echo "✅ Agents installed to:"
    for loc in "${installed_agents[@]}"; do
        echo "   → $loc"
    done
fi

# Register the knowledge graph as a native MCP tool in Claude Code (idempotent),
# so agents call kg_locate instead of falling back to grep.
if [ "${MAXILUN_NO_MODIFY:-0}" != "1" ] && command -v claude >/dev/null 2>&1 && ! claude mcp get maxilun-kg >/dev/null 2>&1; then
    kg_py=$(command -v python3 || command -v python || true)
    if [ "$PROJECT_MODE" = true ]; then
        kg_candidates=("${CURRENT_DIR}/.claude/skills/maxilun-knowledge-graph/mcp_server.py:project")
    else
        kg_candidates=("${HOME}/.claude/skills/maxilun-knowledge-graph/mcp_server.py:user")
    fi
    for kg in "${kg_candidates[@]}"; do
        if [ -n "$kg_py" ] && [ -f "${kg%:*}" ]; then
            claude mcp add --scope "${kg##*:}" maxilun-kg -- "$kg_py" "${kg%:*}" >/dev/null 2>&1 \
                && echo "✅ maxilun-kg MCP server registered in Claude Code (${kg##*:} scope)" || true
            break
        fi
    done
fi

# Codex: register maxilun-kg in $CODEX_HOME/config.toml (global only) or .codex/config.toml (project) when absent.
if [ "$PROJECT_MODE" = true ]; then
    codex_home="${CURRENT_DIR}/.codex"
else
    codex_home="${CODEX_HOME:-${HOME}/.codex}"
fi
codex_kg="${codex_home}/skills/maxilun-knowledge-graph/mcp_server.py"
codex_py=$(command -v python3 || command -v python || true)
if [ "${MAXILUN_NO_MODIFY:-0}" != "1" ] && [ -n "$codex_py" ] && [ -f "${codex_home}/config.toml" ] && [ -f "$codex_kg" ] && ! grep -q '^\[mcp_servers.maxilun-kg\]' "${codex_home}/config.toml"; then
    printf '\n[mcp_servers.maxilun-kg]\ncommand = "%s"\nargs = ["%s"]\n' "$codex_py" "$codex_kg" >> "${codex_home}/config.toml" \
        && echo "✅ maxilun-kg MCP server registered in Codex" || true
fi

# Council mode survives compaction via a UserPromptSubmit hook (idempotent).
# No `claude` CLI check: the desktop app reads ~/.claude/settings.json without it on PATH.
council_hook="${HOME}/.claude/skills/maxilun/scripts/council_hook.py"
[ "$PROJECT_MODE" = true ] && council_hook="${CURRENT_DIR}/.claude/skills/maxilun/scripts/council_hook.py"
council_py="$(command -v python3 || command -v python || true)"
if [ "${MAXILUN_NO_MODIFY:-0}" != "1" ] && [ -n "$council_py" ] && [ -f "$council_hook" ]; then
    "$council_py" "$council_hook" --install || echo "⚠️  council_hook.py --install failed; run manually if needed."
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
    if [ "$skill_count" -ge "$expected_skill_count" ]; then
        echo "  ✅ ${platform_label}: ${skill_count}/${expected_skill_count} skills"
    else
        echo "  ❌ ${platform_label}: only ${skill_count}/${expected_skill_count} skills — reinstall recommended"
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
