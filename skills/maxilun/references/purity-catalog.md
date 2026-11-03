# Maxilun Purity Catalog

<!-- metadata:
  version: "1.0.0"
  last_updated: "2026-11-02"
  sync_target: "scripts/test-suite.py:BANNED_WORDS"
  origin: "Maxilun Purity Engine"
-->

Katalog penolakan pola generik (*Purity Catalog*) untuk ekosistem Maxilun pada tiga domain: **Konten/Teks**, **Desain Antarmuka**, dan **Kode/Interaksi**. Panduan ini dipakai untuk evaluasi berbasis konteks produk — bukan pemindai buta yang menolak pola sah tanpa melihat fungsinya.

> **Sinkronisasi Test Suite**: Daftar kosakata buzzword terlarang di Bagian A.5 selaras dengan `BANNED_WORDS` pada `scripts/test-suite.py`.

---

## A. Pola Klise pada Konten & Teks

Tulis ulang teks bila memenuhi satu atau lebih tanda berikut:

1. **Generik tanpa jangkar domain (*Identity Swap Failure*)** — kalimat dapat dipindah ke produk kompetitor atau industri lain tanpa mengubah satu kata pun. Wajib sebut objek kerja, metrik nyata, atau alur tugas spesifik pengguna.
2. **Rasio sinyal rendah** — banyak kalimat pembuka tetapi miskin fakta atau keputusan. Satu kalimat = satu informasi fungsional baru.
3. **Klaim superlatif tanpa bukti** — menjanjikan hasil bombastis tanpa mekanisme atau angka terverifikasi.
4. **Statistik atau testimoni karangan** — angka seperti `"99.9% akurasi"` atau `"10.000+ tim percaya kami"` tanpa sumber riil wajib dihapus.
5. **Kosakata Buzzword Terlarang (`BANNED_WORDS`)** — dilarang dipakai sebagai klaim positif:
   - Inggris: `delve`, `tapestry`, `synergy`, `holistic`, `leverage`, `seamlessly`, `robust`, `cutting-edge`, `game-changer`, `revolutionary`, `supercharge`, `dive in`, `elevate`, `empower`, `unlock`, `transformative`, `next-level`, `state-of-the-art`, `best-in-class`, `paradigm shift`.
   - Indonesia: `menyelami`, `merajut harmoni`, `sinergi`, `holistik`, `memanfaatkan secara mulus`, `solusi mutakhir/terdepan`, `pengubah permainan`, `revolusioner`, `meningkatkan ke level berikutnya`, `mari selami`, `memberdayakan`, `membuka potensi`, `transformatif`, `kelas dunia`, `pergeseran paradigma`.
6. **Slogan brosur kosong** — frasa cetakan seperti *"Revolutionize Your Workflow"*, *"Unlock Your Potential"*, *"Di era digital yang serba cepat"*, *"Solusi all-in-one terpercaya"*.

---

## B. Pola Klise Visual & Monokultur Desain Antarmuka

Prinsip inti: **tolak klise mentah LLM sekaligus tolak monokultur cetakan tunggal.** Desain antarmuka wajib lahir dari karakter subjek, audiens, dan tugas utama produk.

### B1. Tipografi
1. **Hierarki datar tanpa skala tipografi (`TYPO-001`)** — menggunakan font sistem/standar tanpa pembedaan peran (display vs body vs metadata), tanpa pengaturan `line-height`/`letter-spacing`, atau memakai lebih dari 5 ukuran acak di luar skala (`TYPO-005`). *(Catatan: `Inter`, `Geist`, atau `system-ui` sah untuk aplikasi operasional padat selama skala, kontras bobot, dan `tabular-nums` terkalibrasi; untuk halaman editorial/brand, pasangkan typeface berkarakter).*
2. **Kontras teks lemah (`TYPO-002` / `CLR-002`)** — teks abu-abu pucat di atas permukaan berwarna dengan rasio `< 4.5:1`.
3. **Hitam/abu-abu tak terkalibrasi pada tema terang (`TYPO-003`)** — teks `#000000` murni di atas latar putih menyilaukan yang melelahkan bacaan panjang. *(Pengecualian sah: kanvas gelap kontras tinggi seperti `#010102`/`#000000` pada referensi seperti `linear.app.md` atau `vercel.md`, serta garis tepi media `1px` alpha `oklch(0 0 0 / 0.1)`).*
4. **Panjang baris ekstrem (`TYPO-004`)** — paragraf bacaan melebar `> 75ch` tanpa batas lebar baca (`max-w-[65ch]`).
5. **Input mobile `< 16px` (`TYPO-007`)** — memicu auto-zoom paksa di iOS Safari.

### B2. Warna & Permukaan
6. **Gradien ungu-biru dekoratif default (`CLR-001`)** — gradien `#667eea → #764ba2` atau glow neon acak tanpa makna merek/status.
7. **Latar belakang terlalu jenuh (`CLR-005`)** — permukaan kerja utama menggunakan kroma tinggi (`chroma > 0.05` di OKLCH) yang mengganggu keterbacaan konten.
8. **Status hanya mengandalkan warna (`CLR-004`)** — merah/hijau tanpa ikon atau label teks pendamping.
9. **Dark mode tempelan (`CLR-007`)** — membalik warna secara naif tanpa sistem token permukaan dan tanpa `color-scheme: dark`.

### B3. Tata Letak & Bahaya Monokultur Baru
10. **Tumpukan rata-tengah monoton (`LAY-011`)** — seluruh halaman mengulang pola *overline kapital tengah → H2 tengah → subteks 2 baris tengah → kartu simetris* dari atas ke bawah.
11. **Tiga kartu simetris tanpa diferensiasi (`LAY-008`)** — `grid-cols-3` berisi 3 kotak identik dengan ikon bulat di atas dan 2 kalimat basa-basi. Ganti sesuai sifat konten: tabel perbandingan faktual, alur langkah bernomor, *split showcase* artefak kerja nyata, komposisi editorial, atau grid asimetris bila tiap panel punya peran berbeda.
12. **Monokultur SaaS Bento / `Cmd+K` Salah Tempat (`LAY-013`)** — menyalin mentah estetika dashboard gelap developer tools (Bento gelap, palet biru-slate dingin, badge shortcut `Cmd+K`, label teknis monospaced) untuk produk non-teknis seperti klinik kesehatan, kuliner, pendidikan, media editorial, atau ritel konsumen.
13. **Strip 4 kotak KPI dekoratif (`LAY-009` / `LAY-012`)** — empat kartu angka statis di puncak halaman dengan persentase hijau karangan (`+12.5%`) tanpa konteks waktu, filter, atau tindakan lanjut.
14. **Hero dengan dua tombol primer kembar (`LAY-010` / `CMP-017`)** — dua tombol solid/pill berebut fokus utama. Tetapkan tepat satu aksi primer per tampilan; aksi pendamping tampil netral/sekunder.
15. **Pembungkusan kartu berlapis (`LAY-001` / `LAY-002`)** — kartu di dalam kartu di dalam kartu; gunakan pengelompokan spasi (`2x` jarak antar-grup dibanding intra-grup) sebelum menambah kotak atau garis.

### B4. Komponen & Navigasi
16. **Breadcrumb redundan di halaman datar (`CMP-001` / `CMP-011`)** — menampilkan `Home > Dashboard > Settings` pada landing page, halaman login, atau aplikasi bersarang dangkal. Gunakan judul konteks atau tautan balik tunggal; simpan *breadcrumb* hanya untuk taksonomi dalam (`≥ 3` level seperti dokumentasi besar, sistem berkas, atau katalog multi-kategori).
17. **Kapsul pill dekoratif di atas H1 (`CMP-015`)** — badge melayang `• FITUR BARU •` dengan titik menyala di setiap hero.
18. **Gimmick fiksi ilmiah palsu (`CMP-016`)** — menamai utilitas biasa dengan istilah berlebihan (*"Chamber 01"*, *"Quantum Core"*, bola wireframe 3D tanpa fungsi) alih-alih menampilkan artefak produk asli.
19. **Badge pemasaran tanpa fakta (`CMP-002`)** & **Emoji sebagai ikon fungsional (`CMP-003`)**.
20. **Radius seragam mengabaikan geometri bersarang (`CMP-004`)** — container dan anak memakai radius sama tanpa memperhitungkan padding konsentris.
21. **Elemen navigasi/kontrol mati (`CMP-005` / `CMP-012`)** — kotak cari, ikon lonceng, filter, atau tombol yang tidak melakukan apa-apa saat diklik.
22. **Label navigasi generik tanpa konteks domain (`CMP-010`)** — sidebar hanya menulis *Menu 1, Analytics, Reports* tanpa menyebut entitas bisnis sesungguhnya.

### B5. Gerak & Aksesibilitas
23. **Animasi properti layout (`ANI-002`)** — menganimasikan `width`, `height`, `top`, `left` yang memicu reflow; gunakan `transform` dan `opacity`.
24. **Mengabaikan `prefers-reduced-motion` (`ANI-003`)** atau **memutar media otomatis tanpa kendali (`ANI-005`)**.
25. **Pelanggaran aksesibilitas dasar (`A11Y-001..007`)** — kontrol tanpa nama aksesibel, input tanpa `<label>`, `:focus-visible` dihapus, atau target sentuh mobile `< 44x44px` (`LAY-004`).

---

## C. Ringkasan Kode Pemeriksaan Kontekstual

Gunakan kode referensi ini saat melaporkan hasil audit desain/kode secara presisi (`file:line` + ID + perbaikan konkret):

| Kategori | Rentang ID | Fokus Evaluasi Utama |
|---|---|---|
| Tipografi | `TYPO-001` .. `TYPO-007` | Hierarki skala peran, lebar baca `60–75ch`, kontras terukur, `tabular-nums`, input mobile `≥16px` |
| Warna | `CLR-001` .. `CLR-007` | Bebas gradien dekoratif klise, kroma latar tenang, status punya ikon/teks pendamping, `color-scheme` |
| Tata Letak | `LAY-001` .. `LAY-013` | Bebas cetakan rata-tengah monoton, bebas monokultur Bento salah domain, 1 aksi primer, target sentuh |
| Komponen | `CMP-001` .. `CMP-017` | Bebas kontrol mati, bebas kapsul/gimmick palsu, radius konsentris, navigasi berbasis entitas domain |
| Gerak | `ANI-001` .. `ANI-007` | Hanya `transform`/`opacity`, durasi mikro `≤250ms`, hormati `prefers-reduced-motion` |
| Aksesibilitas | `A11Y-001` .. `A11Y-007` | Nama aksesibel, asosiasi `<label>`, indikator `:focus-visible`, urutan heading semantik |

---

## D. Evaluasi Kontekstual Sebelum Selesai

Sebelum menyerahkan karya teks atau antarmuka, uji tiga hal ini secara jujur:
1. **Uji Tukar Identitas**: Jika logo dan nama produk ditutupi, apakah struktur dan bahasanya masih mencerminkan domain spesifik produk ini, atau tampak seperti seribu template AI lainnya?
2. **Uji Pengurangan**: Adakah kartu, badge, pembungkus `<div>`, atau kalimat pengantar yang jika dihapus justru memperjelas tugas utama pengguna?
3. **Uji Kejujuran Fungsional**: Apakah setiap tombol, state kosong/gagal, dan angka yang tampil di layar benar-benar bekerja dan jujur?
