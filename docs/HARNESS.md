# Maxilun Engineering Harness

Harness evaluasi otomatis, pengujian deterministik, dan gerbang kemurnian (*Purity Gate*) untuk ekosistem Maxilun.

---

## 1. Tujuan & Arsitektur

Jika skill Maxilun bertindak sebagai **governance & instruction layer** bagi model AI, maka **Maxilun Harness** bertindak sebagai **ground-truth validation & benchmark runner**:

```
┌────────────────────────────────────────────────────────┐
│  Agent Runtime / User Prompt                           │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│  Maxilun Router (harness/router.py)                    │
│  - Reversibility Triage (Type 1 vs Type 2)             │
│  - Single Cohesive Owner Assignment                    │
│  - Pre-flight Knowledge Graph Recommendation           │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│  Candidate Generation (Model / Codebase)               │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│  Purity Validator (harness/purity_validator.py)        │
│  - Banned Buzzwords (VOC-001..VOC-012)                 │
│  - Ceremonial HUD Theater (HUD-001..HUD-006)           │
│  - 4 UI States & Tabular Numbers (UI-004, TYPO-002)    │
│  - Security Invariants (SEC-001, SEC-002, SEC-003)     │
└──────────────────────────┬─────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────┐
│  Verdict: PASS / FAIL + Scorecard (harness/cli.py)     │
└────────────────────────────────────────────────────────┘
```

---

## 2. Perintah CLI

Harness dapat dijalankan tanpa dependensi eksternal (stdlib Python 3.8+):

### A. Menjalankan Benchmark Suite Komparatif
Membandingkan kualitas generasi Raw AI tanpa batas vs output yang diatur oleh Maxilun:
```bash
python harness/cli.py bench
```
Untuk format JSON terstruktur:
```bash
python harness/cli.py bench --json -o benchmark_report.json
```
Artefak otomatis disimpan ke:
- `maxilun-out/benchmark_report.json`
- `maxilun-out/BENCHMARK_REPORT.md`

### B. Memvalidasi Berkas / Output terhadap Purity Gate
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
