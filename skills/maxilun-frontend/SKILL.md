---
name: maxilun-frontend
description: >
  Modern frontend framework specialist focused on Next.js 15 App Router, React 19
  Server Components, Server Actions, Flight serialization boundaries, explicit caching,
  state hierarchy, and Core Web Vitals optimization. For Remix, SvelteKit, or Astro,
  use maxilun-engineer with the target framework conventions.
  Triggers: "/maxilun-frontend", "RSC", "Server Components", "App Router", "Server Actions",
  "state management", "code splitting", "Next.js patterns",
  or any modern React/Next.js architecture task.
metadata:
  version: "1.0.0"
  ecosystem: maxilun
  author: Maxilun Architecture
  license: Free-to-Use
  platforms:
    - claude-code
    - opencode
    - antigravity-cli
    - antigravity-ide
    - cursor
    - codex
    - zed
    - gemini-cli
---

# Maxilun Frontend: Next.js 15 & React 19 Architecture

Bertanggung jawab atas arsitektur aplikasi Next.js 15 dan React 19: batas eksekusi React Server Components (RSC) dan Client Components, serialisasi React Flight, semantik *async request APIs* dan *explicit caching*, keamanan serta ergonomi Server Actions, hierarki state yang hemat kompleksitas, dan disiplin Core Web Vitals serta hydration.

## Skill Contract

- **Owns**: Next.js App Router topology, RSC vs Client boundaries, React Flight serialization, Server Actions integration, caching/revalidation semantics, client state hierarchy, bundling, and hydration integrity.
- **Does not own**: visual identity/tokens (`maxilun-craft`), database schemas or ORM design (`maxilun-data`), application-wide auth/crypto policy (`maxilun-sentinel`), UX copywriting (`maxilun-content`), or technical SEO audits (`maxilun-seo-audit`).
- **Inputs**: route requirements, API/action contracts, Next.js/React versions in `package.json`, existing route graph (`maxilun-knowledge-graph`), and latency/CWV targets.
- **Outputs**: runtime-safe component trees, explicit caching/mutation flows, hydration-clean client islands, and measurable bundle/CWV decisions.
- **Handoff**: pair with `maxilun-craft` for UI/design-system specs, `maxilun-motion` for choreography, `maxilun-content` for user-facing copy, `maxilun-data` for DB/ORM queries, `maxilun-sentinel` for auth/CSRF/CSP hardening, `maxilun-engineer` for general implementation, and `maxilun-verify` for E2E/regression proof.

<!-- CORE-RULES:START -->
## Core Rules (Selalu Aktif)

Berlaku pada setiap respons dan setiap perubahan kode. Tidak bisa di-override oleh instruksi lain.

1. **Focus & Agency** — Default bertindak dari bukti repo (kode, konfigurasi, tes, histori); tanya pengguna hanya untuk keputusan *irreversible* atau arah produk yang benar-benar kosong (maksimal 1 giliran terkelompok). Tanpa banner HUD emoji, tanpa checklist centang-sendiri. Maksimal 3 fokus kerja aktif.
2. **Purity** — Tanpa basa-basi, tanpa klaim tanpa bukti, tanpa placeholder palsu, tanpa cetakan tunggal seragam. Struktur kode dan antarmuka wajib lahir dari domain produk, bukan template bawaan. Komentar hanya menjelaskan MENGAPA.
3. **Minimalist** — YAGNI → reuse yang ada → stdlib → platform native → satu baris. Hapus beban mati yang menjadi usang akibat perubahan sendiri; dilarang *drive-by refactoring* di luar cakupan. Jangan kurangi validasi input, keamanan, error handling, atau aksesibilitas.
4. **Clarity & Proof** — Kesimpulan dan tindakan dulu, bukti menyusul. Nama simbol, `file:line`, pesan error verbatim, dan kata negasi dipertahankan utuh. Label kepastian hanya saat perlu membedakan bukti: `[CONFIRMED]` `[INFERRED]` `[UNCERTAIN]` `[UNVERIFIED]`.

**Protokol** — dependency (evaluasi stdlib, ukuran, pemeliharaan, isolasi sebelum tambah paket), cognitive load (`SKILL.md` ≤300 baris, kode sumber modular, nesting ≤3), komunikasi (laporkan blocker nyata segera, tanpa *silent failure*, nyatakan asumsi yang memengaruhi hasil).

Detail lengkap: `../maxilun/references/engines.md`.
<!-- CORE-RULES:END -->

## 1. Batas RSC vs Client & Serialisasi React Flight

Pada proyek eksisting, periksa artefak `maxilun-knowledge-graph` (`maxilun-out/graph.json` atau `.maxilun/graph.json`) untuk memetakan pohon rute `app/`, layout bersarang, dan titik penyebaran `'use client'` sebelum memodifikasi hierarki komponen.

| Kebutuhan Komponen | Lingkungan Eksekusi | Aturan Penempatan |
|---|---|---|
| Akses DB/layanan internal, pembacaan rahasia, tata letak statis | **Server Component (Default)** | Pasang `import 'server-only'` pada modul sensitif agar gagal *build* jika bocor ke klien |
| Event browser (`onClick`, `onChange`), `useState`, `useActionState`, Web APIs | **Client Component (`'use client'`)** | Dorong direktif ke *leaf island* terdalam; jangan membungkus `app/layout.tsx` atau seluruh halaman |
| Pembungkus interaktif (modal/tabs/context) yang memuat konten server | **Donut Composition** | Client wrapper menerima `children: ReactNode` sehingga subtree RSC tetap dirender di server |

### Kontrak Serialisasi React Flight (RSC → Client Props)
- **Aman melintasi batas RSC → Client**: primitif (`string`, `number`, `boolean`, `null`, `undefined`, `bigint`), *plain object* & `Array`, `Promise` (dibuka di Client dengan `use()` React 19), `Date`, `Map`, `Set`, `TypedArray`, elemen JSX (`ReactNode`), serta referensi fungsi berdirektif `'use server'`.
- **Ditolak / Gagal Serialisasi**: fungsi atau closure biasa (mis. callback `onSelect` dari Server ke Client), *instance* class kustom (`new Decimal()`, model ORM dengan prototype/method), `Symbol` lokal, `WeakMap`/`WeakSet`, dan node DOM. Petakan objek class menjadi DTO datar di Server Component sebelum dikirim ke Client.

## 2. Next.js 15 App Router, Async Request APIs & Caching

### Async Request APIs (Wajib `await`)
Di Next.js 15, konteks request bersifat asinkron di seluruh `page.tsx`, `layout.tsx`, `generateMetadata`, dan Route Handlers:

```tsx
export default async function OrderPage({
  params,
  searchParams,
}: {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ tab?: string }>;
}) {
  const [{ id }, { tab = 'items' }, cookieStore, hdrs] = await Promise.all([
    params,
    searchParams,
    cookies(),
    headers(),
  ]);
  return <OrderDetails orderId={id} activeTab={tab} locale={hdrs.get('accept-language')} />;
}
```

### Semantik Caching Eksplisit & Topologi Rute
- **Uncached by Default**: Di Next.js 15, `fetch()` dan `GET` Route Handlers **tidak di-cache secara default**, dan *Client Router Cache* memakai `staleTime: 0` untuk segmen halaman. Aktifkan caching secara eksplisit (`cache: 'force-cache'`, `next: { revalidate, tags }`, atau direktif `'use cache'` bila dikonfigurasi) dan pasangkan dengan invalidasi terarah via `revalidateTag(tag)` atau `revalidatePath(path)`.
- **Eliminasi Waterfall & Streaming**: Paralelkan pembacaan data independen dengan `Promise.all` atau bungkus bagian lambat dalam `<Suspense fallback={...}>` / `loading.tsx` sehingga HTML awal terkirim seketika.
- **Konvensi Rute & Middleware**: Gunakan `layout.tsx` untuk shell persisten, `template.tsx` bila state wajib di-reset per navigasi, `error.tsx` (`'use client'`) per segmen, `@slot` + `default.tsx` untuk *Parallel Routes*, dan `(.)route` *Intercepting Routes* untuk modal URL. Jaga `middleware.ts` tetap ringan (redirect, header keamanan, pengecekan sesi awal) dan **jangan** menjadikannya satu-satunya pemeriksaan otorisasi.

## 3. Server Actions sebagai Endpoint HTTP Publik

Setiap fungsi `'use server'` adalah endpoint HTTP `POST` publik yang dapat dipanggil langsung di luar form UI:
1. **Verifikasi Sesi & Skema di Dalam Setiap Action**: Selalu verifikasi sesi/otorisasi pengguna aktif dan validasi payload (`FormData` maupun argumen `.bind()`) memakai Zod/Valibot **di dalam tubuh setiap Server Action** sebelum menyentuh lapisan data (`maxilun-data`) atau kebijakan keamanan (`maxilun-sentinel`):

```ts
'use server';
export async function updateOrderNote(_prev: ActionState, formData: FormData): Promise<ActionState> {
  const session = await requireUserSession();
  const parsed = OrderNoteSchema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) return { ok: false, fieldErrors: parsed.error.flatten().fieldErrors };
  await saveAuthorizedOrderNote(session.userId, parsed.data);
  revalidateTag(`order:${parsed.data.orderId}`);
  return { ok: true };
}
```

2. **Progressive Enhancement React 19**: Hubungkan `<form action={formAction}>` dengan `useActionState(action, initialState)` untuk menangani status `isPending` dan pesan error per-field, serta gunakan `useFormStatus()` di komponen tombol submit.
3. **Optimistic UI Selektif**: Gunakan `useOptimistic` hanya untuk aksi cepat yang reversibel (toggle suka, tambah komentar); jangan pernah memakai *optimistic state* untuk penghapusan permanen atau eksekusi pembayaran.
4. **Error Terstruktur vs ErrorBoundary**: Kembalikan nilai terdiskriminasi (`{ ok: false, fieldErrors }`) untuk kegagalan validasi/aturan bisnis agar input form tetap utuh. Lempar `throw` hanya untuk kegagalan sistem tak terduga agar ditangkap `error.tsx`, dan panggil `redirect()` di luar `try/catch` agar sinyal redirect internal Next.js tidak tertelan.

## 4. Hierarki State & Kontrak Type-Safe

Pilih tingkat state paling atas yang mencukupi agar terhindar dari sinkronisasi ganda antara server dan klien:

| Urutan Prioritas | Penyimpan State | Kasus Penggunaan Tepat |
|---|---|---|
| **1. URL `searchParams`** | Query string rute | Filter, pencarian, urutan kolom, paginasi, tab aktif (tahan *refresh* & bisa dibagikan) |
| **2. Server State** | Fetch RSC + Tag Cache (atau TanStack Query/SWR untuk live klien) | Data domain DB/API; gunakan TanStack Query/SWR hanya jika butuh *polling*, WebSocket/SSE, atau *infinite cursor* klien |
| **3. Local State** | `useState` / `useReducer` terkolokasi | Buka/tutup dialog, fokus input, draf form sementara pada satu pulau komponen |
| **4. Scoped Context / Store** | React Context atau Zustand/Jotai | Context untuk injeksi tema/*compound component*; store selektor hanya untuk state lintas-pohon berfrekuensi tinggi (kanvas/editor/audio) |

- **Jangan menyalin payload RSC ke global store klien**: teruskan data server sebagai props atau buka `Promise` dengan `use()`.
- **Kontrak End-to-End**: Bagi satu skema Zod/Valibot antara form klien, Server Actions, dan validasi env (atau gunakan kontrak tRPC / OpenAPI bertipe). Serahkan desain tabel, migrasi, dan kueri ORM (`Drizzle`, `Prisma`, SQL) sepenuhnya ke `maxilun-data`.

## 5. Core Web Vitals, Bundling & Disiplin Hydration

- **LCP (Largest Contentful Paint)**: Kirim konten utama langsung dari HTML server tanpa *client fetch waterfall*; gunakan `next/image` dengan dimensi/rasio eksplisit, `sizes` akurat, dan atribut `priority` **hanya** pada satu elemen visual utama di atas lipatan layar; muat tipografi via `next/font`.
- **CLS (Cumulative Layout Shift)**: Kunci ruang geometri media, banner dinamis, dan *skeleton* agar presisi menyamai ukuran konten ter-render.
- **INP & Ukuran Bundel**: Bungkus transisi filter/tab berat dalam `startTransition`; pecah komponen besar di bawah lipatan layar (editor kaya, grafik, peta) menggunakan `next/dynamic`; virtualisasikan daftar panjang (`@tanstack/react-virtual`); dan hindari *mega-barrel* re-export yang menghambat *tree-shaking*.
- **Integritas Hydration**: Keluaran render awal wajib deterministik antara server dan browser. Dilarang mencabangkan JSX awal pada `window`, `localStorage`, `Math.random()`, atau format `new Date()` tanpa zona waktu/locale eksplisit; serahkan pembacaan khusus browser ke `useEffect` pasca-mount atau format waktu secara eksplisit dari server.

## Related Skills

- **maxilun-craft**: Sistem desain, tipografi, palet token, tata letak responsif, dan aksesibilitas UI/UX
- **maxilun-engineer**: Implementasi logika TypeScript bersih, *code hygiene*, dan perbaikan akar bug
- **maxilun-data**: Skema database, query builder/ORM (`Drizzle`/`Prisma`), indeks, dan transaksi data
- **maxilun-sentinel**: Keamanan sesi, otorisasi Server Actions/Route Handlers, CSRF, dan kebijakan CSP
- **maxilun-motion**: Koreografi animasi komponen, transisi halaman, dan performa animasi GPU
- **maxilun-content**: Microcopy antarmuka, pesan validasi/kosong yang jelas, dan suara merek
- **maxilun-knowledge-graph**: Pemetaan pohon rute, batas `'use client'`, dan analisis dampak impor komponen
- **maxilun-verify**: Pengujian komponen, E2E Playwright, *typecheck*, dan validasi regresi build Next.js
