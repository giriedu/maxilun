# Multi-Tenant Isolation & Row-Level Security (RLS) Playbook

Architecture standards for strict tenant isolation, PostgreSQL Row-Level Security (RLS), connection pooling compatibility, and tenant-aware indexing.

---

## 1. Multi-Tenancy Architecture Models

| Model | Isolation Level | Operational Overhead | Resource Efficiency | Recommended Use Case |
|---|---|---|---|---|
| **Shared DB, Shared Schema (RLS)** | High (enforced in DB engine) | Low (single migration set) | High (shared pool & buffer cache) | Default for SaaS applications up to thousands of tenants. |
| **Shared DB, Schema-per-Tenant** | Moderate (namespace separation) | High (N migrations to run) | Moderate (connection pool fragmentation) | Tenants requiring custom schema extensions or separate backups. |
| **Database-per-Tenant** | Maximum (physical separation) | Very High (N database instances) | Low (idle capacity cost) | Enterprise compliance mandates (HIPAA, PCI-DSS Level 1). |

---

## 2. PostgreSQL Row-Level Security (RLS) Implementation

### Enabling RLS and Default Deny
Every table containing tenant data must enable RLS and force security policies on table owners:

```sql
-- 1. Enable RLS
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- 2. Prevent table owner bypass
ALTER TABLE orders FORCE ROW LEVEL SECURITY;
```

### Context-Variable Tenant Policy
Bind tenant identity to PostgreSQL runtime configuration settings (`app.current_tenant_id`) using `SET LOCAL`:

```sql
-- 3. Policy for tenant row visibility and insertion
CREATE POLICY tenant_isolation_orders ON orders
  FOR ALL
  USING (tenant_id = NULLIF(current_setting('app.current_tenant_id', true), '')::uuid)
  WITH CHECK (tenant_id = NULLIF(current_setting('app.current_tenant_id', true), '')::uuid);
```

### Invariant Rules
1. **Never use `current_setting` without the second parameter `true`**: The second parameter allows missing settings to return `NULL` instead of raising an unhandled exception.
2. **`NULLIF` safeguard**: Wrap `current_setting` in `NULLIF(..., '')` so empty strings do not coerce to invalid UUIDs.
3. **`WITH CHECK` requirement**: Always specify `WITH CHECK` alongside `USING` so unauthorized users cannot insert or update records with an arbitrary tenant ID.

---

## 3. PgBouncer & Transaction-Mode Connection Pooling

In pooled environments (PgBouncer in `transaction` pool mode), session state does not persist across transactions.

1. **`SET LOCAL` within Transactions**:
   - Never use `SET session.tenant_id = ...`. It bleeds across client connections.
   - Always use `SET LOCAL app.current_tenant_id = $1` inside an explicit `BEGIN ... COMMIT` block. `SET LOCAL` is automatically cleared at transaction end.

```typescript
// Application transaction wrapper (TypeScript / Node.js)
await db.transaction(async (tx) => {
  await tx.execute(sql`SELECT set_config('app.current_tenant_id', ${tenantId}, true)`);
  return await tx.query.orders.findMany({ where: eq(orders.status, 'active') });
});
```

2. **Application Role Separation**:
   - The application connecting user must **NOT** be a superuser or the table owner, otherwise RLS is bypassed unless `FORCE ROW LEVEL SECURITY` is applied.
   - Create a dedicated unprivileged role: `CREATE ROLE app_user WITH LOGIN PASSWORD '...';`

---

## 4. Tenant-Aware Indexing Strategy

PostgreSQL executes the RLS filter on every scanned row. Without tenant-leading indexes, queries devolve into full table scans.

1. **Tenant-Leading Composite Indexes**:
   - Every index on an RLS table must place `tenant_id` as the **first** column:
   ```sql
   -- Correct: Index seeks directly to the tenant's data slice
   CREATE INDEX idx_orders_tenant_status ON orders (tenant_id, status, created_at DESC);

   -- Incorrect: Scans index across all tenants before filtering
   CREATE INDEX idx_orders_status ON orders (status, created_at DESC);
   ```
2. **Partial Indexes with Tenant Context**:
   - For high-volume hot rows, scope partial indexes by tenant:
   ```sql
   CREATE INDEX idx_orders_tenant_pending ON orders (tenant_id, created_at)
     WHERE status = 'pending';
   ```

---

## 5. Verification & Leak Testing

Verify that cross-tenant access is impossible:

```sql
-- Test 1: Verify tenant A cannot read tenant B data
BEGIN;
SELECT set_config('app.current_tenant_id', '11111111-1111-1111-1111-111111111111', true);
SELECT COUNT(*) FROM orders; -- Returns only Tenant A rows
ROLLBACK;

-- Test 2: Verify missing tenant context returns 0 rows
BEGIN;
SELECT set_config('app.current_tenant_id', '', true);
SELECT COUNT(*) FROM orders; -- Returns 0 rows
ROLLBACK;
```
