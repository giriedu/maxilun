# Triage & Verification Gate: Proof-Driven Finding Validation

Protocol for validating security findings with no room for speculation. Drop any finding that cannot be proven independently before it reaches a report.

---

## 1. The 7-Question Gate

Evaluate every finding through the 7 gate questions in order. **One failed answer = the finding is dropped (KILL) immediately.**

```text
[Q1: Direct Execution?]   ──(Fail)──> [DROP: Cannot be reproduced]
         │ (Pass)
[Q2: Real Impact?]        ──(Fail)──> [DROP: Outside the impact criteria]
         │ (Pass)
[Q3: In-Scope Asset?]     ──(Fail)──> [DROP: Outside the target boundary]
         │ (Pass)
[Q4: Realistic Privileges?]──(Fail)──> [DROP: Centralization risk / admin only]
         │ (Pass)
[Q5: Not Intended Behavior?] (Fail)─> [DROP: Deliberate design]
         │ (Pass)
[Q6: Proof Beyond Theory?] (Fail)──> [LOWER THE SEVERITY / DOWNGRADE]
         │ (Pass)
[Q7: Clear of the Blacklist?] ──(Fail)──> [DROP: On the Never-Submit list]
         │ (Pass)
     [VALID FINDING]
```

### Gate Details

1. **Q1: Can an attacker execute it RIGHT NOW, step by step?**
   - Required format: a complete HTTP request (method, URL, headers, body) ready to replay with curl.
   - If you cannot write a request that produces direct proof -> **DROP**.
2. **Q2: Is the impact on the list of impacts the program/organization recognizes?**
   - The vulnerability must cause real harm: private data theft, unauthorized data modification, account takeover (ATO), or code execution (RCE).
   - If the impact is only public information or a documented exception -> **DROP**.
3. **Q3: Is the root cause in an in-scope asset?**
   - Confirm the domain/host is listed explicitly in the scope.
   - If the domain belongs to a third party (SaaS, external identity provider) -> **DROP**.
4. **Q4: Does the attacker need unrealistic privileges?**
   - An action only the primary administrator can perform (*Admin can do X*) is a centralization-of-authority risk, not a security flaw -> **DROP**.
   - Valid privilege cases: a regular user performs an admin action (*privilege escalation*), or user A accesses user B's data.
5. **Q5: Is this behavior already known or intended by the system design?**
   - Check the official product documentation, release notes, and earlier public issues.
   - If the behavior is a deliberate feature -> **DROP**.
6. **Q6: Can you prove real impact beyond "technically possible"?**
   - SSRF: Must return a data payload from an internal service, not only a DNS ping callback.
   - SQLi: Must extract data from a real table or demonstrate a measured time delay, not merely trigger a 500 error message.
   - If you can prove only theoretical possibility -> **DOWNGRADE**.
7. **Q7: Is this finding in an automatically rejected class (*Never-Submit*)?**
   - Check the Never-Submit table below. If it matches and stands alone without an exploit chain -> **DROP**.

---

## 2. Never-Submit Table (Automatic False-Positive Elimination)

Do not report the findings in this table on their own, because they do not prove real exploitation risk:

| Initial Indication | Reason for Unconditional Drop | Exception Condition (Exploit Chain Required) |
|---|---|---|
| **CORS Wildcard / Reflected** | Without `Access-Control-Allow-Credentials: true`, the victim's session data cannot be extracted to the attacker's domain | Proven extraction of authenticated PII through session credentials |
| **Nuclei / Scanner Info Banner** | Detecting a framework or web server version is not proof of a vulnerability (*version banner disclosure*) | An active CVE with a proven exploit exists for that version |
| **SSRF DNS Callback Only** | OOB DNS interaction is often triggered by an intermediate proxy or web filter, not the target backend | The response contains cloud metadata service data or a private internal port |
| **Self-XSS** | The attacker only executes script in their own browser | Chained with a CSRF flaw on an endpoint that injects the payload into the victim |
| **Missing HTTP Security Headers** | Missing CSP, HSTS, or X-Frame-Options is not an active vulnerability without an attack scenario | Clickjacking proven to trigger a transaction without the user's conscious interaction |
| **Open Redirect Without a Chain** | A bare URL redirect is rated low by most programs | Chained with an OAuth `redirect_uri` token leak or Account Takeover |
| **Logout CSRF** | Forcing the victim out of their session gives the attacker no access gain | No exception (always dropped) |
| **Missing Rate Limiting** | A static page or general search without a rate limit is not a vulnerability | A login/OTP endpoint open to *credential stuffing* or double financial mutation |

---

## 3. Deterministic Verification Engine (The Verification Spine)

A four-value status engine controls report decisions and rejects claims without evidence:

```text
               ┌───────────────────────┐
               │   Evaluate Finding    │
               └───────────┬───────────┘
                           │
             Complete Evidence Bundle?
              ├── NO ─────────────────────────────────> [UNPROVEN] (Suppressed)
              └── YES
                   │
               Run Re-Derivation
              ├── Connection failed / Mutation method not tested -> [INCONCLUSIVE] (Held)
              ├── Vulnerability marker MISSING from the fresh response -> [REFUTED] (Suppressed)
              └── Vulnerability marker FOUND in the fresh response -> [PROVEN] (REPORTABLE)
```

### Decision Status Definitions

- **`PROVEN`**:
  - Has complete baseline HTTP exchange evidence.
  - An independent re-derivation ran successfully and the *confirmation marker* reappears in the fresh response.
  - **The only status allowed to produce a final report.**
- **`REFUTED`**:
  - The re-derivation sent the request, but the vulnerability marker is absent from the fresh response (for example: the endpoint is now protected or returns 403).
  - Status: Suppressed (not reported).
- **`UNPROVEN`**:
  - Has no request/response evidence bundle, or the vulnerability marker is not defined measurably.
  - Status: Suppressed (not reported).
- **`INCONCLUSIVE`**:
  - The re-derivation could not complete (target unreachable, credentials missing, or a dangerous mutation request was stopped for safety).
  - Status: Held in the follow-up evaluation queue; do not report it.

---

## 4. CVSS 3.1 Severity Matrix & Decision Making

Use the CVSS 3.1 standard with a measured vector, not a subjective estimate:

| Severity Level | CVSS Score | Required Evidence Characteristics | Example Classes |
|---|---|---|---|
| **Critical** | 9.0 – 10.0 | No user interaction, full remote access, mass ATO | RCE, SQLi with full data exfiltration, admin Auth Bypass |
| **High** | 7.0 – 8.9 | Cross-tenant read/write access to private data, proven privilege escalation | IDOR with data mutation, SSRF to cloud metadata, Stored XSS |
| **Medium** | 4.0 – 6.9 | Limited data read access, requires specific user interaction | IDOR on non-sensitive data, Reflected XSS with a victim click |
| **Low** | 0.1 – 3.9 | High prerequisites, limited information impact | Minor open redirect, Clickjacking on an informational page |
| **Informational** | 0.0 | Architecture observation without an exploit scenario | Version banner, debug error without credentials |
