# RAG & Retrieval Architecture Patterns

Deterministic document retrieval architecture that reduces LLM hallucination and keeps answers grounded in factual data.

---

## 1. Chunking by Document Structure

Avoid fixed-size character chunking (e.g. fixed 500 characters). It cuts sentences and tables in the middle.

| Document Type | Correct Chunking Pattern | Invariant to Keep |
|---|---|---|
| **Markdown / Technical Specs** | Header-based chunking (`#`, `##`, `###`) | Keep the heading path as chunk metadata (`section: "API > Auth"`). |
| **Codebase / Source Code** | AST-based chunking (class, function, method scope) | Never split a function mid-block; store the function signature on every chunk. |
| **Tabular Data / CSV** | Row-level JSON serialization | Every row carries the column headers so the meaning of each column is not lost. |
| **Narrative / Legal / Articles** | Sentence-boundary chunking with 15% overlap | Split at natural paragraph boundaries; overlap 2-3 sentences to keep semantic continuity. |

---

## 2. Hybrid Search: Dense Vector + Sparse BM25

Pure vector search often fails on exact variable names, error codes, UUIDs, and specific technical terms. Use hybrid search:

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

## 3. "Lost-in-the-Middle" Mitigation & Lean Context

An LLM attends most strongly to the start and end of the prompt window (U-shaped attention curve):
1. **Context Position**: Place the most relevant chunks at the start, or at the very end next to the user instruction. Do not bury them in the middle of a long document.
2. **Context Window Hygiene**: Strip uninformative tokens (excess whitespace, repeated HTML formatting, internal database metadata).
3. **Prompt Prefix Caching**: Put the static system prompt and large reference documents first in the message order so context caching applies (Anthropic Prompt Caching / OpenAI prefix caching). This cuts latency by up to 80% and token cost by up to 50%.
