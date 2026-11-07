"""Maxilun Reversibility-Gated Triage & Specialist Router.

Simulates the Master Orchestrator decision logic:
- Type 1 (Irreversible / High-Cost) vs Type 2 (Reversible / Low-Cost) classification
- Single-owner routing across the 21 specialists
- Conditional companion attachment at hard capability boundaries
- Pre-flight Knowledge Graph inspection recommendation
"""

import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class RoutingDecision:
    prompt: str
    primary_owner: str
    reversibility: str  # "Type 1 (Irreversible)" or "Type 2 (Reversible)"
    decision_type: int  # 1 or 2
    companions: List[str] = field(default_factory=list)
    pre_flight: str = ""
    rationale: str = ""
    is_multi_domain: bool = False
    waves: List[dict] = field(default_factory=list)
    handoff_record: str = ""

    def summary(self) -> str:
        lines = [
            f"Prompt: \"{self.prompt}\"",
            f"Primary Owner: {self.primary_owner}",
            f"Reversibility: {self.reversibility}",
            f"Companions: {', '.join(self.companions) if self.companions else 'None (single cohesive owner)'}",
            f"Multi-Domain: {'Yes (Multi-Wave Coordination Required)' if self.is_multi_domain else 'No (Single-Owner Execution)'}",
            f"Pre-flight: {self.pre_flight}",
            f"Rationale: {self.rationale}",
        ]
        if self.waves:
            lines.append("\nOrchestration Waves:")
            for w in self.waves:
                specs = ", ".join(w.get("specialists", []))
                lines.append(f"  - [{w.get('name')}]: {specs} -> {w.get('goal')}")
        if self.handoff_record:
            lines.append(f"\nFormal Handoff Record:\n{self.handoff_record}")
        return "\n".join(lines)


class MaxilunRouter:
    """Deterministic routing and decision reversibility classifier."""

    TYPE_1_KEYWORDS = [
        "drop column", "drop table", "migrasi destruktif", "pemecahan service",
        "redesign total dari nol", "greenfield identity", "multi-tenant isolation",
        "breaking change", "kontrak publik baru", "delete production data",
        "split monolith", "schema split"
    ]

    def route(self, prompt: str) -> RoutingDecision:
        p = prompt.lower()

        # 1. Reversibility Triage (Type 1 vs Type 2)
        is_type_1 = any(kw in p for kw in self.TYPE_1_KEYWORDS)
        if is_type_1:
            reversibility = "Type 1 (Irreversible / High-Cost — max 1 batched clarification turn)"
            decision_type = 1
        else:
            reversibility = "Type 2 (Reversible / Low-Cost — execute directly from repo evidence)"
            decision_type = 2

        # 2. Single Cohesive Owner Assignment
        owner = "maxilun-engineer"
        companions = []
        pre_flight = "Inspect callers via callsIn: or read affected file range before modifying."
        rationale = "General production code modification or feature implementation."
        def match_tokens(tokens: List[str]) -> bool:
            for tok in tokens:
                if len(tok) <= 4 and tok.isalpha():
                    if re.search(rf"\b{re.escape(tok)}\b", p):
                        return True
                elif tok in p:
                    return True
            return False

        if any(k in p for k in ["login", "auth", "token", "password", "oauth", "jwt", "csrf", "xss", "keamanan", "enkripsi", "secret", "totp"]):
            owner = "maxilun-sentinel"
            rationale = "Authentication, authorization, or trust-boundary hardening."
            pre_flight = "Review trust boundaries, secrets storage, and session lifecycles."
            if any(k in p for k in ["tabel", "skema", "db", "user table"]):
                companions.append("maxilun-data")

        elif any(k in p for k in ["webhook", "signature", "hmac"]):
            owner = "maxilun-sentinel"
            companions.append("maxilun-data")
            rationale = "Cryptographic webhook signature verification and idempotent payload mutation."
            pre_flight = "Check webhook replay window, raw body HMAC, and database idempotency table."

        elif any(k in p for k in ["landing page", "desain ui", "redesign", "komponen ui", "sistem desain", "ui/ux", "tampilan", "dashboard", "halaman web", "website", "logo svg", "brand identity"]):
            owner = "maxilun-craft"
            rationale = "Domain-authentic visual design, OKLCH tokens, 4 UI states, or brand assets."
            pre_flight = "Select 1-2 matching design systems from references/design-md/ and verify tokens."
            if any(k in p for k in ["next.js", "nextjs", "react", "app router", "rsc", "server action"]):
                companions.append("maxilun-frontend")

        elif any(k in p for k in ["app router", "rsc", "server component", "server action", "next.js", "nextjs", "hydration", "flight"]):
            if any(k in p for k in ["halaman", "landing", "tampilan", "ui", "dashboard", "web", "desain"]):
                owner = "maxilun-craft"
                companions.append("maxilun-frontend")
                rationale = "Domain-authentic visual design grounded in design-md/ with Next.js App Router wiring."
                pre_flight = "Select 1-2 matching design systems from references/design-md/ and verify App Router topology."
            else:
                owner = "maxilun-frontend"
                rationale = "Next.js 15 App Router topology, RSC vs Client boundaries, or Server Actions."
                pre_flight = "Check existing app/ directory layout and 'use client' leaf boundary placement."
        elif match_tokens(["powerbuilder", "datawindow", "powerscript", "sqlca", "aplikasi desktop", "windows desktop", "win32", "wpf", "winui", "macos desktop", "appkit", "qt", "tauri", "desktop app"]):
            owner = "maxilun-desktop"
            rationale = "Desktop application engineering (Win32, WPF, AppKit, Qt) or PowerBuilder enterprise systems."
            pre_flight = "Check UI thread message loop separation and verify database transaction or native window handle balance."
            if any(k in p for k in ["tabel", "skema", "database", "query"]):
                companions.append("maxilun-data")

        elif match_tokens(["android", "ios", "flutter", "react native", "swiftui", "jetpack compose", "kotlin mobile", "swift mobile", "kmp", "mobile app", "aplikasi mobile", "apk", "ipa", "xcode", "gradle android"]):
            owner = "maxilun-mobile"
            rationale = "Native Android/iOS or cross-platform mobile application development."
            pre_flight = "Check thread isolation (MainActor / Dispatchers.IO) and verify touch ergonomics & lifecycle memory bounds."

        elif match_tokens(["iot", "embedded", "esp32", "esp8266", "arduino", "stm32", "raspberry pi", "pico", "micropython", "firmware", "freertos", "modbus", "ble", "sensor", "gpio", "i2c", "spi", "uart"]):
            owner = "maxilun-iot"
            rationale = "Embedded systems, microcontroller firmware, hardware buses, and IoT telemetry."
            pre_flight = "Audit ISR memory allocations (zero-heap rule), task stack sizes, and watchdog feeding invariants."

        elif match_tokens(["mikrotik", "routeros", "jaringan", "firewall", "wireguard", "vlan", "routing", "bandwidth", "queue tree", "winbox", "nftables", "bgp", "ospf", "switch", "iproute2"]):
            owner = "maxilun-network"
            rationale = "Network engineering, MikroTik RouterOS automation, Linux networking, and firewall routing policies."
            pre_flight = "Inspect default-drop firewall policy, interface lists, and verify routing table convergence."

        elif match_tokens(["rag", "retrieval augmented", "vector search", "embedding", "embeddings", "prompt eval", "context caching", "llm app", "rerank", "chunking", "vector database", "pgvector", "qdrant"]):
            owner = "maxilun-ai"
            rationale = "AI & LLM engineering, deterministic RAG retrieval, prompt evals, or context caching."
            pre_flight = "Inspect document chunking boundaries, hybrid search weights, and prompt regression rubrics."
            if any(k in p for k in ["tabel", "skema", "db", "pgvector"]):
                companions.append("maxilun-data")

        elif any(k in p for k in ["skema", "tabel", "database", "migrasi", "index", "query plan", "rls", "postgres", "sql", "explain"]):
            owner = "maxilun-data"
            rationale = "Physical schema modeling, expand-contract migrations, indexing, or RLS isolation."
            pre_flight = "Check existing ORM models, migration lockfiles, and EXPLAIN query plan."

        elif any(k in p for k in ["root cause", "kenapa lambat", "memory leak", "audit kode", "diagnosis", "profiling"]):
            owner = "maxilun-insight"
            rationale = "Diagnostic symptom tracing and blast-radius investigation before writing fixes."
            pre_flight = "Run Knowledge Graph query callsIn: to map callers of the failing codepath."

        elif any(k in p for k in ["arsitektur", "microservice", "batas modul", "adr", "migration plan", "system design"]):
            owner = "maxilun-architect"
            rationale = "Module boundary definition, cross-service contracts, or architecture decision records."
            pre_flight = "Evaluate bounded contexts, deep module seams, and failure mode invariants."

        elif any(k in p for k in ["diagram", "sequence diagram", "er diagram", "mermaid"]):
            owner = "maxilun-diagrams"
            rationale = "Structural architecture, sequence, or entity-relationship diagram authoring."
            pre_flight = "Extract confirmed entities and relationships from codebase or schema."

        elif any(k in p for k in ["video", "remotion", "mp4", "webm", "render video"]):
            owner = "maxilun-cinecode"
            companions.append("maxilun-motion")
            rationale = "Programmatic React/Remotion video compilation to MP4/WebM."
            pre_flight = "Verify frame-indexed composition math (useCurrentFrame) and FFmpeg availability."

        elif any(k in p for k in ["animasi", "three.js", "webgl", "motion", "pegas"]):
            owner = "maxilun-motion"
            rationale = "Interactive web motion, analytical springs, or 3D WebGL scenes."
            pre_flight = "Check spring physics parameters (stiffness, damping) and GPU frame budget."

        elif any(k in p for k in ["copywriting", "microcopy", "naskah", "copy produk"]):
            owner = "maxilun-content"
            rationale = "Product UI microcopy, terminology inventory, or cinematic video scripts."
            pre_flight = "Audit existing domain nouns, action-specific button verbs, and brand tone."

        elif any(k in p for k in ["seo", "sitemap", "json-ld", "canonical", "core web vitals"]):
            owner = "maxilun-seo-audit"
            rationale = "Technical SEO crawlability, canonical link hygiene, or JSON-LD structured data."
            pre_flight = "Inspect robot.txt, sitemap indices, and head metadata serialization."

        elif any(k in p for k in ["init docs", "scaffold docs", "buat prd awal", "bootstrap context"]):
            owner = "maxilun-scaffold"
            rationale = "Bootstrapping initial project context documents in docs/ from codebase evidence."
            pre_flight = "Inspect package.json, schema files, and existing folder structure."

        elif any(k in p for k in ["rfc", "openapi", "runbook", "llms.txt", "tulis spesifikasi"]):
            owner = "maxilun-docsmith"
            rationale = "In-depth engineering RFC, OpenAPI 3.1 contract, production runbook, or llms.txt."
            pre_flight = "Read OpenAPI templates and align API payload schemas with data models."

        elif any(k in p for k in ["jalankan tes", "typecheck", "cek build", "uji regresi", "lint kode"]):
            owner = "maxilun-verify"
            rationale = "Quality assurance, typechecking, build gates, and factual verification reporting."
            pre_flight = "Check package.json scripts / Makefile to find repository native test runner."

        elif any(k in p for k in ["ci/cd", "docker", "pipeline", "deploy", "ssl", "kubernetes"]):
            owner = "maxilun-deploy"
            rationale = "CI/CD automation, container hardening, zero-downtime release, or observability."
            pre_flight = "Check runtime environment variables, lockfiles, and hosting target topology."

        elif any(k in p for k in ["petakan kode", "cari simbol", "siapa panggil", "blast radius", "knowledge graph"]):
            owner = "maxilun-knowledge-graph"
            rationale = "Codebase symbol lookup, call hierarchy mapping, or dependency graph generation."
            pre_flight = "Query maxilun-out/graph.json cache or run python cli.py scan."


        # 3. Wave Coordination Decomposition (Maxilun Section 4)
        is_multi = len(companions) > 0 or any(k in p for k in ["lengkap", "fullstack", "end-to-end", "dan test", "beserta ui", "arsitektur"])
        waves = []
        if is_multi:
            w1_specs = [owner] if owner in ("maxilun-architect", "maxilun-data", "maxilun-sentinel", "maxilun-scaffold", "maxilun-network") else []
            for c in companions:
                if c in ("maxilun-architect", "maxilun-data", "maxilun-sentinel", "maxilun-scaffold", "maxilun-network") and c not in w1_specs:
                    w1_specs.append(c)
            if not w1_specs:
                w1_specs = [owner]

            w2_specs = []
            for s in [owner] + companions:
                if s in ("maxilun-engineer", "maxilun-frontend", "maxilun-craft", "maxilun-motion", "maxilun-cinecode", "maxilun-content", "maxilun-desktop", "maxilun-mobile", "maxilun-iot", "maxilun-ai"):
                    if s not in w2_specs:
                        w2_specs.append(s)
            if not w2_specs:
                w2_specs = ["maxilun-engineer"]

            waves = [
                {"wave": 1, "name": "Wave 1: Contracts & Design", "specialists": w1_specs[:3], "goal": "Define schemas, API boundaries, or visual tokens"},
                {"wave": 2, "name": "Wave 2: Implementation", "specialists": w2_specs[:3], "goal": "Consume contracts to write convergent production code"},
                {"wave": 3, "name": "Wave 3: Verification & Proof", "specialists": ["maxilun-verify"], "goal": "Execute test suite, typecheck, and runtime proof"}
            ]
        else:
            waves = [
                {"wave": 1, "name": "Direct Execution", "specialists": [owner], "goal": "Execute single-surface change"},
                {"wave": 2, "name": "Verification Proof", "specialists": ["maxilun-verify"], "goal": "Validate build & exit code 0"}
            ]

        # 4. Standard Handoff Record (Maxilun Section 5)
        handoff_record = f"""Owner: {owner}
Artifacts: {owner} contract deliverables for "{prompt[:40]}"
Verification: Invariant verification [CONFIRMED]
Next: {', '.join(companions) if companions else 'maxilun-verify'}
Residual risks: Disclose operational or runtime boundary limits explicitly"""

        return RoutingDecision(
            prompt=prompt,
            primary_owner=owner,
            reversibility=reversibility,
            decision_type=decision_type,
            companions=companions,
            pre_flight=pre_flight,
            rationale=rationale,
            is_multi_domain=is_multi,
            waves=waves,
            handoff_record=handoff_record
        )
