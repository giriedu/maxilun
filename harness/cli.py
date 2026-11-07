#!/usr/bin/env python3
"""Maxilun Harness CLI — Complete Agent Runtime & Governance Center.

Usage:
    python -m harness chat
    python -m harness run "<task prompt>"
    python -m harness skills
    python -m harness dashboard [--open]
    python -m harness check [<path> | -]
    python -m harness route "<prompt>"
    python -m harness bench [--json] [--view] [-o <report.json>]
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
import webbrowser
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
from harness.dashboard import DashboardGenerator
from harness.engine.skills_loader import SkillsLoader
from harness.engine.provider import UniversalProvider
from harness.engine.agent_loop import MaxilunAgentLoop


def cmd_run(args):
    provider = UniversalProvider(
        provider=args.provider,
        endpoint=args.endpoint,
        api_key=args.api_key,
        model=args.model
    )
    agent = MaxilunAgentLoop(provider=provider, max_turns=args.max_turns)
    agent.run_task(args.task)

def cmd_agent(args):
    agent_name = args.name.lower().strip()
    macro_map = {
        "scout": "maxilun-knowledge-graph",
        "maxilun-scout": "maxilun-knowledge-graph",
        "architect": "maxilun-architect",
        "maxilun-architect": "maxilun-architect",
        "maker": "maxilun-engineer",
        "maxilun-maker": "maxilun-engineer",
        "studio": "maxilun-craft",
        "maxilun-studio": "maxilun-craft",
        "verifier": "maxilun-verify",
        "maxilun-verifier": "maxilun-verify",
        "orchestrator": "maxilun",
        "maxilun-orchestrator": "maxilun"
    }
    target = macro_map.get(agent_name, agent_name)
    if not target.startswith("maxilun"):
        target = f"maxilun-{target}"

    provider = UniversalProvider(
        provider=args.provider,
        endpoint=args.endpoint,
        api_key=args.api_key,
        model=args.model
    )
    agent_loop = MaxilunAgentLoop(provider=provider, max_turns=args.max_turns)
    print(f"\n🚀 Launching Autonomous Macro-Agent: [{agent_name}] (Mapped skill: {target})")
    print(f"   Task: {args.task}")
    print("=" * 65)
    agent_loop.run_task(args.task, forced_skill=target)



def cmd_chat(args):
    provider = UniversalProvider(
        provider=args.provider,
        endpoint=args.endpoint,
        api_key=args.api_key,
        model=args.model
    )
    agent = MaxilunAgentLoop(provider=provider, max_turns=args.max_turns)
    print("🌑 Maxilun Harness Agent Session (type 'exit' or 'quit' to end)")
    print("   Governed by Maxilun Core Rules & 21 Specialist Skills (22 skills total)")
    print("=" * 60)

    while True:
        try:
            prompt = input("\nmaxilun> ").strip()
            if not prompt:
                continue
            if prompt.lower() in ("exit", "quit"):
                print("Session ended.")
                break
            agent.run_task(prompt)
        except (KeyboardInterrupt, EOFError):
            print("\nSession interrupted.")
            break


def cmd_skills(args):
    loader = SkillsLoader()
    skills = loader.list_skills()
    print(f"\n🌑 Maxilun Ecosystem Skills ({len(skills)} specialists discovered):")
    print("=" * 75)
    for s in skills:
        status = "✅ PASS" if s.line_count <= 300 else "❌ OVER"
        triggers = ", ".join(s.triggers[:3]) if s.triggers else "none"
        print(f"[{status}] {s.name:<25} ({s.line_count:3d} lines, {len(s.references):2d} refs) | Triggers: {triggers}")
    print("=" * 75)


def cmd_dashboard(args):
    out_path = DashboardGenerator.generate()
    print(f"✅ Maxilun Interactive Dashboard generated: {out_path}")
    if args.open:
        try:
            webbrowser.open(str(out_path.resolve()))
        except Exception:
            pass


def cmd_swarm(args):
    out_path = DashboardGenerator.generate()
    print(f"✨ Launching Maxilun Live Swarm Studio: {out_path}")
    try:
        webbrowser.open(str(out_path.resolve()))
    except Exception:
        pass


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
        skip_dirs = {".git", "node_modules", "__pycache__", ".next", "dist", "build", "maxilun-out", ".agents", ".claude"}
        for f in p.rglob("*"):
            if any(part in skip_dirs or part.startswith("_maxilun_backup") for part in f.parts):
                continue
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

    if args.view:
        dashboard_path = DashboardGenerator.generate()
        print(f"  - Interactive Dashboard: {dashboard_path}")
        try:
            webbrowser.open(str(dashboard_path.resolve()))
        except Exception:
            pass


def cmd_eval(args):
    target_model = args.model or "deepseek-chat"
    print(f"🌑 Starting Live Model Evaluation (Provider: {args.provider or 'auto'}, Model: {target_model})...")
    evaluator = LiveModelEvaluator(
        provider=args.provider,
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

def cmd_doctor(args):
    print("\n🌑 Maxilun Ecosystem Healthcheck (Doctor):")
    print("=" * 65)
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    py_ok = sys.version_info >= (3, 8)
    print(f"[{'✅ PASS' if py_ok else '❌ FAIL'}] Python runtime: {py_ver} (>= 3.8 required)")

    import shutil
    node_bin = shutil.which("node")
    npx_bin = shutil.which("npx")
    print(f"[{'✅ PASS' if node_bin else '⚠️  WARN'}] Node.js runtime: {node_bin or 'Not found (optional for npx skills)'}")
    print(f"[{'✅ PASS' if npx_bin else '⚠️  WARN'}] npx package runner: {npx_bin or 'Not found'}")

    loader = SkillsLoader()
    skills = loader.list_skills()
    skills_ok = len(skills) >= 23 and all(s.line_count <= 300 for s in skills)
    print(f"[{'✅ PASS' if skills_ok else '❌ FAIL'}] Skills inventory: {len(skills)}/23 skills discovered (all <= 300 lines)")

    repo_root = Path(__file__).resolve().parent.parent
    agents_dir = repo_root / "agents"
    agents_found = list(agents_dir.glob("*.md")) if agents_dir.exists() else []
    agents_ok = len(agents_found) >= 6
    print(f"[{'✅ PASS' if agents_ok else '❌ FAIL'}] Autonomous agents: {len(agents_found)}/6 macro-agents present in agents/")
    for a in sorted(agents_found):
        print(f"     • {a.name}")

    user_home = Path.home()
    detected_editors = []
    if (user_home / ".claude").exists() or (repo_root / ".claude").exists():
        detected_editors.append("Claude Code")
    if (user_home / ".agents").exists() or (repo_root / ".agents").exists():
        detected_editors.append("Antigravity / Zed")
    if (user_home / ".cursor").exists():
        detected_editors.append("Cursor")
    if (user_home / ".codex").exists():
        detected_editors.append("Codex")
    if (user_home / ".config" / "opencode").exists() or (user_home / ".opencode").exists():
        detected_editors.append("OpenCode")
    print(f"[ℹ️  INFO] Detected AI Platforms: {', '.join(detected_editors) if detected_editors else 'None (standalone mode)'}")
    print("=" * 65)
    print("🎉 Maxilun ecosystem is ready for multi-agent autonomous engineering.\n")



def main():
    parser = argparse.ArgumentParser(
        prog="maxilun-harness",
        description="Maxilun Autonomous Agent Runtime, Purity Gate & Quality Governance Center."
    )
    subparsers = parser.add_subparsers(dest="command")

    # chat
    chat_parser = subparsers.add_parser("chat", help="Start an interactive Maxilun agent session in terminal")
    chat_parser.add_argument("--provider", choices=["deepseek", "openai", "openrouter", "ollama", "groq", "gemini"], default=None, help="Provider preset")
    chat_parser.add_argument("--model", default=None, help="Model name (e.g. deepseek-chat, gpt-4o, qwen2.5-coder:7b)")
    chat_parser.add_argument("--endpoint", default=None, help="LLM endpoint URL")
    chat_parser.add_argument("--api-key", default=None, help="LLM API key")
    chat_parser.add_argument("--max-turns", type=int, default=10, help="Max interaction turns")

    # run
    run_parser = subparsers.add_parser("run", help="Execute an autonomous task through Maxilun agent harness")
    run_parser.add_argument("task", help="Task description or prompt to execute")
    run_parser.add_argument("--provider", choices=["deepseek", "openai", "openrouter", "ollama", "groq", "gemini"], default=None, help="Provider preset")
    run_parser.add_argument("--model", default=None, help="Model name")
    run_parser.add_argument("--endpoint", default=None, help="LLM endpoint URL")
    run_parser.add_argument("--api-key", default=None, help="LLM API key")
    run_parser.add_argument("--max-turns", type=int, default=10, help="Max interaction turns")

    # agent
    agent_parser = subparsers.add_parser("agent", help="Directly run a macro-role agent (scout, architect, maker, studio, verifier, orchestrator)")
    agent_parser.add_argument("name", help="Macro agent name: scout, architect, maker, studio, verifier, orchestrator")
    agent_parser.add_argument("task", help="Task prompt to execute")
    agent_parser.add_argument("--provider", choices=["deepseek", "openai", "openrouter", "ollama", "groq", "gemini"], default=None, help="Provider preset")
    agent_parser.add_argument("--model", default=None, help="Model name")
    agent_parser.add_argument("--endpoint", default=None, help="LLM endpoint URL")
    agent_parser.add_argument("--api-key", default=None, help="LLM API key")
    agent_parser.add_argument("--max-turns", type=int, default=10, help="Max interaction turns")

    # skills
    subparsers.add_parser("skills", help="List and inspect all 23 Maxilun ecosystem skills (1 orchestrator + 22 specialists)")
    subparsers.add_parser("doctor", help="Run diagnostic healthcheck on environment, 23 skills, and 6 autonomous agents")

    # dashboard
    dash_parser = subparsers.add_parser("dashboard", help="Generate and open the interactive visual HTML dashboard")
    dash_parser.add_argument("--open", action="store_true", default=True, help="Automatically open in browser")

    # swarm
    subparsers.add_parser("swarm", help="Launch the Live Swarm Studio multiplayer agent visualizer in browser")

    # check
    check_parser = subparsers.add_parser("check", help="Validate a file, text, or directory against Purity Gate & AST")
    check_parser.add_argument("path", nargs="?", default=None, help="Target file/folder or '-' for stdin")

    # route
    route_parser = subparsers.add_parser("route", help="Simulate Orchestrator reversibility triage and specialist routing")
    route_parser.add_argument("prompt", help="User task prompt to classify")

    # bench
    bench_parser = subparsers.add_parser("bench", help="Run canonical Maxilun engineering benchmarks")
    bench_parser.add_argument("--json", action="store_true", help="Output JSON instead of Markdown")
    bench_parser.add_argument("--view", action="store_true", help="Generate and open interactive visual dashboard")
    bench_parser.add_argument("-o", "--output", default="benchmark_report.json", help="Output JSON file name")

    # eval
    eval_parser = subparsers.add_parser("eval", help="Run live model comparison evaluation against OpenAI/DeepSeek endpoint")
    eval_parser.add_argument("--provider", choices=["deepseek", "openai", "openrouter", "ollama", "groq", "gemini"], default=None, help="Provider preset")
    eval_parser.add_argument("--model", default=None, help="Target model name")
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
        "chat": cmd_chat,
        "run": cmd_run,
        "agent": cmd_agent,
        "skills": cmd_skills,
        "dashboard": cmd_dashboard,
        "swarm": cmd_swarm,
        "check": cmd_check,
        "route": cmd_route,
        "bench": cmd_bench,
        "eval": cmd_eval,
        "verify-code": cmd_verify_code,
        "install-hook": cmd_install_hook,
        "uninstall-hook": cmd_uninstall_hook,
        "generate-ci": cmd_generate_ci,
        "doctor": cmd_doctor,
    }

    fn = dispatch.get(args.command)
    if fn:
        fn(args)


if __name__ == "__main__":
    main()
