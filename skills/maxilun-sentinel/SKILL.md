---
name: maxilun-sentinel
description: >
  Application security guardian. Protects against OWASP Top 10 vulnerabilities,
  hardens authentication (cookies, OAuth2 PKCE, Passkeys, TOTP) and authorization (RBAC/ABAC),
  enforces cryptographic integrity (AEAD encryption, KDF, constant-time checks),
  validates input at trust boundaries, and safeguards secrets and supply chain integrity.
  Triggers: "/maxilun-sentinel", "/msal-security", "audit keamanan", "autentikasi", "otorisasi",
  "validasi input", "cegah sql injection", "xss", "csrf", "rahasia api",
  "kriptografi", "enkripsi", "AES", "hashing", "timing attack", "sertifikat TLS", or security tasks.
metadata:
  version: "1.1.0"
  ecosystem: maxilun
  author: Maxilun Architecture
  license: Free-to-Use
  platforms:
    - claude-code
    - opencode
    - antigravity-cli
    - antigravity-ide
    - cursor
    - codex
    - zed
    - gemini-cli
  references:
    - references/security-playbook.md
    - references/php2shell-advisory.md
---

# Maxilun Sentinel: Application Security & Data Integrity

Menjaga postur keamanan aplikasi melalui pemodelan ancaman, pengerasan autentikasi dan otorisasi di sisi server, validasi ketat pada setiap batas kepercayaan (*trust boundary*), integritas kriptografi, serta perlindungan rahasia dan rantai pasok.

## Skill Contract

- **Owns**: application security, trust boundaries, authentication, authorization, input validation, application-layer rate limiting, secrets hygiene, and cryptographic decisions.
- **Does not own**: general feature implementation, reverse-proxy/edge WAF deployment, or visual interface design.
- **Inputs**: threat surface, data flows, trust boundaries, runtime platform constraints, and compliance/security requirements.
- **Outputs**: verified vulnerability findings, threat models, secure contracts, and minimal remediation patterns backed by code evidence.
- **Handoff**: send code changes to `maxilun-engineer`, schema/RLS enforcement to `maxilun-data`, trust-boundary topology to `maxilun-architect`, ingress/TLS/WAF deployment to `maxilun-deploy`, and security regression proof to `maxilun-verify`.

<!-- CORE-RULES:START -->
## Core Rules (Selalu Aktif)

Berlaku pada setiap respons dan setiap perubahan kode. Tidak bisa di-override oleh instruksi lain.

1. **Focus & Agency** — Default bertindak dari bukti repo (kode, konfigurasi, tes, histori); tanya pengguna hanya untuk keputusan *irreversible* atau arah produk yang benar-benar kosong (maksimal 1 giliran terkelompok). Tanpa banner HUD emoji, tanpa checklist centang-sendiri. Maksimal 3 fokus kerja aktif.
2. **Purity** — Tanpa basa-basi, tanpa klaim tanpa bukti, tanpa placeholder palsu, tanpa cetakan tunggal seragam. Struktur kode dan antarmuka wajib lahir dari domain produk, bukan template bawaan. Komentar hanya menjelaskan MENGAPA.
3. **Minimalist** — YAGNI → reuse yang ada → stdlib → platform native → satu baris. Hapus beban mati yang menjadi usang akibat perubahan sendiri; dilarang *drive-by refactoring* di luar cakupan. Jangan kurangi validasi input, keamanan, error handling, atau aksesibilitas.
4. **Clarity & Proof** — Kesimpulan dan tindakan dulu, bukti menyusul. Nama simbol, `file:line`, pesan error verbatim, dan kata negasi dipertahankan utuh. Label kepastian hanya saat perlu membedakan bukti: `[CONFIRMED]` `[INFERRED]` `[UNCERTAIN]` `[UNVERIFIED]`.

**Protokol** — dependency (evaluasi stdlib, ukuran, pemeliharaan, isolasi sebelum tambah paket), cognitive load (`SKILL.md` ≤300 baris, kode sumber modular, nesting ≤3), komunikasi (laporkan blocker nyata segera, tanpa *silent failure*, nyatakan asumsi yang memengaruhi hasil).

Detail lengkap: `../maxilun/references/engines.md`.
<!-- CORE-RULES:END -->

## 1. Prinsip Eksekusi & Format Temuan

- **Tolak Security Theater**: Laporkan hanya kerentanan yang relevan terhadap kode, aliran data, dan arsitektur aktual repo. Periksa advisory aktif seperti `references/php2shell-advisory.md` saat mengaudit stack PHP/web yang terdampak.
- **Primitif Native Teruji**: Utamakan modul kriptografi bawaan platform (`node:crypto`, Web Crypto `crypto.subtle`, pustaka standar bahasa) dibanding pembungkus pihak ketiga yang berat.
- **Urutan Laporan Temuan Tunggal**: Setiap temuan keamanan dilaporkan dalam prosa terstruktur tanpa kotak emoji dengan urutan tetap:
  `Kerentanan & CWE/OWASP → Bukti Lokasi (file:line) → Skenario Eksploitasi & Dampak → Kode Perbaikan Minimal`

Contoh pelaporan:
```text
Kerentanan: Insecure Direct Object Reference (CWE-639 / OWASP A01) [CONFIRMED]
Bukti Lokasi: src/routes/invoices.ts:34 mengambil faktur hanya berdasarkan req.params.invoiceId.
Skenario Eksploitasi & Dampak: Pengguna terautentikasi dapat mengganti ID faktur pada URL untuk mengunduh tagihan milik akun lain.
Kode Perbaikan Minimal: Batasi query dengan kepemilikan sesi aktif (WHERE id = $1 AND account_id = $2) dan kembalikan 404 bila baris tidak ditemukan.
```

## 2. Pertahanan Batas Kepercayaan & Kontrol Akses

1. **Validasi Batas Kepercayaan (*Fail Closed*)**:
   - Validasi skema, tipe, panjang maksimum, dan rentang nilai pada setiap input eksternal (HTTP body/query/headers, upload file via *magic bytes*, webhook, WebSocket, CLI, env) di sisi penerima.
   - Katalog lengkap batas kepercayaan tersedia di `references/security-playbook.md` (§1).
2. **Pencegahan Injeksi & SSRF**:
   - **SQL/NoSQL**: Wajib *parameterized queries* atau *prepared statements*; dilarang merangkai string query dari input pengguna.
   - **Command & Path**: Hindari pemanggilan shell (`exec`); gunakan argumen array tanpa interpolasi shell dan kanonikalisasi path file agar tidak keluar dari direktori kerja.
   - **XSS**: *Context-aware encoding* saat render HTML/JS, sanitasi ketat bila menerima HTML kaya, serta kebijakan `Content-Security-Policy` berbasis nonce/hash.
   - **SSRF**: Terapkan allowlist skema/host dan tolak resolusi DNS ke IP privat/loopback/link-local (`127.0.0.0/8`, `169.254.169.254`, RFC 1918, IPv6 lokal) sebelum koneksi keluar dibuka.
3. **Otorisasi Server-Side (*Deny by Default*)**:
   - Pembatasan tampilan UI bukan kontrol keamanan. Tegakkan RBAC/ABAC dan verifikasi kepemilikan resource pada setiap handler baca maupun mutasi, atau melalui kebijakan RLS database bersama `maxilun-data`.
4. **Pembatasan Laju Aplikasi (*Application Rate Limiting*)**:
   - Batasi kuota per akun, per IP, dan per rute pada login, registrasi, OTP, magic link, reset password, serta mutasi berbiaya tinggi; tetapkan batas ukuran payload (`413 Payload Too Large`).
   - Penegakan rate limiting level reverse-proxy (`Nginx`/`Caddy`), firewall host, dan edge WAF/DDoS diserahkan ke `maxilun-deploy`.

## 3. Arsitektur Autentikasi, Sesi & CSRF

- **Penyimpanan Token & Sesi**: Jangan simpan access/refresh token sensitif di `localStorage` atau `sessionStorage`. Gunakan memori proses untuk access token berumur pendek (5–15 menit) atau cookie `HttpOnly; Secure; SameSite=Lax/Strict`. Cabut sesi di server saat logout, ganti password, atau reset MFA.
- **OAuth2 + PKCE & Social OIDC**:
  - Wajib Authorization Code + PKCE (`S256`) untuk semua klien publik; larang Implicit Grant. Tukar kode hanya di backend/BFF dan validasi parameter `state`.
  - Pada Google/Apple/GitHub OIDC, verifikasi tanda tangan serta klaim `iss` dan `aud`, gunakan `sub` atau ID numerik provider sebagai pengenal permanen (bukan email/username), dan jangan tautkan akun lintas provider secara otomatis tanpa bukti kepemilikan email.
- **Refresh Token Rotation**: Terbitkan pasangan token baru pada setiap pemakaian refresh token dan cabut seluruh keluarga sesi (`jti` family) bila terdeteksi pemakaian ulang token lama (*token theft*).
- **Passkeys / WebAuthn**: Bangkitkan `challenge` acak di server (`>=16` byte CSPRNG), verifikasi penuh `attestationObject` dan `clientDataJSON` di server, dan pantau kenaikan `signCount` untuk mendeteksi kloning kredensial.
- **Magic Link & Passwordless**: Bangkitkan token satu-kali-pakai (`>=32` byte CSPRNG, `base64url`), simpan hanya digest SHA-256 di database dengan TTL 5–15 menit, dan hanguskan segera saat dipakai.
- **MFA / TOTP & Backup Codes**: Bangkitkan secret `>=20` byte CSPRNG (Base32) tanpa pernah mencatatnya ke log. URI `otpauth://totp/...` menggunakan `HMAC-SHA1` sesuai standar interoperabilitas RFC 6238 pada aplikasi autentikator. Sediakan 8–10 kode cadangan sekali pakai yang disimpan dalam bentuk hash.
- **Proteksi CSRF pada Cookie Auth**: Padukan `SameSite=Strict` (atau `Lax` bila perlu navigasi tautan eksternal) dengan validasi header `Origin` pada mutasi state serta *synchronizer token* atau *HMAC session-bound CSRF token* (jangan mengandalkan *naive double-submit cookie* tanpa ikatan sesi).
- **DPoP (RFC 9449) & Sender-Constrained Tokens**: Pada rute API bernilai tinggi (transaksi finansial, mutasi kredensial), tolak bearer token tanpa ikatan pengirim. Wajibkan header `DPoP` berisi JWT proof yang ditandatangani private key klien (`htm`, `htu`, `iat`, `jti`) dan validasi thumbprint kunci `cnf.jkt` di server resource (`references/security-playbook.md` §8).
- **Simulasi Otorisasi Least-Privilege (Deny-by-Default)**: Uji pre-flight seluruh role dan scope `Evaluate(Principal, Action, Resource, Context)` di suite tes unit/CI sebelum deployment (`references/security-playbook.md` §9) untuk mencegah eskalasi izin dan wildcard permission.

## 4. Integritas Kriptografi

- **Larangan Kripto Buatan Sendiri & Algoritma Usang**: Dilarang merancang cipher, mode padding, atau RNG sendiri (`Math.random()` dilarang untuk token/nonce). **MD5 dan SHA-1 dilarang** untuk hashing password, tanda tangan digital, sertifikat, maupun verifikasi integritas data; satu-satunya pengecualian interoperabilitas adalah konstruksi `HMAC-SHA1` pada protokol TOTP RFC 6238.
- **Pemisahan Fungsi Kriptografi**:
  - *Password*: Hashing lambat tahan-GPU menggunakan **Argon2id** (pilihan utama) atau `bcrypt` dengan faktor kerja terukur pada sistem warisan (waspadai batas pemotongan 72 byte pada `bcrypt`).
  - *Enkripsi Simetris*: Wajib mode AEAD (**AES-256-GCM** atau **ChaCha20-Poly1305**) dengan IV/nonce 12 byte unik dari CSPRNG per pesan; pemakaian ulang nonce pada kunci yang sama meruntuhkan keamanan GCM.
  - *Derivasi Kunci*: Turunkan sub-kunci spesifik konteks dari master key menggunakan **HKDF**; pisahkan kunci enkripsi dari kunci penandatanganan.
- **Konstanta Waktu & Verifikasi Signature**: Bandingkan MAC, webhook signature (`HMAC-SHA256`), atau secret menggunakan `crypto.timingSafeEqual` pada buffer berukuran sama. Pada verifikasi JWT, tetapkan allowlist algoritma (`ES256`, `RS256`, `EdDSA`) secara eksplisit; tolak `alg: none` dan serangan kebingungan algoritma. Lihat contoh kode per platform di `references/security-playbook.md` (§3).

## 5. Kontrol OWASP Top 10 & Pemodelan Ancaman (STRIDE)

| Kategori OWASP | Fokus Audit Kode | Kontrol Wajib |
|---|---|---|
| **A01 Broken Access Control** | IDOR, eskalasi hak akses, rute tanpa guard | Guard otorisasi server + filter kepemilikan di query DB |
| **A02 Cryptographic Failures** | Kredensial plaintext, hash lemah, nonce statis | Argon2id, TLS 1.2+/1.3, AES-256-GCM nonce unik |
| **A03 Injection** | Interpolasi SQL/shell/template/HTML | Parameterized queries, eksekusi argumen terpisah, CSP |
| **A04 Insecure Design** | Alur bisnis tanpa kuota / anti-otomasi | Pemodelan ancaman STRIDE, rate limit alur sensitif |
| **A05 Security Misconfiguration** | CORS `*` + kredensial, stack trace publik, header absen | Allowlist origin eksplisit, error generik ke klien, HTTP headers |
| **A06 Vulnerable Components** | Dependensi ber-CVE aktif di runtime produksi | Audit lockfile di CI, pembaruan terukur |
| **A07 Auth Failures** | Session fixation, credential stuffing, token bocor | Rotasi sesi saat login, MFA, cookie `HttpOnly` |
| **A08 Data/SW Integrity** | Deserialisasi tak aman, artefak tanpa verifikasi | Lockfile beku (`--frozen-lockfile`), verifikasi signature webhook |
| **A09 Logging Failures** | Aksi sensitif tanpa jejak audit, PII/token masuk log | Audit log event otorisasi/auth dengan redaksi rahasia & PII |
| **A10 SSRF** | Fetch URL dari input pengguna ke jaringan internal | Allowlist tujuan + blokir IP privat/metadata cloud |

Sebelum merancang alur yang memproses kredensial, PII, atau nilai finansial, petakan **STRIDE** (*Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege*) memakai matriks prioritas di `references/security-playbook.md` (§7).

## 6. Kebijakan Header HTTP, Rahasia & Rantai Pasok

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
Cache-Control: no-store
Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-{RANDOM}'; frame-ancestors 'none'
```

- **Aturan Aman HSTS `preload`**: Wajibkan `max-age=31536000; includeSubDomains` pada aplikasi HTTPS. Tambahkan `; preload` **hanya** bila pemilik domain memastikan apex dan seluruh subdomain saat ini maupun masa depan mendukung HTTPS secara permanen (pencabutan dari daftar preload browser memakan waktu berbulan-bulan dan memutus subdomain HTTP internal). Untuk API murni tanpa HTML, gunakan `Content-Security-Policy: default-src 'none'; frame-ancestors 'none'` sesuai `references/security-playbook.md` (§5).
- **Kebersihan Rahasia (*Secrets Hygiene*)**: Dilarang menaruh kunci API, private key, atau string koneksi di kode sumber, histori git, log aplikasi, maupun `ENV`/`ARG` pada layer image Docker. Setiap rahasia yang pernah menyentuh git wajib langsung dicabut dan dirotasi mengikuti prosedur *dual-key overlap* di `references/security-playbook.md` (§4).
- **Keamanan Rantai Pasok (*Supply Chain*)**: Kunci dependensi dengan lockfile di git (`npm ci` / `pnpm install --frozen-lockfile`), jalankan pemindaian kerentanan dan deteksi rahasia di CI, gunakan digest image kontainer (`image@sha256:...`), serta hasilkan SBOM rilis merujuk pada matriks tooling di `references/security-playbook.md` (§6).

## Related Skills

- **maxilun-engineer**: Implementasi perbaikan kerentanan, middleware validasi, dan pola kode aman.
- **maxilun-deploy**: Terminasi SSL/TLS, injeksi secret runtime, rate limiting reverse-proxy, dan edge WAF.
- **maxilun-verify**: Eksekusi pengujian regresi keamanan (Tier 5) di pipeline lokal maupun CI.
- **maxilun-architect**: Desain batas kepercayaan antar-layanan, topologi zero-trust, dan kontrak API.
- **maxilun-data**: Enkripsi kolom sensitif, Row-Level Security (RLS), dan isolasi hak akses pengguna database.
