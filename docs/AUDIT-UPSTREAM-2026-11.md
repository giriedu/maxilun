# Audit & Sintesis: 13 Repositori Eksternal (November 2026)

Audit 13 repositori open-source dan sintesis prinsip rekayasanya ke referensi original Maxilun. Metode: **clean-room**. Setiap repo dibaca untuk memahami tekniknya, lalu referensi Maxilun ditulis ulang dengan kalimat, contoh, dan kode sendiri. Tidak ada prosa, kode, template, dataset, gambar, atau aset upstream yang disalin ke `skills/`.

---

## 1. Batas Hukum

- Ide, teknik, dan prinsip rekayasa tidak dilindungi hak cipta; ekspresinya (teks, kode, dataset) dilindungi. Karena itu Maxilun hanya mengambil prinsip, lalu menulis ulang ekspresinya.
- Kode upstream **tidak** di-vendor dan **tidak** dilisensikan ulang. Jika suatu saat kode upstream ingin disertakan apa adanya, lisensi MIT/Apache-2.0 mewajibkan notis hak cipta asli tetap ada (Apache-2.0 juga mewajibkan `NOTICE` dan penanda perubahan). Kode seperti itu tidak bisa diklaim original Maxilun dan tidak bisa dilisensikan ulang di bawah Maxilun Free-to-Use.
- Dua repo memakai lisensi non-OSI yang lebih ketat (`app-store-compliance`: OpenRoots ORA 2.3, `transitions.dev`: lisensi kustom). Dari keduanya hanya diambil fakta kebijakan publik dan prinsip umum.
- Pemeriksaan tumpang-tindih: setiap referensi baru dibandingkan dengan seluruh berkas teks repo sumbernya memakai 10-gram kata. Kalimat prosa yang sama ditulis ulang. Sisa kecocokan hanya pada sintaks teknis generik, yaitu flag `ffmpeg`/x264 dan markup ARIA/SVG standar.

## 2. Ringkasan Lisensi & Pemetaan

| Repo | Lisensi | Referensi Maxilun | Pemilik |
|---|---|---|---|
| `zhouxiaoka/autoclip` | MIT, (c) 2024 AutoClip Team | `skills/maxilun-cinecode/references/auto-clip-pipeline.md` | `maxilun-cinecode` |
| `heygen-com/hyperframes` | Apache-2.0, (c) 2026 HeyGen, Inc. | `skills/maxilun-cinecode/references/html-frame-rendering.md` | `maxilun-cinecode` |
| `cathrynlavery/diagram-design` | MIT, (c) 2025 Cathryn Lavery | `skills/maxilun-diagrams/references/editorial-svg-diagrams.md` | `maxilun-diagrams` |
| `mjmirza/app-store-compliance` | OpenRoots ORA 2.3 (non-OSI; AI training butuh lisensi Compute) | `skills/maxilun-mobile/references/store-review-compliance.md` | `maxilun-mobile` |
| `plugin87/ux-ui-agent-skills` | MIT, (c) 2026 Thientan Soparat | `skills/maxilun-craft/references/measured-design-gates.md` | `maxilun-craft` |
| `Ormus-Solutions/LibreUIUX-Claude-Code` | MIT, (c) 2025-2026 Hermetic Ormus; (c) 2024 Seth Hobson | `skills/maxilun-craft/references/uiux-workflow-hooks.md` | `maxilun-craft` |
| `Jakubantalik/thinking-orbs` | MIT, (c) 2026 Jakub Antalik | `skills/maxilun-motion/references/agent-state-indicators.md` | `maxilun-motion` |
| `Jakubantalik/transitions.dev` | Kustom non-OSI (larangan redistribusi sebagai library), (c) 2026 Jakub Antalik | `skills/maxilun-motion/references/css-transition-recipes.md` | `maxilun-motion` |
| `standardagents/arrow-js` | MIT, (c) 2022 Justin Schroeder | `skills/maxilun-frontend/references/lightweight-reactive-islands.md` | `maxilun-frontend` |
| `farion1231/cc-switch` | MIT, (c) 2025 Jason Young | `skills/maxilun-desktop/references/config-manager-patterns.md` | `maxilun-desktop` |
| `affaan-m/ECC` | MIT, (c) 2026 Affaan Mustafa | `skills/maxilun/references/harness-hooks-memory.md` | `maxilun` |
| `deepseek-ai/deepseek-harness` | MIT, (c) 2026 DeepSeek | `skills/maxilun/references/plugin-harness-architecture.md` | `maxilun` |
| `ruvnet/ruflo` | MIT, (c) 2024-2026 ruvnet | `skills/maxilun/references/swarm-coordination.md` | `maxilun` |

`uiux-workflow-hooks.md` juga memakai desain receipt ber-hash dan pemeriksaan akhir giliran dari `ux-ui-agent-skills`.

---

## 3. Temuan per Repositori

### 3.1 autoclip → `auto-clip-pipeline.md`
- **Diadopsi**: output tiap tahap disimpan, dan respons model yang di-cache diputar ulang lewat validator yang sama. Satu profil durasi berdasarkan panjang sumber. Batas klip di-snap ke akhir kalimat, dengan jeda diam dihitung sebagai akhir kalimat. Satu tabel platform. Caption maksimal dua baris. Biaya dibatasi per chunk dan per job. QA output: loudness sekitar -14 LUFS / -1 dBTP dan sinkronisasi A/V.
- **Ditolak**: lima versi `title_art` hidup berdampingan → satu pemilik per kapabilitas. Durasi di-hardcode di prompt lalu ditambal blok override → satu objek profil. Urutan fallback provider berdasarkan sponsor → urutan berdasarkan bukti kapabilitas dan biaya.
- **Risiko**: Sentry aktif kecuali pengguna opt-out. OpenCV di-`pip install` saat runtime.

### 3.2 hyperframes → `html-frame-rendering.md`
- **Diadopsi**: model seek-not-play dengan waktu rasional. Virtualisasi waktu (`Date`, `performance.now`, rAF, timer). Gerbang kesiapan untuk font, gambar, dan media. Video sumber didekode di luar halaman. Encode: padding untuk dimensi ganjil, range BT.709 limited. Uji determinisme: frame identik antar-run dan antar-jumlah worker.
- **Ditolak**: renderer HTML kedua di samping Remotion → CineCode tetap memakai Remotion dan hanya meminjam model seek. Library dimuat dari CDN saat render → di-vendor dan di-pin. Telemetri aktif secara default. Berkas 3000-6000 baris.
- **Risiko**: telemetri CLI (opt-out). Dokumentasinya memuat installer `curl|bash` untuk CLI pihak ketiga. GSAP dimuat dari CDN tanpa SRI.

### 3.3 diagram-design → `editorial-svg-diagrams.md`
- **Diadopsi**: jenis diagram dipilih dari pertanyaan pembaca. Anggaran kepadatan dengan maksimal dua elemen yang ditonjolkan. Tata letak dihitung pada grid 4/8px. Warna semantik lewat CSS variable. Konektor ortogonal. SVG aksesibel (`role="img"`, `aria-labelledby`). Satu berkas self-contained.
- **Ditolak**: 50+ jenis diagram dan SKILL.md sekitar 33 KB → disiplin ukuran. Google Fonts di berkas yang disebut "self-contained" → system font stack. Wawancara branding yang memblokir di awal. Checklist selera yang dicentang sendiri → probe geometri headless.

### 3.4 app-store-compliance → `store-review-compliance.md`
- **Diadopsi**, hanya dari fakta kebijakan publik Apple/Google: yang diperiksa adalah artefak build, bukan hanya source. Deklarasi di store harus sesuai perilaku aplikasi ke dua arah. Satu inventaris data menjadi sumber privacy manifest, purpose string, Data safety, dan label privasi. Setiap kelas penolakan dijadikan gate yang bisa dicek mesin. Gate dijalankan per PR, per release, dan mingguan.
- **Ditolak**: korpus aturan sekitar 2000 baris. Hook yang memblokir shell. Klaim kebijakan masa depan yang spekulatif. Heuristik grep yang dilaporkan sebagai pass/fail.
- **Risiko**: lisensi membatasi AI training, jadi tidak ada teks, ID aturan, atau skrip yang dipakai.

### 3.5 ux-ui-agent-skills → `measured-design-gates.md`
- **Diadopsi**: gate punya tiga hasil (pass / fail / tidak terukur), dan "tidak terukur" tidak pernah dianggap lulus. Receipt pengukuran terikat SHA-256 berkas. Kontras diukur terhadap latar yang benar-benar terlihat setelah komposit. Warna harus sesuai makna aksi. Kontrol yang mengklaim state harus benar-benar berubah. Overflow diuji dengan konten panjang. Mobile-first dibuktikan dengan menghapus media query lalu merender di 320px. Sensus token.
- **Ditolak**: perpustakaan 2.144 design system merek pihak ketiga (juga ada risiko merek dagang). Gate lulus default saat browser tidak ada → `[UNVERIFIED]`. Aturan "radius seragam itu buruk" bertentangan dengan pilihan radius tunggal Maxilun.

### 3.6 LibreUIUX-Claude-Code → `uiux-workflow-hooks.md`
- **Diadopsi**: setiap pemeriksaan craft dipetakan ke event hook (session start, pre-edit blast radius, post-edit scan berkas yang berubah). Hook diam kalau tidak ada masalah. Jadwal review empat tingkat.
- **Ditolak**: framing arketipe Jung/Tarot dan persona "master". Ikon emoji (`CMP-003`). Cek kontras berbasis regex. 73 plugin yang sebagian besar bukan UI. Hook bash+jq yang `exit 0` diam-diam kalau jq tidak ada.

### 3.7 thinking-orbs → `agent-state-indicators.md`
- **Diadopsi**: geometri sebagai fungsi murni waktu yang menghasilkan draw list. Satu jam bersama. Animasi berhenti saat offscreen atau tab tersembunyi. DPR dibatasi 2. Tiap ukuran disetel terpisah. Tanpa `ctx.filter`.
- **Ditolak**: sembilan state dekoratif yang tidak terhubung ke event backend → 3-5 state yang dipetakan ke event nyata. Canvas `role="img"` tanpa live region → `role="status"`. Satu rAF per instance → satu ticker bersama.

### 3.8 transitions.dev → `css-transition-recipes.md`
- **Diadopsi**: resep dipilih dari jenis perubahan. Swap bertumpuk di satu sel grid. Pop-in hanya untuk digit yang berubah. Morph prefix/suffix untuk label yang mirip. Exit lebih cepat dari entry. Ditambah ekstensi Maxilun dengan API native: `linear()`, `interpolate-size`, View Transitions, `@starting-style`.
- **Ditolak**: reduced motion sebagai `transition: none !important`. Urutan animasi lewat `setTimeout`. Spring dipalsukan dengan 20+ keyframe. `will-change: width, height`. Status "thinking" yang berputar dengan timer.
- **Risiko**: lisensi kustom non-OSI, jadi tidak ada snippet yang disalin. Situsnya memuat analytics pihak ketiga.

### 3.9 arrow-js → `lightweight-reactive-islands.md`
- **Diadopsi**: gerbang keputusan kapan runtime tanpa build lebih tepat daripada React/Next. Mekanika reaktivitas granular. Rendering yang escape secara konstruksi. Tabel sink XSS yang tidak tercakup. Cleanup per owner. UI hasil generate agen dijalankan di sandbox.
- **Ditolak**: binding `.innerHTML` dan `href` tanpa validasi skema URL → gate XSS. Import CDN tanpa pin → pin, SRI, dan CSP. Model komponen kedua di samping React.

### 3.10 cc-switch → `config-manager-patterns.md`
- **Diadopsi**: klasifikasi kepemilikan key. Patcher per format yang mempertahankan komentar. Atomic write dengan backup pada tulisan pertama. Jurnal multi-berkas untuk pemulihan crash. Deteksi penulis eksternal lewat hash. Keychain OS. Hardening restore SQLite. Update yang ditandatangani.
- **Ditolak**: capability Tauri yang tidak mencakup command aplikasi. YAML ditulis ulang sehingga komentar hilang. Sekitar 350 command dalam satu crate dan berkas sekitar 10k baris. Path ekspor diambil dari webview.
- **Risiko `[CONFIRMED]`**: sinkronisasi cloud mengunggah `db.sql` beserta API key provider tanpa enkripsi sisi klien. Password WebDAV dan secret S3 disimpan plaintext di `settings.json`. Command aplikasi bisa dipanggil dari webview mana pun.

### 3.11 ECC → `harness-hooks-memory.md`
- **Diadopsi**: setiap aturan ditempatkan di lapisan yang tepat (prosa, hook pre-tool, batch saat Stop, CI). Disiplin hook: timeout, stdin dibatasi, fail-closed atau fail-open sesuai jenis hook. Gerbang fakta sebelum edit pertama. Anggaran konteks dihitung dari token nyata. Memori dua lapis (checkpoint dan lesson) dengan decay. Urutan prioritas aturan.
- **Ditolak**: ratusan skill sempit yang diduplikasi per platform → 24 pemilik kohesif. Instinct yang otomatis berubah jadi skill baru. Hook yang mengomel di setiap pemanggilan. Klaim efektivitas yang belum direproduksi.
- **Risiko**: hook menjalankan Node/Python di setiap tool call dengan one-liner `node -e` besar yang sulit diaudit.

### 3.12 deepseek-harness → `plugin-harness-architecture.md`
- **Diadopsi**: tidak ada core yang diistimewakan. Setiap registrasi adalah efek yang bisa dibatalkan lewat disposer. Seam punya tiga peran. Event bus tiga domain. Pipeline tool: dicatat sebelum dijalankan, guard hanya boleh memperketat, approval fail-closed. Kontrak adapter provider. Compaction dengan marker yang tercatat di log.
- **Ditolak**: ratusan paket kecil. Katalog yang di-generate dijadikan panduan utama. Hook deprecated tetap hidup. Preset akses penuh tanpa approval.
- **Risiko**: proyek menyatakan dirinya belum diaudit keamanannya. Sandbox parsial di Windows. Ada plugin telemetri OTLP (opt-in).

### 3.13 ruflo → `swarm-coordination.md`
- **Diadopsi**: topologi dipilih dari otoritas dan tumpang-tindih write set. Lock lintas proses dengan atomic rename. Klaim sebagai lease compare-and-set. Satu penulis per worktree. Circuit breaker 3/5. Anggaran biaya ditegakkan di titik spawn. Voting dengan roster tetap.
- **Ditolak**: swarm 6-8 agen sebagai default. Istilah Raft/BFT/CRDT untuk logika single-process. CLAUDE.md 1.562 baris. Emoji di output. `npx @latest` di setiap pemanggilan.
- **Tidak terverifikasi di kode**: konsensus Raft/BFT (default-nya EventEmitter in-process), "89% routing accuracy", "self-learning".
- **Risiko**: installer `curl ... | bash` dari branch `main` tanpa pin. `claim()` di level library rawan race.

---

## 4. Status Integrasi & Verifikasi

- 13 referensi baru (145-268 baris), terdaftar di `metadata.references` pada `SKILL.md` pemiliknya dan di `references/index.md` jika ada. Untuk `maxilun`, `maxilun-craft`, dan `maxilun-desktop` juga ditambahkan pointer di badan SKILL.md.
- Tidak ada nama, penulis, atau URL upstream di dalam `skills/`. Atribusi hanya ada di dokumen ini.
- `python scripts/test-suite.py`: semua suite lulus.
