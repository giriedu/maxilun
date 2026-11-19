# Multimodal RAG Pipeline (Text, Tables, Equations, Images, Audio & Video)

Architecture standards for `maxilun-ai` when building retrieval systems over mixed-modality documents (PDFs, Office files, technical diagrams, spreadsheets, audio, and video).

## 1. Adaptive Content Decomposition & Modality Routing
Never flatten rich documents into raw text alone. Decompose documents into typed content blocks and route each modality to a dedicated processor:
- **Text**: Chunk by document heading/section hierarchy while preserving parent section path.
- **Tables**: Preserve exact row/column structure (Markdown/JSON) and generate a natural-language summary of schema, units, trends, and edge values for retrieval.
- **Equations (LaTeX / OMML)**: Preserve raw mathematical notation alongside plain-language variable definitions and domain meaning.
- **Images & Diagrams**: Generate context-aware captions describing visual entities, spatial relationships, and labels; retain file/page coordinates for VLM-enhanced query synthesis.
- **Audio & Video**: Extract time-stamped transcripts, keyframe captions, and speaker/scene metadata aligned to timecodes.

## 2. Context-Aware Surrounding Window & Token Budgeting
Non-text blocks (a chart, table, or equation) lose meaning in isolation:
- **Surrounding Context Injection**: Pass a bounded context window (e.g. `1–2` blocks or pages before and after the target asset) to the modality processor so captions and table interpretations resolve acronyms and units from surrounding prose.
- **Deterministic Token Budget**: Enforce explicit per-modality token caps (`max_context_tokens`, `max_caption_tokens`) and truncate gracefully before assembling the final prompt so multimodal payloads never overflow the model context window.

## 3. Dual-Graph Retrieval & VLM-Enhanced Query Mode
- **Entity + Chunk Indexing**: Store both semantic chunk embeddings and cross-modal entity/relationship links (`document -> section -> table/figure -> entity`) so queries can traverse related diagrams and tables across pages.
- **VLM-Enhanced Synthesis**: When retrieved chunks reference visual diagrams or charts and a vision-capable model is available, attach the referenced image(s) alongside the `<retrieved_context>` text block during answer synthesis.
- **Resilience & Graceful Degradation**: Isolate per-item parser/VLM failures with bounded retries and fallback to extracted text/metadata so one corrupt image or equation never aborts a batch ingestion pipeline.

