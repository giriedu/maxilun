# Surface State Topology: Deterministic UI Finite State Machines

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-craft/SKILL.md"
  origin: "Maxilun Craft Engine"
-->

Panduan pemodelan status antarmuka (*surface states*) menggunakan mesin status terhingga (*finite state machine* / FSM). Setiap komponen asinkron dan permukaan layar dinamis wajib memiliki representasi visual terukur untuk keenam status diskrit guna menolak *impossible states*.

---

## 1. Taksonomi 6 Status Antarmuka Diskrit

```text
       [Inisiasi / Idle]
               │
               ▼
       [Loading / Shimmer] ◄───┐
         │           │          │
         ▼           ▼          │ (Refetch / Retry)
    [Populated]   [Empty]       │
         │           │          │
         ▼           ▼          │
      [Pending / Mutating]      │
               │                │
               ▼                │
       [Error / Degraded] ──────┘
```

1. **Idle / Inisial**:
   - Status sebelum pengguna melakukan interaksi atau sebelum pemuatan data pertama kali dipicu.
   - Permukaan menampilkan struktur dasar, navigasi sistem, dan ruang konten yang tenang.
2. **Loading / Shimmer (Disiplin CLS = 0)**:
   - Dilarang menempatkan spinner animasi terisolasi di tengah layar kosong.
   - Wajib menggunakan kerangka geometri (*skeleton*) dengan dimensi, rasio aspek, dan spasi yang persis 1:1 terhadap konten data akhir yang akan muncul.
3. **Populated (Data Berisi)**:
   - Status normal saat payload data sukses diterima dan dirender.
   - Wajib tahan terhadap variasi ekstrem: teks nama panjang tanpa spasi (`min-w-0` + `truncate`), angka ratusan juta (`tabular-nums`), dan gambar dengan rasio tak terduga (`object-fit: cover`).
4. **Empty / Zero-Data**:
   - Status ketika kueri berhasil namun koleksi entitas bernilai kosong ($N = 0$).
   - Wajib menyertakan 3 komponen:
     1. Penjelasan faktual mengapa data kosong (bukan pesan sedih atau ilustrasi kosong berlebih).
     2. Tombol atau tautan aksi langkah pertama untuk mengisi data tersebut.
     3. Tautan dokumentasi atau bantuan jika kekosongan data memerlukan izin akses khusus.
5. **Pending / Optimistic Mutating**:
   - Status saat mutasi data sedang dikirim ke server.
   - Terapkan pembaruan optimistik pada antarmuka dengan indikator mikro non-intrusif (tombol menampilkan state *busy*, opasitas $0.8$, teks aksi tetap terbaca).
6. **Error / Degraded (Toleransi Gangguan)**:
   - Status saat transmisi jaringan gagal, API mengembalikan kode non-200, atau koneksi terputus.
   - Pisahkan antara galat tingkat field (ditangani secara inline) dan galat tingkat layar penuh (ditangani dengan fallback terisolasi).

---

## 2. Tabel Transisi Status & Pencegahan Status Mustahil

Dilarang merancang variabel boolean terpisah yang rentan konflik logika (misal: `isLoading = true` bersamaan dengan `isError = true`). Gunakan tipe diskrit seragam:

```typescript
type SurfaceState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'populated'; data: T }
  | { status: 'empty'; reason: string; actionText: string; onAction: () => void }
  | { status: 'error'; message: string; recoverable: boolean; retry: () => void };
```

| Status Saat Ini | Event Pemicu | Status Berikutnya | Invarian Visual yang Wajib Terpenuhi |
|---|---|---|---|
| `idle` | `FETCH_START` | `loading` | Tampilkan skeleton geometri; kunci scroll jika layar penuh. |
| `loading` | `FETCH_SUCCESS (len > 0)` | `populated` | Gantikan skeleton tanpa lonjakan layout (*zero shift*). |
| `loading` | `FETCH_SUCCESS (len == 0)`| `empty` | Tampilkan panduan pembuatan data perdana. |
| `loading` | `FETCH_FAILURE` | `error` | Tampilkan pesan spesifik dekat titik gagal + tombol coba lagi. |
| `populated` | `MUTATE_OPTIMISTIC` | `pending` | Perbarui tampilan lokal seketika; catat snapshot rollback. |
| `pending` | `MUTATE_REJECTED` | `error` | Kembalikan data ke snapshot awal (*rollback*) + notifikasi undo. |

---

## 3. Disiplin Geometri Skeleton

1. **Rasio Aspek Terkunci**: Gunakan `aspect-ratio` CSS eksplisit pada kotak gambar placeholder untuk mencegah reflow ketika file gambar dimuat.
2. **Kroma Rendah**: Warna latar belakang shimmer wajib menggunakan warna netral bersuhu sama dengan tema aktif, dengan kontras kontur minimal agar tidak menyilaukan.
3. **Peredaman Gerak**: Patuhi kueri `@media (prefers-reduced-motion: reduce)` dengan mematikan animasi denyut berkilau (*pulsing wave*) dan menggantinya dengan warna statis transparan.
