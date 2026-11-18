# Security Playbook

Execution reference for `maxilun-sentinel`. It contains templates, catalogs, and patterns to apply directly, not general principles.

---

## 1. Trust Boundary Catalog

A trust boundary is a point where data moves from a trusted zone to an untrusted zone, or the reverse. Give every boundary explicit validation.

| Trust Boundary | Input Source | Required Validation | Example Attack If Skipped |
|---|---|---|---|
| **HTTP API Endpoint** | Request body, query params, headers | Schema validation (Zod/Joi), type coercion, length limits | SQL injection, parameter tampering, mass assignment |
| **Form Submission** | Form fields, file uploads | Server-side validation (not client-only), CSRF token, file type whitelist | XSS stored, path traversal, CSRF |
| **File Upload** | Binary content, filename, MIME type | Magic byte verification, size limit, sandboxed storage, no execution permission | Remote code execution, directory traversal |
| **Environment Variable** | Process env, .env files | Type parsing, secret detection, no logging | Secret leakage, type confusion |
| **Database Query** | User-supplied filter/sort/search | Parameterized queries only, no string concatenation | SQL injection, data exfiltration |
| **External API Response** | Third-party JSON/XML/HTML | Response schema validation, timeout, circuit breaker | Supply chain attack, data poisoning |
| **WebSocket Message** | Real-time client messages | Same validation as HTTP API, rate limiting per connection | Injection, resource exhaustion |
| **CLI Argument** | Command-line input | Argument parsing library, no eval/exec, sanitize shell metacharacters | Command injection, argument injection |
| **Config File** | YAML/JSON/TOML from disk | Schema validation, no code execution in config parser | Config injection, arbitrary code execution |
| **Inter-Service Call** | gRPC/REST between microservices | mTLS or service mesh auth, request signing, zero trust network | Lateral movement, service impersonation |

### Application Rules

1. **Identify every trust boundary** before writing code. Use the table above as the checklist.
2. **Validate on the receiving side**, not the sending side. Client-side validation is a UX enhancement, not a security control.
3. **Fail closed**: when validation fails, reject the request. Do not fall back to a more permissive default behavior.
4. **Log rejections**: log every failed validation with context, without logging sensitive data.
5. **Review on change**: whenever you add an endpoint, field, or integration, check whether it creates a new trust boundary.

---

## 2. Security Test Patterns (for maxilun-verify)

Security test patterns that integrate into CI/CD. Each pattern has a trigger condition, a test method, and pass criteria.

### 2.1 Authentication & Authorization Tests

| Pattern | Method | Pass Criteria |
|---|---|---|
| **Auth bypass** | Send a request to a protected endpoint without a token | 401/403, not 200 or 500 |
| **Expired token** | Use a JWT with `exp` in the past | 401 with the message "token expired" |
| **Privilege escalation** | A regular user accesses an admin endpoint | 403, not 200 |
| **IDOR** | Replace the resource ID in the URL/body with another user's | 403/404, not 200 with someone else's data |
| **Session fixation** | Check that the session ID changes after login | New session ID, not a reused one |
| **Brute force protection** | Send 10+ consecutive failed logins | Account locked or rate limited after N attempts |

### 2.2 Injection Tests

| Pattern | Method | Pass Criteria |
|---|---|---|
| **SQL injection** | Input `' OR 1=1 --` in a search/filter field | No DB error, result empty or filtered |
| **XSS reflected** | Input `<script>alert(1)</script>` in a query param | Output escaped or blocked, script does not execute |
| **XSS stored** | Submit an XSS payload through a form, reload the page | Payload does not render as HTML |
| **Command injection** | Input `; ls /etc/passwd` in a field processed by a shell | Command does not execute, input rejected |
| **Path traversal** | Input `../../etc/passwd` in a file path param | Path canonicalized, access denied |
| **Template injection** | Input `{{7*7}}` or `${7*7}` in user input | No server-side expression evaluation |

### 2.3 Data Protection Tests

| Pattern | Method | Pass Criteria |
|---|---|---|
| **Sensitive data in logs** | Trigger an operation with PII/tokens, check log output | No plaintext password, token, or PII in logs |
| **Sensitive data in error** | Trigger an error with sensitive input | Generic error message, no leaked stack trace or data |
| **Encryption at rest** | Check the database/storage for sensitive fields | Encrypted or hashed, not plaintext |
| **TLS enforcement** | Access over HTTP (non-TLS) | Redirect to HTTPS or connection refused |
| **Data minimization** | Check the API response for fields that were not requested | Only the required fields are returned |

### 2.4 Rate Limiting & DoS Tests

| Pattern | Method | Pass Criteria |
|---|---|---|
| **API rate limit** | Send >limit requests within the window | 429 after the threshold, with a Retry-After header |
| **Login rate limit** | >N failed login attempts | Lockout or CAPTCHA challenge |
| **Large payload** | Send a request body >size limit | 413 Payload Too Large |
| **Slowloris** | Open a connection, send a partial request slowly | Connection timeout after N seconds |

### 2.5 Integration with maxilun-verify

Add a security tier after Tier 4 (Regression):

```
Tier 5: Security Validation
├── Auth/Authz tests (2.1)
├── Injection tests (2.2)  
├── Data protection tests (2.3)
└── Rate limiting tests (2.4)
```

Every PR that changes authentication, authorization, input handling, or data storage **must** run Tier 5. A PR that changes only UI/copy may skip Tier 5.

---

## 3. Cryptographic Implementation Reference

Code templates per platform. Do not implement crypto from scratch; use an audited library.

### 3.1 Password Hashing

| Platform | Library | Function | Notes |
|---|---|---|---|
| Node.js | `argon2` | `argon2.hash(password, {type: argon2.id})` | Argon2id preferred. Fallback: bcrypt cost ≥12 |
| Python | `argon2-cffi` | `PasswordHasher().hash(password)` | Argon2id default |
| Go | `golang.org/x/crypto/argon2` | `argon2.IDKey()` | Manual salt generation required |
| Rust | `argon2` crate | `Argon2::default().hash_password()` | Argon2id default |
| Java | `spring-security-crypto` | `Argon2PasswordEncoder` | Spring Boot standard |

**Do not use**: MD5, SHA-1/256 for passwords, custom hashing, XOR cipher.

### 3.2 Symmetric Encryption (Data at Rest)

| Platform | Library | Algorithm | Mode |
|---|---|---|---|
| Node.js | `crypto` (built-in) | AES-256-GCM | `createCipheriv('aes-256-gcm', ...)` |
| Python | `cryptography` | AES-256-GCM | `AESGCM(key).encrypt(nonce, data, aad)` |
| Go | `crypto/aes` + `crypto/cipher` | AES-256-GCM | `cipher.NewGCM(block)` |
| Rust | `aes-gcm` crate | AES-256-GCM | `Aes256Gcm::new(&key)` |

**Required**: unique nonce per encryption, authenticated encryption (GCM/ChaCha20-Poly1305), key from a KMS, not hardcoded.

### 3.3 Token Signing (JWT)

| Platform | Library | Algorithm | Notes |
|---|---|---|---|
| Node.js | `jose` | ES256 or RS256 | Avoid HS256 except for a single service |
| Python | `PyJWT` | RS256 | `jwt.encode(payload, private_key, algorithm="RS256")` |
| Go | `golang-jwt/jwt/v5` | RS256 | `jwt.NewWithClaims(jwt.SigningMethodRS256, claims)` |
| Rust | `jsonwebtoken` | RS256 | `encode(&Header::new(Algorithm::RS256), &claims, &key)` |

**Do not**: use alg:none, use HS256 with a shared secret across multiple services, or store sensitive data in the JWT payload (base64 ≠ encrypted).

### 3.4 Secure Random

| Platform | Function | Notes |
|---|---|---|
| Node.js | `crypto.randomBytes(n)` | Not Math.random() |
| Python | `secrets.token_bytes(n)` | Not the random module |
| Go | `crypto/rand.Read(buf)` | Not math/rand |
| Rust | `rand::rngs::OsRng` | Not rand::thread_rng() for crypto |
| Browser | `crypto.getRandomValues(buf)` | Not Math.random() |

---

## 4. Secrets Rotation Protocol

A structured secret rotation procedure. Do not rotate ad hoc.

### 4.1 Rotation Schedule

| Secret Type | Rotation Frequency | Trigger |
|---|---|---|
| Database credentials | 90 days | Scheduled + on compromise |
| API keys (third-party) | Per provider policy | Check provider docs |
| JWT signing keys | 30 days | Scheduled, overlap period 7 days |
| TLS certificates | Before expiry | Automated via cert-manager/Let's Encrypt |
| SSH keys | 1 year | Scheduled + on personnel change |
| Encryption keys (data at rest) | 1 year | Scheduled, re-encrypt data |
| OAuth client secrets | 90 days | Scheduled |

### 4.2 Rotation Procedure

```
1. Generate the new credential
2. Deploy the new credential alongside the old one (dual-write/dual-read)
3. Verify the new credential works in staging
4. Switch production to the new credential
5. Monitor the error rate during the overlap period (min 24 hours)
6. Revoke the old credential
7. Audit log: record who rotated, when, and why
```

### 4.3 Leakage Detection

| Tool | Scope | Integration |
|---|---|---|
| `gitleaks` | Git history + staged files | Pre-commit hook + CI |
| `trufflehog` | Git history + filesystem | CI pipeline |
| `detect-secrets` | Codebase | Pre-commit + IDE plugin |
| GitHub Secret Scanning | Repository | Enable in repo settings |
| AWS GuardDuty / CloudTrail | Cloud credentials | Continuous monitoring |

**Response when a leak is detected**:
1. Revoke the credential immediately (do not investigate first)
2. Generate a new credential
3. Assess the blast radius: what can that credential access?
4. Notify affected parties if PII/sensitive data was exposed
5. Post-incident review: how the leak happened, how to prevent it again

---

## 5. Security Headers Baseline (Extended)

Extends the HTTP security header policy in `SKILL.md`. These headers are required for production services.

### 5.1 Mandatory Headers

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains
# Note: add '; preload' only if the apex & every subdomain permanently support HTTPS
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()
X-DNS-Prefetch-Control: off
Cache-Control: no-store (for responses with sensitive data)
```

### 5.2 Content-Security-Policy Templates

**SPA with CDN:**
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

- Automated scan: [securityheaders.com](https://securityheaders.com) or `curl -I` + parse
- CI integration: `testssl.sh` or the `observatory.mozilla.org` API
- Pre-deploy gate: block the deployment if mandatory headers are missing

---

## 6. Supply Chain Security Tooling

Extends the supply chain policy in `SKILL.md`. Specific tools per ecosystem.

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

Standard format for STRIDE analysis output. Use it so results stay consistent and reviewable.

```markdown
# Threat Model: [Feature/System Name]

## Scope
- **Boundary**: [what is included, what is not]
- **Data classification**: [PII, financial, public, internal]
- **Actors**: [user types, services, external systems]

## STRIDE Analysis

| # | Threat | Specific Scenario | Likelihood | Impact | Mitigation | Status | Residual Risk |
|---|---------|-------------------|------------|--------|----------|--------|-------------|
| 1 | Spoofing | Attacker steals a JWT from the logs | Medium | High | Do not log tokens, short expiry | ✅ Implemented | Low |
| 2 | Tampering | Price modified in the cart before checkout | High | Critical | Server-side price recalculation | ⚠️ Planned | Medium |
| ... | ... | ... | ... | ... | ... | ... | ... |

## Mitigations Priority Matrix

| Priority | Threat # | Action | Owner | Deadline |
|----------|----------|--------|-------|----------|
| P0 | 2 | Implement server-side price validation | Backend team | Sprint 3 |
| P1 | 1 | Add token redaction to logger | DevOps | Sprint 2 |

## Assumptions & Constraints
- [assumptions made during modeling]
- [constraints that limit mitigation]

## Review
- **Reviewed by**: [name]
- **Date**: [YYYY-MM-DD]
- **Next review**: [date or trigger condition]
```

Status values: `✅ Implemented`, `⚠️ Planned`, `❌ Not addressed`, `🔄 In progress`.

---

## 8. DPoP (RFC 9449) & Sender-Constrained Tokens

Use **Demonstrating Proof-of-Possession at the Application Layer (DPoP)** to bind an access token to the client's cryptographic key pair. A token stolen from server logs, a proxy cache, or a network leak then cannot be replayed by an attacker (*Anti-Token-Replay*).

### 8.1 DPoP Verification Mechanism

1. **The client creates the proof JWT**:
   On every request to a DPoP-protected API, the client signs an ephemeral JWT with its local private key:
   ```http
   POST /api/v1/transfers HTTP/1.1
   Host: api.example.com
   Authorization: DPoP eyJhbGciOiJFUzI1Ni... (access_token)
   DPoP: eyJ0eXAiOiJkcG9wK2p3dCIsImFsZyI6IkVTMjU2IiwiandrIjp7...}}... (proof_jwt)
   ```

2. **Proof JWT header & claims**:
   - Header: `typ: "dpop+jwt"`, `alg: "ES256"`, `jwk: { kty: "EC", crv: "P-256", x: "...", y: "..." }`
   - Payload:
     - `htm`: HTTP method verbatim (`POST`, `GET`, etc.)
     - `htu`: HTTP target URI without the query string (`https://api.example.com/api/v1/transfers`)
     - `iat`: Issued-at timestamp (must fall within a clock drift tolerance of $\le 300\text{s}$)
     - `jti`: Unique nonce/ID that prevents replay of the same proof

3. **Checks on the resource server**:
   - Verify that `typ` equals `dpop+jwt` and that the signature is valid under the JWK included in the proof header.
   - Compute the SHA-256 thumbprint of the client JWK (`jkt`).
   - Match that `jkt` against the `cnf.jkt` confirmation claim embedded in the `access_token` payload. On mismatch, reject with HTTP `401 Unauthorized`.
   - Validate that `htm` and `htu` match the active request to prevent cross-endpoint proof misuse.

---

## 9. Least-Privilege Authorization Policy Simulation

Prevent *privilege escalation* and *over-privileged roles* by validating policy pre-flight, before a data mutation runs:

### 9.1 Authorization Policy Evaluation Matrix
Evaluate every request with an explicit quartet:
`Evaluate(Principal, Action, Resource, Context) -> ALLOW | DENY (Deny by default)`

| Component | Evaluated Values | Security Validation |
|---|---|---|
| **Principal** | `userId`, `tenantId`, `roles`, `scopes` | Taken solely from the server-verified token/session, never from client input |
| **Action** | Domain operation (`invoice:create`, `user:delete`) | Explicit action allowlist; reject wildcard `*` in production |
| **Resource** | Target entity (`invoice:1042`) | Verify tenant ownership via PostgreSQL RLS or a server guard |
| **Context** | Time, IP allowlist, MFA level, auth freshness | Evaluate whether a sensitive operation needs step-up re-authentication |

### 9.2 Pre-Flight Policy Simulator in CI & Unit Tests
Write deterministic policy tests for every role before release:
```typescript
// Example authorization policy simulation (Deny by default)
describe("Authorization Policy Simulator", () => {
  it("denies a regular member access to the tenant administration endpoint", () => {
    const decision = evaluateAccess({
      principal: { userId: "u-1", tenantId: "t-1", role: "member" },
      action: "tenant:billing:update",
      resource: { tenantId: "t-1" }
    });
    expect(decision).toBe("DENY");
  });
});
```
