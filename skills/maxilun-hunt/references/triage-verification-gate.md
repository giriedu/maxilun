# Triage & Verification Gate: Proof-Driven Finding Validation

Protokol validasi temuan keamanan tanpa celah spekulasi. Temuan yang tidak dapat dibuktikan secara independen wajib digugurkan sebelum diajukan ke laporan.

---

## 1. The 7-Question Gate

Setiap temuan wajib dievaluasi berurutan melalui 7 pertanyaan gerbang. **Satu jawaban gagal = temuan digugurkan (KILL) seketika.**

```text
[Q1: Eksekusi Langsung?]  ──(Gagal)──> [GUGURKAN: Tidak dapat direproduksi]
         │ (Lulus)
[Q2: Dampak Nyata?]       ──(Gagal)──> [GUGURKAN: Di luar kriteria dampak]
         │ (Lulus)
[Q3: Aset In-Scope?]      ──(Gagal)──> [GUGURKAN: Di luar batasan target]
         │ (Lulus)
[Q4: Hak Akses Realistis?]──(Gagal)──> [GUGURKAN: Risiko sentralisasi / admin only]
         │ (Lulus)
[Q5: Bukan Perilaku Intended?] (Gagal)─> [GUGURKAN: Desain yang disengaja]
         │ (Lulus)
[Q6: Bukti Melampaui Teori?] (Gagal)──> [TURUNKAN DERAJAT KEPARAHAN / DOWNGRADE]
         │ (Lulus)
[Q7: Bebas Daftar Hitam?] ──(Gagal)──> [GUGURKAN: Masuk daftar Never-Submit]
         │ (Lulus)
     [TEMUAN VALID]
```

### Rincian Gerbang Evaluasi

1. **Q1: Dapatkah penyerang mengeksekusinya SEKARANG langkah-demi-langkah?**
   - Format wajib: Request HTTP lengkap (metode, URL, headers, body) yang siap di-curl ulang.
   - Jika tidak dapat menuliskan request yang menghasilkan pembuktian langsung -> **GUGURKAN**.
2. **Q2: Apakah dampaknya berada dalam daftar dampak yang diakui program/organisasi?**
   - Kerentanan harus menimbulkan kerugian nyata: pencurian data privat, perubahan data tanpa izin, pengambilalihan akun (ATO), atau eksekusi kode (RCE).
   - Jika dampak hanya berupa informasi publik atau pengecualian yang didokumentasikan -> **GUGURKAN**.
3. **Q3: Apakah akar penyebab berada pada aset in-scope?**
   - Pastikan domain/host tercantum eksplisit dalam daftar cakupan.
   - Jika domain milik pihak ketiga (SaaS, identity provider eksternal) -> **GUGURKAN**.
4. **Q4: Apakah penyerang memerlukan hak akses tidak realistis?**
   - Aksi yang hanya bisa dilakukan oleh administrator utama (*Admin can do X*) adalah risiko sentralisasi wewenang, bukan celah keamanan -> **GUGURKAN**.
   - Hak akses yang sah: pengguna biasa melakukan aksi admin (*privilege escalation*), atau pengguna A mengakses data pengguna B.
5. **Q5: Apakah perilaku ini sudah diketahui atau disengaja oleh desain sistem?**
   - Periksa dokumentasi resmi produk, release notes, atau isu publik terdahulu.
   - Jika perilaku tersebut merupakan fitur yang disengaja -> **GUGURKAN**.
6. **Q6: Dapatkah Anda membuktikan dampak nyata melebihi indikasi "secara teknis memungkinkan"?**
   - SSRF: Wajib mengembalikan payload data dari layanan internal, bukan hanya callback ping DNS.
   - SQLi: Wajib mengekstrak data dari tabel nyata atau mendemonstrasikan delay waktu terukur, bukan sekadar memicu pesan error 500.
   - Jika hanya bisa membuktikan kemungkinan teoritis -> **TURUNKAN DERAJAT (DOWNGRADE)**.
7. **Q7: Apakah temuan ini masuk dalam daftar kelas yang ditolak otomatis (*Never-Submit*)?**
   - Periksa tabel Never-Submit di bawah. Jika cocok dan berdiri sendiri tanpa rantai eksploitasi -> **GUGURKAN**.

---

## 2. Tabel Never-Submit (Eliminasi False-Positive Otomatis)

Temuan pada tabel berikut dilarang dilaporkan secara mandiri karena tidak membuktikan risiko eksploitasi nyata:

| Indikasi Awal | Alasan Pengguguran Mutlak | Syarat Pengecualian (Wajib Rantai Eksploitasi) |
|---|---|---|
| **CORS Wildcard / Reflected** | Tanpa `Access-Control-Allow-Credentials: true`, data sesi korban tidak dapat diekstraksi ke domain penyerang | Terbukti berhasil mengekstrak data PII terautentikasi melalui kredensial sesi |
| **Nuclei / Scanner Info Banner** | Deteksi versi framework atau web server bukan bukti kerentanan (*version banner disclosure*) | Terdapat CVE aktif dengan eksploit terbukti pada versi tersebut |
| **SSRF DNS Callback Saja** | Interaksi DNS OOB seringkali dipicu oleh proxy perantara atau web filter, bukan backend target | Respon memuat data layanan metadata cloud atau port internal privat |
| **Self-XSS** | Penyerang hanya mengeksekusi script pada browser mereka sendiri | Terangkai dengan celah CSRF pada endpoint yang menyuntikkan payload ke korban |
| **Absen HTTP Security Headers** | Absennya CSP, HSTS, atau X-Frame-Options bukan kerentanan aktif tanpa skenario serangan | Clickjacking terbukti berhasil memicu transaksi tanpa interaksi sadar pengguna |
| **Open Redirect Tanpa Rantai** | Pengalihan URL semata dinilai rendah oleh sebagian besar program | Terangkai dengan kebocoran token OAuth `redirect_uri` atau Account Takeover |
| **Logout CSRF** | Memaksa korban keluar dari sesi tidak memberikan keuntungan akses kepada penyerang | Tidak ada pengecualian (selalu digugurkan) |
| **Rate Limiting Absen** | Halaman statis atau pencarian umum tanpa batasan laju bukan kerentanan | Endpoint login/OTP rentan *credential stuffing* atau mutasi finansial ganda |

---

## 3. Mesin Verifikasi Deterministik (The Verification Spine)

Penilaian laporan dikendalikan oleh mesin status empat nilai yang menolak klaim tanpa bukti:

```text
               ┌───────────────────────┐
               │    Evaluasi Temuan    │
               └───────────┬───────────┘
                           │
             Ada Paket Bukti Lengkap?
              ├── TIDAK ──────────────────────────────> [UNPROVEN] (Ditekan)
              └── YA
                   │
            Jalankan Re-Derivasi Ulang
              ├── Gagal koneksi / Metode mutasi tidak diuji -> [INCONCLUSIVE] (Ditahan)
              ├── Penanda kerentanan HILANG dari respon fresh -> [REFUTED] (Ditekan)
              └── Penanda kerentanan DITEMUKAN di respon fresh -> [PROVEN] (DAPAT DILAPORKAN)
```

### Definisi Status Keputusan

- **`PROVEN` (Terbukti)**:
  - Memiliki bukti pertukaran HTTP baseline yang lengkap.
  - Re-derivasi independen berhasil dijalankan dan penanda bukti (*confirmation marker*) muncul kembali pada respon segar.
  - **Satu-satunya status yang diizinkan untuk dibuatkan laporan final.**
- **`REFUTED` (Tersanggah)**:
  - Re-derivasi berhasil mengirim request, namun penanda kerentanan tidak ditemukan pada respon segar (misal: endpoint sudah diproteksi atau mengembalikan 403).
  - Status: Ditekan (tidak dilaporkan).
- **`UNPROVEN` (Belum Terbukti)**:
  - Tidak memiliki paket bukti request/response, atau penanda kerentanan tidak terdefinisi secara terukur.
  - Status: Ditekan (tidak dilaporkan).
- **`INCONCLUSIVE` (Tidak Konklusif)**:
  - Re-derivasi tidak dapat diselesaikan (target tidak terjangkau, kredensial hilang, atau request mutasi berbahaya dihentikan demi keselamatan).
  - Status: Ditahan dalam antrean evaluasi lanjutan, dilarang dilaporkan.

---

## 4. Matriks Keparahan CVSS 3.1 & Pengambilan Keputusan

Gunakan standar CVSS 3.1 berbasis vektor terukur, bukan perkiraan subjektif:

| Tingkat Keparahan | Nilai CVSS | Karakteristik Bukti Wajib | Contoh Kelas |
|---|---|---|---|
| **Critical** | 9.0 – 10.0 | Tanpa interaksi pengguna, akses penuh dari jarak jauh, ATO massal | RCE, SQLi exfiltrasi data penuh, Auth Bypass admin |
| **High** | 7.0 – 8.9 | Akses baca/tulis data privat lintas tenant, eskalasi hak akses terbukti | IDOR dengan mutasi data, SSRF ke metadata cloud, Stored XSS |
| **Medium** | 4.0 – 6.9 | Akses baca data terbatas, membutuhkan interaksi pengguna spesifik | IDOR data non-sensitif, Reflected XSS dengan klik korban |
| **Low** | 0.1 – 3.9 | Kebutuhan prasyarat tinggi, dampak informasi terbatas | Open redirect minor, Clickjacking halaman informasi |
| **Informational** | 0.0 | Observasi arsitektur tanpa skenario eksploitasi | Version banner, error debug tanpa kredensial |
