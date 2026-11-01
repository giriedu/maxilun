<!-- metadata:
  version: "1.0.0"
  ecosystem: "maxilun"
  last_updated: "2026-11-01"
  source: "Maxilun Architecture (diselaraskan dari observasi rekayasa LLM Andrej Karpathy)"
-->

# Maxilun Surgical Engineering Discipline
# (Disiplin Rekayasa Bedah Maxilun)

Disiplin operasional untuk menekan kegagalan laten model AI (LLM) saat menulis, mengaudit, dan merefaktor kode produksi. Mengintegrasikan prinsip rekayasa presisi tinggi ke dalam empat engine utama Maxilun (**Focus, Purity, Minimalist, Clarity**).

**Trade-off dasar:** Disiplin ini memprioritaskan kehati-hatian (*caution*) dan presisi di atas kecepatan sesaat (*speed*). Untuk tugas trivial (perbaikan typo teks, string tunggal terisolasi), gunakan pertimbangan praktis tanpa memaksakan seluruh seremoni.

---

## 4 Titik Rawan Rekayasa AI (The 4 Pitfalls)

1. **Wrong Assumptions & Hidden Confusion**: Model membuat asumsi sepihak tanpa konfirmasi, menyembunyikan kebingungan, tidak meminta klarifikasi, dan memilih cabang implementasi yang berisiko secara diam-diam.
2. **Overcomplication & Bloated Abstractions**: Model cenderung merancang kode berlebihan (*overengineering*), menciptakan abstraksi prematur untuk komponen sekali pakai, dan menulis ratusan baris saat puluhan baris sudah cukup.
3. **Collateral & Orthogonal Damage**: Model mengubah indentasi, merombak komentar sekitar, atau melakukan pembersihan formatting liar (*drive-by refactoring*) pada area yang tidak diminta.
4. **Weak Success Criteria**: Model berhenti tanpa bukti eksekusi nyata karena bekerja berdasarkan perintah imperatif yang kabur alih-alih kriteria sukses yang dapat diuji.

---

## 4 Pilar Disiplin Rekayasa Bedah

| Pilar | Fokus Masalah | Integrasi Engine Maxilun |
|---|---|---|
| **1. Pre-flight Reasoning** | Asumsi salah, kebingungan tersembunyi, trade-off hilang | **Clarity Engine & Proactive Communication** |
| **2. Radical Simplicity** | Overengineering, abstraksi bengkak, konfigurasi spekulatif | **Minimalist Engineering & Purity Engine** |
| **3. Surgical Precision** | Modifikasi orthogonal, perbaikan liar (*drive-by refactoring*) | **Purity Engine & Code Hygiene** |
| **4. Verifiable Goal Loop** | Klaim selesai tanpa bukti, ketiadaan verifikasi | **Focus Engine & Verify Gate** |

---

## 1. Pre-flight Reasoning (Pikir Sebelum Koding)

**Jangan berasumsi sepihak. Jangan sembunyikan kebingungan. Paparkan trade-off.**

Sebelum memodifikasi kode atau merancang perubahan struktur:
- **Nyatakan asumsi secara eksplisit**: Jika konteks memiliki ambiguitas, tanyakan kepada pengguna atau beri penanda `[ASUMSI]` yang transparan daripada menebak diam-diam.
- **Paparkan beberapa interpretasi**: Jika instruksi memiliki lebih dari satu arti teknis, tampilkan opsi dan trade-off masing-masing — jangan memilih satu cabang secara rahasia.
- **Ajukan alternatif lebih sederhana**: Jika pendekatan yang diminta pengguna terlalu rumit atau ada solusi native/stdlib yang jauh lebih bersih, sampaikan alternatif tersebut dengan bukti.
- **Berhenti saat membingungkan**: Sebutkan bagian yang kabur dan ajukan satu pertanyaan terarah yang menentukan langkah berikutnya.

### Contoh Kasus

**Permintaan:** *"Buat pencarian data lebih cepat."*

❌ **Pelanggaran Disiplin (Memilih Diam-diam Tanpa Konfirmasi):**
Langsung menginstal Redis cache, membuat index database, dan menulis async background worker (~200 baris) tanpa verifikasi letak bottleneck nyata.

✅ **Penerapan Benar (Pre-flight Reasoning):**
```markdown
Pencarian lebih cepat dapat berarti beberapa hal:
1. Menurunkan latensi query (optimasi index atau seleksi kolom minimal).
2. Menangani konkurensi lebih tinggi (connection pooling atau worker terpisah).
3. Meningkatkan persepsi kecepatan (debouncing UI atau skeleton state).

Profil saat ini: query memakan waktu ~450ms akibat full table scan pada kolom `email`.
Rekomendasi: tambahkan index pada `users(email)`. Apakah ini yang diinginkan?
```

---

## 2. Radical Simplicity (Kesederhanaan Radikal)

**Kode minimal yang menuntaskan masalah. Tolak konstruksi spekulatif.**

- **Hanya fitur yang diminta**: Dilarang menambah fungsionalitas ekstra "untuk jaga-jaga masa depan".
- **Tanpa abstraksi untuk kode sekali pakai**: Jangan membuat interface, factory, atau strategy pattern jika hanya ada 1 implementasi nyata (*no single-use abstractions*).
- **Tanpa konfigurabilitas spekulatif**: Hindari opsi parameter atau flags yang tidak diminta.
- **Tanpa error handling skenario mustahil**: Jangan menangani error yang secara struktural mustahil terjadi pada alur yang dibangun.
- **Aturan 200 ke 50 baris**: Jika solusi ditulis sepanjang 200 baris padahal bisa diselesaikan dalam 50 baris bersih, tulis ulang (*rewrite*).
- **Senior Engineer Test**: Tanyakan pada diri sendiri: *"Apakah senior engineer akan menilai kode ini overcomplicated?"* Jika ya, sederhanakan.

### Contoh Kasus

**Permintaan:** *"Buat fungsi hitung diskon persentase."*

❌ **Pelanggaran Disiplin (Overengineering):**
Membuat `interface DiscountStrategy`, `class PercentageDiscountStrategy`, `class DiscountCalculatorFactory`, dan `DiscountConfigDTO` (60+ baris).

✅ **Penerapan Benar (Radical Simplicity):**
```typescript
export function calculateDiscount(amount: number, percentage: number): number {
  if (percentage <= 0) return 0;
  return amount * (Math.min(percentage, 100) / 100);
}
```

---

## 3. Surgical Precision (Perubahan Bedah Presisi)

**Sentuh hanya yang wajib disentuh. Bersihkan hanya sampah sendiri.**

Ketika memodifikasi berkas yang sudah ada (*existing code*):
- **Dilarang *drive-by refactoring***: Jangan "memperbaiki", merapikan indentasi, atau mengubah format baris di luar cakupan tugas langsung.
- **Dilarang menyentuh kode yang tidak rusak**: Jika suatu fungsi berjalan benar dan berada di luar permintaan, pertahankan apa adanya.
- **Patuhi konvensi setempat**: Ikuti gaya penamaan dan arsitektur kode yang sudah ada di repositori, meskipun Anda memiliki preferensi pribadi yang berbeda.
- **Penanganan dead code lama**: Jika mendeteksi dead code lawas yang tidak terkait tugas, catat di Parking Lot — jangan menghapusnya tanpa instruksi pengguna.
- **Pembersihan orphan (*orphan cleanup*)**: Hapus import, variabel, atau helper lokal yang menjadi tidak terpakai HANYA karena perubahan Anda sendiri.
- **Uji Lacak (The Trace Test)**: Setiap baris dalam `git diff` harus dapat dipertanggungjawabkan dan terlacak langsung ke instruksi pengguna.

### Contoh Kasus

**Permintaan:** *"Perbaiki crash jika email bernilai kosong pada validator user."*

❌ **Pelanggaran Disiplin (Perubahan Liar / Orthogonal):**
```diff
- // check email
- if (!user.email) throw new Error("Email missing");
+ /**
+  * Validates user input payload.
+  */
+ const trimmedEmail = (user.email || '').trim();
+ if (!trimmedEmail || !trimmedEmail.includes('@')) {
+   throw new ValidationError("Invalid email address");
+ }
+ // Cleanup tidak diminta pada baris sekitar:
- if (user.age < 18) throw new Error("Underage");
+ if (Number(user.age) < 18) throw new ValidationError("Must be 18+");
```

✅ **Penerapan Benar (Perubahan Bedah Presisi):**
```diff
- if (!user.email) throw new Error("Email missing");
+ const email = typeof user.email === 'string' ? user.email.trim() : '';
+ if (!email) throw new Error("Email missing");
```

---

## 4. Verifiable Goal Loop (Loop Verifikasi Terarah)

**Tetapkan kriteria sukses yang dapat diuji. Ulangi (*loop*) sampai terbukti.**

Ubah instruksi imperatif menjadi target deklaratif yang terverifikasi:

| Perintah Awal | Transformasi Target Terarah |
|---|---|
| "Tambah validasi payload" | "Tulis test dengan input invalid, lalu buat test lulus." |
| "Perbaiki bug null pointer" | "Tulis test/skrip reproduksi yang gagal, lalu buat test lulus." |
| "Refactor fungsi parse" | "Pastikan test yang ada lulus sebelum dan sesudah refactor." |

Untuk tugas multi-langkah, tetapkan rencana verifikasi konkret:
```
1. [Langkah] → verifikasi: [pemeriksaan konkret]
2. [Langkah] → verifikasi: [pemeriksaan konkret]
3. [Langkah] → verifikasi: [pemeriksaan konkret]
```

Kriteria sukses yang eksplisit memberi arah verifikasi mandiri tanpa perlu tebak-tebakan.

---

## Checklist Evaluasi Pra-Delivery

Sebelum menyerahkan hasil perubahan kode:

- [ ] **Trace Test**: Setiap baris dalam diff memiliki korelasi langsung dengan instruksi pengguna.
- [ ] **No Drive-by Refactor**: Tidak ada pembersihan format atau refactor liar pada kode sekitar.
- [ ] **Orphan Clean**: Import atau variabel yang menjadi usang akibat editan sendiri telah dibersihkan.
- [ ] **Senior Engineer Test**: Kode bebas dari layer abstraksi palsu untuk komponen sekali pakai.
- [ ] **Verifiable Loop**: Ada bukti eksekusi nyata (perintah tes, skrip reproduksi, atau build exit code 0).
