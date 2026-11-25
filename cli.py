#!/usr/bin/env python3
"""
Maxilun Unified CLI — Single Production Entrypoint
==================================================

Unifies all autonomous capabilities of the Maxilun ecosystem:
  maxilun route "<prompt>"       # Triage Type 1/2 & multi-wave DAG dispatch
  maxilun scan [paths...]        # Incremental AST graph scan + report
  maxilun locate "<question>"    # Ranked file:line read plan with excerpts
  maxilun query <op> <symbol>    # Graph query (defOf, callsIn, callsOut, importersOf)
  maxilun serve                  # Start interactive Knowledge Graph web UI
  maxilun snapshot [path]        # Archive dated graph snapshot
  maxilun diff <t1> <t2>         # Compare architectural graphs/snapshots
  maxilun context <symbol>       # Fast LLM prompt blast-radius context
  maxilun lint [path] [--fix]    # 45 AI design tells linter & auto-fixer
  maxilun verify <surface>       # Surface & mobile 320px reflow audit
  maxilun new [target]           # Scaffold slop-free app (Next.js/Vite-PHP/GAS)
  maxilun alias                  # Manage custom agent personas & team presets
  maxilun n8n-lint <workflow>    # Validate n8n workflow JSON + Mermaid diagram
  maxilun init-hook [path]       # Install git pre-commit purity gate hook
  maxilun uninstall-hook [path]  # Remove git pre-commit purity gate hook
  maxilun test                   # Run full ecosystem validation test suite
  maxilun dashboard [--open]     # Generate interactive Maxilun visual HUD
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


def _load_module(mod_name: str, path: Path):
    import importlib.util
    spec = importlib.util.spec_from_file_location(mod_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _kg_cli():
    return _load_module("maxilun_kg_cli", REPO_ROOT / "skills" / "maxilun-knowledge-graph" / "cli.py")


def cmd_alias(args):
    _load_module("harness_cli", REPO_ROOT / "harness" / "cli.py").cmd_alias(args)


def cmd_n8n_lint(args):
    path = REPO_ROOT / "skills" / "maxilun-n8n" / "scripts" / "n8n_validate.py"
    module = _load_module("n8n_val_mod", path)
    sys.argv = [str(path), args.workflow]
    if args.mermaid:
        sys.argv.append("--mermaid")
    module.main()


def cmd_new(args):
    module = _load_module("greenfield_mod", REPO_ROOT / "skills" / "maxilun-scaffold" / "scripts" / "greenfield.py")

    target_dir = Path(args.target or ".").resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    if args.stack == "nextjs":
        module.scaffold_nextjs(target_dir, args.name, args.title, domain=args.domain)
    elif args.stack == "vite-php":
        module.scaffold_vite_php(target_dir, args.name, args.title, domain=args.domain)
    elif args.stack == "gas":
        module.scaffold_gas(target_dir, args.name, args.title, domain=args.domain)

    print(f"\nGreenfield project '{args.name}' ({args.stack} / domain: {args.domain}) generated at {target_dir}")


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
    return _kg_cli().cmd_scan(args)


def cmd_snapshot(args):
    return _kg_cli().cmd_snapshot(args)


def cmd_diff(args):
    return _kg_cli().cmd_diff(args)


def cmd_context(args):
    return _kg_cli().cmd_context(args)


def cmd_locate(args):
    return _kg_cli().cmd_locate(args)


def cmd_query(args):
    return _kg_cli().cmd_query(args)


def cmd_serve(args):
    return _kg_cli().cmd_serve(args)


def cmd_uninstall_hook(args):
    _load_module("harness_cli", REPO_ROOT / "harness" / "cli.py").cmd_uninstall_hook(args)


def cmd_lint(args):
    import importlib
    ui_linter_mod = importlib.import_module("scripts.ui-purity-linter")
    target_path = Path(args.path or ".").resolve()
    if not target_path.exists():
        print(f"Error: Path '{target_path}' does not exist.", file=sys.stderr)
        sys.exit(1)
    linter = ui_linter_mod.UIPurityLinter()

    if args.fix:
        fix_res = linter.fix_path(target_path)
        if not args.json:
            print(f"\nPurity Auto-Fixer: Remediated {fix_res['fixed_files']} / {fix_res['total_files']} files.")
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
        report_data = engine.audit_surface_file(target_file, static_only=getattr(args, "static", False))
    except Exception as e:
        print(f"Error during verification: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        import json
        print(json.dumps(report_data, indent=2))
    else:
        print("\n" + engine.format_markdown_report(report_data) + "\n")

    sys.exit(report_data["exit_code"])


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
    from harness.dashboard import DashboardGenerator
    out_path = DashboardGenerator.generate(REPO_ROOT)
    print(f"Maxilun dashboard generated: {out_path}")
    if getattr(args, "open", False):
        import webbrowser
        try:
            webbrowser.open(str(out_path.resolve()))
        except Exception:
            pass


def main():
    parser = argparse.ArgumentParser(
        prog="maxilun",
        description="Maxilun Unified CLI — Single Production Entrypoint",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
        allow_abbrev=False,
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

    # locate
    locate_parser = subparsers.add_parser("locate", help="Locate code by plain-language question or stack trace")
    locate_parser.add_argument("question", nargs="+", help="Question, stack trace, or symbol")
    locate_parser.add_argument("--path", help="Project path (default: .)")
    locate_parser.add_argument("--graph", "-g", help="Graph file path")
    locate_parser.add_argument("--also", help="Comma-separated identifier hints")
    locate_parser.add_argument("--top", type=int, default=5, help="Max files (default: 5)")
    locate_parser.add_argument("--lines", type=int, default=14, help="Max excerpt lines (default: 14)")
    locate_parser.add_argument("--budget", type=int, default=6000, help="Total excerpt budget (default: 6000)")
    locate_parser.add_argument("--tests", action="store_true", help="Include test files equally")
    locate_parser.add_argument("--refresh", action="store_true", help="Refresh index before locating")
    locate_parser.add_argument("--json", action="store_true", help="JSON output format")

    # query
    query_parser = subparsers.add_parser("query", help="Query symbols from Knowledge Graph")
    query_parser.add_argument("operator", help="Operator (defOf:, callsIn:, callsOut:, importersOf:)")
    query_parser.add_argument("symbol", nargs="?", default="", help="Target symbol or file")
    query_parser.add_argument("--json", action="store_true", help="JSON output format")
    query_parser.add_argument("--graph", "-g", help="Graph file path")
    query_parser.add_argument("--path", help="Project path")

    # serve
    serve_parser = subparsers.add_parser("serve", help="Start interactive Knowledge Graph visualizer server")
    serve_parser.add_argument("--port", "-p", type=int, default=8765, help="Server port (default: 8765)")
    serve_parser.add_argument("--host", default="127.0.0.1", help="Server host (default: 127.0.0.1)")
    serve_parser.add_argument("--open", "-o", action="store_true", help="Auto-open browser")
    serve_parser.add_argument("--graph", "-g", help="Existing graph JSON file")

    # lint
    lint_parser = subparsers.add_parser("lint", help="Audit code against 45 AI Design Tells taxonomy")
    lint_parser.add_argument("path", nargs="?", default=".", help="File or directory to scan")
    lint_parser.add_argument("--fix", action="store_true", help="Auto-remediate detected violations")
    lint_parser.add_argument("--strict", action="store_true", help="Fail if any warning exists")
    lint_parser.add_argument("--json", action="store_true", help="JSON output format")

    # verify
    verify_parser = subparsers.add_parser("verify", help="Audit surface HTML/SVG for syntax, mobile 320px reflow, and a11y")
    verify_parser.add_argument("surface", help="HTML or SVG surface file to audit")
    verify_parser.add_argument("--static", action="store_true", help="Skip headless browser launch (returns exit 2 [UNVERIFIED] when static passes)")
    verify_parser.add_argument("--json", action="store_true", help="JSON output format")

    # new
    new_parser = subparsers.add_parser("new", help="Scaffold a slop-free greenfield application (Next.js, Vite-PHP, GAS)")
    new_parser.add_argument("target", nargs="?", default=".", help="Target project root directory")
    new_parser.add_argument("--stack", choices=["nextjs", "vite-php", "gas"], default="nextjs", help="Technology stack")
    new_parser.add_argument("--domain", choices=["edtech", "saas", "ledger"], default="edtech", help="Domain archetype")
    new_parser.add_argument("--name", default="my-app", help="Project slug name")
    new_parser.add_argument("--title", default="EduCore Platform", help="Human-readable project title")

    # alias
    alias_parser = subparsers.add_parser("alias", help="Manage custom agent personas, callnames, and team presets")
    alias_parser.add_argument("--preset", choices=["default", "nusantara-squad", "global-forge"], default=None, help="Apply a built-in agent persona preset")
    alias_parser.add_argument("--list-presets", action="store_true", help="List all available persona presets")
    alias_parser.add_argument("--show", action="store_true", help="Show currently configured agent aliases")
    alias_parser.add_argument("--set", nargs=2, metavar=("AGENT", "ALIAS"), help="Assign a custom alias to an agent (e.g. --set maxilun-architect Bram)")
    alias_parser.add_argument("--callsign", default="", help="Optional role title / callsign when using --set")
    alias_parser.add_argument("--interactive", action="store_true", help="Interactive persona preset setup")

    # n8n-lint
    n8n_parser = subparsers.add_parser("n8n-lint", help="Validate an n8n workflow JSON file and generate Mermaid diagram")
    n8n_parser.add_argument("workflow", help="Path to .json workflow file")
    n8n_parser.add_argument("--mermaid", action="store_true", help="Emit Mermaid flowchart")

    # init-hook / uninstall-hook
    hook_parser = subparsers.add_parser("init-hook", help="Install git pre-commit purity gate hook")
    hook_parser.add_argument("path", nargs="?", default=None, help="Repository root path")
    subparsers.add_parser("uninstall-hook", help="Remove Maxilun git pre-commit purity gate hook")

    # test
    test_parser = subparsers.add_parser("test", help="Run full ecosystem validation test suite")

    # dashboard
    dash_parser = subparsers.add_parser("dashboard", help="Render Maxilun CLI HUD & routing matrix")
    dash_parser.add_argument("--open", action="store_true", help="Open generated dashboard in default browser")

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
        "locate": cmd_locate,
        "query": cmd_query,
        "serve": cmd_serve,
        "lint": cmd_lint,
        "verify": cmd_verify,
        "init-hook": cmd_init_hook,
        "uninstall-hook": cmd_uninstall_hook,
        "new": cmd_new,
        "alias": cmd_alias,
        "n8n-lint": cmd_n8n_lint,
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
