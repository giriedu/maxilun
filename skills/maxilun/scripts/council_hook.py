#!/usr/bin/env python3
"""Keep Maxilun council mode alive and stop it from editing before ACC.

Council mode lives in the conversation, so a summarised or fresh session forgets it.
The marker file `.maxilun/council` in the project root is the durable switch.

    python council_hook.py --on [root]   start council: marker + Antigravity edit lock
    python council_hook.py --off [root]  stop council: remove both
    python council_hook.py --install     register (or repair) the Claude Code hook in ~/.claude/settings.json
    python council_hook.py               Claude Code UserPromptSubmit hook (re-injects the mode)
    python council_hook.py --agy         Antigravity hook (PreInvocation reminder, PreToolUse edit lock)
"""

import json
import os
import re
import sys
from pathlib import Path

MARKER = Path(".maxilun") / "council"
AGY_HOOKS = Path(".agents") / "hooks.json"
AGY_NAME = "maxilun-council"
REMINDER = (
    "[maxilun] Council mode is ON for this project (marker: .maxilun/council). "
    "Run this message as a council meeting per the maxilun skill §5.1 and "
    "references/agent-council.md: 2-5 relevant agents speak in turn, each answering the "
    "previous speakers by @name, then the chair's synthesis. Do not create, edit, or delete "
    "files and do not run commands that change anything until the user replies ACC; end the "
    "turn after the synthesis. If the user says \"stop council\", \"stop maxilun\", or "
    "\"normal mode\", run \"%s\" \"%s\" --off and answer normally." % (
        Path(sys.executable).as_posix(), Path(__file__).resolve().as_posix())
)
# A turn whose user message starts with one of these is the approval to implement.
ACC = re.compile(r"^\s*(acc|approve[d]?|lanjut|gas|setuju|ok(e|ay)?|go|eksekusi)\b", re.I)
# Antigravity tool names are lowercased step types; anything that writes is held.
WRITE_TOOL = re.compile(r"write|replace|edit|create|delete|remove|move|rename|patch|apply|code_action", re.I)
READ_TOOL = re.compile(r"(view|read|list|grep|find|search|codebase|get|kg_)", re.I)
READ_CMD = re.compile(
    r"^\s*(git\s+(status|diff|log|show)|ls|dir|cat|type|head|tail|rg|grep|findstr|"
    r"(python3?|py(\s+-3)?)\s+\S*(maxilun-knowledge-graph\S*cli\.py\s+(locate|query|context|scan)|slopscan\.py))\b",
    re.I)


def read_payload() -> dict:
    try:
        return json.load(sys.stdin)
    except ValueError:
        return {}


def hook() -> None:
    payload = read_payload()
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or ".")
    if (root / MARKER).is_file():
        print(REMINDER)


def agy_hook() -> None:
    p = read_payload()
    roots = [p.get("cwd")] + list(p.get("workspacePaths") or [])
    on = any(r and (Path(r) / MARKER).is_file() for r in roots)
    event = p.get("hookEventName")
    if event == "PreInvocation":
        print(json.dumps({"injectSteps": [{"systemMessage": {"systemMessage": REMINDER}}]} if on else {}))
        return
    # PreToolUse. "ask" leaves the user's own permission settings in charge.
    call = p.get("toolCall") or {}
    name, args = call.get("name", ""), call.get("args") or {}
    approved = bool(ACC.match(p.get("lastUserInput") or ""))
    cmd = str(args.get("CommandLine", ""))
    stopping = "council_hook.py" in cmd and "--off" in cmd
    held = WRITE_TOOL.search(name) or (name == "run_command" and not (READ_CMD.match(cmd) or stopping))
    if on and held and not approved:
        print(json.dumps({"decision": "deny", "reason": (
            "Maxilun council is on: no edits or state-changing commands before the user replies ACC. "
            "Finish the meeting minutes and synthesis, then end the turn.")}))
    elif on and READ_TOOL.match(name) and not held:
        print(json.dumps({"decision": "allow"}))
    else:
        print(json.dumps({"decision": "ask"}))


def toggle(on: bool, root: Path) -> None:
    marker, hooks_file = root / MARKER, root / AGY_HOOKS
    data = json.loads(hooks_file.read_text(encoding="utf-8")) if hooks_file.is_file() else {}
    if on:
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.touch()
        # Absolute paths: Antigravity runs hooks from .agents/, not the skill folder.
        cmd = f'"{Path(sys.executable).as_posix()}" "{Path(__file__).resolve().as_posix()}" --agy'
        data[AGY_NAME] = {
            "PreInvocation": [{"type": "command", "command": cmd, "timeout": 10}],
            "PreToolUse": [{"matcher": "*",
                            "hooks": [{"type": "command", "command": cmd, "timeout": 10}]}],
        }
    else:
        marker.unlink(missing_ok=True)
        data.pop(AGY_NAME, None)
    if data:
        hooks_file.parent.mkdir(parents=True, exist_ok=True)
        hooks_file.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    elif hooks_file.is_file():
        hooks_file.unlink()
    print("council %s in %s" % ("on" if on else "off", root))


def install() -> None:
    settings = Path.home() / ".claude" / "settings.json"
    data = json.loads(settings.read_text(encoding="utf-8")) if settings.is_file() else {}
    # Current interpreter + this file: no bare `python` (absent on macOS/Linux) and no
    # path copied from another machine's settings.
    command = f'"{Path(sys.executable).as_posix()}" "{Path(__file__).resolve().as_posix()}"'
    entries = data.setdefault("hooks", {}).setdefault("UserPromptSubmit", [])
    old = [h for e in entries for h in e.get("hooks", []) if "council_hook.py" in h.get("command", "")]
    if old and old[0]["command"] == command:
        print("council hook already registered")
        return
    if old:
        old[0]["command"] = command
    else:
        entries.append({"hooks": [{"type": "command", "command": command}]})
    settings.parent.mkdir(parents=True, exist_ok=True)
    settings.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"council hook registered in {settings}")


if __name__ == "__main__":
    args = sys.argv[1:]
    rest = [a for a in args if not a.startswith("--")]
    if "--on" in args or "--off" in args:
        toggle("--on" in args, Path(rest[0] if rest else ".").resolve())
    elif "--install" in args:
        install()
    elif "--agy" in args:
        agy_hook()
    else:
        hook()
