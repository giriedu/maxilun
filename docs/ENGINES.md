# Four Always-On Engines and Three Operating Protocols

Empat engine pertama adalah fondasi kualitas. Tiga bagian berikutnya adalah protokol kerja pendukung. Versi lengkap ada di `skills/maxilun/references/engines.md`, dan ringkasannya tertanam sebagai blok `CORE-RULES` di setiap SKILL.md.

## 1. Focus Engine

- Membuka respon dengan Executive HUD 2-baris (`🎯 [FOKUS]`, `⚡ [TINDAKAN]`).
- Membatasi tugas aktif maksimal 3 subtask untuk mencegah kelebihan beban kognitif (*cognitive overload*).
- Menjaga momentum penyelesaian dan estimasi waktu terukur.

## 2. Purity Engine

- Menghilangkan klise AI (*delve, tapestry, seamlessly, robust, cutting-edge, game-changer*).
- Menegakkan *Purpose Gate*: setiap baris kode, teks antarmuka, dan elemen visual harus memiliki fungsi riil yang jelas.
- Higienitas komentar kode (hanya menjelaskan *mengapa*, bukan *apa*) dan menolak placeholder fiktif.

## 3. Minimalist Engineering Engine

- Menjalankan *Tangga Kesederhanaan* (*Simplicity Ladder*): YAGNI → Helper internal → Standard Library → Platform Native → 1 baris kode.
- Mengutamakan perbaikan akar masalah (*root cause*) dan pengurangan kode mubazir (*deletion over addition*).

## 4. Clarity Engine

- Sintesis teknis telegrafis, tinggi sinyal dan bebas filler percakapan.
- Mempertahankan presisi simbol kode, path file, nomor baris, dan pesan error secara verbatim.
- Menjaga kata negasi agar arti logika tidak berbalik.

---

## Three Operating Protocols

Bagian ini menetapkan kebiasaan kerja pendukung dan bukan engine terpisah:

- **Dependency Decision Framework** — Checklist 5 langkah sebelum menambah dependency baru.
- **Cognitive Load Reduction** — Batas ukuran file, kedalaman nesting, dan naming convention.
- **Proactive Communication Rules** — Laporkan blocker segera, no silent failures, asumsi eksplisit.

---

## Disiplin Rekayasa Bedah (Maxilun Surgical Discipline)

Disiplin rekayasa presisi tinggi untuk menekan kesalahan laten model AI saat menulis dan mengubah kode:

1. **Pre-flight Reasoning**: Nyatakan asumsi eksplisit (`[ASUMSI]`), jangan memilih cabang tafsir diam-diam, paparkan trade-off, dan usulkan pendekatan lebih sederhana jika overengineered.
2. **Radical Simplicity**: Kode minimal yang menyelesaikan masalah. Tolak abstraksi untuk kode sekali pakai (*no single-use abstractions*). Jika 200 baris bisa ditulis dalam 50 baris bersih, tulis ulang. Uji Senior Engineer: sederhanakan jika dinilai *overcomplicated*.
3. **Surgical Precision**: Sentuh hanya yang diminta (*touch only what you must*). Dilarang perbaikan liar (*no drive-by refactoring*). Bersihkan orphan variabel/import buatan sendiri, jangan hapus dead code lama di luar cakupan tanpa izin. Setiap baris perubahan wajib terlacak ke permintaan pengguna.
4. **Verifiable Goal Loop**: Ubah tugas imperatif menjadi target verifikasi (test reproduksi sebelum fix bug, cek sebelum dan sesudah refactor). Tetapkan rencana `[Langkah] → verifikasi: [cek]`.

Rujukan lengkap: [`skills/maxilun/references/surgical-discipline.md`](../skills/maxilun/references/surgical-discipline.md).
---

Selengkapnya lihat [`skills/maxilun/references/engines.md`](../skills/maxilun/references/engines.md).
