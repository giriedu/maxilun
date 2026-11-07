# Game Design Lifecycle & Balancing Playbook

Metodologi perancangan Game Design Document (GDD), perumusan model matematika balancing, tahapan produksi studio, dan anggaran performa runtime game.

---

## 1. Spesifikasi Standar GDD (8 Bagian Wajib)

Setiap dokumen desain sistem game wajib memuat delapan bagian deterministik berikut agar implementasi engineering tidak menimbulkan ambiguitas logika:

1. **Overview**: Ringkasan fungsi sistem, tujuan dalam loop game, dan audiens target dalam 2–3 kalimat lugas.
2. **Player Fantasy**: Dampak mekanik terhadap pengalaman dan agensi pemain (misal: "Pemain merasakan ketegangan manajemen sumber daya saat stamina habis di tengah serangan").
3. **Detailed Rules**: Alur logika mekanik deterministik, transisi state, kondisi menang/kalah, input mapping, dan interaksi antar sistem.
4. **Formulas**: Perhitungan numerik formal (damage, kalkulasi experience, drop rates, cooldown scaling).
5. **Edge Cases**: Penanganan kondisi ekstrem (disconnection saat trade, frame drop di window input buffer, input bentrok simultan, death saat animasi skill aktif).
6. **Dependencies**: Daftar ketergantungan modul eksternal (UI HUD, audio triggers, persistent save system, inventory data, network replication).
7. **Tuning Knobs**: Parameter numerik yang dapat disesuaikan desainer tanpa menyentuh kode (base speed, multiplier, duration, tick rate).
8. **Acceptance Criteria**: Kondisi terukur untuk validasi penyelesaian fitur yang dapat diuji secara empiris via automated test.

---

## 2. Model Matematika & Formula Balancing

### 2.1 Formula Mitigasi Kerusakan (Damage Mitigation)

Hindari pengurangan flat stat murni ($Damage - Armor$) yang rentan memicu nilai nol atau invulnerability eksploitatif. Gunakan model kurva *diminishing returns*:

$$DamageTaken = RawDamage \times \left(\frac{K}{K + Armor}\right)$$

Di mana $K$ adalah konstanta armor (misal $K = 100$).
- $Armor = 100 \implies \text{kerusakan berkurang } 50\%$.
- $Armor = 300 \implies \text{kerusakan berkurang } 75\%$.
- Setiap penambahan 1 poin Armor secara konsisten meningkatkan Effective Health Pool (EHP) sebesar $1/K$ dari Base Health.

### 2.2 Kurva Progresi Level & Experience

Gunakan polinomial atau eksponensial terkontrol untuk progresi leveling:

$$XP_{Required}(Level) = A \times Level^B + C \times Level$$

Contoh parameter kurva RPG terstandarisasi: $A = 50, B = 2, C = 100$.
- Level 1 ke 2: $50(1)^2 + 100(1) = 150 \text{ XP}$.
- Level 10 ke 11: $50(10)^2 + 100(10) = 6000 \text{ XP}$.

### 2.3 Formula Time-To-Kill (TTK) Budgeting

Anggaran TTK menentukan ritme pertarungan game:

$$TTK = \frac{TargetHealth}{DamagePerSecond \times (1 - MitigationRatio)}$$

- *Fast Paced Tactical*: Target TTK 0.2s – 0.6s.
- *Hero Shooter / Arena*: Target TTK 1.2s – 2.5s.
- *MMORPG / Raid Boss*: Target TTK 180s – 600s.

### 2.4 Sistem Ekonomi Tertutup (Sinks & Sources)

Setiap mata uang atau sumber daya game wajib memiliki persamaan ekuilibrium:

$$\Delta Currency = \sum Sources(Inflow) - \sum Sinks(Outflow)$$

- **Sources**: Misi, drop musuh, reward harian, trade masuk.
- **Sinks**: Biaya perbaikan gear, pajak transaksi market, upgrade konsumtif, reroll stat.
- Aturan desainer: Tanpa *sink* yang proporsional terhadap *inflow*, ekonomi akan mengalami hiperinflasi yang merusak sistem progresi jangka panjang.

---

## 3. Tahapan Produksi Studio Game

Siklus produksi studio game dijalankan secara bertahap dengan gerbang evaluasi empiris:

```
[Concept / Brief] -> [Systems GDD] -> [Prototype] -> [Vertical Slice] -> [Production] -> [Polish & QA] -> [Gold Master]
```

1. **Concept / Game Brief**: Dokumen 1–2 halaman mendefinisikan *core hook*, pilar permainan, platform sasaran, dan batasan teknis.
2. **Systems GDD**: Pemecahan rinci seluruh mekanik ke dalam 8 bagian GDD sebelum penulisan kode dimulai.
3. **Prototype (Greybox)**: Validasi mekanik inti (*game feel*, kontrol, responsivitas) menggunakan geometri primitif tanpa aset final. Menjawab pertanyaan: "Apakah mekanik inti menyenangkan dimainkan?"
4. **Vertical Slice**: Potongan game berdurasi 5–15 menit dengan kualitas representatif penuh (grafis, audio, HUD, performa stabil 60 FPS, save data). Berfungsi sebagai acuan kualitas (*quality benchmark*) untuk seluruh fase produksi selanjutnya.
5. **Production**: Penskalaan konten (level, variasi musuh, quest, balancing) berbasis arsitektur yang sudah terbukti di Vertical Slice.
6. **Polish & QA**: Optimasi frame pacing, perbaikan bug regresi, profiling alokasi memori, audio mixing, dan compliance platform.
7. **Gold Master / Release**: Build terfinalisasi yang lulus sertifikasi platform, smoke test lintas resolusi, dan verifikasi zero-crash.

---

## 4. Anggaran Performa Runtime & Frame Pacing

Target frame rate wajib ditentukan sejak fase awal proyek dengan alokasi anggaran frame time yang ketat:

| Target FPS | Total Frame Budget | CPU Gameplay & Fisika | Render & Draw Calls | GPU Shading & Post-Process |
|---|---|---|---|---|
| **60 FPS** | 16.67 ms | $\le 6.0\text{ ms}$ | $\le 4.5\text{ ms}$ | $\le 6.0\text{ ms}$ |
| **120 FPS** | 8.33 ms | $\le 3.0\text{ ms}$ | $\le 2.0\text{ ms}$ | $\le 3.3\text{ ms}$ |
| **30 FPS (Mobile)** | 33.33 ms | $\le 12.0\text{ ms}$ | $\le 8.0\text{ ms}$ | $\le 13.0\text{ ms}$ |

### Batasan Teknis Performa:
- **Draw Calls**: Maksimal 500–1000 per frame untuk target PC kelas menengah; maksimal 80–150 per frame untuk perangkat mobile.
- **Alokasi Garbage Collection (GC)**: Wajib 0 bytes per frame di loop utama (`_process`, `Update`, `Tick`). Semua instansiasi dinamis wajib menggunakan object pool yang dialokasikan di awal (pre-allocated).
- **Physics Ticks**: Jalankan pembaruan fisika pada frekuensi tetap (misal 50 Hz atau 60 Hz) menggunakan akumulator waktu delta terisolasi untuk menghindari *physics hitching*.
