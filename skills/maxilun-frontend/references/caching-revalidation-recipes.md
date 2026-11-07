# Next.js 15 Caching, Revalidation & Route Topology Recipes

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-frontend/SKILL.md"
  origin: "Maxilun Frontend Engine"
-->

Panduan operasional semantik caching eksplisit, invalidasi berbasis tag, dan topologi rute asinkron di Next.js 15.

---

## 1. Perubahan Paradigma Caching di Next.js 15

Di Next.js 15, seluruh fungsi `fetch()` dan Route Handler GET bersifat **tidak di-cache secara default** (*uncached by default*), dan Client Router Cache menggunakan `staleTime: 0` untuk rute halaman dinamis.

### Pengaktifan Cache Eksplisit
Gunakan opsi cache secara sadar sesuai kebutuhan data:

```typescript
// 1. Caching statis dengan durasi waktu (Time-based Revalidation)
const res = await fetch('https://api.example.com/products', {
  next: { revalidate: 3600 }, // 1 jam
});

// 2. Caching berbasis tag terarah (On-demand Revalidation)
const res = await fetch(`https://api.example.com/orders/${id}`, {
  next: { tags: [`order:${id}`, 'orders'] },
});
```

---

## 2. Invalidasi Tag Terarah (On-Demand Revalidation)

Hindari penggunaan `revalidatePath('/')` global yang membatalkan cache seluruh aplikasi. Gunakan invalidasi presisi berbasis tag:

```typescript
import { revalidateTag } from 'next/cache';

export async function updateOrderStatus(orderId: string, status: string) {
  'use server';
  await db.updateOrder(orderId, status);
  // Hanya invalidasi cache untuk order spesifik ini
  revalidateTag(`order:${orderId}`);
}
```

---

## 3. Topologi Rute Asinkron (Async Request APIs)

Di Next.js 15, `params`, `searchParams`, `cookies()`, dan `headers()` bersifat asinkron dan wajib di-`await`:

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

## 4. Eliminasi Waterfall dengan Streaming & Suspense

1. **Paralelisasi Kueri Independen**:
   Gunakan `Promise.all` saat membaca beberapa sumber data yang tidak saling bergantung.
2. **Streaming Komponen Lambat**:
   Bungkus komponen yang memproses data eksternal lambat dengan `<Suspense fallback={<Skeleton />}>` sehingga kerangka halaman utama dan navigasi langsung terkirim ke browser tanpa menunggu komponen tersebut selesai.
