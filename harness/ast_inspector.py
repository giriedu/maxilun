"""Maxilun AST & Structural Code Inspector.

Performs deterministic AST analysis on Python code, comment-stripped structural
analysis on TypeScript/JavaScript, and syntax/pattern analysis on SQL DDL.
Zero external dependencies (stdlib only).
"""

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class ASTFinding:
    rule_id: str
    message: str
    line_number: Optional[int] = None
    severity: str = "ERROR"  # "ERROR" or "WARNING"
    snippet: Optional[str] = None


@dataclass
class ASTInspectionResult:
    passed: bool
    findings: List[ASTFinding] = field(default_factory=list)
    language: str = "unknown"

    def summary(self) -> str:
        status = "✅ PASS" if self.passed else "❌ FAIL"
        lines = [f"AST Inspection ({self.language}): {status} ({len(self.findings)} findings)"]
        for f in self.findings:
            loc = f":{f.line_number}" if f.line_number else ""
            lines.append(f"  - [{f.severity}] [{f.rule_id}] {f.message}{loc}")
            if f.snippet:
                lines.append(f"      `{f.snippet.strip()}`")
        return "\n".join(lines)


class PythonSecurityVisitor(ast.NodeVisitor):
    """Inspects Python AST for security vulnerabilities and code hygiene."""

    def __init__(self, source_lines: List[str]):
        self.source_lines = source_lines
        self.findings: List[ASTFinding] = []
        self.fstring_vars = set()

    def visit_Assign(self, node):
        # Track variables that hold f-strings
        if isinstance(node.value, ast.JoinedStr):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.fstring_vars.add(target.id)

        # Detect hardcoded secret tokens
        for target in node.targets:
            if isinstance(target, ast.Name) and any(k in target.id.lower() for k in ["api_key", "secret_key", "password", "auth_token"]):
                if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                    val = node.value.value
                    if len(val) > 8 and not val.startswith(("${", "env:", "os.environ")):
                        self.findings.append(ASTFinding(
                            rule_id="SEC-004",
                            message=f"Hardcoded credential/secret assigned to '{target.id}'",
                            line_number=node.lineno,
                            severity="ERROR",
                            snippet=self._get_line(node.lineno)
                        ))
        self.generic_visit(node)

    def visit_Call(self, node):
        func_name = ""
        if isinstance(node.func, ast.Attribute):
            func_name = node.func.attr
        elif isinstance(node.func, ast.Name):
            func_name = node.func.id

        # Detect raw unparameterized SQL query execution
        if func_name in ("execute", "query", "raw", "raw_query"):
            if node.args:
                first_arg = node.args[0]
                if isinstance(first_arg, ast.JoinedStr):
                    self.findings.append(ASTFinding(
                        rule_id="SEC-003",
                        message=f"Direct f-string SQL interpolation in database call '{func_name}'",
                        line_number=node.lineno,
                        severity="ERROR",
                        snippet=self._get_line(node.lineno)
                    ))
                elif isinstance(first_arg, ast.Name) and first_arg.id in self.fstring_vars:
                    self.findings.append(ASTFinding(
                        rule_id="SEC-003",
                        message=f"Interpolated f-string variable '{first_arg.id}' passed to SQL call '{func_name}'",
                        line_number=node.lineno,
                        severity="ERROR",
                        snippet=self._get_line(node.lineno)
                    ))
                elif isinstance(first_arg, ast.BinOp) and isinstance(first_arg.op, ast.Mod):
                    self.findings.append(ASTFinding(
                        rule_id="SEC-003",
                        message=f"Unparameterized '%' string formatting in SQL call '{func_name}'",
                        line_number=node.lineno,
                        severity="ERROR",
                        snippet=self._get_line(node.lineno)
                    ))

        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        if node.type is None:
            self.findings.append(ASTFinding(
                rule_id="ERR-001",
                message="Bare 'except:' handler catches SystemExit/KeyboardInterrupt (use 'except Exception:')",
                line_number=node.lineno,
                severity="ERROR",
                snippet=self._get_line(node.lineno)
            ))
        elif len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
            self.findings.append(ASTFinding(
                rule_id="ERR-002",
                message="Silent swallowed exception with 'pass' without logging or recovery",
                line_number=node.lineno,
                severity="WARNING",
                snippet=self._get_line(node.lineno)
            ))
        self.generic_visit(node)

    def _get_line(self, lineno: int) -> str:
        if 1 <= lineno <= len(self.source_lines):
            return self.source_lines[lineno - 1]
        return ""


class ASTInspector:
    """Multi-language structural and semantic AST inspector."""

    @staticmethod
    def strip_js_comments(code: str) -> str:
        """Removes single-line and multi-line JS/TS comments cleanly."""
        def replacer(match):
            s = match.group(0)
            if s.startswith('/'):
                return " " * len(s)
            else:
                return s
        pattern = re.compile(
            r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
            re.DOTALL | re.MULTILINE
        )
        return re.sub(pattern, replacer, code)

    def inspect_file(self, file_path: str) -> ASTInspectionResult:
        p = Path(file_path)
        if not p.exists():
            return ASTInspectionResult(passed=False, findings=[ASTFinding("F-001", f"File '{file_path}' not found")])

        source = p.read_text(encoding="utf-8", errors="replace")
        ext = p.suffix.lower()

        if ext == ".py":
            return self.inspect_python(source, filename=file_path)
        elif ext in (".ts", ".tsx", ".js", ".jsx"):
            return self.inspect_typescript(source, filename=file_path)
        elif ext == ".sql":
            return self.inspect_sql(source, filename=file_path)

        return ASTInspectionResult(passed=True, language="unsupported_ast")

    def inspect_python(self, source: str, filename: str = "<memory>") -> ASTInspectionResult:
        lines = source.splitlines()
        try:
            tree = ast.parse(source, filename=filename)
        except SyntaxError as e:
            return ASTInspectionResult(
                passed=False,
                language="python",
                findings=[ASTFinding(
                    rule_id="SYN-001",
                    message=f"Python syntax error: {e.msg}",
                    line_number=e.lineno,
                    severity="ERROR"
                )]
            )

        visitor = PythonSecurityVisitor(lines)
        visitor.visit(tree)
        passed = not any(f.severity == "ERROR" for f in visitor.findings)
        return ASTInspectionResult(passed=passed, findings=visitor.findings, language="python")

    def inspect_typescript(self, source: str, filename: str = "<memory>") -> ASTInspectionResult:
        findings: List[ASTFinding] = []
        clean_code = self.strip_js_comments(source)
        lines = source.splitlines()

        # 1. SQL injection in template strings
        for idx, line in enumerate(lines, 1):
            if re.search(r'(?:db\.query|pool\.query|execute)\s*\(\s*`[^`]*\$\{[^}]+\}[^`]*`', line):
                findings.append(ASTFinding(
                    rule_id="SEC-003",
                    message="Template literal interpolation inside database query (SQL injection risk)",
                    line_number=idx,
                    severity="ERROR",
                    snippet=line.strip()[:80]
                ))

        # 2. Timing attack on signature comparison
        has_crypto = bool(re.search(r'(?:createHmac|hmac|signature|verifyWebhook)', clean_code, re.IGNORECASE))
        if has_crypto:
            has_timing_safe = bool(re.search(r'(?:timingSafeEqual|constant_time_compare)', clean_code))
            has_insecure_cmp = bool(re.search(r'(?:sig|signature|hash|digest)\s*!==?\s*(?:expected|received|sig|signature)', clean_code))
            if has_insecure_cmp and not has_timing_safe:
                findings.append(ASTFinding(
                    rule_id="SEC-001",
                    message="Cryptographic signature verification uses standard '!==' operator instead of timingSafeEqual",
                    severity="ERROR"
                ))

        # 3. Floating-point currency calculations
        for idx, line in enumerate(lines, 1):
            if re.search(r'(?:amount|price|balance|fee)\s*[\+\-\*\/]\s*(?:0\.\d+|0\.\d+f)', line, re.IGNORECASE):
                findings.append(ASTFinding(
                    rule_id="FIN-001",
                    message="Floating-point arithmetic detected on currency variable (use integer minor units or BigInt)",
                    line_number=idx,
                    severity="WARNING",
                    snippet=line.strip()[:80]
                ))

        passed = not any(f.severity == "ERROR" for f in findings)
        return ASTInspectionResult(passed=passed, findings=findings, language="typescript")

    def inspect_sql(self, source: str, filename: str = "<memory>") -> ASTInspectionResult:
        findings: List[ASTFinding] = []
        lines = source.splitlines()

        # Check for blocking NOT NULL without default on ADD COLUMN
        for idx, line in enumerate(lines, 1):
            upper = line.upper()
            if "ALTER TABLE" in upper and "ADD COLUMN" in upper and "NOT NULL" in upper and "DEFAULT" in upper:
                findings.append(ASTFinding(
                    rule_id="MIG-001",
                    message="ALTER TABLE ADD COLUMN NOT NULL with DEFAULT causes full table locks in legacy RDBMS (use Expand-Contract phases)",
                    line_number=idx,
                    severity="WARNING",
                    snippet=line.strip()[:80]
                ))

            if "DROP COLUMN" in upper and not any(k in upper for k in ["IF EXISTS", "-- SAFE", "DEPRECATED"]):
                findings.append(ASTFinding(
                    rule_id="MIG-002",
                    message="Irreversible DROP COLUMN without deprecation contract phase",
                    line_number=idx,
                    severity="WARNING",
                    snippet=line.strip()[:80]
                ))

        passed = not any(f.severity == "ERROR" for f in findings)
        return ASTInspectionResult(passed=passed, findings=findings, language="sql")
