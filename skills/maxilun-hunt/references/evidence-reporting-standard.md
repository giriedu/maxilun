# Evidence & Reporting Standard: Reproducible Proofs & Redaction

Standard for assembling vulnerability reproduction evidence that anyone can re-run, that leaks no secrets, and that the engineering team can act on directly.

---

## 1. Reproducible Evidence Bundle Structure

Store every finding that passes verification in a deterministic directory layout:

```text
findings/<target>-<vuln-class>/evidence/<finding-id>/
├── request.http       # Complete raw request (method, path, headers, body)
├── response.http      # Complete raw response (status, headers, proof body)
├── repro.sh           # Standalone curl command using environment variables
├── evidence.har       # HAR 1.2 recording for import into a proxy/analysis tool
├── manifest.json      # Metadata, ISO timestamp, body SHA-256, and marker
└── report-draft.md    # Industry-standard report draft, ready to hand over
```

### Main File Formats

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
# Standalone reproduction — supply active credentials through environment variables
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

## 2. Secret Redaction Standard (Secrets Hygiene)

Every artifact saved to disk or copied into a report draft **must pass through secret redaction**:

1. **Sensitive headers to redact**:
   - `Authorization`, `Proxy-Authorization`
   - `Cookie`, `Set-Cookie`
   - `X-Api-Key`, `Api-Key`, `X-Auth-Token`
   - `X-Session-Token`, `X-CSRF-Token`
2. **Rules for writing `repro.sh`**:
   - Never put a plaintext token or password string in the script.
   - Reference secret values through environment variables: `${AUTHORIZATION}`, `${COOKIE}`.
3. **PII filtering**:
   - Mask any victim credit card number, national identity number, or phone number captured unintentionally: `4111-XXXX-XXXX-1234`.

---

## 3. Report Title Formula

Keep the report title short and specific, and lead with business impact:

```text
[Flaw Class] in [Specific Endpoint / Feature] allows [Attacker Role] to [Real Impact] [Victim Scope]
```

### Effective vs Ineffective Titles
- **Effective**:
  - `IDOR in GET /api/v2/invoices/{id} allows an authenticated user to read another tenant's invoices`
  - `Broken Authentication in POST /api/admin/users/invite allows a regular user to invite admin-role accounts`
  - `SSRF in the imageUrl parameter of /api/export extracts internal AWS EC2 metadata`
- **Ineffective (rejected)**:
  - `Security flaw on the website` (too generic)
  - `IDOR bug found` (no endpoint or impact detail)
  - `Potential XSS flaw` (theoretical language)

---

## 4. Finding Submission Report Format

```markdown
# Security Finding Report: [Title Per Formula]

## 1. Executive Summary
One dense paragraph that states what the flaw is, where it is, the prerequisites the attacker needs, and the direct harm to the system.

## 2. Vulnerability Details
- **Vulnerability Class**: Insecure Direct Object Reference (IDOR)
- **CWE / OWASP**: CWE-639 / OWASP A01:2021-Broken Access Control
- **CVSS 3.1 Score**: 6.5 (Medium) — `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N`
- **Affected Endpoint**: `POST /api/v2/workspaces/{id}/members`

## 3. Measured Reproduction Steps
1. Prepare Account A (Attacker, ID: 101) and Account B (Victim, Workspace ID: 9102).
2. Obtain an access token for Account A.
3. Run the following request with Account A's credentials against Account B's workspace:
   ```bash
   curl -i -X POST "https://api.target.com/api/v2/workspaces/9102/members" \
     -H "Authorization: Bearer ${ACCOUNT_A_TOKEN}" \
     -H "Content-Type: application/json" \
     -d '{"user_id": 101, "role": "admin"}'
   ```
4. Observe the response:
   ```json
   HTTP/1.1 200 OK
   {"success": true, "workspace_id": 9102, "role": "admin"}
   ```
   Account A was added as an admin to Account B's workspace without the owner's permission.

## 4. Proof of Real Impact
The HTTP 200 response above proves that the workspace member entity was mutated directly, without validating whether the request sender holds administrative authority over workspace 9102. An attacker can take full ownership of another tenant's workspace.

## 5. Fix Recommendation for the Engineering Team
In the handler `src/controllers/workspaceMembers.ts:45`, add an ownership check before the mutation:
```typescript
const isOwner = await db.workspaces.findFirst({
  where: { id: workspaceId, ownerId: req.session.userId }
});
if (!isOwner) {
  return res.status(404).json({ error: "Workspace not found" });
}
```
Hand the code fix to `maxilun-engineer` and verify the regression through `maxilun-verify`.
```
