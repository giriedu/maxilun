# Uninstall Maxilun

Installer akan menghapus semua skill dan rules Maxilun dari seluruh platform AI yang terdeteksi secara selektif (tidak menghapus skill lain milik Anda).

## macOS / Linux

```bash
bash scripts/uninstall.sh
```

## Windows PowerShell

```powershell
powershell -ExecutionPolicy Bypass -File scripts\uninstall.ps1
```

## Via npm

```bash
npm run uninstall-skills
```

## Manual

Hapus folder `maxilun-*` dari direktori skill platform Anda:

| Platform | Lokasi |
|---|---|
| Claude Code | `~/.claude/skills/maxilun-*` |
| OpenCode | `~/.config/opencode/skills/maxilun-*` |
| Codex | `~/.codex/skills/maxilun-*` |
| Antigravity | `~/.agents/skills/maxilun-*` |
| Cursor / Windsurf | `~/.cursor/skills/maxilun-*` |
