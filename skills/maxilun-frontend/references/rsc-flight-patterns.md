# React Server Components, Flight Serialization & Server Actions

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-frontend/SKILL.md"
  origin: "Maxilun Frontend Engine"
-->

Panduan arsitektur batas eksekusi React Server Components (RSC) dan protokol serialisasi React Flight pada Next.js 15 dan React 19.

---

## 1. Batas Eksekusi RSC vs Client Island

1. **Server Component sebagai Default**:
   - Seluruh komponen di dalam direktori `app/` berstatus Server Component secara default.
   - Gunakan `import 'server-only'` pada modul yang membaca variabel rahasia internal atau langsung mengakses basis data agar gagal kompilasi jika tidak sengaja diimpor ke Client Component.
2. **Client Leaf Component (`'use client'`)**:
   - Dorong direktif `'use client'` sedalam mungkin ke daun pohon komponen (*leaf component*).
   - Dilarang membungkus `app/layout.tsx` atau seluruh halaman dengan `'use client'`.
3. **Komposisi Donat (Donut Pattern)**:
   - Saat komponen interaktif (seperti modal, dropdown, atau tab) membutuhkan konten yang dirender di server, teruskan konten server sebagai `children: ReactNode` ke dalam Client Component wrapper:

```tsx
// ClientWrapper.tsx ('use client')
export function ModalShell({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);
  return isOpen ? <div className="modal-backdrop">{children}</div> : null;
}

// Page.tsx (Server Component)
export default async function Page() {
  const data = await fetchSensitiveData();
  return (
    <ModalShell>
      <ServerRenderedContent data={data} />
    </ModalShell>
  );
}
```

---

## 2. Kontrak Serialisasi React Flight

Protokol Flight mengubah tree RSC menjadi stream byte terstruktur. Hanya tipe data tertentu yang aman dikirim melintasi batas Server $\rightarrow$ Client:

### Tipe yang Didukung
- Tipe primitif: `string`, `number`, `boolean`, `null`, `undefined`, `bigint`.
- Struktur data standar: `Array`, *plain object* (`{}`), `Map`, `Set`, `TypedArray`.
- Kontrak asinkron: `Promise` (dibuka di Client Component menggunakan hook `use()` React 19).
- Komponen & elemen: Node JSX (`ReactNode`), referensi Server Action berdirektif `'use server'`.

### Tipe yang Gagal Serialisasi (Dilarang)
- Fungsi atau callback biasa (misal: `onClick` yang didefinisikan di Server Component).
- Instance class kustom dengan prototype atau method internal (misal: objek model ORM, `Decimal.js`). Wajib dipetakan menjadi objek data datar (*Plain Old JavaScript Object* / POJO) sebelum dikirim ke Client.
- Node DOM asli, `Symbol`, dan `WeakMap`/`WeakSet`.

---

## 3. Server Actions sebagai Endpoint HTTP Publik

Setiap fungsi berdirektif `'use server'` adalah endpoint HTTP POST yang dapat dipanggil langsung dari luar antarmuka:

1. **Otorisasi di Dalam Action**:
   - Selalu periksa sesi pengguna aktif di baris pertama setiap Server Action.
2. **Validasi Skema Masukan**:
   - Validasi seluruh payload masukan (`FormData` maupun objek) menggunakan Zod atau pustaka validasi serupa sebelum mengeksekusi mutasi.
3. **Pola Pengembalian Hasil Terdiskriminasi**:
   - Kembalikan objek status terstruktur `{ ok: true, data }` atau `{ ok: false, fieldErrors }` agar input form tetap aman dan tidak hilang saat gagal.
