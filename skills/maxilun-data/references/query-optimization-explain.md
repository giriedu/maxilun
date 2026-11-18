# Database Query Optimization & EXPLAIN ANALYZE Diagnostics

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-data/SKILL.md"
  origin: "Maxilun Data Engine"
-->

How to diagnose query performance, read an `EXPLAIN ANALYZE` execution plan, and design precise indexes.

---

## 1. Reading the Execution Plan (EXPLAIN ANALYZE)

When a query is slow, do not add indexes speculatively. Run `EXPLAIN (ANALYZE, BUFFERS)` and inspect 4 main checkpoints:

1. **Sequential Scan vs Index Scan**:
   - If the table has thousands of rows and the plan shows `Seq Scan`, check whether the `WHERE` filter or the `JOIN` clause is not covered by an existing index.
2. **Estimate vs Actual Rows**:
   - If the query planner estimates `rows=1` but the real count is `actual rows=100000`, the table statistics are stale. Run `ANALYZE table_name;`.
3. **Memory vs Disk Sort (Sort Method)**:
   - Check whether the sort operation (`ORDER BY`) uses `quicksort Memory` or `external merge Disk`. A disk sort means you need an ordered index or a higher `work_mem`.
4. **Buffer Hit Ratio**:
   - Check `Buffers: shared hit=... read=...`. A high `read` number signals slow physical disk reads, which a leaner index should reduce.

---

## 2. Composite Index Design Rules

When a query filters on multiple columns (`WHERE tenant_id = ? AND status = ? ORDER BY created_at DESC`):

1. **Equality First column order**:
   - Put columns compared with the equality operator (`=`) leftmost in the index.
   - Put range columns (`<`, `>`, `BETWEEN`) or sort columns (`ORDER BY`) after them.
   - Example of an optimal index: `(tenant_id, status, created_at DESC)`.
2. **Partial Index**:
   - If the query only looks for rows with a specific status (for example: a queue of unprocessed items):
   ```sql
   CREATE INDEX CONCURRENTLY idx_orders_unprocessed 
   ON orders (created_at) 
   WHERE status = 'PENDING';
   ```
   - Saves up to 90% of disk size compared with indexing the whole table.

---

## 3. Row-Level Security (RLS) Optimization

1. **Index the policy columns**:
   - A column used in an RLS policy expression (`tenant_id` or `user_id`) must have its own index or be the leading column of a composite index.
2. **Prevent repeated evaluation**:
   - Wrap the session-reading function in a subquery expression so it executes once per query instead of being evaluated per table row:
   ```sql
   -- Good: evaluated once
   USING (tenant_id = (SELECT current_setting('app.current_tenant')::uuid))
   ```

---

## 4. 5-Step Systematic Query Optimization Flow

Do not optimize queries by guesswork. Follow this deterministic 5-step flow:

```
┌────────────────────────────────────────────────────────┐
│  1. Measure Baseline: EXPLAIN (ANALYZE, BUFFERS)       │
│     (Record execution time, actual rows, buffer read)  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  2. Evaluate Selectivity & Prune Monolithic Scans      │
│     (Compute predicate selectivity, remove Seq Scan)   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  3. Eliminate Spill-to-Disk (Sorts & Hash Aggregates)  │
│     (Detect external merge Disk, adjust work_mem)      │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  4. Rewrite Query Pattern & Covering Index (Rewrite)   │
│     (Subquery -> JOIN, Keyset Pagination, INCLUDE)     │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│  5. Comparative Regression Proof (Before vs After)     │
│     (Verify lower buffers read & execution ms)         │
└────────────────────────────────────────────────────────┘
```

### 4.1 Step 1: Measure the Baseline Execution Plan
Run the slow query in staging or inside a safe transaction:
```sql
EXPLAIN (ANALYZE, BUFFERS, COSTS, TIMING, SUMMARY)
SELECT o.id, o.total_amount, c.name
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.status = 'COMPLETED' AND o.created_at >= '2026-01-01'
ORDER BY o.created_at DESC LIMIT 50;
```
Record three key numbers:
- `Execution Time`: the actual query execution duration in milliseconds.
- `Buffers: shared hit=... read=...`: the ratio of memory pages (*hit*) to physical disk I/O (*read*).
- `Rows Removed by Filter`: the number of rows scanned and then discarded.

### 4.2 Step 2: Predicate Selectivity & Precise Indexes
- If `Rows Removed by Filter` is high on an index scan, the composite index column order is wrong.
- Apply the fixed rule: **Equality (`=`) $\to$ Range (`>`, `<`) $\to$ Sort (`ORDER BY`)**.
- For a status with a skewed distribution (for example 98% `COMPLETED` and 2% `PENDING`), do not index the majority status; create a **Partial Index** for the minority predicate only.

### 4.3 Step 3: Eliminate Spill-to-Disk
- Look for the warning: `Sort Method: external merge Disk: 18432kB` or `spill to temp file`.
- Danger: a sort that exceeds the memory limit must write to temporary disk, which multiplies query latency 10x–50x.
- Fix:
  1. Provide an index whose order exactly matches the `ORDER BY` clause, so the database scans it directly without an in-memory sort (*presorted index scan*).
  2. If the sort is unavoidable for a batch or analytics report, raise the memory limit for the local transaction:
     ```sql
     SET LOCAL work_mem = '64MB';
     ```

### 4.4 Step 4: Rewrite the Query Pattern (Query Rewrite)
1. **Remove N+1 loops**: Replace queries inside an ORM loop with a batch `WHERE parent_id = ANY($1)`.
2. **Cursor-based pagination (Keyset Pagination)**: Do not use `OFFSET 100000` (the database scans and discards the first 100,000 rows). Use an ordered Primary Key cursor:
   ```sql
   -- Replace: OFFSET 50000 LIMIT 20
   -- With keyset:
   WHERE created_at < $last_created_at OR (created_at = $last_created_at AND id < $last_id)
   ORDER BY created_at DESC, id DESC LIMIT 20;
   ```
3. **Index-Only Scan with a Covering Index**:
   ```sql
   CREATE INDEX CONCURRENTLY idx_orders_covering
   ON orders (customer_id, status) INCLUDE (total_amount, created_at);
   ```

### 4.5 Step 5: Comparative Regression Proof
Prove the fix works by comparing the metrics before and after:

| Metric | Before Optimization | After Optimization | Improvement Delta |
|---|---|---|---|
| **Scan Method** | `Seq Scan on orders` | `Index Only Scan` | Full scan eliminated |
| **Buffers Read (Disk I/O)** | `14,280 pages (111 MB)` | `0 pages (0 MB)` | 100% cache hit |
| **Sort Buffer** | `external merge Disk: 24MB` | `None (Index Presorted)` | Zero disk spill |
| **Execution Time** | `1,450 ms` | `3.2 ms` | **$\sim 450\times$ faster** |
