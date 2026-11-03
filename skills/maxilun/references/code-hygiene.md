<!-- metadata:
  version: "1.0.0"
  last_updated: "2026-11-02"
-->

# Maxilun Code Hygiene Rules

Standar kebersihan kode yang berlaku otomatis saat spesialis Maxilun menulis atau memodifikasi kode sumber.

## 1. Kualitas Komentar

### Pola Komentar yang Dilarang
- Garis pemisah dekoratif (`// ========= SECTION =========`)
- Mengulang isi kode (`// Set count to 0` di atas `let count = 0`)
- Narasi langkah (`// Step 1:`, `// First validate input, then save`)
- Label kosong (`// Helper functions`, `// Main logic`)
- TODO kabur tanpa konteks atau syarat selesai (`// TODO: fix later`)
- JSDoc/docstring yang hanya menyalin ulang nama parameter tanpa informasi kontrak tambahan
- Emoji dekoratif atau penanda penutup blok (`} // end if`)

### Komentar yang Wajib Dipertahankan
- Invarian bisnis dan aturan domain non-intuitif
- Alasan keamanan dan batasan kepercayaan (*trust boundary*)
- Kompromi performa yang didasarkan pada hasil ukur nyata
- Kontrak protokol eksternal, format byte, atau *workaround* bug platform/browser tertentu

Ringkas: satu baris untuk satu alasan. Baris kedua hanya jika memuat fakta teknis baru.

## 2. Penamaan & Struktur Kontrol

- **Fungsi & Metode**: kata kerja spesifik + objek (`verifyWebhookSignature`, `parseInvoiceCsv`, bukan `process` atau `handleData`).
- **Boolean**: terbaca sebagai predikat tegas (`isExpired`, `hasActiveSubscription`, `canVoidPayment`).
- **Variabel State**: kontekstual terhadap domain (`isSubmittingOrder`, `validationErrors`, bukan sekadar `flag` atau `temp`).
- **Alur Kontrol Datar**: gunakan *guard clauses* dan *early return* di awal fungsi; jaga kedalaman indentasi maksimal 3 level.
- **Tipe Eksplisit di Batas Modul**: hindari `any` atau objek tak bertipe pada tanda tangan fungsi publik dan kontrak API.

## 3. Kebersihan Markup, CSS & Styling

1. **Ikuti Sistem Styling Repositori**:
   - Jika proyek memakai **Tailwind / utility CSS**, gunakan utility sesuai konfigurasi token proyek dan ekstrak ke komponen hanya saat pola berulang secara fungsional.
   - Jika proyek memakai **CSS Modules / Vanilla CSS**, beri nama kelas berbasis peran komponen (`.invoice-row`, `.auth-form`), bukan pembungkus tanpa makna (`.wrapper-inner-box`).
2. **Semantik HTML Lebih Dulu**: gunakan `<main>`, `<nav>`, `<section>`, `<article>`, `<form>`, `<button>`, `<dialog>` sebelum jatuh ke `<div>` generik. Jangan menggunakan `<div onClick>` untuk kontrol interaktif.
3. **Disiplin Token Visual**: rujuk variabel skala spasi, warna semantik, dan radius yang berlaku di proyek; hindari angka piksel ganjil acak atau warna hex mentah yang memutus konsistensi tema terang/gelap.
4. **Inline Style**: hanya untuk nilai dinamis yang dihitung saat runtime (mis. koordinat drag, lebar bar progres dari data); properti statis berada di stylesheet atau kelas token.

## 4. Higienitas Form & Interaksi Mikro

- Jangan pernah memblokir tempel (`onPaste` dengan `preventDefault()`) pada input password, kode OTP, atau formulir.
- Pasang `spellCheck={false}` dan `autoCapitalize="none"` pada input email, username, kode, URL, dan token API.
- Ikat setiap input ke `<label>` eksplisit (`htmlFor` atau pembungkusan langsung) tanpa celah klik mati pada checkbox/radio.
- Tambahkan `min-w-0` pada elemen anak flexbox yang menggunakan pemotongan teks (`truncate` / `text-overflow: ellipsis`) agar layout tidak meluber.
- Pasang `overscroll-behavior: contain` pada modal, sheet, dan popover yang memiliki area scroll sendiri.
- Gunakan karakter tipografi tepat pada teks antarmuka: elipsis `…` (bukan `...`), `text-wrap: balance` pada judul utama, dan `tabular-nums` pada angka yang berubah atau disejajarkan vertikal.
