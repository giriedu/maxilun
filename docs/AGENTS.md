# Maxilun Autonomous Agents Architecture

Maxilun menyediakan **13 Autonomous Agents** yang terdiri dari **6 Macro-Role Agents** (orkestrasi gelombang & tata kelola sistem) serta **7 Specialized Coding & UI/UX Agents** (eksekusi pengkodean dan desain tingkat tinggi tanpa kompromi). Arsitektur agen ini memecah eksekusi tugas ke dalam subagent dengan konteks terisolasi, hak akses tool terikat (*Principle of Least Privilege*), dan gating verifikasi faktual.

---

## 1. Perbandingan: Skill vs Agent di Maxilun

| Dimensi | Maxilun Skill (`skills/maxilun-*`) | Maxilun Agent (`agents/maxilun-*`) |
|---|---|---|
| **Sifat** | Instruksi prosedural & playbook domain (*Passive Guidance*). | Pelaksana tugas otonom dengan lifecycle independen (*Active Worker*). |
| **Context Window** | Dimuat bersamaan ke dalam context window percakapan utama (rentan bloat). | Menjalankan tugas dalam konteks subagent terisolasi; hanya sintesis akhir yang dikembalikan. |
| **Hak Akses Tool** | Semua tool terbuka (read, write, edit, bash) pada satu sesi. | **Tool Whitelist Ketat**: agen read-only (Scout) tidak bisa merusak kode; Verifier tidak bisa mengedit kode produksi. |
| **Tiering Model** | Mengikuti model aktif editor host. | Dapat diarahkan ke model berbeda (Haiku/Flash untuk Scout; Sonnet/Opus untuk Architect & Maker). |

---

## 2. Peta 6 Macro-Role Agents & 21 Spesialis

```mermaid
flowchart TD
    Orch["🎯 maxilun-orchestrator<br/>Reversibility Triage & Wave Sequencing"]

    subgraph Wave1["Wave 1: Discovery & Contracts"]
        Scout["🔍 maxilun-scout<br/>Read-Only Code Intelligence<br/>(knowledge-graph, insight, seo-audit)"]
        Arch["📐 maxilun-architect<br/>System Boundaries & Schemas<br/>(architect, data, sentinel, docsmith)"]
    end

    subgraph Wave2["Wave 2: Implementation & Design"]
        Maker["⚡ maxilun-maker<br/>Surgical Code Writing<br/>(engineer, frontend, desktop, mobile, iot, network)"]
        Studio["🎨 maxilun-studio<br/>Design, Motion & Media<br/>(craft, motion, cinecode, diagrams, content)"]
    end

    subgraph Wave3["Wave 3: Verification & Release"]
        Verif["🛡️ maxilun-verifier<br/>Quality Gatekeeper & CI/CD<br/>(verify, deploy)"]
    end

    Orch -->|Delegasi Wave 1| Scout
    Orch -->|Delegasi Wave 1| Arch
    Scout -.->|Blast Radius & Defs| Arch
    Arch -->|Schema & API Contracts| Maker
    Arch -->|Design Specs| Studio
    Maker -->|Code Diffs| Verif
    Studio -->|UI & Video Assets| Verif
    Verif -->|Test Pass Proof [CONFIRMED]| Orch
```

### Detail Peran, Hak Tool, dan Spesialis Terkait

| Nama Agent | Spesialis yang Dibungkus | Izin Tool (*Whitelist*) | Tanggung Jawab Utama |
|---|---|---|---|
| **`maxilun-orchestrator`** | `maxilun` | `Read`, `Grep`, `Glob`, `Bash` | Triase reversibilitas (Type 1 vs Type 2), penunjukan pemilik utama, orkestrasi Wave 1 $\rightarrow$ Wave 2 $\rightarrow$ Wave 3, dan gate bukti nyata. |
| **`maxilun-scout`** | `maxilun-knowledge-graph`, `maxilun-insight`, `maxilun-seo-audit` | **Strict Read-Only**: `Read`, `Grep`, `Glob` | Pemetaan graf simbol (`defOf:`, `callsIn:`), pencarian akar masalah, audit radius dampak edit, dan crawlability SEO tanpa risiko mengubah file. |
| **`maxilun-architect`** | `maxilun-architect`, `maxilun-data`, `maxilun-sentinel`, `maxilun-docsmith` | `Read`, `Grep`, `Glob`, `Write`, `Edit` (kontrak & docs) | Batas modul dalam (*Deep Modules*), migrasi skema zero-downtime, threat modeling OWASP/STRIDE, kontrak OpenAPI 3.1, dan ADR. |
| **`maxilun-maker`** | `maxilun-engineer`, `maxilun-frontend`, `maxilun-desktop`, `maxilun-mobile`, `maxilun-iot`, `maxilun-network` | `Read`, `Grep`, `Glob`, `Write`, `Edit`, `Bash` | Payung makro eksekusi kode produksi lintas-surface dengan diff minimal. |
| **`maxilun-studio`** | `maxilun-craft`, `maxilun-motion`, `maxilun-cinecode`, `maxilun-diagrams`, `maxilun-content` | `Read`, `Grep`, `Glob`, `Write`, `Edit`, `Bash` | Payung makro desain visual, motion graphics, video programatik Remotion, dan diagram Mermaid. |
| **`maxilun-verifier`** | `maxilun-verify`, `maxilun-deploy` | `Read`, `Grep`, `Glob`, `Bash` (**Tanpa izin edit kode**) | Eksekusi test runner (unit, E2E Playwright), typecheck, audit aksesibilitas WCAG, hardening Docker non-root, dan pipeline CI/CD. |
| **`maxilun-coder-frontend`** | `maxilun-frontend`, `maxilun-engineer` | `Read`, `Grep`, `Glob`, `Write`, `Edit`, `Bash` | Next.js 15 App Router, React 19 RSC vs Client boundaries, Server Actions, serialisasi Flight, client state, dan zero-leak layout. |
| **`maxilun-coder-backend`** | `maxilun-engineer`, `maxilun-data`, `maxilun-sentinel`, `maxilun-docsmith` | `Read`, `Grep`, `Glob`, `Write`, `Edit`, `Bash` | API REST / OpenAPI 3.1, skema 3NF relasional, transaksi ACID, idempotensi webhook, timing-safe crypto, dan RFC 9457 errors. |
| **`maxilun-coder-mobile`** | `maxilun-mobile`, `maxilun-engineer` | `Read`, `Grep`, `Glob`, `Write`, `Edit`, `Bash` | Native Android (Kotlin Compose), iOS (Swift SwiftUI), Flutter, React Native, arsitektur offline-first, dan touch ergonomics $\ge 44\text{pt}$. |
| **`maxilun-coder-systems`** | `maxilun-desktop`, `maxilun-iot`, `maxilun-network` | `Read`, `Grep`, `Glob`, `Write`, `Edit`, `Bash` | Native Desktop Win32/WPF/Qt/PowerBuilder, firmware IoT ESP32 FreeRTOS (zero-heap ISR), dan enterprise MikroTik RouterOS scripts. |
| **`maxilun-ui-designer`** | `maxilun-craft` | `Read`, `Grep`, `Glob`, `Write`, `Edit`, `Bash` | 100 sistem desain brand nyata, protokol buka kunci desain (*Clean Cutover*), tata letak asimetris, tipografi display solid, dan anti-slop. |
| **`maxilun-ui-motion`** | `maxilun-motion` | `Read`, `Grep`, `Glob`, `Write`, `Edit`, `Bash` | Animasi browser 60 FPS, ScrollBlurReveal (hide $\to$ blur $\to$ focus), kurva pegas fisika teredam, dan 3D WebGL autentik domain. |
| **`maxilun-ui-reviewer`** | `maxilun-verify`, `maxilun-craft` | **Strict Read-Only**: `Read`, `Grep`, `Glob`, `Bash` (**Tanpa izin edit kode**) | Quality gatekeeper visual: audit 45 AI design tells (`ui-purity-linter`), radius konsentris eksak, kontras WCAG, dan uji zero canvas leak 375px. |
---

## 3. Cara Menggunakan Agen di Editor AI

### A. Claude Code Subagents
Ketika diinstal ke `.claude/agents/` (atau `~/.claude/agents/`), Claude Code secara otomatis mengenali subagent ini. Anda dapat memanggil agen tertentu secara eksplisit:
```text
@maxilun-scout Siapa saja yang memanggil fungsi calculateTax() di repositori ini?
@maxilun-architect Buatkan skema migrasi expand-contract untuk tabel users
@maxilun-verifier Jalankan seluruh test suite dan typecheck
```
Atau cukup jalankan `@maxilun-orchestrator` untuk mendelegasikan tugas multi-wave secara otomatis.

### B. Antigravity & Universal AI Editors
Agen terpasang di `.agents/agents/` dan dapat dipanggil melalui tool delegasi `task` bawaan editor:
```json
{
  "agent": "maxilun-scout",
  "task": "Petakan seluruh import circular dan fungsi lambat di module order"
}
```

### C. Maxilun Autonomous Python Harness
Jalankan agen langsung dari terminal:
```bash
# Diagnosa kesiapan ekosistem dan agent yang terpasang:
python harness/cli.py doctor

# Jalankan tugas otonom dengan subagent delegator:
python harness/cli.py run "Audit keamanan endpoint login dan buktikan dengan test"
```
