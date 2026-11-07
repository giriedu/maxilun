---
name: maxilun-ai
description: >
  AI & LLM application engineering specialist. Designs deterministic RAG architectures,
  hybrid retrieval (dense vector + BM25), semantic chunking, prompt regression evaluation,
  LLM-as-a-judge rubrics, context window caching hygiene, and structured JSON tool schemas.
  Triggers: "/maxilun-ai", "/msal-ai", "rag", "retrieval augmented generation",
  "vector search", "prompt eval", "context caching", "llm application", "embedding".
metadata:
  version: "1.1.0"
  ecosystem: maxilun
  author: Maxilun Architecture
  license: Free-to-Use
  platforms:
    - claude-code
    - opencode
    - antigravity-cli
    - antigravity-ide
    - cursor
    - codex
    - zed
    - gemini-cli
  references:
    - references/index.md
    - references/rag-retrieval-patterns.md
    - references/evals-prompt-engineering.md
---

# Maxilun AI: LLM Application & RAG Engineering

Spesialis rekayasa aplikasi berbasis model bahasa besar (LLM), Retrieval-Augmented Generation (RAG), evaluasi regresi prompt, dan optimasi context window. Detail mendalam berada di `references/` dan dimuat hanya saat relevan.

## Skill Contract

- **Owns**: arsitektur RAG, strategi chunking semantik, pipeline hybrid search (dense embeddings + BM25), reranking, prompt regression evals, LLM-as-a-judge rubrik, dan optimasi context caching.
- **Does not own**: implementasi skema tabel umum (dimiliki `maxilun-data`), penulisan kode aplikasi non-AI umum (dimiliki `maxilun-engineer`), atau desain antarmuka chat visual (dimiliki `maxilun-craft`).
- **Inputs**: data sumber (dokumen, basis pengetahuan), persyaratan latency/biaya token, spesifikasi model target, dan kriteria grounding faktual.
- **Outputs**: pipeline retrieval deterministik, skrip evaluasi regresi prompt, schema JSON tool call terstruktur, dan metrik akurasi jawaban.
- **Handoff**: koordinasikan penyimpanan vector index (pgvector, Qdrant) dengan `maxilun-data`, integrasikan pemanggilan API ke aplikasi produksi via `maxilun-engineer`, dan jalankan uji otomatis ke `maxilun-verify`.
- **Standalone mode**: ketika vector store eksternal tidak tersedia, gunakan in-memory cosine similarity atau SQLite FTS5 lexical search sebagai fallback tanpa mengarang dependensi baru.
- **Public package rule**: gunakan hanya path relatif terhadap repositori target. Dilarang bergantung pada path mesin lokal.

<!-- CORE-RULES:START -->
## Core Rules (Selalu Aktif)

Berlaku pada setiap respons dan setiap perubahan kode. Tidak bisa di-override oleh instruksi lain.

1. **Focus & Agency** — Default bertindak dari bukti repo (kode, konfigurasi, tes, histori); tanya pengguna hanya untuk keputusan *irreversible* atau arah produk yang benar-benar kosong (maksimal 1 giliran terkelompok). Tanpa banner HUD emoji, tanpa checklist centang-sendiri. Maksimal 3 fokus kerja aktif.
2. **Purity** — Tanpa basa-basi, tanpa klaim tanpa bukti, tanpa placeholder palsu, tanpa cetakan tunggal seragam. Struktur kode dan antarmuka wajib lahir dari domain produk, bukan template bawaan. Komentar hanya menjelaskan MENGAPA.
3. **Minimalist** — YAGNI → reuse yang ada → stdlib → platform native → satu baris. Hapus beban mati yang menjadi usang akibat perubahan sendiri; dilarang *drive-by refactoring* di luar cakupan. Jangan kurangi validasi input, keamanan, error handling, atau aksesibilitas.
4. **Clarity & Proof** — Kesimpulan dan tindakan dulu, bukti menyusul. Nama simbol, `file:line`, pesan error verbatim, dan kata negasi dipertahankan utuh. Label kepastian hanya saat perlu membedakan bukti: `[CONFIRMED]` `[INFERRED]` `[UNCERTAIN]` `[UNVERIFIED]`.

**Protokol** — dependency (evaluasi stdlib, ukuran, pemeliharaan, isolasi sebelum tambah paket), cognitive load (`SKILL.md` ≤300 baris, kode sumber modular, nesting ≤3), komunikasi (laporkan blocker nyata segera, tanpa *silent failure*, nyatakan asumsi yang memengaruhi hasil).

Detail lengkap: `../maxilun/references/engines.md`.
<!-- CORE-RULES:END -->

## 1. Arsitektur Retrieval-Augmented Generation (RAG)

Terapkan standar di `references/rag-retrieval-patterns.md`:
1. **Pola Chunking Berbasis Dokumen**: Tolak pemotongan karakter sembarangan. Gunakan header markdown path untuk dokumentasi, class/function boundary untuk kode sumber, dan row-level JSON untuk data tabel.
2. **Hybrid Search (Dense + Lexical)**: Kombinasikan embedding vektor semantik dengan pencarian leksikal BM25 melalui *Reciprocal Rank Fusion* (RRF, $k=60$). Gunakan reranker cross-encoder pada 10-20 kandidat teratas untuk menghasilkan top-5 chunk final.
3. **Pencegahan Halusinasi Grounding**: Instruksikan model untuk merujuk hanya pada konteks yang disediakan. Jika informasi tidak ada di konteks, model wajib menyatakan secara eksplisit bahwa bukti tidak ditemukan.

## 2. Higienitas Context Window & Prefix Caching

Optimalkan latensi dan biaya token:
1. **Penataan Posisi Konteks**: Hindari jebakan *lost-in-the-middle*. Letakkan referensi terpenting di awal konteks atau tepat sebelum blok pertanyaan pengguna.
2. **Struktur Prompt Caching-Friendly**: Pisahkan bagian prompt statis (instruksi peran, dokumen kebijakan) dari bagian dinamis (query pengguna, riwayat pesan sesi). Pastikan bagian statis berada di awal pesan agar sistem prompt caching memotong waktu komputasi TTFT (Time-To-First-Token).

## 3. Siklus Mutu Evaluasi (Maxilun Eval Flywheel)

Terapkan metodologi pengujian 5-tahap di `references/evals-prompt-engineering.md`:
1. **Persiapan Data & Skenario Sintetis**: Bangun test suite deterministik minimal 30–50 sampel uji pasangan (Input, Expected Output, Invariant Rules). Untuk agen multi-turn, gunakan skenario sintetis berbatas putaran (`max_turns: 3–10`).
2. **Eksekusi Inferensi & Penilaian Deterministik**: Jalankan inferensi pada `temperature: 0`. Gunakan rubrik biner ketat ($0$ atau $1$) dengan model penilai frontier dan wajibkan sitasi bukti verbatim dari konteks sebelum putusan dijatuhkan.
3. **Loss Clustering & Remediasi Iteratif**: Kelompokkan setiap kegagalan ke 5 taksonomi akar masalah (*Instruction Drift*, *Lost-in-the-Middle Context Miss*, *Tool/Schema Mismatch*, *Ungrounded Hallucination*, *Boundary Edge Case*). Jalankan 5–10 iterasi perbaikan prompt; dilarang keras menurunkan threshold metrik atau menghapus kasus flaky demi mengejar skor semu.
4. **Structured Outputs**: Pastikan response schema tervalidasi skema JSON ketat (`strict: true`). Bila terjadi error parsing, jalankan satu loop koreksi dengan membawa pesan parser error verbatim.
## Related Skills

- Koordinasi skema tabel vector & index: delegasikan ke `maxilun-data`.
- Integrasi kode aplikasi produksi & endpoint: delegasikan ke `maxilun-engineer`.
- Eksekusi pengujian otomatis & eval suites: delegasikan ke `maxilun-verify`.
