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
from typing import Dict, Any, Optional, Callable, Set, List

from .skills_loader import SkillsLoader, SkillDefinition
from .context import SessionContext
from .provider import UniversalProvider, ProviderResponse
from .middleware import MiddlewarePipeline
from .compressor import OutputCompressor
from .meeting import AgentMeeting, MEETING_TOOLS, MAX_PARTICIPANTS, MAX_ROUNDS
from ..tools.registry import ToolRegistry

# Agent persona -> skill that supplies its system prompt.
AGENT_SKILL_MAP = {
    "maxilun-orchestrator": "maxilun",
    "maxilun-scout": "maxilun-knowledge-graph",
    "maxilun-architect": "maxilun-architect",
    "maxilun-maker": "maxilun-engineer",
    "maxilun-studio": "maxilun-craft",
    "maxilun-verifier": "maxilun-verify",
    "maxilun-coder-frontend": "maxilun-frontend",
    "maxilun-coder-backend": "maxilun-data",
    "maxilun-coder-mobile": "maxilun-mobile",
    "maxilun-coder-systems": "maxilun-desktop",
    "maxilun-ui-designer": "maxilun-craft",
    "maxilun-ui-motion": "maxilun-motion",
    "maxilun-ui-reviewer": "maxilun-verify",
    "maxilun-planner": "maxilun-scaffold",
    "maxilun-security-auditor": "maxilun-hunt",
    "maxilun-coder-ai": "maxilun-ai",
    "maxilun-data-engineer": "maxilun-data",
    "maxilun-devops": "maxilun-deploy",
    "maxilun-docsmith": "maxilun-docsmith",
}


def _normalize_agent(name: str) -> str:
    clean = name.strip().lstrip("@")
    try:
        from .aliases import get_alias_manager
        resolved = get_alias_manager().resolve_agent(clean)
        if resolved:
            return resolved
    except Exception:
        pass
    clean_lower = clean.lower()
    return clean_lower if clean_lower.startswith("maxilun") else f"maxilun-{clean_lower}"


def _last_reply(sub_ctx: SessionContext) -> str:
    for m in reversed(sub_ctx.messages):
        if m.role == "assistant" and m.content:
            return m.content
    return ""


class MaxilunAgentLoop:
    """The central agent runtime engine for the Maxilun ecosystem."""

    def __init__(
        self,
        repo_root: Optional[Path] = None,
        provider: Optional[UniversalProvider] = None,
        max_turns: int = 10,
        verbose: bool = True,
        is_subagent: bool = False,
        allowed_tools: Optional[Set[str]] = None,
        agent_name: Optional[str] = None,
        shared_bus: Optional[List[Dict[str, Any]]] = None,
    ):
        self.root = repo_root or Path.cwd()
        self.loader = SkillsLoader(self.root)
        self.registry = ToolRegistry(self.root)
        self.provider = provider or UniversalProvider()
        self.middleware = MiddlewarePipeline(self.root)
        self.max_turns = max_turns
        self.verbose = verbose
        self.is_subagent = is_subagent
        self.allowed_tools = allowed_tools
        self.agent_name = agent_name
        self.shared_bus = shared_bus

    def run_task(
        self,
        prompt: str,
        on_chunk: Optional[Callable[[str], None]] = None,
        forced_skill: Optional[str] = None,
        context: Optional[SessionContext] = None,
    ) -> SessionContext:
        """Executes a complete task end-to-end; pass `context` to continue an earlier conversation."""
        resumed = context is not None and bool(context.messages)
        context = context or SessionContext()
        if self.shared_bus is not None:
            context.agent_bus = self.shared_bus

        # Register inter-agent communication tools (available to all agents)
        sender_id = self.agent_name or ("maxilun-orchestrator" if not self.is_subagent else "subagent")

        def handle_send_handoff(to_agent: str, summary: str, artifacts: Optional[List[str]] = None,
                                reply_to: Optional[int] = None) -> Dict[str, Any]:
            entry = context.post_handoff(sender_id, to_agent, summary, artifacts, reply_to=reply_to)
            return {"status": "sent", "handoff": entry}

        def handle_read_handoffs(for_agent: Optional[str] = None) -> Dict[str, Any]:
            msgs = context.read_handoffs(for_agent or sender_id)
            return {"count": len(msgs), "messages": msgs}

        self.registry.register_tool(
            "send_handoff",
            handle_send_handoff,
            {
                "type": "function",
                "function": {
                    "name": "send_handoff",
                    "description": "Send a structured handoff packet (contracts, file:line citations, defects, or verification status) to another Maxilun agent or '*' broadcast. Set reply_to to answer a specific bus message.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "to_agent": {"type": "string", "description": "Target agent name (e.g. maxilun-coder-backend, maxilun-verifier, or '*')"},
                            "summary": {"type": "string", "description": "Compact handoff summary with file:line citations"},
                            "artifacts": {"type": "array", "items": {"type": "string"}, "description": "Modified or referenced file paths"},
                            "reply_to": {"type": "integer", "description": "Bus message id this message answers"}
                        },
                        "required": ["to_agent", "summary"]
                    }
                }
            }
        )
        self.registry.register_tool(
            "read_handoffs",
            handle_read_handoffs,
            {
                "type": "function",
                "function": {
                    "name": "read_handoffs",
                    "description": "Read upstream handoff packets addressed to this agent or broadcast on the shared agent bus.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "for_agent": {"type": "string", "description": "Optional agent filter (defaults to current agent)"}
                        }
                    }
                }
            }
        )

        # 1. Routing & Specialist Selection
        decision_type = self.middleware.check_reversibility(prompt)
        context.decision_type = decision_type

        if forced_skill:
            active_skill = self.loader.get_skill(forced_skill) or self.loader.match_skill(forced_skill)
        else:
            active_skill = self.loader.match_skill(prompt)

        context.active_skill = active_skill.name
        context.record_swarm_event(active_skill.name, "Routed task", prompt[:80])

        if not self.is_subagent:
            def handle_delegate(specialist: str, task: str) -> Dict[str, Any]:
                clean = _normalize_agent(specialist)
                # Unknown names would spawn with no tool limits, so they are refused outright.
                if not self.loader.get_agent(clean):
                    return {"status": "error", "error": f"Unknown agent: {clean}"}
                # Upstream handoffs and meeting outcomes; individual meeting turns stay in the thread.
                upstream = [m for m in context.read_handoffs(clean) if m.get("kind") != "meeting_turn"]
                enriched_task = task
                if upstream:
                    bus_lines = [f"- #{m['id']} [{m['from']} -> {m['to']}] {m['summary']}" for m in upstream[-5:]]
                    enriched_task = f"## Upstream Agent Handoffs\n" + "\n".join(bus_lines) + f"\n\n## Assigned Task\n{task}"

                if self.verbose:
                    print(f"\n🚀 [Delegation] Spawning subagent: {clean}...")
                    print(f"   Subtask: {task[:80]}...")

                target_skill, sub_ctx = self._spawn_agent(context, clean, enriched_task)
                handoff = _last_reply(sub_ctx) or "Subagent completed."
                failed = handoff.startswith("Execution Error")
                files_mod = sorted(sub_ctx.touched_files)
                context.post_handoff(clean, sender_id, handoff[:400], artifacts=files_mod)
                context.record_swarm_event(clean, "Subagent failed" if failed else "Subagent finished",
                                           f"{len(files_mod)} file(s) modified")
                return {
                    "status": "error" if failed else "success",
                    "agent": clean,
                    "specialist": target_skill,
                    "handoff_result": handoff,
                    "files_modified": files_mod,
                    "commands_executed": sub_ctx.commands_run,
                }

            def handle_meeting(agenda: str, participants: List[str], rounds: int = 2) -> Dict[str, Any]:
                return self.hold_meeting(context, agenda, participants, rounds)

            roster_list = "maxilun-scout, maxilun-planner, maxilun-architect, maxilun-ui-designer, maxilun-ui-motion, maxilun-studio, maxilun-coder-frontend, maxilun-coder-backend, maxilun-coder-mobile, maxilun-coder-systems, maxilun-maker, maxilun-verifier, maxilun-ui-reviewer, maxilun-security-auditor"
            schema = {
                "type": "function",
                "function": {
                    "name": "delegate_task",
                    "description": "Spawn a specialized subagent to execute a bounded subtask across Wave 1 (maxilun-scout, maxilun-planner, maxilun-architect), Wave 2 (maxilun-ui-designer, maxilun-ui-motion, maxilun-studio, maxilun-coder-frontend, maxilun-coder-backend, maxilun-coder-mobile, maxilun-coder-systems, maxilun-maker), or Wave 3 (maxilun-verifier, maxilun-ui-reviewer, maxilun-security-auditor).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "specialist": {
                                "type": "string",
                                "description": f"Target specialist agent or skill (e.g. {roster_list})"
                            },
                            "task": {
                                "type": "string",
                                "description": "Concrete instructions, upstream contracts/file:line, and expected deliverable for the subagent"
                            }
                        },
                        "required": ["specialist", "task"]
                    }
                }
            }
            self.registry.register_tool("delegate_task", handle_delegate, schema)
            self.registry.register_tool(
                "convene_meeting",
                handle_meeting,
                {
                    "type": "function",
                    "function": {
                        "name": "convene_meeting",
                        "description": (
                            "Hold a read-only roundtable before planning cross-domain or Type 1 work. Participants speak in turn, "
                            "each hearing the full minutes, answering questions addressed to them, and agreeing or objecting with evidence. "
                            "Ends early on a round with no objections. Returns minutes and open objections; no files are edited."
                        ),
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "agenda": {"type": "string", "description": "The decision to reach, with known constraints and file:line context"},
                                "participants": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": f"2-{MAX_PARTICIPANTS} agents whose domains the decision crosses, in speaking order ({roster_list})"
                                },
                                "rounds": {"type": "integer", "description": f"Maximum rounds, 1-{MAX_ROUNDS} (default 2)"}
                            },
                            "required": ["agenda", "participants"]
                        }
                    }
                }
            )
        if self.verbose:
            print(f"\n🌑 Maxilun Harness Engine: [Active Specialist: {active_skill.name}] (Type {decision_type})")
            print(f"   Contract: Owns {active_skill.contract.get('Owns', 'implementation')[:60]}...")
        # 2. Compile Active System Prompt
        if not resumed:
            context.add_system_message(self.loader.build_system_prompt(active_skill.name, agent_name=self.agent_name))
        context.add_user_message(prompt)

        # 3. Agent Execution Loop
        turn = 0
        while turn < self.max_turns:
            turn += 1
            if self.verbose:
                print(f"⚡ Turn {turn}/{self.max_turns}: Requesting completion from {self.provider.model}...")

            messages = context.to_provider_messages()
            tools = self.registry.get_tool_schemas(allowed_tools=self.allowed_tools)
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
                    args = None
                if not isinstance(args, dict):
                    context.add_tool_result(call_id, fn_name, json.dumps({"error": "Tool arguments must be a JSON object."}))
                    continue

                # Middleware: Pre-flight Knowledge Graph inspection & security guard
                pre_notice = self.middleware.before_tool_call(fn_name, args)
                if pre_notice:
                    if pre_notice.startswith("[BLOCKED]"):
                        if self.verbose:
                            print(f"   🚫 {pre_notice}")
                        context.add_tool_result(call_id, fn_name, json.dumps({"error": pre_notice}))
                        continue
                    elif self.verbose:
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
                result = self.registry.execute(fn_name, args, allowed_tools=self.allowed_tools)
                if fn_name == "execute_bash" and isinstance(result, dict):
                    for stream_key in ("stdout", "stderr", "output"):
                        if isinstance(result.get(stream_key), str):
                            result[stream_key] = OutputCompressor.compress_bash_output(result[stream_key])
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

        self.save_artifacts(context)
        return context

    def save_artifacts(self, context: SessionContext) -> Path:
        """Writes swarm events and the inter-agent bus to maxilun-out/ for the dashboard."""
        out_dir = self.root / "maxilun-out"
        try:
            out_dir.mkdir(exist_ok=True)
            (out_dir / "swarm_events.json").write_text(json.dumps(context.swarm_events, indent=2), encoding="utf-8")
            (out_dir / "agent_bus.json").write_text(json.dumps(context.agent_bus, indent=2), encoding="utf-8")
        except OSError:
            pass
        return out_dir / "agent_bus.json"

    def hold_meeting(self, context: SessionContext, agenda: str, participants: List[str], rounds: int = 2) -> Dict[str, Any]:
        """Runs a read-only roundtable; each turn is a real subagent on the shared bus."""
        def speak(agent: str, brief: str) -> str:
            _, sub_ctx = self._spawn_agent(context, agent, brief, meeting=True)
            return _last_reply(sub_ctx)

        roster = [_normalize_agent(p) for p in participants]
        unknown = [p for p in roster if not self.loader.get_agent(p)]
        if unknown:
            return {"status": "error", "error": f"Unknown agents: {', '.join(unknown)}"}
        if self.verbose:
            print(f"\n🗣️ [Meeting] {', '.join(roster)} on: {agenda[:80]}")
        chair = self.agent_name or "maxilun-orchestrator"
        return AgentMeeting(context, speak, chair=chair).convene(agenda, roster, rounds)

    def _spawn_agent(self, context: SessionContext, agent: str, task: str, meeting: bool = False):
        """Runs one specialist subagent on the shared bus; meeting turns are read-only and short."""
        agent_def = self.loader.get_agent(agent)
        target_skill = AGENT_SKILL_MAP.get(agent, agent)
        allowed = agent_def.allowed_harness_tools if agent_def else None
        if meeting:
            allowed = (allowed & MEETING_TOOLS) if allowed is not None else set(MEETING_TOOLS)
        subagent = MaxilunAgentLoop(
            repo_root=self.root,
            provider=self.provider,
            max_turns=min(self.max_turns, 3 if meeting else 6),
            verbose=self.verbose,
            is_subagent=True,
            allowed_tools=allowed,
            agent_name=agent if agent_def else None,
            shared_bus=context.agent_bus,
        )
        return target_skill, subagent.run_task(task, forced_skill=target_skill)
