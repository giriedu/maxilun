# Locate: Question-to-Coordinates Retrieval

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-knowledge-graph/SKILL.md"
  origin: "Maxilun Knowledge Graph Engine"
-->

Reference for `cli.py locate`: what it indexes, how it ranks, what the output means, and where it stops being reliable.

---

## 1. Why It Exists

A graph answers "who calls `validateToken`" only after someone knows the name `validateToken`. Most tasks start one step earlier: "where is the session checked", "why does export fail", a stack trace from a user. Without a retrieval step the agent bridges that gap by opening files one after another, which costs more context than the change itself. `locate` closes the gap in one call and returns coordinates that are small enough to read in full.

## 2. Command

```text
python <skill-dir>/cli.py locate "<question | stack trace | symbol>" [options]
```

| Flag | Default | Effect |
|---|---|---|
| `--path <repo>` | `.` | Repository root to search |
| `--also a,b,c` | none | Extra identifiers or synonyms, weighted like the question's own words |
| `--top N` | 5 | Maximum files returned (up to two ranges per file) |
| `--lines N` | 14 | Maximum excerpt lines per range |
| `--budget N` | 6000 | Total excerpt characters; later ranges keep coordinates but drop the excerpt |
| `--tests` | off | Rank test files equally with production code |
| `--refresh` | off | Run an incremental graph scan first |
| `--json` | off | Machine-readable result for a harness or script |
| `--graph <file>` | auto | Use a specific `graph.json` |

## 3. What Is Indexed

- Source, markup, style, schema, config, and documentation files by extension, up to 400 KB each.
- Skipped: dependency and build folders, dot-folders, gitignored files, lockfiles, minified bundles, and anything whose name looks like a secret (`.env*`, key and certificate files, names containing `secret` or `credential`). Skipped files never appear in an excerpt.
- Each file is cut into chunks at the symbol boundaries the graph already knows (function, method, class, heading). Spans longer than 60 lines and files without symbols are cut into 40-line windows.
- The chunk index lives in `.maxilun/cache/locate-index.json`. A file is re-read only when its size, modification time, or symbol boundaries change.

## 4. Ranking

1. **Terms.** The question is split into identifier-aware tokens (`processPayment` also yields `process` and `payment`), stop words are dropped, and a small Indonesian-to-English map adds likely code-side words at reduced weight.
2. **Lexical score.** BM25 over chunk bodies, with extra weight when a term appears in the symbol name or the file path.
3. **Exact symbol.** A question word that equals a symbol name lifts that declaration to the top.
4. **Coverage.** Chunks that match more of the distinct question terms outrank chunks that repeat one term.
5. **Graph expansion.** Callers and callees of the strongest symbols inherit a fraction of their score, so the handler next to the matched helper still surfaces.
6. **Demotions.** Test files and documentation rank lower unless the question asks for them (`--tests`, or words such as "test", "docs", "readme").
7. **Trace pinning.** `path:line` frames found in the question are placed first, in the order they appear.

## 5. Reading the Output

```text
locate [strong] 3 range(s) in 2 file(s) (index: 412 files, 5310 chunks)

Read plan (read these ranges only):
  1. src/billing/invoice.ts:88-131  calculateTotal [function]  score 31.4
  2. src/billing/tax.ts:12-40  applyTax [function]  score 18.9

--- 1. src/billing/invoice.ts:88-131  matched: =calculateTotal, invoice, total
   88| export function calculateTotal(invoice: Invoice): Money {
   ...
      callers: src/api/checkout.ts:54, src/jobs/renew.ts:21
      calls: applyTax, roundHalfEven
```

- **Confidence.** `strong`: a trace frame, an exact symbol, or most question terms matched in one chunk. `partial`: confirm the top range before editing. `weak`: leads only. `none`: nothing matched.
- **`matched`.** The terms that produced the hit; `=name` marks an exact symbol match, `trace:N` a stack frame.
- **`(inside name)`.** A later window of a long function; the declaration is in an earlier range of the same file.
- **`No hit for: ...`.** Question terms that appeared nowhere in the returned ranges. Retry once with the vocabulary the output actually uses.

## 6. Limits

- Ranking is lexical. A question whose words share nothing with the code ("make it faster") returns weak leads; add identifiers through `--also` or start from a measurement in `maxilun-insight`.
- Dynamic dispatch (event names, DI tokens, reflection, string-built routes) is found only when the string itself appears in the question or in `--also`.
- Symbol boundaries come from the graph. In languages scanned at the generic tier, chunks follow declarations but call edges are name-based, so `callers:` lines carry the same `[name-only]` caution as §5 of the skill.
- Excerpts are read from disk at call time and are exact; coordinates of a file edited since the last scan can be off by the size of the edit until `--refresh` runs.
