"""Maxilun Autonomous Agent Loop & Orchestrator Execution Engine.

Implements the complete execution lifecycle:
- Match specialist skill & build system prompt
- Decision reversibility triage (Type 1 vs Type 2)
- Autonomous ReAct loop with native tool execution
- Active middleware (pre-flight KG inspection, Purity Gate feedback)
- Factual verification reporting
Zero external dependencies.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, Callable

from .skills_loader import SkillsLoader, SkillDefinition
from .context import SessionContext
from .provider import UniversalProvider, ProviderResponse
from .middleware import MiddlewarePipeline
from ..tools.registry import ToolRegistry


class MaxilunAgentLoop:
    """The central agent runtime engine for the Maxilun ecosystem."""

    def __init__(
        self,
        repo_root: Optional[Path] = None,
        provider: Optional[UniversalProvider] = None,
        max_turns: int = 10,
        verbose: bool = True
    ):
        self.root = repo_root or Path.cwd()
        self.loader = SkillsLoader(self.root)
        self.registry = ToolRegistry(self.root)
        self.provider = provider or UniversalProvider()
        self.middleware = MiddlewarePipeline(self.root)
        self.max_turns = max_turns
        self.verbose = verbose

    def run_task(self, prompt: str, on_chunk: Optional[Callable[[str], None]] = None) -> SessionContext:
        """Executes a complete task end-to-end through the Maxilun ecosystem."""
        context = SessionContext()

        # 1. Routing & Specialist Selection
        decision_type = self.middleware.check_reversibility(prompt)
        context.decision_type = decision_type

        active_skill = self.loader.match_skill(prompt)
        context.active_skill = active_skill.name
        context.record_swarm_event(active_skill.name, "Routed task", prompt[:80])

        if self.verbose:
            print(f"\n🌑 Maxilun Harness Engine: [Active Specialist: {active_skill.name}] (Type {decision_type})")
            print(f"   Contract: Owns {active_skill.contract.get('Owns', 'implementation')[:60]}...")
        # 2. Compile Active System Prompt
        system_prompt = self.loader.build_system_prompt(active_skill.name)
        context.add_system_message(system_prompt)
        context.add_user_message(prompt)

        # 3. Agent Execution Loop
        turn = 0
        while turn < self.max_turns:
            turn += 1
            if self.verbose:
                print(f"⚡ Turn {turn}/{self.max_turns}: Requesting completion from {self.provider.model}...")

            messages = context.to_provider_messages()
            tools = self.registry.get_tool_schemas()
            resp: ProviderResponse = self.provider.complete(messages, tools=tools)

            if resp.error:
                if self.verbose:
                    print(f"❌ Provider Error: {resp.error}")
                context.add_assistant_message(f"Execution Error: {resp.error}")
                break

            context.tokens_in += resp.prompt_tokens
            context.tokens_out += resp.completion_tokens

            # Record assistant message
            context.add_assistant_message(resp.content, resp.tool_calls)
            if resp.content and on_chunk:
                on_chunk(resp.content)

            # If no tool calls, validate purity and decide whether to yield
            if not resp.tool_calls:
                # Middleware: Purity Gate check
                purity_correction = self.middleware.post_model_response(resp.content or "")
                if purity_correction and turn < self.max_turns - 1:
                    if self.verbose:
                        print("⚠️ Purity Gate detected slop/invariants issue — injecting corrective feedback loop...")
                    context.purity_warnings.append(purity_correction)
                    context.add_user_message(purity_correction)
                    continue
                else:
                    break

            # Handle Tool Calls
            for tool_call in resp.tool_calls:
                fn_name = tool_call["function"]["name"]
                args_raw = tool_call["function"]["arguments"]
                call_id = tool_call["id"]

                try:
                    args = json.loads(args_raw) if isinstance(args_raw, str) else args_raw
                except Exception:
                    args = {}

                # Middleware: Pre-flight Knowledge Graph inspection before file edits
                pre_notice = self.middleware.before_tool_call(fn_name, args)
                if pre_notice and self.verbose:
                    print(f"   🔍 {pre_notice}")

                if self.verbose:
                    print(f"   🛠️ Tool Call: {fn_name}({', '.join(f'{k}={repr(v)[:30]}' for k, v in args.items())})")

                # Track changes in context
                if fn_name in ("write_file", "edit_file"):
                    context.record_file_edit(args.get("path", ""))
                    context.record_swarm_event(active_skill.name, f"Modified file", args.get("path", ""))
                elif fn_name == "execute_bash":
                    context.record_command(args.get("command", ""))
                    context.record_swarm_event(active_skill.name, "Executed command", args.get("command", "")[:50])
                else:
                    context.record_swarm_event(active_skill.name, f"Tool call {fn_name}", str(args)[:50])
                # Execute tool
                result = self.registry.execute(fn_name, args)
                result_str = json.dumps(result, ensure_ascii=False)

                context.add_tool_result(call_id, fn_name, result_str)

        if self.verbose:
            summary = context.summary()
            print("\n" + "=" * 50)
            print(f"🎉 Task Execution Completed — Session {summary['session_id']}")
            print(f"   Specialist : {summary['active_skill']}")
            print(f"   Decision   : {summary['decision_type']}")
            print(f"   Files Mod  : {len(summary['touched_files'])} file(s)")
            print(f"   Commands   : {summary['commands_run_count']} command(s)")
            print(f"   Duration   : {summary['duration_seconds']}s")
            print("=" * 50)

        # Save swarm events artifact
        out_dir = self.root / "maxilun-out"
        out_dir.mkdir(exist_ok=True)
        try:
            (out_dir / "swarm_events.json").write_text(json.dumps(context.swarm_events, indent=2), encoding="utf-8")
        except Exception:
            pass

        return context
