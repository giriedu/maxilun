#!/usr/bin/env python3
"""Maxilun Harness CLI.

Usage:
    python -m harness check [<path> | -]
    python -m harness route "<prompt>"
    python -m harness bench [--json] [-o <report.json>]
    python -m harness eval [--model <model>] [--endpoint <url>] [--api-key <key>]
    python -m harness verify-code <path>
    python -m harness install-hook
    python -m harness uninstall-hook
    python -m harness generate-ci
"""

import argparse
import sys
import os
import json
from pathlib import Path

# Add repo root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from harness.purity_validator import PurityValidator
from harness.router import MaxilunRouter
from harness.benchmarks import BenchmarkRunner
from harness.ast_inspector import ASTInspector
from harness.sandbox_runner import SandboxRunner
from harness.live_evaluator import LiveModelEvaluator
from harness.hook_installer import HookInstaller


def cmd_check(args):
    validator = PurityValidator()
    ast_inspector = ASTInspector()
    target = args.path

    if target == "-" or (target is None and not sys.stdin.isatty()):
        content = sys.stdin.read()
        res = validator.validate_text(content, file_path="stdin")
        print(res.summary())
        sys.exit(0 if res.passed else 1)

    if not target:
        print("Error: Target file or path required, or '-' for stdin.", file=sys.stderr)
        sys.exit(2)

    p = Path(target)
    if not p.exists():
        print(f"Error: Path '{target}' not found.", file=sys.stderr)
        sys.exit(2)

    if p.is_file():
        text = p.read_text(encoding="utf-8", errors="replace")
        res = validator.validate_text(text, file_path=str(p))
        ast_res = ast_inspector.inspect_file(str(p))

        print(f"File: {target}")
        print(res.summary())
        if not ast_res.passed:
            print(f"\n{ast_res.summary()}")

        passed = res.passed and ast_res.passed
        sys.exit(0 if passed else 1)

    elif p.is_dir():
        total_files = 0
        failed_files = 0
        for f in p.rglob("*"):
            if f.is_file() and f.suffix in {".ts", ".tsx", ".js", ".jsx", ".py", ".md", ".go", ".sql"}:
                total_files += 1
                text = f.read_text(encoding="utf-8", errors="replace")
                res = validator.validate_text(text, file_path=str(f))
                ast_res = ast_inspector.inspect_file(str(f))

                if not (res.passed and ast_res.passed):
                    failed_files += 1
                    print(f"\n❌ {f.relative_to(p)}")
                    for v in res.violations:
                        print(f"   [{v.rule_id}] {v.message}")
                    for fnd in ast_res.findings:
                        print(f"   [AST-{fnd.rule_id}] {fnd.message}")

        print(f"\nPurity Scan Complete: {total_files - failed_files}/{total_files} passed.")
        sys.exit(1 if failed_files > 0 else 0)


def cmd_route(args):
    router = MaxilunRouter()
    prompt = args.prompt
    decision = router.route(prompt)
    print("\n🌑 Maxilun Master Orchestrator — Triage Result")
    print("=" * 50)
    print(decision.summary())
    print("=" * 50)


def cmd_bench(args):
    runner = BenchmarkRunner()
    print("🌑 Running Maxilun Engineering Harness Benchmarks...")
    report = runner.run_all()

    if args.json:
        data = {
            "total_benchmarks": report.total_benchmarks,
            "raw_average_score": report.raw_average_score,
            "maxilun_average_score": report.maxilun_average_score,
            "overall_improvement": report.overall_improvement,
            "results": [
                {
                    "id": r.benchmark_id,
                    "title": r.title,
                    "prompt": r.prompt,
                    "raw_score": r.raw_score,
                    "raw_passed": r.raw_passed,
                    "maxilun_score": r.maxilun_score,
                    "maxilun_passed": r.maxilun_passed,
                    "score_delta": r.score_delta,
                }
                for r in report.results
            ]
        }
        print(json.dumps(data, indent=2))
    else:
        print(report.to_markdown())

    # Save artifact to maxilun-out/ if possible
    out_dir = Path("maxilun-out")
    out_dir.mkdir(exist_ok=True)
    report_file = out_dir / (args.output or "benchmark_report.json")
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump({
            "total_benchmarks": report.total_benchmarks,
            "raw_average_score": report.raw_average_score,
            "maxilun_average_score": report.maxilun_average_score,
            "overall_improvement": report.overall_improvement,
            "results": [
                {
                    "id": r.benchmark_id,
                    "title": r.title,
                    "raw_score": r.raw_score,
                    "maxilun_score": r.maxilun_score,
                    "score_delta": r.score_delta,
                    "verdict": r.governance_verdict
                }
                for r in report.results
            ]
        }, f, indent=2)

    md_file = out_dir / "BENCHMARK_REPORT.md"
    md_file.write_text(report.to_markdown(), encoding="utf-8")
    print(f"\nArtifacts generated:")
    print(f"  - JSON Report: {report_file}")
    print(f"  - Markdown Report: {md_file}")


def cmd_eval(args):
    print(f"🌑 Starting Live Model Evaluation (Model: {args.model})...")
    evaluator = LiveModelEvaluator(
        api_key=args.api_key,
        endpoint=args.endpoint,
        model=args.model
    )
    report = evaluator.run_evaluation()

    if args.json:
        data = {
            "model": report.model,
            "endpoint": report.endpoint,
            "total_scenarios": report.total_scenarios,
            "raw_avg_score": report.raw_avg_score,
            "maxilun_avg_score": report.maxilun_avg_score,
            "overall_delta": report.overall_delta,
            "scenarios": [
                {
                    "id": s.scenario_id,
                    "prompt": s.prompt,
                    "raw_score": s.raw_purity_score,
                    "maxilun_score": s.maxilun_purity_score,
                    "delta": s.score_delta
                }
                for s in report.scenarios
            ]
        }
        print(json.dumps(data, indent=2))
    else:
        print(report.to_markdown())


def cmd_verify_code(args):
    target = args.path
    p = Path(target)
    if not p.exists():
        print(f"Error: File '{target}' not found.", file=sys.stderr)
        sys.exit(2)

    content = p.read_text(encoding="utf-8", errors="replace")
    ext = p.suffix.lower()

    print(f"🌑 Verifying Code & Runtime Sandbox for: {target}")
    print("=" * 50)

    # 1. AST Inspection
    ast_inspector = ASTInspector()
    ast_res = ast_inspector.inspect_file(str(p))
    print(ast_res.summary())

    # 2. Sandbox Execution
    sandbox_res = None
    if ext == ".py":
        sandbox_res = SandboxRunner.verify_python(content)
    elif ext in (".js", ".ts"):
        sandbox_res = SandboxRunner.verify_javascript(content)
    elif ext == ".sql":
        sandbox_res = SandboxRunner.verify_sql_migration(content)

    if sandbox_res:
        print("\n" + sandbox_res.summary())

    passed = ast_res.passed and (sandbox_res is None or sandbox_res.passed)
    print("=" * 50)
    print(f"Final Code Verdict: {'✅ PASS' if passed else '❌ FAIL'}")
    sys.exit(0 if passed else 1)


def cmd_install_hook(args):
    ok = HookInstaller.install_git_hook()
    sys.exit(0 if ok else 1)


def cmd_uninstall_hook(args):
    ok = HookInstaller.uninstall_git_hook()
    sys.exit(0 if ok else 1)


def cmd_generate_ci(args):
    ok = HookInstaller.generate_ci_workflow()
    sys.exit(0 if ok else 1)


def main():
    parser = argparse.ArgumentParser(
        prog="maxilun-harness",
        description="Maxilun Automated Evaluation, Purity Gate, AST Inspector & Triage Harness."
    )
    subparsers = parser.add_subparsers(dest="command")

    # check
    check_parser = subparsers.add_parser("check", help="Validate a file, text, or directory against Purity Gate")
    check_parser.add_argument("path", nargs="?", default=None, help="Target file/folder or '-' for stdin")

    # route
    route_parser = subparsers.add_parser("route", help="Simulate Orchestrator reversibility triage and specialist routing")
    route_parser.add_argument("prompt", help="User task prompt to classify")

    # bench
    bench_parser = subparsers.add_parser("bench", help="Run canonical Maxilun engineering benchmarks")
    bench_parser.add_argument("--json", action="store_true", help="Output JSON instead of Markdown")
    bench_parser.add_argument("-o", "--output", default="benchmark_report.json", help="Output JSON file name")

    # eval
    eval_parser = subparsers.add_parser("eval", help="Run live model comparison evaluation against OpenAI/DeepSeek endpoint")
    eval_parser.add_argument("--model", default="deepseek-chat", help="Target model name (default: deepseek-chat)")
    eval_parser.add_argument("--endpoint", default=None, help="OpenAI-compatible base URL")
    eval_parser.add_argument("--api-key", default=None, help="Model provider API key")
    eval_parser.add_argument("--json", action="store_true", help="Output JSON instead of Markdown")

    # verify-code
    verify_parser = subparsers.add_parser("verify-code", help="Run AST security inspection and in-memory runtime sandbox")
    verify_parser.add_argument("path", help="Path to code file (.py, .ts, .js, .sql)")

    # Git hooks & CI
    subparsers.add_parser("install-hook", help="Install Maxilun pre-commit Git hook in .git/hooks/pre-commit")
    subparsers.add_parser("uninstall-hook", help="Remove Maxilun pre-commit Git hook")
    subparsers.add_parser("generate-ci", help="Generate GitHub Actions workflow in .github/workflows/maxilun-harness.yml")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    dispatch = {
        "check": cmd_check,
        "route": cmd_route,
        "bench": cmd_bench,
        "eval": cmd_eval,
        "verify-code": cmd_verify_code,
        "install-hook": cmd_install_hook,
        "uninstall-hook": cmd_uninstall_hook,
        "generate-ci": cmd_generate_ci,
    }

    fn = dispatch.get(args.command)
    if fn:
        fn(args)


if __name__ == "__main__":
    main()
