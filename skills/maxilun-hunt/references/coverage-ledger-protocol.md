# Coverage-Led Adversarial Audit & Validation Protocol

Deterministic vulnerability hunting protocol for `maxilun-hunt` and `maxilun-security-auditor`.

## 1. Coverage Ledger (Zero Silent Gaps)
Before hunting, enumerate all in-scope trust boundaries, auth surfaces, routes, and sinks into a coverage ledger (`maxilun-out/coverage-ledger.json`):
- **Units**: route/handler, auth middleware, webhook receiver, SQL/ORM query boundary, LLM tool boundary.
- **Status**: `untested` | `checked_clean` | `candidate` | `confirmed` | `needs_validation` | `rejected`.

## 2. Independent Candidate Validation (Disproval Pass)
Every candidate flaw must be challenged by a fresh validation pass before reporting:
- **`confirmed`**: Complete source-to-sink `file:line` trace AND bounded reproducible PoC (curl/script/test output).
- **`needs_validation`**: Exact unresolved runtime fact stated; assign **no speculative severity**.
- **`rejected`**: Disproved candidate with the exact guard or control (`file:line`) that blocks exploitation.

## 3. High-Value Attack Classes
- **Web & Auth**: IDOR/BOLA on sibling endpoints, JWT/DPoP replay, HMAC timing/raw-body bypass, SSRF, HTTP request smuggling.
- **Client-Side**: DOM XSS sinks, `postMessage` origin trust gaps, prototype pollution, UI redressing.
- **AI / LLM**: Prompt injection across untrusted RAG/tool outputs, unvalidated tool-call arguments, unsafe HTML/SQL execution of model output.

