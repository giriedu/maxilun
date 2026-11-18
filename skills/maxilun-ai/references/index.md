# Maxilun AI & LLM Engineering Playbook

Technical guide for engineering systems built on Large Language Models (LLM): Retrieval-Augmented Generation (RAG), context window hygiene, prompt regression evaluation, and function calling with structured outputs.

## Main Topics

1. [RAG & Retrieval Architecture](rag-retrieval-patterns.md) — Hybrid search (dense + BM25), semantic chunking, reciprocal rank fusion (RRF), re-ranking, and vector indexing.
2. [Evals & Prompt Engineering](evals-prompt-engineering.md) — Prompt regression suites, synthetic test dataset generation, LLM-as-a-judge rubrics, context caching, structured JSON schemas, the 5-stage Maxilun Eval Flywheel, and the loss clustering taxonomy.
3. [Structured Tools & Guardrails](structured-tool-guardrails.md) — Strict JSON schemas (`strict: true`), function calling invariants, prompt injection defense at trust boundaries, and single-turn error correction loops.
