# Instalasi Maxilun

## Via `npx skills` (Standar Resmi skills.sh)

Mendukung instalasi langsung dari GitHub untuk Claude Code, Antigravity, Cursor, Codex, OpenCode, dll. Setiap instalasi via `npx skills` tercatat secara otomatis pada metrik publik di [skills.sh/giriedu/maxilun](https://skills.sh/giriedu/maxilun).

```bash
# 1. Perintah Standar (Interaktif - pilih skill & agen target):
npx skills add giriedu/maxilun

# 2. Pasang seluruh 18 skill secara global (-g) tanpa prompt (-y):
npx skills add giriedu/maxilun -g -y

# 3. Khusus Claude Code (Level Project Workspace):
npx skills add giriedu/maxilun -a claude-code

# 4. Pasang skill spesifik tertentu:
npx skills add giriedu/maxilun --skill maxilun-engineer
npx skills add giriedu/maxilun --skill maxilun-architect
```

> [!TIP]
> **Catatan Pengguna Windows (Symlink Restriction):**  
> Di Windows, jika akun Anda membatasi pembuatan *Symbolic Link* (tanpa Developer Mode/Admin), tambahkan flag `--copy` (misal: `npx skills add giriedu/maxilun -g -y --copy`) atau pilih opsi **Copy** di menu interaktif CLI.

## Via Script Installer Mandiri

**macOS / Linux:**
```bash
git clone https://github.com/giriedu/maxilun.git
cd maxilun && bash scripts/install.sh
```

**Windows PowerShell:**
```powershell
git clone https://github.com/giriedu/maxilun.git
cd maxilun; .\scripts\install.ps1
```
*(Tambahkan parameter `-Project` jika ingin memasang ke project aktif saat ini: `.\scripts\install.ps1 -Project`)*

## Cara Update Skill ke Versi Terbaru

### 1. Update Otomatis via `npx skills`
Jika sebelumnya memasang lewat CLI `skills`:
```bash
# Update seluruh skill yang terpasang ke versi terbaru:
npx skills update

# Update skill global (-g) tanpa konfirmasi prompt:
npx skills update -g -y

# Atau install ulang langsung dari repo (otomatis memperbarui):
npx skills add giriedu/maxilun -g -y
```

### 2. Update via Repositori Lokal (Git)
Jika memakai clone repositori Maxilun:
```bash
# 1. Tarik pembaruan terbaru dari GitHub:
git pull origin main

# 2. Jalankan installer update (otomatis mencadangkan versi lama):
npm run update-skills
# atau jalankan langsung scripts/install.ps1 (Windows) / bash scripts/install.sh (macOS/Linux)
```
*(Script installer Maxilun otomatis mencadangkan file lama ke folder `_maxilun_backup_<timestamp>` sebelum menimpa dengan versi terbaru, sehingga aman dari risiko kehilangan custom rule)*

## Manual Copy

Salin folder `skills/*` ke direktori skill platform Anda (misal: `~/.claude/skills/` atau `~/.agents/skills/`).

Tidak ada folder `rules/` yang perlu disalin. Aturan inti tertanam di setiap `SKILL.md` sebagai blok `CORE-RULES`, dan materi lengkap ada di `skills/maxilun/references/`. Jika Anda menyalin satu skill saja, skill itu tetap membawa aturannya sendiri.

## Upgrade dari v1 ke v2

v1 menaruh aturan di `rules/` pada root repo. `npx skills add` hanya menyalin folder skill, sehingga aturan itu tidak pernah ikut terpasang. v2 memindahkannya ke dalam skill.

1. Jalankan ulang instalasi: `npx skills add giriedu/maxilun -g -y` (atau `npm run update-skills`).
2. Installer v2 menghapus sisa file aturan v1 di luar folder skill secara otomatis, hanya jika file tersebut membawa penanda Maxilun.
3. Verifikasi: setiap `SKILL.md` harus memuat blok `<!-- CORE-RULES:START -->`, dan `skills/maxilun/references/engines.md` harus ada.

Jika Anda memakai skill di luar ekosistem ini, hapus rujukan ke paket eksternal di luar 18 skill Maxilun: v2 berdiri mandiri sepenuhnya tanpa dependensi skill pihak ketiga.


## Kompatibilitas Multi-Platform

| Platform AI | Workspace Project | Lokasi Global | Cara Auto-Install |
|---|---|---|---|
| **Claude Code** | `.claude/skills/` | `~/.claude/skills/` | Otomatis via `npx skills add` atau `install.sh` / `install.ps1` |
| **OpenCode** | `.opencode/skills/` | `~/.config/opencode/skills/` | Otomatis via `npx skills add` atau `install.sh` / `install.ps1` |
| **Codex** | `.codex/skills/` | `~/.codex/skills/` | Otomatis via `npx skills add` atau `install.sh` / `install.ps1` |
| **Antigravity CLI / IDE** | `.agents/skills/` | `~/.agents/skills/` | Otomatis via `npx skills add` atau `install.sh` / `install.ps1` |
| **Zed Editor** | `.agents/skills/` | `~/.agents/skills/` | Otomatis via `npx skills add -a zed` atau Universal Agent Standard |
| **Termul (`termul.dev`)** | `.claude/skills/` & `.agents/skills/` | `~/.claude/skills/` & `~/.agents/skills/` | Otomatis via Claude Code / Antigravity CLI / OpenCode harness di Termul workspace |
| **Cursor / Windsurf** | `.cursor/skills/` | `~/.cursor/skills/` | Otomatis via `npx skills add` atau `install.sh` / `install.ps1` |
| **Universal Git Standard** | `skills/` | — | Standar terbuka vendor-neutral bawaan repositori ini |

*Catatan: Saat menggunakan `npx skills add giriedu/maxilun`, CLI akan secara interaktif menampilkan menu pemilihan skill dan agen target Anda (termasuk Zed via flag `-a zed`).*
