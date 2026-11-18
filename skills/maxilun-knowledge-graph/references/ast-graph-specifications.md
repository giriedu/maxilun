# Knowledge Graph AST Schema & Blast-Radius Specifications

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-knowledge-graph/SKILL.md"
  origin: "Maxilun Knowledge Graph Engine"
-->

Reference for the knowledge graph data structure, the node-edge schema, and the AST-based symbolic query protocol.

---

## 1. Graph Node & Edge Schema

The graph is exported to `maxilun-out/graph.json` in a standardized JSON format:

```json
{
  "version": "1.0.0",
  "nodes": [
    {
      "id": "file:src/auth/session.ts",
      "type": "FILE",
      "path": "src/auth/session.ts",
      "language": "typescript"
    },
    {
      "id": "func:src/auth/session.ts:verifySession",
      "type": "FUNCTION",
      "name": "verifySession",
      "line": 42,
      "exported": true
    }
  ],
  "edges": [
    {
      "source": "func:src/routes/api.ts:handleLogin",
      "target": "func:src/auth/session.ts:verifySession",
      "type": "CALLS"
    },
    {
      "source": "file:src/routes/api.ts",
      "target": "file:src/auth/session.ts",
      "type": "IMPORTS"
    }
  ]
}
```

---

## 2. Symbol Query Grammar

Use the CLI command `python cli.py query "<grammar>"` to trace the graph without reading full text files:

1. **`defOf:<symbol>`**:
   - Finds the definition point of a function, class, or type (returns `file:line`).
2. **`callsIn:<function>`**:
   - Finds all downstream callers, or which functions the target calls.
3. **`importersOf:<file>`**:
   - Returns the list of all files that import the target module, used to compute the blast radius.

---

## 3. Blast Radius Calculation

Before a public function is changed:
1. **Direct Dependency Degree (Degree 1)**: Modules that directly import the symbol to be edited.
2. **Transitive Dependency Degree (Degree 2+)**: Downstream modules that consume the output of Degree 1 modules.
3. If Degree 1 $> 10$ files, escalate as a *Type 1 (Irreversible / High-Blast)* decision before changing the function signature.

---

## 4. Incremental AST Cache Architecture & Fingerprinting

Maxilun Knowledge Graph uses a layered cache so that scanning an unchanged file costs $O(1)$:

1. **`stat-index.json`**: Stores `st_size` and `st_mtime_ns` for every indexed file. If the filesystem stat is the same, the file is not re-read from disk.
2. **Content Fingerprint (SHA-256)**: If the timestamp changed but the content is identical, the hash prevents AST re-parsing.
3. **Per-file Granular AST Cache**: Extraction results are stored in `.maxilun/cache/ast/<version>/<sha256>.json`.
4. **Community Stability**: Community member signatures are stored in `.maxilun/community_signatures.json` so module IDs and labels stay consistent between scans.

---

## 5. Temporal Snapshotting & Architectural Diff

1. **Snapshot Archive**: Running `python cli.py scan --snapshot` archives the artifacts to `maxilun-out/snapshots/YYYY-MM-DD/`.
2. **Diff Comparison**: Run `python cli.py diff <target1> <target2>` to compare two dated snapshots or two `graph.json` files:
   - Symbol delta (`+ / - nodes`)
   - Relationship delta (`+ / - edges`)
   - Detection of *God Node* shifts and new dependencies.
