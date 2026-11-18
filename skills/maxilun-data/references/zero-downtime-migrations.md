# Zero-Downtime Database Migrations: The Expand-Contract Pattern

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-data/SKILL.md"
  origin: "Maxilun Data Engine"
-->

How to change a production database schema with no service interruption (*zero-downtime migrations*) using the staged *Expand-Contract* pattern.

---

## 1. The Four Phases of Expand-Contract

Never ship a *breaking* schema change (such as renaming a column or moving a relation) in a single DDL transaction step. Use the 4-phase flow:

```text
[Phase 1: Expand] ──> [Phase 2: Dual Write] ──> [Phase 3: Backfill] ──> [Phase 4: Contract]
```

1. **Phase 1: Expand (widen the schema)**:
   - Add a new column or table that allows `NULL`, without modifying the old column.
   - Example: add a `phone_e164` column next to the old `phone_number` column.
2. **Phase 2: Dual Write**:
   - Update the application code to write to both columns (old and new) while it still reads from the old column.
3. **Phase 3: Backfill (historical data)**:
   - Run a batched background worker (PK cursor: `WHERE id > $last_id ORDER BY id LIMIT 1000` with a $50\text{ms}$ pause) to copy data from the old column to the new one.
   - Do not update millions of rows at once in one giant transaction, because that locks the table exclusively.
4. **Phase 4: Contract (shrink the schema)**:
   - Switch application reads entirely to the new column.
   - Once it is stable under production observation, drop the old column or mark it `deprecated` in a separate migration.

---

## 2. Safe DDL Operation Invariants (PostgreSQL / MySQL)

1. **Lock timeout**:
   - Set `lock_timeout = '2s'` before executing DDL, so the migration fails automatically instead of blocking the production query queue:
   ```sql
   SET lock_timeout = '2s';
   ALTER TABLE orders ADD COLUMN status_code VARCHAR(32);
   ```
2. **Index creation without a table lock**:
   - On PostgreSQL, always use `CREATE INDEX CONCURRENTLY`.
   - On MySQL/InnoDB, use `ALGORITHM=INPLACE, LOCK=NONE`.
3. **Adding a column with a default value**:
   - On PostgreSQL 11+, adding a column with a constant `DEFAULT` does not rewrite the table (*zero rewrite*). On older versions, add the column as `NULL` first, then fill it in stages.
