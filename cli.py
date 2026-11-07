#!/usr/bin/env python3
"""
Maxilun Unified CLI — Single Production Entrypoint
==================================================

Unifies all autonomous capabilities of the Maxilun ecosystem:
  maxilun route "<prompt>"       # Triage Type 1/2 & multi-wave DAG dispatch
  maxilun scan [paths...]        # Incremental AST graph scan + report
  maxilun snapshot [path]        # Archive dated graph snapshot
  maxilun diff <t1> <t2>         # Compare architectural graphs/snapshots
  maxilun context <symbol>       # Fast LLM prompt blast-radius context
  maxilun lint [path] [--fix]    # 45 AI design tells linter & auto-fixer
  maxilun verify <surface.html>  # Surface & mobile 375px overflow audit
  maxilun init-hook [path]       # Install git pre-commit purity hook
  maxilun test                   # Run full ecosystem validation suite
  maxilun dashboard              # Display live HUD & routing matrix
"""

import sys
import argparse
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "skills" / "maxilun-knowledge-graph"))
sys.path.insert(0, str(REPO_ROOT / "skills" / "maxilun-verify"))
sys.path.insert(0, str(REPO_ROOT / "harness"))
sys.path.insert(0, str(REPO_ROOT / "scripts"))


def cmd_route(args):
    from harness.router import MaxilunRouter
    router = MaxilunRouter()
    decision = router.route(args.prompt)
    print("\n" + "=" * 55)
    print("  Maxilun Autonomous Routing & Triage Decision")
    print("=" * 55)
    print(decision.summary())
    print("=" * 55 + "\n")


def cmd_scan(args):
    import cli as kg_cli
    return kg_cli.cmd_scan(args)


def cmd_snapshot(args):
    import cli as kg_cli
    return kg_cli.cmd_snapshot(args)


def cmd_diff(args):
    import cli as kg_cli
    return kg_cli.cmd_diff(args)


def cmd_context(args):
    import cli as kg_cli
    return kg_cli.cmd_context(args)


def cmd_lint(args):
    import importlib
    ui_linter_mod = importlib.import_module("scripts.ui-purity-linter")
    target_path = Path(args.path or ".").resolve()
    linter = ui_linter_mod.UIPurityLinter()

    if args.fix:
        fix_res = linter.fix_path(target_path)
        if not args.json:
            print(f"\n🔧 Purity Auto-Fixer: Remediated {fix_res['fixed_files']} / {fix_res['total_files']} files.")
            for fp, fixes in fix_res['details'].items():
                print(f"   - {Path(fp).name}: {', '.join(fixes)}")
            print()

    result = linter.scan_path(target_path)
    if args.json:
        import json
        payload = {
            "passed": result.passed,
            "score": result.score,
            "total_files": result.total_files,
            "scanned_lines": result.scanned_lines,
            "violations": [
                {
                    "rule_id": v.rule_id,
                    "category": v.category,
                    "severity": v.severity,
                    "message": v.message,
                    "file_path": v.file_path,
                    "line_number": v.line_number,
                    "snippet": v.snippet,
                    "remedy": v.remedy
                }
                for v in result.violations
            ]
        }
        print(json.dumps(payload, indent=2))
    else:
        print(ui_linter_mod.format_report(result))

    if args.strict:
        sys.exit(0 if len(result.violations) == 0 else 1)
    else:
        sys.exit(0 if result.passed else 1)


def cmd_verify(args):
    from verify_engine import VerifyEngine
    engine = VerifyEngine()
    target_file = Path(args.surface).resolve()
    try:
        report_data = engine.audit_surface_file(target_file)
    except Exception as e:
        print(f"Error during verification: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        import json
        print(json.dumps(report_data, indent=2))
    else:
        print("\n" + engine.format_markdown_report(report_data) + "\n")

    sys.exit(0 if report_data["passed"] else 1)


def cmd_init_hook(args):
    import importlib
    hook_installer = importlib.import_module("scripts.install-hook")
    target = Path(args.path).resolve() if args.path else None
    success = hook_installer.install_hook(target)
    sys.exit(0 if success else 1)


def cmd_test(args):
    res = subprocess.run([sys.executable, str(REPO_ROOT / "scripts" / "test-suite.py")])
    sys.exit(res.returncode)


def cmd_dashboard(args):
    import importlib
    dash_mod = importlib.import_module("harness.dashboard")
    dash = dash_mod.MaxilunDashboard()
    dash.render()


def main():
    parser = argparse.ArgumentParser(
        prog="maxilun",
        description="Maxilun Unified CLI — Single Production Entrypoint",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # route
    route_parser = subparsers.add_parser("route", help="Triage prompt and dispatch specialist orchestration wave")
    route_parser.add_argument("prompt", help="User prompt or task description")

    # scan
    scan_parser = subparsers.add_parser("scan", help="Scan codebase and build AST Knowledge Graph")
    scan_parser.add_argument("paths", nargs="*", default=["."], help="Project path(s) to scan")
    scan_parser.add_argument("--name", "-n", help="Project name")
    scan_parser.add_argument("--view", "-v", action="store_true", help="Launch visualizer server")
    scan_parser.add_argument("--port", "-p", type=int, default=8765, help="Visualizer server port")
    scan_parser.add_argument("--output", "-o", help="Custom output JSON path")
    scan_parser.add_argument("--no-cache", action="store_true", help="Bypass incremental cache")
    scan_parser.add_argument("--snapshot", action="store_true", help="Archive dated snapshot")

    # snapshot
    snapshot_parser = subparsers.add_parser("snapshot", help="Archive a dated snapshot of Knowledge Graph")
    snapshot_parser.add_argument("path", nargs="?", default=".", help="Project path")

    # diff
    diff_parser = subparsers.add_parser("diff", help="Compare two architectural graphs or snapshots")
    diff_parser.add_argument("target1", help="Base target (date string YYYY-MM-DD or graph.json)")
    diff_parser.add_argument("target2", help="Compare target (date string YYYY-MM-DD or graph.json)")
    diff_parser.add_argument("--path", help="Project path")

    # context
    context_parser = subparsers.add_parser("context", help="Extract compact blast-radius prompt context for LLMs")
    context_parser.add_argument("symbol", help="Target symbol")
    context_parser.add_argument("--graph", "-g", help="Graph file path")
    context_parser.add_argument("--path", help="Project path")

    # lint
    lint_parser = subparsers.add_parser("lint", help="Audit code against 45 AI Design Tells taxonomy")
    lint_parser.add_argument("path", nargs="?", default=".", help="File or directory to scan")
    lint_parser.add_argument("--fix", action="store_true", help="Auto-remediate detected violations")
    lint_parser.add_argument("--strict", action="store_true", help="Fail if any warning exists")
    lint_parser.add_argument("--json", action="store_true", help="JSON output format")

    # verify
    verify_parser = subparsers.add_parser("verify", help="Audit surface HTML for syntax, mobile 375px overflow, and a11y")
    verify_parser.add_argument("surface", help="HTML surface file to audit")
    verify_parser.add_argument("--json", action="store_true", help="JSON output format")

    # init-hook
    hook_parser = subparsers.add_parser("init-hook", help="Install git pre-commit purity gate hook")
    hook_parser.add_argument("path", nargs="?", default=None, help="Repository root path")

    # test
    test_parser = subparsers.add_parser("test", help="Run full ecosystem validation test suite")

    # dashboard
    dash_parser = subparsers.add_parser("dashboard", help="Render Maxilun CLI HUD & routing matrix")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    dispatch = {
        "route": cmd_route,
        "scan": cmd_scan,
        "snapshot": cmd_snapshot,
        "diff": cmd_diff,
        "context": cmd_context,
        "lint": cmd_lint,
        "verify": cmd_verify,
        "init-hook": cmd_init_hook,
        "test": cmd_test,
        "dashboard": cmd_dashboard
    }

    handler = dispatch.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
