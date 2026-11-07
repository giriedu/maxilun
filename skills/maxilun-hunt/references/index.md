# Maxilun Hunt Reference Corpus

Indeks navigasi cepat untuk playbooks, matriks verifikasi, dan standar pelaporan temuan kerentanan adversarial:

- **[Vulnerability Hunt Playbook](vulnerability-hunt-playbook.md)**: Metodologi adversarial, pemetaan attack surface, pengujian sibling endpoints, varian IDOR multi-session, bypass auth, blind SSRF, race condition, dan tata kelola keamanan non-destruktif.
- **[Triage & Verification Gate](triage-verification-gate.md)**: 7-Question Gate, tabel eliminasi false-positive (never-submit list), pohon keputusan keparahan CVSS 3.1, dan mesin status deterministik (`PROVEN`, `REFUTED`, `UNPROVEN`, `INCONCLUSIVE`).
- **[Evidence & Reporting Standard](evidence-reporting-standard.md)**: Struktur paket bukti reproducible (`request.http`, `response.http`, `repro.sh`, manifest SHA-256), standar redaksi rahasia (`$AUTHORIZATION`, `$COOKIE`), dan format pelaporan berdampak bisnis.
