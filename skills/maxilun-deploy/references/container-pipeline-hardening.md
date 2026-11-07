# Container & Pipeline Hardening Playbook

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-deploy/SKILL.md"
  origin: "Maxilun Deploy Engine"
-->

Panduan rekayasa kontainer Docker berbobot minimal, pengerasan keamanan gambar produksi, dan optimasi pipeline CI/CD.

---

## 1. Disiplin Multi-Stage Build Docker

Gunakan pemisahan tahap build dan tahap runtime untuk meminimalkan ukuran image dan membuang toolchain kompilasi dari lingkungan produksi:

```dockerfile
# Tahap 1: Builder
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Tahap 2: Runner Produksi Minimalis
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

# Jalankan sebagai user non-root
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 appuser

COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist

USER appuser
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

### Invarian Keamanan Kontainer:
1. **User Non-Root Wajib**: Dilarang menjalankan proses aplikasi di dalam kontainer sebagai `root`.
2. **Pembersihan Cache Package Manager**: Selalu bersihkan cache package manager dalam layer yang sama (misal: `rm -rf /var/cache/apk/*` atau `apt-get clean`).
3. **Penyematan Versi Image Spesifik**: Dilarang menggunakan tag `:latest` di lingkungan produksi. Gunakan tag semantik eksplisit (misal: `node:20.18-alpine3.20`) atau digest SHA.

---

## 2. Optimasi Cache Pipeline CI/CD

1. **Urutan Cache Dependensi**:
   - Cache direktori dependensi (`~/.npm`, `~/.cache/pip`, `~/.m2`) berdasarkan hash dari file lockfile (`package-lock.json`, `poetry.lock`, `go.sum`).
2. **Fail Fast & Sharding Paralel**:
   - Jalankan pemeriksaan linter dan format kode di langkah paling awal sebelum menjalankan suite pengujian berat.
   - Pecah kasus uji pengujian integrasi menjadi beberapa shard paralel jika total waktu eksekusi melebihi 10 menit.

---

## 3. SRE SLO Alerting: Multi-Window Multi-Burn-Rate

Alihkan pemantauan produksi dari alert threshold mentah (misal: CPU > 80% atau Memory > 85% yang kerap memicu *alert fatigue*) ke pemantauan **Symptom-Based Alerting** berbasis **Error Budget SLO**.

### 3.1 Formula Burn Rate
Jika SLO target ketersediaan adalah $99.9\%$ selama jendela 30 hari (Error Budget = $0.1\% = 0.001$):
- **Burn Rate 1.0**: Menghabiskan 100% error budget tepat dalam 30 hari (kondisi konsumsi wajar).
- **Burn Rate 14.4**: Menghabiskan 2% error budget hanya dalam 1 jam ($100\% / (30 \times 24 / 14.4)$) $\to$ Darurat kritis (*Critical Outage*).

### 3.2 Matriks Alerting Multi-Window Multi-Burn-Rate

Gunakan kombinasi long-window (untuk mendeteksi tren degradasi) dan short-window (untuk meredam peringatan palsu saat pemulihan):

| Tingkat Keparahan | Konsumsi Budget | Long Window | Short Window | Burn Rate | Target Respon & Tindakan |
|---|---|---|---|---|---|
| **P1 - Critical (Pager)** | 2% budget habis dalam 1 jam | 1 Jam | 5 Menit | **14.4x** | Pager on-call seketika. Pemadaman aktif atau lonjakan 5xx masif. Hubungkan langsung ke runbook rollback / failover. |
| **P2 - High (Urgent)** | 5% budget habis dalam 6 jam | 6 Jam | 30 Menit | **6.0x** | Notifikasi darurat ke tim. Investigasi dalam 30 menit. Cek degradasi database atau API pihak ketiga. |
| **P3 - Medium (Ticket)** | 10% budget habis dalam 3 hari | 3 Hari | 6 Jam | **1.0x** | Tiket otomatis ke backlog sprint aktif. Degradasi lambat yang menggerus keandalan sistem. |

### 3.3 Aturan Operasional Alert
1. **Wajib Tautan Runbook**: Setiap alert yang dikirim ke pager atau Slack/Discord wajib menyertakan URL runbook tindakan operasional spesifik. Alert tanpa runbook dilarang aktif di produksi.
2. **Kondisi Reset Otomatis**: Alert darurat hanya padam jika short window kembali di bawah batas burn rate, membuktikan bahwa perbaikan/rollback telah efektif menghentikan pendarahan budget.
