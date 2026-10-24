# Discovery Protocol

Dipakai pada Wave 0 untuk permintaan yang belum jelas hasil akhirnya: fitur baru, produk baru, redesign, atau brief satu baris. Tujuan: mengubah permintaan kabur menjadi hasil yang bisa dieksekusi tanpa menebak.

Protokol ini **tidak** dipakai untuk tugas yang hasilnya sudah jelas (perbaikan bug dengan stack trace, rename simbol, tambah validasi field). Untuk tugas seperti itu, langsung kerjakan.

---

## 1. Prinsip

1. **Satu pertanyaan per giliran.** Daftar 8 pertanyaan sekaligus membuat pengguna berhenti menjawab.
2. **Tanya hanya yang mengubah keputusan.** Jika jawabannya tidak mengubah file, arsitektur, atau copy yang dihasilkan, jangan tanya.
3. **Cek dulu, tanya kemudian.** Konteks yang bisa dibaca dari repo (stack, konvensi, entitas, bahasa) tidak perlu ditanyakan.
4. **Asumsi boleh, asal ditandai.** Jika pengguna menyerahkan keputusan, ambil asumsi minimum, tandai `[ASUMSI]`, lanjutkan.
5. **Berhenti saat cukup.** Discovery selesai ketika 4 hal di bawah terisi, bukan ketika semua pertanyaan habis.

## 2. Empat Hal yang Harus Terisi

| Elemen | Pertanyaan inti | Contoh jawaban yang cukup |
|---|---|---|
| **Outcome** | Apa yang berubah bagi pengguna setelah ini ada? | "Staf klinik bisa melihat jadwal hari ini tanpa menelepon" |
| **Batasan** | Apa yang tidak boleh dilanggar? | Stack existing, deadline, integrasi wajib, bahasa UI |
| **Non-goals** | Apa yang sengaja tidak dibangun? | "Tanpa pembayaran, tanpa multi-bahasa" |
| **Kriteria selesai** | Bagaimana kita tahu ini berhasil? | "Booking selesai <3 klik, tanpa reload" |

Jika salah satu kosong dan tidak bisa diinferensi dari repo, tanyakan. Selain itu, lanjutkan.

## 3. Urutan Pertanyaan

Ajukan berurutan, lewati yang sudah terjawab:

1. **Siapa penggunanya, dan apa tugas konkret mereka di layar ini?**
   Hindari "semua orang". Jawaban "semua orang" = belum dijawab.
2. **Apa yang mereka lakukan sekarang tanpa ini?**
   Menjawab ini memisahkan fitur yang dibutuhkan dari fitur yang hanya terdengar bagus.
3. **Apa yang paling tidak boleh salah?**
   Menentukan di mana effort desain dan verifikasi diarahkan.
4. **Apa yang jelas tidak termasuk?**
   Non-goals mencegah scope creep lebih efektif daripada daftar fitur.
5. **Ada referensi, brand, atau konvensi yang harus diikuti?**
   Jika tidak ada, nyatakan arah sebagai draft dan lanjut.

## 4. Dari Jawaban ke Keputusan

Setelah empat elemen terisi:

1. **Rumuskan satu baris tujuan** — dipakai sebagai target aktif di HUD.
2. **Pilih 2–3 pendekatan** yang benar-benar berbeda (bukan variasi kosmetik).
3. **Sebutkan trade-off tiap pendekatan** dalam satu baris masing-masing: biaya, risiko, waktu.
4. **Rekomendasikan satu**, dengan alasan konkret. Jangan menyerahkan pilihan tanpa opini.
5. **Konfirmasi hanya jika keputusan mahal untuk dibalik.** Jika murah, ambil rekomendasi dan kerjakan.

## 5. Format Output Discovery

```
🎯 [FOKUS]: <outcome satu baris>
📌 [BATASAN]: <stack / integrasi / deadline>
🚫 [NON-GOALS]: <yang tidak dibangun>
✅ [SELESAI JIKA]: <kriteria terukur>
[ASUMSI]: <asumsi yang diambil, jika ada>
```

Ringkas. Ini bukan dokumen; ini kontrak kerja yang muat di layar.

## 6. Anti-Pattern Discovery

| Dilarang | Alasan | Ganti dengan |
|---|---|---|
| 8 pertanyaan sekaligus | Pengguna berhenti menjawab | Satu pertanyaan, pilih yang paling memblokir |
| "Bisa jelaskan lebih detail?" | Tidak terarah | "Siapa yang memakai layar ini setiap hari?" |
| Menanyakan stack yang terlihat di `package.json` | Membuang giliran | Baca repo, konfirmasi satu baris |
| Menunggu brief sempurna | Menunda tanpa hasil | Asumsi bertanda, lalu kerjakan |
| "Terserah Anda" | Menghindari tanggung jawab | Rekomendasikan satu opsi dengan alasan |

## 7. Kapan Berhenti

Berhenti bertanya ketika:

- Empat elemen §2 terisi, atau
- Pengguna secara eksplisit menyerahkan keputusan, atau
- Dua pertanyaan berturut-turut tidak mengubah rencana.

Setelah itu masuk ke routing spesialis. Discovery bukan tahap desain.


---

## 8. Contoh Interaksi Discovery

### Skenario: "Buat fitur booking"

**User**: Buat fitur booking untuk klinik gigi.

**Orchestrator** (Wave 0):
> 🎯 [FOKUS]: ?
> 
> Sebelum mulai, saya perlu satu hal: siapa yang menggunakan fitur booking ini?
> - Pasien yang booking sendiri?
> - Staf resepsionis yang booking untuk pasien?
> - Keduanya?

**User**: Pasien booking sendiri via web.

**Orchestrator**:
> 📌 [BATASAN]: ?
> 
> Stack apa yang dipakai? Saya lihat `package.json` ada Next.js + Prisma. Konfirmasi: pakai stack itu, atau ada constraint lain (deadline, integrasi wajib)?

**User**: Ya Next.js + Prisma. Deadline 2 minggu. Harus integrate dengan Google Calendar.

**Orchestrator**:
> 🚫 [NON-GOALS]: ?
> 
> Apa yang TIDAK termasuk? Misalnya: payment, reminder email, multi-practitioner, admin dashboard?

**User**: Tanpa payment dulu. Reminder email nanti fase 2. Single practitioner saja.

**Orchestrator**:
> ✅ [SELESAI JIKA]: Pasien bisa pilih slot tersedia → konfirmasi booking → booking muncul di Google Calendar. <3 klik dari halaman booking ke konfirmasi.
> 
> 🎯 [FOKUS]: Self-service booking untuk pasien klinik gigi
> 📌 [BATASAN]: Next.js + Prisma, Google Calendar API, deadline 2 minggu
> 🚫 [NON-GOALS]: Payment, reminder email, multi-practitioner, admin dashboard
> ✅ [SELESAI JIKA]: Booking selesai <3 klik, sync ke Google Calendar
> 
> Lanjut ke Wave 1: `maxilun-architect` (data model + API contract) + `maxilun-craft` (booking UI flow).

Discovery selesai dalam 3 giliran. Empat elemen terisi. Tidak ada pertanyaan tentang warna, font, atau detail implementasi — itu domain specialist.
