# Maxilun Hunt Reference Corpus

Quick navigation index for the playbooks, verification matrices, and reporting standards for adversarial vulnerability findings:

- **[Vulnerability Hunt Playbook](vulnerability-hunt-playbook.md)**: Adversarial methodology, attack surface mapping, sibling endpoint testing, multi-session IDOR variants, auth bypass, blind SSRF, race conditions, and non-destructive safety governance.
- **[Triage & Verification Gate](triage-verification-gate.md)**: The 7-Question Gate, the false-positive elimination table (never-submit list), the CVSS 3.1 severity decision tree, and the deterministic status engine (`PROVEN`, `REFUTED`, `UNPROVEN`, `INCONCLUSIVE`).
- **[Evidence & Reporting Standard](evidence-reporting-standard.md)**: Reproducible evidence bundle structure (`request.http`, `response.http`, `repro.sh`, SHA-256 manifest), the secret redaction standard (`$AUTHORIZATION`, `$COOKIE`), and the business-impact report format.
