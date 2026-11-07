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
