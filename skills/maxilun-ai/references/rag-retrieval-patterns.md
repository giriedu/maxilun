# RAG & Retrieval Architecture Patterns

Arsitektur pengambilan dokumen deterministik untuk mengurangi halusinasi LLM dan memastikan grounding data faktual.

---

## 1. Strategi Chunking Berbasis Struktur Dokumen

Hindari chunking berbasis karakter tetap (e.g. fixed 500 characters) yang memotong kalimat atau tabel di tengah jalan.

| Tipe Dokumen | Pola Chunking yang Benar | Invarian yang Dijaga |
|---|---|---|
| **Markdown / Technical Specs** | Header-based chunking (`#`, `##`, `###`) | Pertahankan heading path sebagai metadata chunk (`section: "API > Auth"`). |
| **Codebase / Source Code** | AST-based chunking (class, function, method scope) | Jangan memotong fungsi di tengah blok; simpan signature fungsi pada setiap chunk. |
| **Tabular Data / CSV** | Row-level JSON serialization | Setiap baris menyertakan header kolom agar konteks makna kolom tidak hilang. |
| **Narrative / Legal / Articles** | Sentence-boundary chunking dengan 15% overlap | Batas paragraf alami; overlap 2-3 kalimat untuk menjaga kontinuitas semantik. |

---

## 2. Hybrid Search: Dense Vector + Sparse BM25

Pencarian vektor murni sering gagal pada nama variabel persis, kode error, UUID, atau istilah teknis spesifik. Gunakan hybrid search:

```text
Query
  ├──> Dense Embeddings (e.g. OpenAI text-embedding-3, bge-large) -> Semantic Recall
  └──> Sparse Lexical (BM25 / Tantivy / PostgreSQL tsvector)     -> Exact Keyword Recall
              │
              ▼
   Reciprocal Rank Fusion (RRF):
   Score(d) = Σ [ 1 / (k + rank_dense(d)) + 1 / (k + rank_sparse(d)) ]  (k = 60)
              │
              ▼
   Cross-Encoder Reranker (e.g. Cohere Rerank / BGE-Reranker-v2) -> Top 5 Chunks
```

---

## 3. Mitigasi "Lost-in-the-Middle" & Konteks Ramping

LLM memiliki atensi tertinggi pada awal dan akhir jendela prompt (U-shaped attention curve):
1. **Posisi Konteks**: Tempatkan chunk dengan relevansi tertinggi di awal atau di paling akhir dekat instruksi user, bukan tertimbun di tengah dokumen panjang.
2. **Context Window Hygiene**: Pangkas token yang tidak informatif (whitespace berlebih, format HTML berulang, metadata internal database).
3. **Prompt Prefix Caching**: Pastikan sistem prompt statis dan dokumen referensi besar berada di urutan awal pesan agar memanfaatkan fitur context caching (Anthropic Prompt Caching / OpenAI prefix caching), memangkas latensi hingga 80% dan biaya token hingga 50%.
