# Security Playbook

Referensi eksekusi untuk `maxilun-sentinel`. Dokumen ini berisi template, katalog, dan pola yang bisa dieksekusi langsung — bukan prinsip umum.

---

## 1. Trust Boundary Catalog

Trust boundary adalah titik di mana data berpindah dari zona terpercaya ke zona tidak terpercaya (atau sebaliknya). Setiap boundary wajib memiliki validasi eksplisit.

| Trust Boundary | Input Source | Validasi Wajib | Contoh Serangan Jika Dilewati |
|---|---|---|---|
| **HTTP API Endpoint** | Request body, query params, headers | Schema validation (Zod/Joi), type coercion, length limits | SQL injection, parameter tampering, mass assignment |
| **Form Submission** | Form fields, file uploads | Server-side validation (bukan hanya client), CSRF token, file type whitelist | XSS stored, path traversal, CSRF |
| **File Upload** | Binary content, filename, MIME type | Magic byte verification, size limit, sandboxed storage, no execution permission | Remote code execution, directory traversal |
| **Environment Variable** | Process env, .env files | Type parsing, secret detection, no logging | Secret leakage, type confusion |
| **Database Query** | User-supplied filter/sort/search | Parameterized queries only, no string concatenation | SQL injection, data exfiltration |
| **External API Response** | Third-party JSON/XML/HTML | Response schema validation, timeout, circuit breaker | Supply chain attack, data poisoning |
| **WebSocket Message** | Real-time client messages | Same validation as HTTP API, rate limiting per connection | Injection, resource exhaustion |
| **CLI Argument** | Command-line input | Argument parsing library, no eval/exec, sanitize shell metacharacters | Command injection, argument injection |
| **Config File** | YAML/JSON/TOML from disk | Schema validation, no code execution in config parser | Config injection, arbitrary code execution |
| **Inter-Service Call** | gRPC/REST between microservices | mTLS or service mesh auth, request signing, zero trust network | Lateral movement, service impersonation |

### Aturan Penerapan

1. **Identifikasi semua trust boundary** sebelum menulis kode. Gunakan tabel di atas sebagai checklist.
2. **Validasi di sisi penerima**, bukan pengirim. Client-side validation adalah UX enhancement, bukan security control.
3. **Fail closed**: jika validasi gagal, tolak request. Jangan fallback ke perilaku default yang lebih permisif.
4. **Log rejection**: setiap validasi yang gagal harus di-log dengan konteks (tanpa log data sensitif).
5. **Review saat perubahan**: setiap kali menambah endpoint, field, atau integrasi baru, cek apakah trust boundary baru tercipta.

---

## 2. Security Test Patterns (untuk maxilun-verify)

Pola tes keamanan yang bisa diintegrasikan ke CI/CD. Setiap pola memiliki: trigger condition, test method, pass criteria.

### 2.1 Authentication & Authorization Tests

| Pattern | Method | Pass Criteria |
|---|---|---|
| **Auth bypass** | Kirim request ke protected endpoint tanpa token | 401/403, bukan 200 atau 500 |
| **Expired token** | Gunakan JWT dengan exp di masa lalu | 401 dengan pesan "token expired" |
| **Privilege escalation** | User biasa akses admin endpoint | 403, bukan 200 |
| **IDOR** | Ganti resource ID di URL/body dengan milik user lain | 403/404, bukan 200 dengan data orang lain |
| **Session fixation** | Cek session ID berubah setelah login | Session ID baru, bukan reuse |
| **Brute force protection** | Kirim 10+ login gagal berturut-turut | Account locked atau rate limited setelah N attempt |

### 2.2 Injection Tests

| Pattern | Method | Pass Criteria |
|---|---|---|
| **SQL injection** | Input `' OR 1=1 --` di search/filter field | Tidak ada error DB, hasil kosong atau filtered |
| **XSS reflected** | Input `<script>alert(1)</script>` di query param | Output di-escape atau diblokir, script tidak execute |
| **XSS stored** | Submit payload XSS via form, reload halaman | Payload tidak render sebagai HTML |
| **Command injection** | Input `; ls /etc/passwd` di field yang diproses shell | Command tidak tereksekusi, input ditolak |
| **Path traversal** | Input `../../etc/passwd` di file path param | Path canonicalized, akses ditolak |
| **Template injection** | Input `{{7*7}}` atau `${7*7}` di user input | Tidak ada evaluasi ekspresi server-side |

### 2.3 Data Protection Tests

| Pattern | Method | Pass Criteria |
|---|---|---|
| **Sensitive data in logs** | Trigger operasi dengan PII/token, cek log output | Tidak ada plaintext password, token, atau PII di log |
| **Sensitive data in error** | Trigger error dengan input sensitif | Error message generic, tidak leak stack trace atau data |
| **Encryption at rest** | Cek database/storage untuk field sensitif | Terenkripsi atau hashed, bukan plaintext |
| **TLS enforcement** | Akses via HTTP (non-TLS) | Redirect ke HTTPS atau connection refused |
| **Data minimization** | Cek API response untuk field yang tidak diminta | Hanya field yang diperlukan yang dikembalikan |

### 2.4 Rate Limiting & DoS Tests

| Pattern | Method | Pass Criteria |
|---|---|---|
| **API rate limit** | Kirim >limit request dalam window | 429 setelah threshold, dengan Retry-After header |
| **Login rate limit** | >N failed login attempts | Lockout atau CAPTCHA challenge |
| **Large payload** | Kirim request body >size limit | 413 Payload Too Large |
| **Slowloris** | Buka koneksi, kirim partial request perlahan | Connection timeout setelah N detik |

### 2.5 Integration dengan maxilun-verify

Tambahkan tier keamanan setelah Tier 4 (Regression):

```
Tier 5: Security Validation
├── Auth/Authz tests (2.1)
├── Injection tests (2.2)  
├── Data protection tests (2.3)
└── Rate limiting tests (2.4)
```

Setiap PR yang mengubah authentication, authorization, input handling, atau data storage **wajib** menjalankan Tier 5. PR yang hanya mengubah UI/copy boleh skip Tier 5.

---

## 3. Cryptographic Implementation Reference

Template kode per platform. Jangan implement crypto dari nol — gunakan library yang sudah diaudit.

### 3.1 Password Hashing

| Platform | Library | Function | Notes |
|---|---|---|---|
| Node.js | `argon2` | `argon2.hash(password, {type: argon2.id})` | Argon2id preferred. Fallback: bcrypt cost ≥12 |
| Python | `argon2-cffi` | `PasswordHasher().hash(password)` | Argon2id default |
| Go | `golang.org/x/crypto/argon2` | `argon2.IDKey()` | Manual salt generation required |
| Rust | `argon2` crate | `Argon2::default().hash_password()` | Argon2id default |
| Java | `spring-security-crypto` | `Argon2PasswordEncoder` | Spring Boot standard |

**Jangan gunakan**: MD5, SHA-1/256 untuk password, custom hashing, XOR cipher.

### 3.2 Symmetric Encryption (Data at Rest)

| Platform | Library | Algorithm | Mode |
|---|---|---|---|
| Node.js | `crypto` (built-in) | AES-256-GCM | `createCipheriv('aes-256-gcm', ...)` |
| Python | `cryptography` | AES-256-GCM | `AESGCM(key).encrypt(nonce, data, aad)` |
| Go | `crypto/aes` + `crypto/cipher` | AES-256-GCM | `cipher.NewGCM(block)` |
| Rust | `aes-gcm` crate | AES-256-GCM | `Aes256Gcm::new(&key)` |

**Wajib**: unique nonce per encryption, authenticated encryption (GCM/ChaCha20-Poly1305), key dari KMS bukan hardcoded.

### 3.3 Token Signing (JWT)

| Platform | Library | Algorithm | Notes |
|---|---|---|---|
| Node.js | `jose` | ES256 atau RS256 | Hindari HS256 kecuali single-service |
| Python | `PyJWT` | RS256 | `jwt.encode(payload, private_key, algorithm="RS256")` |
| Go | `golang-jwt/jwt/v5` | RS256 | `jwt.NewWithClaims(jwt.SigningMethodRS256, claims)` |
| Rust | `jsonwebtoken` | RS256 | `encode(&Header::new(Algorithm::RS256), &claims, &key)` |

**Jangan**: alg:none, HS256 dengan shared secret di multi-service, store sensitive data di JWT payload (base64 ≠ encrypted).

### 3.4 Secure Random

| Platform | Function | Notes |
|---|---|---|
| Node.js | `crypto.randomBytes(n)` | Bukan Math.random() |
| Python | `secrets.token_bytes(n)` | Bukan random module |
| Go | `crypto/rand.Read(buf)` | Bukan math/rand |
| Rust | `rand::rngs::OsRng` | Bukan rand::thread_rng() untuk crypto |
| Browser | `crypto.getRandomValues(buf)` | Bukan Math.random() |

---

## 4. Secrets Rotation Protocol

Prosedur rotasi secret yang terstruktur. Jangan ad-hoc.

### 4.1 Rotation Schedule

| Secret Type | Rotation Frequency | Trigger |
|---|---|---|
| Database credentials | 90 hari | Scheduled + on compromise |
| API keys (third-party) | Per provider policy | Check provider docs |
| JWT signing keys | 30 hari | Scheduled, overlap period 7 hari |
| TLS certificates | Sebelum expiry | Automated via cert-manager/Let's Encrypt |
| SSH keys | 1 tahun | Scheduled + on personnel change |
| Encryption keys (data at rest) | 1 tahun | Scheduled, re-encrypt data |
| OAuth client secrets | 90 hari | Scheduled |

### 4.2 Rotation Procedure

```
1. Generate credential baru
2. Deploy credential baru alongside lama (dual-write/dual-read)
3. Verifikasi credential baru berfungsi di staging
4. Switch production ke credential baru
5. Monitor error rate selama overlap period (min 24 jam)
6. Revoke credential lama
7. Audit log: catat siapa, kapan, kenapa rotasi dilakukan
```

### 4.3 Leakage Detection

| Tool | Scope | Integration |
|---|---|---|
| `gitleaks` | Git history + staged files | Pre-commit hook + CI |
| `trufflehog` | Git history + filesystem | CI pipeline |
| `detect-secrets` | Codebase | Pre-commit + IDE plugin |
| GitHub Secret Scanning | Repository | Enable di repo settings |
| AWS GuardDuty / CloudTrail | Cloud credentials | Continuous monitoring |

**Response saat leak terdeteksi**:
1. Revoke credential segera (jangan investigasi dulu)
2. Generate credential baru
3. Assess blast radius: apa yang bisa diakses dengan credential tersebut?
4. Notify affected parties jika PII/data sensitif terekspos
5. Post-incident review: bagaimana leak terjadi, bagaimana mencegahnya lagi

---

## 5. Security Headers Baseline (Extended)

Melengkapi §8 di SKILL.md. Header ini wajib untuk production.

### 5.1 Mandatory Headers

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()
X-DNS-Prefetch-Control: off
Cache-Control: no-store (untuk response dengan data sensitif)
```

### 5.2 Content-Security-Policy Templates

**SPA dengan CDN:**
```
default-src 'self'; 
script-src 'self' 'nonce-{RANDOM}' https://cdn.example.com; 
style-src 'self' 'unsafe-inline'; 
img-src 'self' data: https:; 
font-src 'self' https://fonts.gstatic.com; 
connect-src 'self' https://api.example.com; 
frame-ancestors 'none'; 
base-uri 'self'; 
form-action 'self'
```

**API-only:**
```
default-src 'none'; 
frame-ancestors 'none'
```

**Server-rendered app:**
```
default-src 'self'; 
script-src 'self' 'nonce-{RANDOM}'; 
style-src 'self' 'nonce-{RANDOM}'; 
img-src 'self' data:; 
frame-ancestors 'none'
```

### 5.3 Validation

- Scan otomatis: [securityheaders.com](https://securityheaders.com) atau `curl -I` + parse
- CI integration: `testssl.sh` atau `observatory.mozilla.org` API
- Pre-deploy gate: block deployment jika mandatory headers missing

---

## 6. Supply Chain Security Tooling

Melengkapi §6 di SKILL.md. Tools spesifik per ekosistem.

| Ecosystem | Dependency Audit | Signature Verification | SBOM |
|---|---|---|---|
| npm | `npm audit`, `socket.dev` | `npm provenance` | `cyclonedx-npm` |
| pip | `pip-audit`, `safety` | `sigstore-python` | `cyclonedx-python` |
| Go | `govulncheck` | `cosign` | `syft` |
| Cargo | `cargo-audit` | `cosign` | `cargo-cyclonedx` |
| Maven | `dependency-check-maven` | `sigstore-java` | `cyclonedx-maven` |
| Docker | `trivy`, `grype` | `cosign` | `syft` |

### CI Integration Pattern

```yaml
# GitHub Actions example
- name: Dependency audit
  run: npm audit --audit-level=high
  
- name: SBOM generation  
  run: npx @cyclonedx/cyclonedx-npm --output-file sbom.json
  
- name: Container scan
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ${{ env.IMAGE }}
    severity: HIGH,CRITICAL
    exit-code: 1
```

---

## 7. Threat Model Output Template

Format standar untuk output STRIDE analysis. Gunakan ini agar hasil konsisten dan bisa direview.

```markdown
# Threat Model: [Nama Fitur/Sistem]

## Scope
- **Boundary**: [apa yang termasuk, apa yang tidak]
- **Data classification**: [PII, financial, public, internal]
- **Actors**: [user types, services, external systems]

## STRIDE Analysis

| # | Ancaman | Skenario Spesifik | Likelihood | Impact | Mitigasi | Status | Sisa Risiko |
|---|---------|-------------------|------------|--------|----------|--------|-------------|
| 1 | Spoofing | Attacker mencuri JWT dari log | Medium | High | Jangan log token, short expiry | ✅ Implemented | Low |
| 2 | Tampering | Modifikasi price di cart sebelum checkout | High | Critical | Server-side price recalculation | ⚠️ Planned | Medium |
| ... | ... | ... | ... | ... | ... | ... | ... |

## Mitigations Priority Matrix

| Priority | Threat # | Action | Owner | Deadline |
|----------|----------|--------|-------|----------|
| P0 | 2 | Implement server-side price validation | Backend team | Sprint 3 |
| P1 | 1 | Add token redaction to logger | DevOps | Sprint 2 |

## Assumptions & Constraints
- [asumsi yang dibuat selama modeling]
- [constraint yang membatasi mitigasi]

## Review
- **Reviewed by**: [nama]
- **Date**: [YYYY-MM-DD]
- **Next review**: [date atau trigger condition]
```

Status values: `✅ Implemented`, `⚠️ Planned`, `❌ Not addressed`, `🔄 In progress`.
