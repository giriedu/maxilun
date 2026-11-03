#!/usr/bin/env python3
"""Maxilun Harness CLI.

Usage:
    python -m harness check [<path> | -]
    python -m harness route "<prompt>"
    python -m harness bench [--json] [-o <report.json>]
    python -m harness inspect <path>
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


def cmd_check(args):
    validator = PurityValidator()
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
        print(f"File: {target}")
        print(res.summary())
        sys.exit(0 if res.passed else 1)

    elif p.is_dir():
        total_files = 0
        failed_files = 0
        for f in p.rglob("*"):
            if f.is_file() and f.suffix in {".ts", ".tsx", ".js", ".jsx", ".py", ".md", ".go", ".sql"}:
                total_files += 1
                text = f.read_text(encoding="utf-8", errors="replace")
                res = validator.validate_text(text, file_path=str(f))
                if not res.passed:
                    failed_files += 1
                    print(f"\n❌ {f.relative_to(p)}")
                    for v in res.violations:
                        print(f"   [{v.rule_id}] {v.message}")

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


def main():
    parser = argparse.ArgumentParser(
        prog="maxilun-harness",
        description="Maxilun Automated Evaluation, Purity Gate & Triage Harness."
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

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "check":
        cmd_check(args)
    elif args.command == "route":
        cmd_route(args)
    elif args.command == "bench":
        cmd_bench(args)


if __name__ == "__main__":
    main()
