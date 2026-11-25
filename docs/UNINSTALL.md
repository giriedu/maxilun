# Uninstaller Maxilun

Uninstaller menghapus 27 skill dan 21 agen Maxilun dari semua target installer secara selektif. Hanya item milik Maxilun yang dihapus: folder skill yang `SKILL.md`-nya bertanda `ecosystem: maxilun`, file agen `maxilun-*.md`, file aturan v1 yang membawa penanda Maxilun, dan folder cadangan `_maxilun_backup_*` yang dibuat installer. Skill dan agen lain milik Anda tidak disentuh.

## macOS / Linux

```bash
bash scripts/uninstall.sh            # global
bash scripts/uninstall.sh --project  # project aktif (alias -p)
```

## Windows PowerShell

```powershell
powershell -ExecutionPolicy Bypass -File scripts\uninstall.ps1            # global
powershell -ExecutionPolicy Bypass -File scripts\uninstall.ps1 -Project   # project aktif
```

## Via npm

```bash
npm run uninstall-skills
```

## Lokasi yang Dibersihkan

Mode global:

| Platform | Skills | Agents | Aturan v1 |
|---|---|---|---|
| Antigravity CLI / IDE & Zed | `~/.agents/skills/` | `~/.agents/agents/` | `~/.agents/rules/` |
| Claude Code & Termul | `~/.claude/skills/` | `~/.claude/agents/` | `~/.claude/rules/` |
| OMP | — | `~/.omp/agent/agents/` | — |
| Codex | `~/.codex/skills/` | `~/.codex/agents/` | `~/.codex/rules/` |
| OpenCode | `~/.config/opencode/skills/` dan `~/.opencode/skills/` | `~/.config/opencode/agents/` dan `~/.opencode/agents/` | `.../rules/` |
| Gemini Config | `~/.gemini/config/skills/` | — | — |
| Gemini CLI | `~/.gemini/skills/` | — | `~/.gemini/rules/` |
| Cursor | `~/.cursor/skills/` | — | — |
| Trae | `~/.trae/skills/` | — | — |
| Windsurf | `~/.windsurf/skills/` | — | — |
| CodeBuddy | `~/.codebuddy/skills/` | — | — |

Mode project (`-Project` / `--project` / `-p`), relatif ke direktori kerja:

| Platform | Skills | Agents | Aturan v1 |
|---|---|---|---|
| Universal / Antigravity / Zed | `.agents/skills/` | `.agents/agents/` | `.agents/rules/` |
| OpenCode | `.opencode/skills/` | `.opencode/agents/` | `.opencode/rules/` |
| Claude Code / Termul | `.claude/skills/` | `.claude/agents/` | `.claude/rules/` |
| Cursor | `.cursor/skills/` | — | — |
| OMP | — | `.omp/agents/` | — |
| Trae | `.trae/skills/` | — | — |
| Windsurf | `.windsurf/skills/` | — | — |
| CodeBuddy | `.codebuddy/skills/` | — | — |

Cadangan `_maxilun_backup_*` dihapus dari direktori induk setiap folder skills (misal `~/.claude/`).

## Manual

Hapus folder `maxilun` dan `maxilun-*` dari direktori skills, serta file `maxilun-*.md` dari direktori agents pada tabel di atas.
