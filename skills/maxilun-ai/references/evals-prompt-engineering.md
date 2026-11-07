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

---

## 4. Siklus Mutu Evaluasi Maxilun (Maxilun Eval Flywheel)

Metodologi iteratif 5-tahap untuk mengukur, mengevaluasi, dan menaikkan mutu model bahasa serta agen otonom:

```
   ┌────────────────────────────────────────────────────────┐
   │  1. Persiapan Data (Dataset & Skenario Sintetis)       │
   └───────────────────────────┬────────────────────────────┘
                               │
                               ▼
   ┌────────────────────────────────────────────────────────┐
   │  2. Eksekusi Inferensi / Simulasi Multi-Turn           │
   └───────────────────────────┬────────────────────────────┘
                               │
                               ▼
   ┌────────────────────────────────────────────────────────┐
   │  3. Penilaian (Rubrik Biner + Grounding Sitasi)        │
   └───────────────────────────┬────────────────────────────┘
                               │
                               ▼
   ┌────────────────────────────────────────────────────────┐
   │  4. Loss Clustering & Pengelompokan Pola Kegagalan     │
   └───────────────────────────┬────────────────────────────┘
                               │
                               ▼
   ┌────────────────────────────────────────────────────────┐
   │  5. Loop Remediasi Iteratif (5–10x tanpa turunkan bar) │
   └───────────────────────────┬────────────────────────────┘
                               ▲                           │
                               └────── Iterasi 2 → 5 ──────┘
```

### 4.1 Tahap 1: Persiapan Dataset & Skenario Percakapan
Sediakan dataset deterministik sebelum menguji:
1. **Kasus Uji Deterministik**: Pasangan `(Prompt, Response, Reference, Invariants)`.
2. **Simulasi Percakapan Multi-Turn**: Untuk agen percakapan atau tool-calling, uji seluruh jejak percakapan (`AgentTrace` $\to$ `ConversationTurn` $\to$ `AgentEvent`), bukan potongan prompt terisolasi.
3. **Skenario Sintetis Persona Pengguna**: Jika data riil belum mencukupi (cold-start), bangkitkan skenario percakapan sintetis dengan batasan instruksi simulasi eksplisit (role, constraints, goals) dan batasi jumlah putaran (`max_turns: 3–10`).

### 4.2 Tahap 2: Eksekusi Inferensi & Simulasi
- **Evaluasi Model**: Uji determinisme output pada `temperature: 0` atau seed tetap.
- **Evaluasi Agen Multi-Turn**: Jalankan callable agen berhadapan dengan simulator pengguna yang memainkan skenario hingga selesai atau mencapai batas `max_turns`.

### 4.3 Tahap 3: Penilaian Ketat (Grading & Grounding)
- **Metrik Lokal Deterministik**: Evaluasi skema JSON, regex pola statis, toleransi latensi token, dan pemeriksaan invarian bisnis secara in-process.
- **LLM-as-a-Judge**: Gunakan model penilai frontier dengan rubrik biner ketat ($0$ atau $1$) dan wajibkan ekstraksi kutipan bukti teks sebelum putusan final dijatuhkan.

### 4.4 Tahap 4: Loss Clustering & Taksonomi Akar Masalah
Jangan memperbaiki kegagalan satu per satu secara acak. Kelompokkan setiap kasus uji yang gagal ke dalam 5 kelas kegagalan utama:

| Kelas Kegagalan | Ciri Teramati | Tindakan Remediasi |
|---|---|---|
| **Instruction Drift** | Model mengabaikan batasan peran atau menghasilkan format di luar kontrak | Pertegas bagian statis system prompt, kunci urutan aturan |
| **Lost-in-the-Middle Context Miss** | Informasi krusial diabaikan karena berada di tengah chunk panjang | Susun ulang konteks: letakkan fakta krusial di awal atau tepat sebelum pertanyaan |
| **Tool / Schema Mismatch** | Parameter function call melanggar tipe data atau enum | Perketat skema JSON (`strict: true`), sertakan contoh minimal di deskripsi tool |
| **Ungrounded Hallucination** | Model mengklaim fakta yang tidak tertulis pada referensi konteks | Tambahkan instruksi penolakan eksplisit: jika bukti absen, nyatakan tidak ditemukan |
| **Boundary / Edge Case Break** | Input kosong, karakter khusus, atau overflow konteks | Tambahkan sanitasi input dan pemotongan terkontrol di layer aplikasi |

### 4.5 Tahap 5: Loop Remediasi Iteratif & Anti-Jalan Pintas

Lakukan 5–10 iterasi perbaikan prompt dan instruksi agen sampai target kualitas tercapai.

**Jalan Pintas yang Merusak Kualitas (Dilarang Keras):**

| Jalan Pintas | Mengapa Ditolak | Tindakan yang Benar |
|---|---|---|
| *"Saya turunkan threshold skor agar lulus."* | Menyembunyikan cacat nyata. | Perbaiki prompt/instruksi agen, bukan menurunkan standar mutu. |
| *"Kasus ini flaky/kadang gagal, di-skip saja."* | Flakiness menandakan non-determinisme. | Gunakan `temperature: 0` atau instruksi yang lebih deterministik. |
| *"Saya sesuaikan expected output dataset agar cocok dengan jawaban agen."* | Dataset uji mencerminkan kebenaran domain. | Perbaiki perilaku agen agar menghasilkan output yang sesuai domain. |
| *"Dari satu sampel trace terlihat sudah bagus, skip pengujian penuh."* | Evaluasi satu sampel tidak menjamin generalisasi. | Jalankan seluruh suite uji regresi (minimal 30 sampel). |
| *"Satu iterasi perbaikan sudah cukup."* | Perubahan satu prompt kerap memicu regresi di metrik lain. | Uji ulang seluruh test suite setiap kali prompt diubah. |
