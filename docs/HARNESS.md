# Maxilun Engineering Harness

Harness evaluasi otomatis, pengujian deterministik, dan gerbang kemurnian (*Purity Gate*) untuk ekosistem Maxilun.

---

## 1. Tujuan & Arsitektur

Jika skill Maxilun bertindak sebagai **governance & instruction layer** bagi model AI, maka **Maxilun Harness** bertindak sebagai **ground-truth validation & benchmark runner**:

```
┌────────────────────────────────────────────────────────┐
│  User Prompt / CLI Terminal / Interactive Session      │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│  Maxilun Autonomous Agent Engine (harness/engine/)     │
│  - Skills Loader: parses 18 specialists on disk        │
│  - Reversibility Gate: Type 1 vs Type 2 triage         │
│  - ReAct Execution Loop: tool calls & state tracking   │
└───────────┬────────────────────────────────┬───────────┘
            │                                │
┌───────────▼───────────┐        ┌───────────▼───────────┐
│ Native Tool Registry  │        │ Runtime Middleware    │
│ - read, write, edit   │        │ - PreFlightGraphHook  │
│ - glob, grep, bash    │        │ - PurityInterceptor   │
│ - in-process kg_query │        │ - ReversibilityGuard  │
└───────────┬───────────┘        └───────────┬───────────┘
            │                                │
┌───────────▼────────────────────────────────▼───────────┐
│  Universal LLM Provider (DeepSeek / Ollama / OpenAI)   │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│  Verified Delivery / Interactive Visual Dashboard      │
└────────────────────────────────────────────────────────┘

---

## 2. Perintah CLI

Harness dapat dijalankan tanpa dependensi eksternal (stdlib Python 3.8+):

### A. Sesi Interaktif & Eksekusi Tugas Otonom
Menjalankan sesi agen terminal lengkap dengan 18 spesialis dan pemanggilan tool bawaan:
```bash
# Sesi chat interaktif mandiri:
python harness/cli.py chat

# Menjalankan satu tugas otonom:
python harness/cli.py run "Baca package.json dan verifikasi skrip build"
```

### B. Inspeksi 18 Spesialis Ekosistem
Memeriksa status, kepatuhan batas baris (`≤ 300`), dan pemicu seluruh spesialis:
```bash
python harness/cli.py skills
```

### C. Dashboard Visual Interaktif
Membuka dashboard HTML visual mandiri di peramban:
```bash
python harness/cli.py dashboard --open
```

### D. Menjalankan Benchmark Suite Komparatif
Membandingkan kualitas generasi Raw AI tanpa batas vs output yang diatur oleh Maxilun:
```bash
python harness/cli.py bench --view
```
Artefak otomatis disimpan ke:
- `maxilun-out/benchmark_report.json`
- `maxilun-out/BENCHMARK_REPORT.md`
- `maxilun-out/dashboard.html`

### E. Memvalidasi Berkas / Output terhadap Purity Gate
Memeriksa file kode, diff, atau dokumen markdown:
```bash
python harness/cli.py check src/components/Dashboard.tsx
```
Atau melalui *pipe standard input* (misal: output model atau git diff):
```bash
git diff | python harness/cli.py check -
```

### C. Simulasi Triase Master Orchestrator
Menguji klasifikasi reversibilitas dan penugasan spesialis:
```bash
python harness/cli.py route "Buat endpoint webhook pembayaran dan update saldo invoice"
```
Output:
```text
Primary Owner: maxilun-sentinel
Reversibility: Type 2 (Reversible / Low-Cost)
Companions: maxilun-data
Pre-flight: Check webhook replay window, raw body HMAC, and database idempotency table.
```

### D. Evaluasi Live Model (OpenAI / DeepSeek / Ollama)
Mengirim prompt secara live ke endpoint model dan membandingkan Raw vs Maxilun-governed output:
```bash
# Default menggunakan deepseek-chat (atau mock fallback saat offline):
python harness/cli.py eval

# Menggunakan API key & endpoint kustom:
python harness/cli.py eval --model deepseek-chat --endpoint https://api.deepseek.com/v1 --api-key $DEEPSEEK_API_KEY

# Menggunakan Ollama lokal:
python harness/cli.py eval --model llama3 --endpoint http://localhost:11434/v1
```

### E. Verifikasi AST Struktural & Eksekusi Sandbox
Memeriksa kode dengan AST parser dan menjalankan kompilasi/DDL di sandbox terisolasi:
```bash
python harness/cli.py verify-code src/db/migration.sql
python harness/cli.py verify-code src/auth/session.py
```

### F. Pemasangan Git Pre-Commit Hook Otomatis
Mencegah AI slop dan kode rentan masuk ke riwayat git:
```bash
# Pasang hook ke .git/hooks/pre-commit
python harness/cli.py install-hook

# Copot hook jika tidak diperlukan lagi
python harness/cli.py uninstall-hook

# Hasilkan workflow CI GitHub Actions (.github/workflows/maxilun-harness.yml)
python harness/cli.py generate-ci

---

## 3. Skenario Benchmark Bawaan

| Skenario | Domain | Aturan yang Diuji |
|---|---|---|
| `fintech_ui` | Frontend / UI | 4 UI States, tabular numbers pada kolom moneter, anti gradien ungu klise |
| `payment_webhook` | Security & Data | `timingSafeEqual` HMAC, toleransi replay 300s, kueri berparameter, idempotency |
| `schema_migration` | Database | Pola Expand-Contract zero-downtime, larangan table lock `NOT NULL DEFAULT` |
| `surgical_refactor` | Clean Code | Eliminasi banner emoji HUD, checklist palsu `- [ ]`, presisi perubahan minimal |
| `purity_prose` | Komunikasi | Pembersihan 12 buzzword AI klise (`delve`, `tapestry`, `game-changer`, dll.) |

---

## 4. Integrasi CI/CD & Agent Hook

### Integrasi GitHub Actions
```yaml
- name: Run Maxilun Purity & Benchmark Harness
  run: |
    python harness/cli.py bench
    python harness/cli.py check src/
```

### Integrasi dengan DeepSeek Harness (`dsh`) / OpenCode
Harness ini dapat dipanggil sebagai *pre-tool execution hook* atau *output verification filter* untuk memastikan tidak ada kode rentan atau teks klise yang keluar dari siklus agent.
