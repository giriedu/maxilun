"""Maxilun Purity Gate & Invariant Validator.

Implements deterministic evaluation of code, prose, and markup against
Maxilun Core Rules (Focus & Agency, Purity, Minimalist, Clarity & Proof)
and references/purity-catalog.md constraints.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any, Optional


@dataclass
class Violation:
    category: str
    rule_id: str
    message: str
    line_number: Optional[int] = None
    snippet: Optional[str] = None
    severity: str = "ERROR"  # "ERROR" or "WARNING"


@dataclass
class ValidationResult:
    passed: bool
    score: float
    violations: List[Violation] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)

    def summary(self) -> str:
        status = "✅ PASS" if self.passed else "❌ FAIL"
        lines = [
            f"Purity Gate Verdict: {status} (Score: {self.score:.1f}/100)",
            f"Total Violations: {len(self.violations)} (Errors: {sum(1 for v in self.violations if v.severity == 'ERROR')}, Warnings: {sum(1 for v in self.violations if v.severity == 'WARNING')})"
        ]
        for v in self.violations:
            loc = f":{v.line_number}" if v.line_number else ""
            lines.append(f"  - [{v.severity}] [{v.rule_id}] {v.message}{loc}")
            if v.snippet:
                lines.append(f"      `{v.snippet.strip()}`")
        return "\n".join(lines)


class PurityValidator:
    """Deterministic validator enforcing Maxilun Purity Gate and Code Hygiene standards."""

    BANNED_WORDS = [
        (r"\bdelve\b", "VOC-001", "Forbidden AI buzzword 'delve'"),
        (r"\btapestry\b", "VOC-002", "Forbidden AI metaphor 'tapestry'"),
        (r"\bsynergy\b", "VOC-003", "Corporate buzzword 'synergy'"),
        (r"\bholistic\b", "VOC-004", "Vague buzzword 'holistic'"),
        (r"\bleverage\b", "VOC-005", "Overused verb 'leverage' (use specific action)"),
        (r"\bseamlessly\b", "VOC-006", "Generic adverb 'seamlessly'"),
        (r"\brobust\b", "VOC-007", "Empty quality claim 'robust' (specify concrete invariant)"),
        (r"\bcutting-edge\b", "VOC-008", "Marketing hyperbole 'cutting-edge'"),
        (r"\bgame-changer\b", "VOC-009", "Marketing hyperbole 'game-changer'"),
        (r"\brevolutionary\b", "VOC-010", "Marketing hyperbole 'revolutionary'"),
        (r"\bsupercharge\b", "VOC-011", "Marketing buzzword 'supercharge'"),
        (r"\bdive in\b", "VOC-012", "Filler conversational phrase 'dive in'"),
    ]

    CEREMONIAL_PATTERNS = [
        (r"(?i)🎯\s*\[?fokus\]?", "HUD-001", "Ceremonial emoji HUD banner '🎯 [FOKUS]'"),
        (r"(?i)⚡\s*\[?tindakan\]?", "HUD-002", "Ceremonial emoji HUD banner '⚡ [TINDAKAN]'"),
        (r"(?i)🔒\s*\[?delivery\s+gate\]?", "HUD-003", "Self-checked delivery gate theater '🔒 DELIVERY GATE'"),
        (r"(?i)📋\s*\[?parking\s+lot\]?", "HUD-004", "Ceremonial HUD block '📋 Parking Lot'"),
        (r"(?i)^\s*\|\s*gate\s*\|\s*status\s*\|", "HUD-005", "Self-asserted PASS/FAIL table theater"),
        (r"^\s*-\s*\[[ x]\]\s+.*(?:gate|delivery|purity)", "HUD-006", "Self-checked checkbox gate theater"),
    ]

    AI_CLICHE_GRADIENTS = re.compile(
        r'linear-gradient\([^)]*#(?:667eea|764ba2|8b5cf6|ec4899|a855f7|9333ea)',
        re.IGNORECASE
    )

    def validate_text(self, text: str, file_path: Optional[str] = None) -> ValidationResult:
        """Validates raw text/code against general Purity Gate rules."""
        violations: List[Violation] = []
        lines = text.splitlines()
        norm_path = file_path.replace("\\", "/") if file_path else ""
        is_normative_catalog = any(k in norm_path for k in ["purity-catalog.md", "engines.md"])

        # 1. Banned Words Check (Exempt for normative catalog specifications)
        if not is_normative_catalog:
            for pattern, rule_id, msg in self.BANNED_WORDS:
                for idx, line in enumerate(lines, 1):
                    m = re.search(pattern, line, re.IGNORECASE)
                    if m:
                        violations.append(Violation(
                            category="banned_vocabulary",
                            rule_id=rule_id,
                            message=f"{msg} (matched '{m.group(0)}')",
                            line_number=idx,
                            snippet=line.strip()[:80],
                            severity="ERROR"
                        ))

        # 2. Ceremonial HUD Check (Exempt for normative catalog specifications)
        if not is_normative_catalog:
            for pattern, rule_id, msg in self.CEREMONIAL_PATTERNS:
                for idx, line in enumerate(lines, 1):
                    m = re.search(pattern, line)
                    if m:
                        violations.append(Violation(
                            category="ceremonial_theater",
                            rule_id=rule_id,
                            message=msg,
                            line_number=idx,
                            snippet=line.strip()[:80],
                            severity="ERROR"
                        ))
        # 3. Contextual Invariants based on file extension / content
        ext = Path(file_path).suffix.lower() if file_path else ""
        if ext in {".tsx", ".jsx", ".vue", ".svelte", ".html", ".css", ".scss", ".swift", ".kt"} or any(k in text for k in ["<div", "return (", "className=", "SwiftUI", "VStack", "Composable", "@Composable"]):
            self._validate_ui_invariants(text, lines, violations, file_path=file_path)

        if ext in {".ts", ".js", ".py", ".go"} or any(k in text for k in ["webhook", "crypto", "createHmac", "SELECT", "UPDATE"]):
            self._validate_backend_security_invariants(text, lines, violations)

        # Calculate Score: 100 - (errors * 15 + warnings * 5)
        err_count = sum(1 for v in violations if v.severity == "ERROR")
        warn_count = sum(1 for v in violations if v.severity == "WARNING")
        penalty = (err_count * 15) + (warn_count * 5)
        score = max(0.0, 100.0 - penalty)
        passed = (err_count == 0)

        return ValidationResult(
            passed=passed,
            score=score,
            violations=violations,
            metrics={"errors": err_count, "warnings": warn_count, "lines": len(lines)}
        )

    def _validate_ui_invariants(self, text: str, lines: List[str], violations: List[Violation], file_path: Optional[str] = None):
        """Enforces 4 UI States, tabular numbers, and anti-cliché styling."""
        # A. Cliché Gradients
        for idx, line in enumerate(lines, 1):
            if self.AI_CLICHE_GRADIENTS.search(line):
                violations.append(Violation(
                    category="design_purity",
                    rule_id="CLR-001",
                    message="Generic AI purple/pink decorative gradient detected (use domain OKLCH tokens)",
                    line_number=idx,
                    snippet=line.strip()[:80],
                    severity="ERROR"
                ))

        # B. 4 UI States validation for data-driven web components (exempt Remotion video scripts)
        norm_path = file_path.replace("\\", "/") if file_path else ""
        is_remotion = "cinecode" in norm_path or "useCurrentFrame" in text or "Composition" in text
        is_data_component = not is_remotion and bool(re.search(r'(?:items|data|list|records|transactions|users)\.map\(', text))
        if is_data_component:
            has_loading = bool(re.search(r'(?i)(loading|isLoading|skeleton|suspense)', text))
            has_empty = bool(re.search(r'(?i)(empty|length\s*===?\s*0|no\s+data|not\s+found)', text))
            has_error = bool(re.search(r'(?i)(error|isError|catch|failed)', text))

            missing = []
            if not has_loading: missing.append("loading/skeleton")
            if not has_empty: missing.append("empty-state")
            if not has_error: missing.append("inline-error")

            if missing:
                violations.append(Violation(
                    category="ui_states",
                    rule_id="UI-004",
                    message=f"Data-driven UI component missing mandatory states: {', '.join(missing)}",
                    severity="ERROR"
                ))

        # C. Tabular numbers on currency/financial tables
        has_currency = bool(re.search(r'(?:USD|IDR|EUR|Rp|\$|amount|price|balance|revenue|total)', text, re.IGNORECASE))
        has_table_or_list = bool(re.search(r'(?:<table|<tr|<td|\.map\()', text))
        has_tabular = bool(re.search(r'tabular-nums|tnum|tabularNums', text))
        if has_currency and has_table_or_list and not has_tabular:
            violations.append(Violation(
                category="typography",
                rule_id="TYPO-002",
                message="Monetary or numerical list missing 'font-variant-numeric: tabular-nums' (causes horizontal jitter)",
                severity="WARNING"
            ))

        # D. 45 AI Design Tells Scanner Integration
        ui_exts = {".html", ".htm", ".css", ".scss", ".tsx", ".jsx", ".vue", ".svelte", ".swift", ".kt"}
        ext = Path(file_path).suffix.lower() if file_path else ""
        if (ext in ui_exts) or any(k in text for k in ["<div", "className", "style={{", "VStack", "Composable", "@Composable"]):
            try:
                import importlib.util
                linter_path = Path(__file__).resolve().parent.parent / "scripts" / "ui-purity-linter.py"
                if linter_path.exists():
                    spec = importlib.util.spec_from_file_location("ui_linter_mod", str(linter_path))
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    linter = mod.UIPurityLinter()
                    for idx, line in enumerate(lines, 1):
                        for rule_id, category, severity, msg, remedy, pattern in linter.TELL_RULES:
                            if pattern.search(line):
                                violations.append(Violation(
                                    category="ui_purity_tell",
                                    rule_id=rule_id,
                                     message=f"{msg} ({remedy})",
                                    line_number=idx,
                                    snippet=line.strip()[:80],
                                    severity=severity
                                ))
            except Exception:
                pass

    def _validate_backend_security_invariants(self, text: str, lines: List[str], violations: List[Violation]):
        """Enforces constant-time crypto comparison, replay tolerance, and parameterized SQL."""
        # A. Timing attack on HMAC signature verification
        has_hmac = bool(re.search(r'(?:createHmac|hmac|signature|verifySignature)', text, re.IGNORECASE))
        if has_hmac:
            has_timing_safe = bool(re.search(r'(?:timingSafeEqual|constant_time_compare|HMAC\.equal)', text))
            has_insecure_cmp = bool(re.search(r'(?:sig|signature|hash|digest)\s*!==?\s*(?:expected|received|sig|signature)', text))
            if has_insecure_cmp and not has_timing_safe:
                violations.append(Violation(
                    category="security_invariant",
                    rule_id="SEC-001",
                    message="Signature verification uses standard equality (!==) vulnerable to timing attack (use timingSafeEqual)",
                    severity="ERROR"
                ))

            # B. Replay tolerance check
            has_replay = bool(re.search(r'(?:Date\.now\(\)|time\(\)|timestamp)[^;\n]*(?:300|tolerance|window|expired|replay)', text, re.IGNORECASE))
            if not has_replay:
                violations.append(Violation(
                    category="security_invariant",
                    rule_id="SEC-002",
                    message="Webhook verification missing timestamp expiration / replay window check (e.g. 300s)",
                    severity="WARNING"
                ))

        # C. SQL Injection via raw template string interpolation
        for idx, line in enumerate(lines, 1):
            if re.search(r'(?:db\.query|pool\.query|execute)\s*\(\s*`[^`]*\$\{[^}]+\}[^`]*`', line):
                violations.append(Violation(
                    category="security_invariant",
                    rule_id="SEC-003",
                    message="Raw template literal interpolation inside database query (SQL injection risk; use parameterized queries)",
                    line_number=idx,
                    snippet=line.strip()[:80],
                    severity="ERROR"
                ))
