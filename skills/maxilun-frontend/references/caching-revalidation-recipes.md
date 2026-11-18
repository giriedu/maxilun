# Next.js 15 Caching, Revalidation & Route Topology Recipes

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-frontend/SKILL.md"
  origin: "Maxilun Frontend Engine"
-->

Operational guide to explicit caching semantics, tag-based invalidation, and async route topology in Next.js 15.

---

## 1. The Caching Model Change in Next.js 15

In Next.js 15, every `fetch()` call and GET Route Handler is **uncached by default**, and the Client Router Cache uses `staleTime: 0` for dynamic page routes.

### Enabling the Cache Explicitly
Choose a cache option deliberately, according to what the data needs:

```typescript
// 1. Static caching with a time window (Time-based Revalidation)
const res = await fetch('https://api.example.com/products', {
  next: { revalidate: 3600 }, // 1 hour
});

// 2. Targeted tag-based caching (On-demand Revalidation)
const res = await fetch(`https://api.example.com/orders/${id}`, {
  next: { tags: [`order:${id}`, 'orders'] },
});
```

---

## 2. Targeted Tag Invalidation (On-Demand Revalidation)

Avoid a global `revalidatePath('/')`, which invalidates the cache for the whole application. Use precise tag-based invalidation:

```typescript
import { revalidateTag } from 'next/cache';

export async function updateOrderStatus(orderId: string, status: string) {
  'use server';
  await db.updateOrder(orderId, status);
  // Invalidate the cache for this specific order only
  revalidateTag(`order:${orderId}`);
}
```

---

## 3. Async Route Topology (Async Request APIs)

In Next.js 15, `params`, `searchParams`, `cookies()`, and `headers()` are asynchronous and must be `await`ed:

```tsx
export default async function ProductPage({
  params,
  searchParams,
}: {
  params: Promise<{ slug: string }>;
  searchParams: Promise<{ view?: string }>;
}) {
  const [{ slug }, { view = 'grid' }] = await Promise.all([
    params,
    searchParams,
  ]);

  return <ProductCatalog slug={slug} initialView={view} />;
}
```

---

## 4. Eliminating Waterfalls with Streaming & Suspense

1. **Parallelize independent queries**:
   Use `Promise.all` when reading several data sources that do not depend on each other.
2. **Stream slow components**:
   Wrap a component that processes slow external data in `<Suspense fallback={<Skeleton />}>`, so the main page shell and navigation reach the browser immediately without waiting for that component to finish.
