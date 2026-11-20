# Rust Systems Migration & Behavior-Proving Protocol

A deterministic protocol for migrating performance-critical services, native CLI tools, and legacy codebases to Rust. Grounded in the behavior-recording and differential verification methodology of Erkam Yaman's rust-anything.

---

## 1. The Behavior-Proving Migration Methodology

Rewriting software without verifying behavioral equivalence introduces silent regressions. This protocol guarantees that the Rust rewrite behaves identically to the original before any cutover occurs:

```text
[Legacy App] ──> [1. Record Baseline Traces] ──> golden_traces/ (inputs, outputs, exit codes)
                                                       │
[Rust Binary] ──> [2. Differential Replay Engine] <────┘
                        │
                        ├── All traces match exactly? ──> [3. Zero-Downtime Cutover]
                        └── Mismatch detected? ─────────> [Loopback Fix in Rust code]
```

---

## 2. Four Migration Stages

### Stage 1: Golden Trace Recording
Before writing any Rust code, record the existing system under realistic workloads:
1. **CLI Tools**: Capture command-line arguments, environment variables, stdin payloads, stdout streams, stderr streams, and exact exit status codes.
2. **HTTP/RPC Services**: Record incoming requests (headers, paths, payloads) and matching HTTP responses (status codes, JSON bodies, headers).
3. Store records in a deterministic test suite (`tests/fixtures/golden_*.json`).

### Stage 2: Modular Slice-by-Slice Porting
Never attempt a "big-bang" whole-repo rewrite. Break the work into isolated capability slices:
1. **Core Data Structures & Types**: Port domain entities with `serde::{Serialize, Deserialize}`.
2. **Pure Algorithms & Business Logic**: Port domain functions with $100\%$ unit test coverage matching existing test fixtures.
3. **I/O & Boundary Adapters**: Implement CLI parsing (`clap`), HTTP servers (`axum`), or database clients (`sqlx`).

### Stage 3: Differential Verification Gate
Replay every golden trace against the compiled Rust binary:
- **Command**: Run the differential test runner (`cargo test --test differential`).
- **Assertion**: Output bytes, JSON structures, error codes, and HTTP statuses must match the baseline recordings within defined tolerance (e.g., dynamic timestamps excluded).

### Stage 4: Verified Cutover
Deploy the Rust service or binary only after all golden traces pass with exit code 0.

---

## 3. High-Performance Rust Engineering Invariants

1. **Zero Unsafe Invariant**: Never use `unsafe` blocks unless interfacing with native C ABI / OS handles, and every `unsafe` block MUST carry a `// SAFETY:` invariant comment.
2. **Error Handling Architecture**:
   - Use `thiserror` for domain-specific library errors with explicit enums.
   - Use `anyhow` for top-level application CLI and daemon entrypoints.
   - **Banned in Production**: `.unwrap()` and `.expect()` on fallible I/O or user data; handle errors explicitly with `?` or `match`.
3. **Async Concurrency**:
   - Use `tokio` multi-threaded runtime for I/O-bound services.
   - For CPU-bound tasks, offload to `tokio::task::spawn_blocking` or `rayon` thread pools.
4. **Structured Tracing**:
   - Use `tracing` and `tracing-subscriber` for JSON-formatted structured logging with spans and correlation IDs.
