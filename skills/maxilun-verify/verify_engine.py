#!/usr/bin/env python3
"""
Maxilun Headless & Surface Verification Engine
=============================================

Automates surface verification across mobile (320px reflow), tablet (768px), and desktop (1440px):
1. HTML syntax and DOM integrity (html.parser) + XML/XSS safety checks on SVG.
2. Static overflow, viewport meta, and iOS input font-size heuristics.
3. Real headless browser measurement via Playwright / render.py when available:
   - Exit 0: [CONFIRMED] PASS (real browser measured scrollWidth <= clientWidth at 320/768/1440).
   - Exit 1: FAIL (static DOM/overflow/security error or real browser overflow detected).
   - Exit 2: [UNVERIFIED] (static checks passed, but no browser renderer ran to prove layout).
"""

import argparse
import codecs
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from html.parser import HTMLParser
from typing import Dict, List, Any, Tuple


def _read_text_auto(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith(codecs.BOM_UTF16_LE) or raw.startswith(codecs.BOM_UTF16_BE):
        return raw.decode("utf-16", errors="replace")
    if raw.startswith(codecs.BOM_UTF8):
        return raw.decode("utf-8-sig", errors="replace")
    return raw.decode("utf-8", errors="replace")


class DOMStructureAuditor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags_stack = []
        self.unclosed_tags = []
        self.tag_errors = []
        self.interactive_elements = []
        self.images = []
        self.has_viewport_meta = False
        self.viewport_content_ok = False
        self.has_root_overflow_x_hidden = False
        self.inputs = []
        self.self_closing = {
            "area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "param", "source", "track", "wbr",
        }

    def handle_starttag(self, tag, attrs):
        attr_dict = {k: ("" if v is None else str(v)) for k, v in attrs}
        line, _ = self.getpos()

        if tag == "meta" and attr_dict.get("name", "").lower() == "viewport":
            self.has_viewport_meta = True
            content = attr_dict.get("content", "").lower().replace(" ", "")
            if "width=device-width" in content:
                self.viewport_content_ok = True

        cls = attr_dict.get("class", "")
        if tag in ("html", "body", "main") and "overflow-x-hidden" in cls:
            self.has_root_overflow_x_hidden = True

        if tag in ("button", "a"):
            self.interactive_elements.append({
                "tag": tag,
                "class": cls,
                "aria-label": attr_dict.get("aria-label", ""),
                "line": line,
            })

        if tag == "img":
            self.images.append({
                "src": attr_dict.get("src", ""),
                "alt": dict(attrs).get("alt"),
                "line": line,
            })

        if tag in ("input", "select", "textarea"):
            self.inputs.append({
                "tag": tag,
                "type": attr_dict.get("type", "text"),
                "class": cls,
                "line": line,
            })

        if tag not in self.self_closing:
            self.tags_stack.append((tag, line))

    def handle_endtag(self, tag):
        if tag in self.self_closing:
            return
        if not self.tags_stack:
            self.tag_errors.append(f"Unexpected closing </{tag}> with empty tag stack")
            return
        last_tag, line = self.tags_stack[-1]
        if last_tag == tag:
            self.tags_stack.pop()
        else:
            self.unclosed_tags.append((last_tag, line))
            if any(t == tag for t, _ in self.tags_stack):
                while self.tags_stack and self.tags_stack[-1][0] != tag:
                    self.tags_stack.pop()
                if self.tags_stack:
                    self.tags_stack.pop()

    def finalize(self):
        self.close()
        while self.tags_stack:
            self.unclosed_tags.append(self.tags_stack.pop())


class VerifyEngine:
    VIEWPORTS = (
        ("Mobile (Reflow)", 320, 720),
        ("Tablet", 768, 1024),
        ("Desktop", 1440, 900),
    )

    @staticmethod
    def _load_render_module():
        """Loads maxilun-craft/scripts/render.py if present (optional in partial installs)."""
        import importlib.util
        candidates = [
            Path(__file__).resolve().parent.parent / "maxilun-craft" / "scripts" / "render.py",
        ]
        for cand in candidates:
            if cand.is_file():
                spec = importlib.util.spec_from_file_location("maxilun_craft_render", str(cand))
                if spec and spec.loader:
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    return mod
        return None

    def _measure_with_browser(self, path: Path) -> Tuple[str, List[Dict[str, Any]], str]:
        """Runs real viewport measurements via Playwright when available, or render.py Chrome fallback."""
        try:
            from playwright.sync_api import sync_playwright
            url = path.resolve().as_uri()
            measured = []
            with sync_playwright() as p:
                browser = p.chromium.launch()
                for label, width, height in self.VIEWPORTS:
                    page = browser.new_page(viewport={"width": width, "height": height})
                    page_errors = []
                    page.on("pageerror", lambda err: page_errors.append(str(err)))
                    page.goto(url, wait_until="networkidle")
                    metrics = page.evaluate("""() => {
                        const prevHtml = document.documentElement.style.overflowX;
                        const prevBody = document.body ? document.body.style.overflowX : '';
                        document.documentElement.style.setProperty('overflow-x', 'visible', 'important');
                        if (document.body) document.body.style.setProperty('overflow-x', 'visible', 'important');
                        const sw = document.documentElement.scrollWidth;
                        const cw = document.documentElement.clientWidth;
                        document.documentElement.style.overflowX = prevHtml;
                        if (document.body) document.body.style.overflowX = prevBody;
                        return {scrollWidth: sw, clientWidth: cw, emptyBody: !document.body || document.body.innerText.trim().length === 0};
                    }""")
                    overflow = metrics["scrollWidth"] - metrics["clientWidth"]
                    passed = overflow <= 0 and not page_errors and not metrics.get("emptyBody")
                    measured.append({
                        "name": label,
                        "w": width,
                        "h": height,
                        "scrollW": metrics["scrollWidth"],
                        "clientW": metrics["clientWidth"],
                        "overflow": overflow,
                        "page_errors": len(page_errors),
                        "passed": passed,
                    })
                    page.close()
                browser.close()
            all_ok = all(v["passed"] for v in measured)
            return ("CONFIRMED" if all_ok else "FAIL"), measured, "Playwright Chromium"
        except ImportError:
            pass
        except Exception as exc:
            return "UNVERIFIED", [], f"Playwright error: {exc}"

        render_mod = self._load_render_module()
        if render_mod and render_mod.find_browser():
            return (
                "UNVERIFIED",
                [],
                "Chrome/Edge found via render.py, but Playwright is required to probe scrollWidth numerically",
            )
        return "UNVERIFIED", [], "No Playwright/Chromium renderer available"

    def audit_surface_file(self, file_path: Path, static_only: bool = False) -> Dict[str, Any]:
        """Performs static DOM/layout/security checks plus real headless browser verification when available."""
        path = Path(file_path).resolve()
        if not path.is_file():
            raise FileNotFoundError(f"Surface file not found: {path}")

        raw_content = _read_text_auto(path)
        total_lines = len(raw_content.splitlines())
        is_svg = path.suffix.lower() == ".svg"

        auditor = DOMStructureAuditor()
        auditor.feed(raw_content)
        auditor.finalize()

        # 1. Markup, XML & Active-Content Security Integrity
        security_risks = []
        if is_svg:
            xml_ok = True
            try:
                ET.fromstring(raw_content)
            except ET.ParseError as exc:
                xml_ok = False
                auditor.tag_errors.append(f"SVG XML ParseError: {exc}")
            if re.search(r"<script\b|<foreignObject\b|\bon[a-z]+\s*=|javascript:", raw_content, re.IGNORECASE):
                security_risks.append("Active script, event handler, foreignObject, or javascript: URL forbidden inside SVG")
            dom_passed = xml_ok and "<svg" in raw_content.lower() and "viewbox=" in raw_content.lower() and not security_risks
        else:
            dom_passed = len(auditor.unclosed_tags) == 0 and len(auditor.tag_errors) == 0

        # 2. Static Overflow & Viewport Heuristics (320px reflow ceiling)
        overflow_risks = []
        if not is_svg:
            if not auditor.has_viewport_meta:
                overflow_risks.append("Missing <meta name='viewport' content='width=device-width, initial-scale=1'>")
            elif not auditor.viewport_content_ok:
                overflow_risks.append("<meta name='viewport'> must specify width=device-width for 320px reflow")

            if re.search(r'\b100vw\b|w-screen', raw_content) and not auditor.has_root_overflow_x_hidden:
                overflow_risks.append("Contains 100vw/w-screen without root overflow-x-hidden container")

            width_patterns = re.finditer(
                r'(?<![a-z-])(?:width|min-width)\s*:\s*([3-9]\d{2}|\d{4,})px|'
                r'\bw-\[([3-9]\d{2}|\d{4,})px\]|'
                r'\bwidth\s*=\s*["\']([3-9]\d{2}|\d{4,})["\']',
                raw_content,
                re.IGNORECASE,
            )
            for m in width_patterns:
                val = int(next(g for g in m.groups() if g is not None))
                if val > 320:
                    overflow_risks.append(f"Fixed/min width {val}px risks horizontal overflow on 320px reflow viewport")
                    break

            vw_match = re.search(r'(?<![\d.])(1\d{2}|[2-9]\d{2})vw\b', raw_content, re.IGNORECASE)
            if vw_match:
                overflow_risks.append(f"Viewport width {vw_match.group(0)} exceeds 100vw")

        # 3. Accessibility & Mobile Input Checks
        a11y_warnings = []
        if is_svg:
            if not re.search(r"<title\b", raw_content, re.IGNORECASE):
                a11y_warnings.append("SVG missing <title> accessible label")
            if 'role="img"' not in raw_content and "aria-hidden=" not in raw_content:
                a11y_warnings.append("SVG missing role='img' or aria-hidden attribute")
        else:
            for inp in auditor.inputs:
                classes = inp.get("class", "").split()
                if "text-xs" in classes and not any(c.startswith(("sm:text-sm", "sm:text-base", "sm:text-lg", "text-base", "text-sm")) for c in classes):
                    a11y_warnings.append(f"Input at line {inp['line']} has text-xs (font < 16px triggers iOS auto-zoom)")

            for img in auditor.images:
                if img.get("alt") is None:
                    a11y_warnings.append(f"Image at line {img['line']} missing alt attribute")

        static_passed = dom_passed and len(overflow_risks) == 0 and len(security_risks) == 0

        # 4. Real Browser Verification (3-exit gate: 0 PASS, 1 FAIL, 2 UNVERIFIED)
        if static_only:
            browser_status, viewports, browser_note = "UNVERIFIED", [], "Static-only mode (--static); browser not launched"
        else:
            browser_status, viewports, browser_note = self._measure_with_browser(path)

        if not static_passed or browser_status == "FAIL":
            exit_code = 1
            verdict = "FAIL"
            overall_passed = False
        elif browser_status == "CONFIRMED":
            exit_code = 0
            verdict = "PASS"
            overall_passed = True
        else:
            exit_code = 2
            verdict = "UNVERIFIED"
            overall_passed = False

        return {
            "file": str(path.name),
            "total_lines": total_lines,
            "dom_integrity": {
                "passed": dom_passed,
                "unclosed_tags": auditor.unclosed_tags,
                "errors": auditor.tag_errors + security_risks,
            },
            "overflow_checks": {
                "passed": static_passed and browser_status == "CONFIRMED",
                "risks": overflow_risks,
                "viewports": viewports,
                "browser_status": browser_status,
                "browser_note": browser_note,
            },
            "accessibility": {
                "warnings": a11y_warnings,
                "interactive_count": len(auditor.interactive_elements),
                "images_count": len(auditor.images),
            },
            "status": verdict,
            "exit_code": exit_code,
            "passed": overall_passed,
        }

    def format_markdown_report(self, res: Dict[str, Any]) -> str:
        """Formats the verification result into the standard Maxilun Evidence table without inventing numbers."""
        dom_res = res["dom_integrity"]
        overflow_res = res["overflow_checks"]
        a11y_res = res["accessibility"]

        status_dom = "[CONFIRMED] PASS" if dom_res["passed"] else "[FAIL]"
        lines = [
            f"### Surface Verification Evidence — {res['file']}",
            "",
            "| Check | Method & Target | Actual Result | Status |",
            "|---|---|---|:---:|",
            f"| Markup & DOM Integrity | Parser/XML scan over {res['file']} | Lines: {res['total_lines']}, Unclosed: {len(dom_res['unclosed_tags'])}, Errors: {len(dom_res['errors'])} | {status_dom} |",
        ]

        if overflow_res["viewports"]:
            for vp in overflow_res["viewports"]:
                vp_status = "[CONFIRMED] PASS" if vp["passed"] else "[FAIL]"
                lines.append(
                    f"| {vp['name']} ({vp['w']}px) | {overflow_res['browser_note']} {vp['w']}x{vp['h']} | "
                    f"scrollW={vp['scrollW']}, clientW={vp['clientW']}, overflow={vp['overflow']}px | {vp_status} |"
                )
        else:
            static_note = "Static heuristic OK (0 risks)" if not overflow_res["risks"] else f"{len(overflow_res['risks'])} static risk(s)"
            lines.append(
                f"| Responsive Reflow (320/768/1440px) | {overflow_res['browser_note']} | {static_note}; runtime scrollW not measured | [UNVERIFIED] |"
            )

        a11y_status = "[CONFIRMED] PASS" if len(a11y_res["warnings"]) == 0 else "[WARNING]"
        lines.append(
            f"| Accessibility & Media Static Check | Static tag & attribute scan | Warnings: {len(a11y_res['warnings'])}, Controls: {a11y_res['interactive_count']} | {a11y_status} |"
        )
        lines.append("")
        lines.append(f"**Verification Verdict**: `{res['status']}` (exit code `{res['exit_code']}`) — {overflow_res['browser_note']}.")
        if dom_res["errors"]:
            lines.append("DOM/Security errors: " + "; ".join(dom_res["errors"]))
        if overflow_res["risks"]:
            lines.append("Static risks: " + "; ".join(overflow_res["risks"]))
        if a11y_res["warnings"]:
            lines.append("Accessibility warnings: " + "; ".join(a11y_res["warnings"]))
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Maxilun Headless & Surface Verification Engine",
        allow_abbrev=False,
    )
    parser.add_argument("target", help="Target HTML or SVG file to verify")
    parser.add_argument("--json", action="store_true", help="Output JSON verdict")
    parser.add_argument("--static", action="store_true", help="Skip headless browser measurement")
    args = parser.parse_args()

    engine = VerifyEngine()
    try:
        report_data = engine.audit_surface_file(Path(args.target), static_only=args.static)
    except Exception as e:
        print(f"Error during verification: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(report_data, indent=2))
    else:
        print(engine.format_markdown_report(report_data))

    sys.exit(report_data["exit_code"])


if __name__ == "__main__":
    main()
