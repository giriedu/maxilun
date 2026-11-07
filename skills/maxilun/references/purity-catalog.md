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
1. **Hierarki datar & font sans generik seragam (`TYPO-001`)** — menggunakan satu font sans polos generik (Inter default tanpa kalibrasi) untuk seluruh tingkatan tanpa pembedaan peran (display vs body vs metadata teknis). Wajib pasangkan typeface display berkarakter kuat untuk judul (`tracking: -0.02em` s.d. `-0.04em`) + monospace fungsional untuk spesifikasi protokol/payload + sans terukur untuk teks tubuh.
2. **Kontras teks lemah (`TYPO-002` / `CLR-002`)** — teks abu-abu pucat di atas permukaan berwarna dengan rasio `< 4.5:1`.
3. **Hitam/abu-abu tak terkalibrasi pada tema terang (`TYPO-003`)** — teks `#000000` murni di atas latar putih menyilaukan yang melelahkan bacaan panjang. *(Pengecualian sah: kanvas gelap kontras tinggi seperti `#010102`/`#000000` pada referensi seperti `linear.app.md` atau `vercel.md`, serta garis tepi media `1px` alpha `oklch(0 0 0 / 0.1)`).*
4. **Panjang baris ekstrem (`TYPO-004`)** — paragraf bacaan melebar `> 75ch` tanpa batas lebar baca (`max-w-[65ch]`).
5. **Input mobile `< 16px` (`TYPO-007`)** — memicu auto-zoom paksa di iOS Safari.
6. **Gradien teks pelangi pada judul (`TYPO-008` / `CLR-008`)** — mewarnai kata-kata judul dengan gradien warna-warni (`bg-gradient-to-r ... bg-clip-text text-transparent`) untuk menutupi tipografi yang membosankan. DILARANG KERAS. Judul wajib bertinta solid dengan kontras tinggi ($\ge 4.5:1$, tema gelap $\ge 7:1$). Wibawa visual lahir dari bentuk huruf (*typeface character*), kontras bobot, dan skala ukuran, bukan efek gradien murahan.
7. **Ukuran teks display raksasa tanpa skala mobile (`TYPO-009`)** — menggunakan ukuran font statis besar (`text-5xl` / `text-6xl` tanpa responsivitas) atau teks panjang (URL, JID, token hash) tanpa `break-words`/`min-w-0`, memicu kata panjang terpotong keluar melebihi canvas layar pada lebar $\le 375\text{px}$. Wajib terapkan fluid scaling (`text-2xl sm:text-4xl lg:text-6xl`) dan `break-words`.

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
16. **Navbar obesitas & menu meluap di mobile (`LAY-015`)** — tinggi navbar mobile $> 64\text{px}$, tautan desktop tidak disembunyikan (`hidden md:flex`), tombol CTA desktop menutupi logo di layar sentuh, atau drawer menu tanpa kunci scroll latar (`overscroll-behavior: contain`).
17. **Kebocoran scroll horizontal mobile (`LAY-016`)** — memakai `width: 100vw` atau `w-screen` (menghitung scrollbar desktop sehingga bocor di mobile), fixed width tanpa `max-w-full`, atau padding `px-12`/`px-20` pada viewport sempit.

### B4. Komponen & Navigasi
16. **Breadcrumb redundan di halaman datar (`CMP-001` / `CMP-011`)** — menampilkan `Home > Dashboard > Settings` pada landing page, halaman login, atau aplikasi bersarang dangkal. Gunakan judul konteks atau tautan balik tunggal; simpan *breadcrumb* hanya untuk taksonomi dalam (`≥ 3` level seperti dokumentasi besar, sistem berkas, atau katalog multi-kategori).
17. **Kapsul pill tagline dekoratif di atas H1 (`CMP-015`)** — badge mengambang `• SIGNAL PROTOCOL TCP • MULTI-DEVICE ... •` berbentuk kapsul pill oval (`rounded-full`) dengan peluru bullet `•` di atas judul utama. Ini adalah *tanda tangan utama template AI*. DILARANG KERAS. Jika konteks teknis atau kategori perlu ditampilkan, gunakan teks murni tanpa kapsul (eyebrow editorial kecil, huruf kapital berjarak, tanpa border, tanpa background pill terisolasi) atau integrasikan langsung ke dalam kalimat judul.
18. **Gimmick fiksi ilmiah & kanvas 3D palsu (`CMP-016`)** — menampilkan kanvas 3D partikel mengambang, kubus wireframe, atau istilah karangan (*"3D MESH TOPOLOGY // 60 FPS"*, *"Tembak Paket 3D ⚡"*, *"Chamber 01"*) pada produk backend, API gateway, atau infrastruktur pesan. Untuk produk developer/infrastruktur, artefak kerja hidup (**The Live Artifact**) **WAJIB berupa konsol operasional nyata**: live WebSocket stream dengan event asli (`messages.upsert`), status pairing WhatsApp QR nyata, latensi p95 faktual, dan blok kode cURL / REST SDK interaktif.
19. **Badge pemasaran tanpa fakta (`CMP-002`)** & **Polusi Emoji/Emoticon pada Antarmuka (`CMP-003`)** — menyusupkan karakter emoji Unicode (`🚀`, `✨`, `🔥`, `⚡`, `💡`, `🎉`, `⭐`, `✅`, `❌`, `⚠️`, `👉`, `💎`, `🌟`, `🤖`, `💬`, dll.) sebagai ikon tombol, prefix judul heading (`<h3>⚡ Performa</h3>`), ikon kartu fitur, peluru checklist (`<li>✅ 99.9%</li>`), badge hero, atau sel status tabel. Ini adalah *tanda tangan kemalasan AI paling mencolok* yang merusak line-height, pecah antar-OS (iOS vs Windows), dan merusak screen reader. DILARANG KERAS. Wajib gunakan ikon vektor SVG monokrom geometris terstandarisasi (`stroke="currentColor"` / `fill="currentColor"`) yang lulus *1-Bit Monochrome Test*.
20. **Radius seragam mengabaikan geometri bersarang (`CMP-004`)** — container dan anak memakai radius sama tanpa memperhitungkan padding konsentris.
21. **Elemen navigasi/kontrol mati (`CMP-005` / `CMP-012`)** — kotak cari, ikon lonceng, filter, atau tombol yang tidak melakukan apa-apa saat diklik.
22. **Label navigasi generik tanpa konteks domain (`CMP-010`)** — sidebar hanya menulis *Menu 1, Analytics, Reports* tanpa menyebut entitas bisnis sesungguhnya.
23. **Border neon saturated pada kartu (`CMP-018`)** — membungkus keliling kartu dengan garis border berwarna saturasi tinggi (`border-cyan-500`, `border-purple-500`, dsb.) dan glow menyala. DILARANG KERAS. Kontainer kartu wajib memakai hairline neutral border `1px solid var(--border)` (`oklch(1 0 0 / 0.08)` pada mode gelap). Warna aksen hanya untuk indikator titik aktif kecil.
24. **Radial glow blob di belakang kartu (`CMP-019`)** — memasang lingkaran blur besar (`blur-3xl bg-cyan-500/20`) di balik kartu untuk menciptakan kesan menyala palsu. Gantikan dengan *4-Level Surface Ladder* dan bayangan kontak transparan tipis.
25. **Telemetri & status teater palsu (`CMP-020`)** — menempelkan badge dekoratif fiktif (`// 60 FPS`, `• PING: 0.1ms`, `SYSTEM NORMAL`) tanpa sumber data riil. Wajib tampilkan telemetri operasional nyata dengan filter atau tindakan.

### B5. Gerak & Aksesibilitas
23. **Animasi properti layout (`ANI-002`)** — menganimasikan `width`, `height`, `top`, `left` yang memicu reflow; gunakan `transform` dan `opacity`.
24. **Mengabaikan `prefers-reduced-motion` (`ANI-003`)** atau **memutar media otomatis tanpa kendali (`ANI-005`)**.
25. **Pelanggaran aksesibilitas dasar (`A11Y-001..007`)** — kontrol tanpa nama aksesibel, input tanpa `<label>`, `:focus-visible` dihapus, atau target sentuh mobile `< 44x44px` (`LAY-004`).

### B6. Kunci Sistem Desain & Jebakan Tambal Sulam Redesign
26. **Kunci Token & Variabel Usang (`SYS-001`)** — mempertahankan token warna/spasi CSS lama (misal: slate generik `#3b82f6`, background `#f8fafc`, `--radius: 0.5rem`) saat pengguna meminta redesign, sehingga antarmuka baru tetap terkungkung estetika kusam lama. Wajib ganti di tingkat root (`globals.css` / theme) dengan OKLCH domain fisik.
27. **Kunci Pembungkus Shell & Layout (`SYS-002`)** — membiarkan kontainer root (`max-w-7xl mx-auto px-4`, hardcoded `bg-gray-50` di body) mencekik komposisi baru. Wajib rombak kontainer agar ritme spasial $2\times$ bernapas bebas.
28. **Kunci Komponen Primitif Zombie (`SYS-003`)** — tetap memakai wrapper `<Card>` atau `<Button>` lama yang memaksakan border pucat flat dan radius seragam tanpa formula konsentris. Wajib mutakhirkan primitif komponen ke standar interface engineering.
29. **Jebakan Redesign Tambal Sulam (`SYS-004`)** — hanya mengedit leaf JSX atau menambahkan inline overrides (`!important` / `style={{...}}`) di atas fondasi sistem desain yang rusak, menghasilkan UI yang "begitu-begitu saja".
30. **Tabrakan Styling Dua Sistem (`SYS-005`)** — menumpuk class styling baru tanpa menghapus CSS lama yang bertentangan, menyisakan kelas zombie dan layout glitch. Wajib lakukan *Clean Cutover* (hapus tuntas kode styling lama).

### B7. Pembunuh Kualitas Studio Kelas Dunia (Studio Score Killers)
31. **Dua Puluh Efek Tanpa Satu Momen Khas (`JURY-001`)** — menumpuk lusinan animasi mikro acak tanpa satu interaksi utama (*One Signature Moment*). Keriuhan efek terbaca oleh penilai sebagai rasa tidak percaya diri visual.
32. **Pembajakan Scroll / Scroll-Jacking Membeku (`JURY-002`)** — melawan inersia roda mouse, menonaktifkan tombol keyboard (`Space`/`PageDown`), atau mematikan inersia scroll alami di perangkat layar sentuh mobile.
33. **Kebocoran Memori GPU Akibat will-change Permanen (`JURY-003`)** — membiarkan `will-change: transform, opacity` aktif terus-menerus di CSS/JS alih-alih me-resetnya ke `auto` setelah animasi selesai, menghabiskan VRAM GPU mobile.
34. **Preloader Menutupi Konten yang Sudah Siap (`JURY-004`)** — memasang layar pembuka yang menahan pengguna selama 3–5 detik padahal konten HTML sudah siap di belakang layar, merusak metrik LCP.
35. **Desain Halaman Beranda Tunggal (`JURY-005`)** — halaman beranda dipoles mewah tetapi halaman dalam (tentang, detail, 404, dokumentasi) dibiarkan berantakan seperti proyek lain. Pengguna profesional selalu menguji halaman dalam.
---

## C. Ringkasan Kode Pemeriksaan Kontekstual

Gunakan kode referensi ini saat melaporkan hasil audit desain/kode secara presisi (`file:line` + ID + perbaikan konkret):

| Kategori | Rentang ID | Fokus Evaluasi Utama |
|---|---|---|
| Tipografi | `TYPO-001` .. `TYPO-009` | Hierarki skala peran, bebas gradien teks pelangi, bebas overflow mobile, `tabular-nums` |
| Warna | `CLR-001` .. `CLR-008` | Bebas gradien dekoratif klise, bebas neon glow berlebih, kroma latar tenang, `color-scheme` |
| Tata Letak | `LAY-001` .. `LAY-016` | Bebas tumpukan senter, bebas navbar obesitas mobile, bebas kebocoran scroll horizontal (`100vw`) |
| Komponen | `CMP-001` .. `CMP-020` | Bebas kapsul pill, bebas border neon kartu, bebas status teater palsu, radius konsentris |
| Gerak | `ANI-001` .. `ANI-007` | Hanya `transform`/`opacity`, durasi mikro `≤250ms`, hormati `prefers-reduced-motion` |
| Aksesibilitas | `A11Y-001` .. `A11Y-007` | Nama aksesibel, asosiasi `<label>`, indikator `:focus-visible`, urutan heading semantik |
| Kunci Desain & Redesign | `SYS-001` .. `SYS-005` | Deteksi pengunci sistem desain, hapus token kusam root, buka shell layout, clean cutover |
| Kualitas Studio & Juri | `JURY-001` .. `JURY-005` | Satu signature moment, bebas scroll-jacking, will-change cleanup, konsistensi halaman dalam |

---

## D. Evaluasi Kontekstual Sebelum Selesai

Sebelum menyerahkan karya teks atau antarmuka, uji tiga hal ini secara jujur:
1. **Uji Tukar Identitas**: Jika logo dan nama produk ditutupi, apakah struktur dan bahasanya masih mencerminkan domain spesifik produk ini, atau tampak seperti seribu template AI lainnya?
2. **Uji Pengurangan**: Adakah kartu, badge, pembungkus `<div>`, atau kalimat pengantar yang jika dihapus justru memperjelas tugas utama pengguna?
3. **Uji Kejujuran Fungsional**: Apakah setiap tombol, state kosong/gagal, dan angka yang tampil di layar benar-benar bekerja dan jujur?
