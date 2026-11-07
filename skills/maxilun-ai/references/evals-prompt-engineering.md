# Evals & Production Prompt Engineering

Protokol pengujian sistem LLM deterministik dan arsitektur evaluasi berbasis bukti.

---

## 1. Structured Output & JSON Schema Invariants

Jangan meminta model menghasilkan format JSON bebas tanpa validasi skema:
1. **Schema Enforcement**: Gunakan `response_format: { type: "json_schema", json_schema: { strict: true, ... } }` pada provider OpenAI atau tool call payload validation.
2. **Deterministic Fallbacks**: Jika parsing JSON gagal, jalankan loop perbaikan tunggal dengan menyertakan pesan syntax error verbatim dari parser (e.g. `json.decoder.JSONDecodeError`).

---

## 2. Framework Evaluasi Regresi Prompt (Prompt Evals)

Setiap perubahan prompt sistem wajib diuji terhadap test suite regresi berukuran minimal 30–50 sampel uji terfokus:

| Kriteria Evaluasi | Metode Pengukuran | Standar Kelulusan |
|---|---|---|
| **Exact Match / Regex** | Ekstraksi pola statis (kode error, status enum, path file) | 100% lulus deterministik |
| **Purity & Grounding** | Purity linter (menolak buzzwords AI klise, gradien palsu) | Skor kemurnian $\ge 95/100$ |
| **Faithfulness / Halusinasi** | LLM-as-a-judge: memverifikasi setiap klaim terhadap dokumen konteks | Zero hallucinated assertions |
| **Latency & Token Budget** | Pengukuran p95 latency dan token completion count | Di bawah target SLA aplikasi |

---

## 3. Rubrik Evaluasi LLM-as-a-Judge

Saat menggunakan model frontier (e.g. Claude 3.7 Sonnet / GPT-4o) untuk menilai output model yang lebih kecil:
1. **Berikan Rubrik Biner Jelas**: Nilai berdasarkan kepatuhan kriteria konkret (1 = memenuhi, 0 = melanggar), bukan skala 1–10 yang subjektif.
2. **Kutipan Bukti Wajib**: Model penilai wajib menyertakan kutipan kalimat verbatim yang mendukung keputusannya sebelum memberikan kesimpulan.
