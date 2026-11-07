# Evidence & Reporting Standard: Reproducible Proofs & Redaction

Standar penyusunan bukti reproduksi kerentanan yang tidak terbantahkan, aman dari kebocoran rahasia, dan langsung dapat ditindaklanjuti oleh tim rekayasa.

---

## 1. Struktur Paket Bukti Reproducible (Evidence Bundle)

Setiap temuan yang berhasil melewati verifikasi disimpan dalam tata letak direktori deterministik:

```text
findings/<target>-<vuln-class>/evidence/<finding-id>/
├── request.http       # Request mentah lengkap (metode, path, headers, body)
├── response.http      # Respon mentah lengkap (status, headers, body bukti)
├── repro.sh           # Perintah curl mandiri dengan variabel lingkungan
├── evidence.har       # Rekaman HAR 1.2 untuk diimpor ke proxy/analisis
├── manifest.json      # Metadata, stempel waktu ISO, SHA-256 body, dan marker
└── report-draft.md    # Draf laporan siap serah berstandar industri
```

### Format File Utama

#### `request.http`
```http
POST /api/v2/workspaces/9102/members HTTP/1.1
Host: api.target.com
Authorization: Bearer ‹redacted:$AUTHORIZATION›
Content-Type: application/json
Accept: application/json

{"user_id": 4012, "role": "admin"}
```

#### `repro.sh`
```bash
#!/usr/bin/env bash
# Reproduksi mandiri — gunakan variabel lingkungan untuk kredensial aktif
: "${TARGET_URL:=https://api.target.com}"
: "${AUTHORIZATION:=YOUR_BEARER_TOKEN}"

curl -sS -i -X POST "${TARGET_URL}/api/v2/workspaces/9102/members" \
  -H "Authorization: Bearer ${AUTHORIZATION}" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 4012, "role": "admin"}'
```

#### `manifest.json`
```json
{
  "finding_id": "fnd-7a1b8c",
  "target": "api.target.com",
  "vuln_class": "idor",
  "endpoint": "/api/v2/workspaces/9102/members",
  "http_method": "POST",
  "verified_at": "2026-11-08T10:00:00Z",
  "verdict": "PROVEN",
  "confirmation_marker": "admin privilege granted to user 4012",
  "response_sha256": "8f4e2...901",
  "redacted_headers": ["Authorization"]
}
```

---

## 2. Standar Redaksi Rahasia (Secrets Hygiene)

Setiap artefak yang disimpan ke disk atau disalin ke draf laporan **wajib melalui proses redaksi rahasia**:

1. **Header Sensitif yang Wajib Diredaksi**:
   - `Authorization`, `Proxy-Authorization`
   - `Cookie`, `Set-Cookie`
   - `X-Api-Key`, `Api-Key`, `X-Auth-Token`
   - `X-Session-Token`, `X-CSRF-Token`
2. **Aturan Penulisan Script `repro.sh`**:
   - Dilarang menaruh string token atau password plaintext di dalam script.
   - Rujuk nilai rahasia via variabel lingkungan: `${AUTHORIZATION}`, `${COOKIE}`.
3. **Penyaringan PII**:
   - Nomor kartu kredit, nomor induk kependudukan, atau nomor telepon korban yang tidak disengaja terekam wajib disamarkan (*masked*): `4111-XXXX-XXXX-1234`.

---

## 3. Formula Judul Laporan (Title Formula)

Judul laporan harus ringkas, spesifik, dan memprioritaskan dampak bisnis:

```text
[Kelas Celah] pada [Endpoint / Fitur Spesifik] memungkinkan [Peran Penyerang] untuk [Dampak Nyata] [Cakupan Korban]
```

### Contoh Judul Efektif vs Tidak Efektif
- **Efektif**:
  - `IDOR pada GET /api/v2/invoices/{id} memungkinkan pengguna terautentikasi membaca tagihan penyewa lain`
  - `Broken Authentication pada POST /api/admin/users/invite memungkinkan pengguna biasa mengundang akun role admin`
  - `SSRF pada parameter imageUrl di /api/export mengekstraksi metadata internal AWS EC2`
- **Tidak Efektif (Ditolak)**:
  - `Celah keamanan pada website` (Terlalu umum)
  - `Ditemukan bug IDOR` (Tidak ada rincian endpoint atau dampak)
  - `Potensi celah XSS` (Menggunakan bahasa teoritis)

---

## 4. Format Laporan Penyerahan Temuan

```markdown
# Laporan Temuan Keamanan: [Judul Sesuai Formula]

## 1. Ringkasan Eksekutif
Satu paragraf padat yang merangkum apa celahnya, di mana lokasinya, prasyarat yang dibutuhkan penyerang, dan dampak kerugian langsung terhadap sistem.

## 2. Detail Kerentanan
- **Kelas Kerentanan**: Insecure Direct Object Reference (IDOR)
- **CWE / OWASP**: CWE-639 / OWASP A01:2021-Broken Access Control
- **Skor CVSS 3.1**: 6.5 (Medium) — `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N`
- **Endpoint Terdampak**: `POST /api/v2/workspaces/{id}/members`

## 3. Langkah Reproduksi Terukur
1. Siapkan Akun A (Penyerang, ID: 101) dan Akun B (Korban, Workspace ID: 9102).
2. Dapatkan token akses untuk Akun A.
3. Eksekusi request berikut menggunakan kredensial Akun A terhadap Workspace milik Akun B:
   ```bash
   curl -i -X POST "https://api.target.com/api/v2/workspaces/9102/members" \
     -H "Authorization: Bearer ${AKUN_A_TOKEN}" \
     -H "Content-Type: application/json" \
     -d '{"user_id": 101, "role": "admin"}'
   ```
4. Amati respon:
   ```json
   HTTP/1.1 200 OK
   {"success": true, "workspace_id": 9102, "role": "admin"}
   ```
   Akun A berhasil ditambahkan sebagai admin ke dalam workspace milik Akun B tanpa izin pemilik.

## 4. Bukti Dampak Nyata
Respon HTTP 200 di atas membuktikan bahwa entitas anggota workspace dimutasi langsung tanpa memvalidasi apakah pengirim request memiliki wewenang administratif pada workspace 9102. Penyerang dapat mengambil alih kepemilikan workspace penyewa lain secara penuh.

## 5. Rekomendasi Perbaikan untuk Tim Rekayasa
Pada handler `src/controllers/workspaceMembers.ts:45`, tambahkan validasi kepemilikan sebelum mutasi:
```typescript
const isOwner = await db.workspaces.findFirst({
  where: { id: workspaceId, ownerId: req.session.userId }
});
if (!isOwner) {
  return res.status(404).json({ error: "Workspace tidak ditemukan" });
}
```
Serahkan perbaikan kode ke `maxilun-engineer` dan verifikasi regresi melalui `maxilun-verify`.
```
