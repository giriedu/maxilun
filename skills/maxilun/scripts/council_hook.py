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
    "references/agent-council.md. Pick the tier from the user's LATEST message only; never reopen "
    "an earlier agenda. CHAT (greeting/small talk, e.g. 'halo tim', 'test'): no agents, reply in "
    "one line and ask what to discuss. QUICK (a real question/advice): no KG scan, dispatch the "
    "2-3 agents who own the topic ALL AT ONCE in one message, one round, each answers in <=3 "
    "short lines, reply = **@agent**: ... per agent + one chair line, under 15 lines total, no "
    "minutes header or process notes. No ACC needed for a question. "
    "DEEP (only when the user asks to check/audit/review the app or code, find kekurangan/"
    "kelebihan, or approve a code change): chair runs kg_locate/kg_query itself, then all agents "
    "in parallel rounds (max 3) replying by @name, synthesis, ACC. Never dispatch agents one at a "
    "time. Do not create, edit, or delete files and do not run commands that change anything "
    "until the user replies ACC. If the user says \"stop council\", \"stop maxilun\", or \"normal mode\", run "
    "\"%s\" \"%s\" --off and answer normally." % (
        Path(sys.executable).as_posix(), Path(__file__).resolve().as_posix())
)
# Approval is the explicit token ACC (notes may follow) or a message that is nothing
# but an approval word. "lanjut diskusi" or "ok tapi ganti warna" is not approval.
ACC_TOKEN = re.compile(r"^\s*(acc|approved?)\b", re.I)
ACC_ONLY = re.compile(r"^\s*(setuju|gas(kan)?|lanjut(kan)?|eksekusi|ok(e|ay)?|go( ahead)?|yes|ya)"
                      r"(\s*(,|aja|saja|gas|lanjut(kan)?|eksekusi|sekarang))*\s*[.!]*\s*$", re.I)
NOT_ACC = re.compile(r"\b(tapi|but|revisi|ganti|ubah|jangan|diskusi|tunggu|nanti|wait|kecuali)\b", re.I)
STOP_PHRASE = re.compile(r"\b(stop\s+(?:council|maxilun)|normal\s+mode|matikan\s+council|keluar\s+council)\b", re.I)


def is_acc(text: str) -> bool:
    if not isinstance(text, str) or NOT_ACC.search(text):
        return False
    if re.match(r"^\s*(?:acc|approved?|ok(?:e|ay)?|yes|ya)\s*\?", text, re.I):
        return False
    return bool(ACC_TOKEN.match(text) or ACC_ONLY.match(text))


# Antigravity & cross-host tool names; anything that mutates or executes shell is gated.
WRITE_TOOL = re.compile(
    r"write|replace|edit|create|delete|remove|move|rename|patch|apply|code_action|generate_|"
    r"save_file|set_properties|update_|append_|batch|undo|redo|pointer|^key$|type_text",
    re.I,
)
_SHELL_TOOLS = {"run_command", "bash", "execute_bash", "shell", "run_terminal_cmd", "send_command_input", "runcommand"}
READ_TOOL = re.compile(r"^(?:mcp__maxilun-kg__)?(?:view|read|list|grep|find|search|codebase|get|kg_(?:locate|query|diff_impact))", re.I)
MCP_KG_READ_TOOLS = {"kg_locate", "kg_query", "kg_diff_impact"}
_PY_NAMES = {"python", "python3", "py"}
_GIT_READ_SUBS = {"status", "diff", "log", "show"}
_SIMPLE_READ_CMDS = {"ls", "dir", "cat", "type", "head", "tail", "rg", "grep", "findstr"}
_KG_READ_SUBS = {"locate", "query", "context"}
_BAD_FLAG_PREFIXES = ("--output", "--pre", "--exec", "--ext-diff")
_HARNESS_READ_SUBS = {"check", "skills", "doctor", "route", "verify-code"}
_CLI_READ_SUBS = {"lint", "verify", "context", "n8n-lint"}


def _strip_quotes(tok: str) -> str:
    if len(tok) >= 2 and tok[0] == tok[-1] and tok[0] in ("'", '"'):
        return tok[1:-1]
    return tok


def _tokenize_safe_cmd(cmd: str):
    """Rejects shell chaining, cmd/PS/POSIX quote-escape desyncs, and subexpressions."""
    if not isinstance(cmd, str) or not cmd.strip():
        return None
    # Reject newlines, subshells, PowerShell @(...), cmd/POSIX operators anywhere, and backslash-quote escapes.
    if any(seq in cmd for seq in ("\n", "\r", "`", "$(", "@(", "${", "<(", ">(", ";", "&", ">", "<", "^", '\\"', "\\'")):
        return None
    # Single quotes do not quote pipes in cmd.exe; only allow '|' inside balanced double quotes.
    in_dq = False
    for ch in cmd:
        if ch == '"':
            in_dq = not in_dq
        elif ch == "|" and not in_dq:
            return None
    if in_dq:
        return None
    import shlex
    try:
        tokens = [_strip_quotes(t) for t in shlex.split(cmd, posix=False)]
    except ValueError:
        return None
    return tokens or None


def _matches_abbrev(low_flag: str, target: str) -> bool:
    flag_name = low_flag.split("=", 1)[0]
    return flag_name == target or (flag_name.startswith("--") and len(flag_name) >= 3 and target.startswith(flag_name))


def _has_bad_flag(tokens: list, block_view: bool = False, block_fix: bool = False) -> bool:
    for tok in tokens:
        low = tok.lower()
        if low == "-o" or (low.startswith("-o") and len(low) > 2):
            return True
        if any(_matches_abbrev(low, p) for p in _BAD_FLAG_PREFIXES):
            return True
        if block_view and (low == "-v" or _matches_abbrev(low, "--view") or _matches_abbrev(low, "--snapshot")):
            return True
        if block_fix and _matches_abbrev(low, "--fix"):
            return True
    return False


def _is_py_script(tokens: list):
    exe = Path(tokens[0].replace("\\", "/")).name.lower()
    if exe.endswith(".exe"):
        exe = exe[:-4]
    if exe not in _PY_NAMES or len(tokens) < 2:
        return None
    idx = 2 if exe == "py" and tokens[1] == "-3" else 1
    if idx >= len(tokens):
        return None
    return tokens[idx].replace("\\", "/").lower(), tokens[idx + 1:]


def _is_stop_council_cmd(cmd: str, last_user_input: str = "") -> bool:
    if last_user_input and not STOP_PHRASE.search(last_user_input):
        return False
    tokens = _tokenize_safe_cmd(cmd)
    if not tokens:
        return False
    parsed = _is_py_script(tokens)
    if not parsed:
        return False
    script, rest = parsed
    return Path(script).name == "council_hook.py" and "--off" in rest and not _has_bad_flag(rest)


def _is_safe_read_cmd(cmd: str) -> bool:
    tokens = _tokenize_safe_cmd(cmd)
    if not tokens:
        return False
    exe = Path(tokens[0].replace("\\", "/")).name.lower()
    if exe.endswith(".exe"):
        exe = exe[:-4]
    if exe == "git":
        return len(tokens) >= 2 and tokens[1].lower() in _GIT_READ_SUBS and not _has_bad_flag(tokens[2:])
    if exe in _SIMPLE_READ_CMDS:
        return not _has_bad_flag(tokens[1:])
    parsed = _is_py_script(tokens)
    if not parsed:
        return False
    script, rest = parsed
    if script == "skills/maxilun-knowledge-graph/cli.py" or script.endswith("/maxilun-knowledge-graph/cli.py"):
        return bool(rest) and rest[0].lower() in _KG_READ_SUBS and not _has_bad_flag(rest[1:], block_view=True)
    if script == "skills/maxilun-craft/scripts/slopscan.py" or script.endswith("/maxilun-craft/scripts/slopscan.py"):
        return not _has_bad_flag(rest)
    if script == "scripts/test-suite.py" or script.endswith("/scripts/test-suite.py"):
        return not _has_bad_flag(rest, block_fix=True)
    if script == "scripts/ui-purity-linter.py" or script.endswith("/scripts/ui-purity-linter.py"):
        return not _has_bad_flag(rest, block_fix=True)
    if script == "skills/maxilun-verify/verify_engine.py" or script.endswith("/maxilun-verify/verify_engine.py"):
        return not _has_bad_flag(rest, block_fix=True)
    if script == "harness/cli.py" or script.endswith("/harness/cli.py"):
        return bool(rest) and rest[0].lower() in _HARNESS_READ_SUBS and not _has_bad_flag(rest[1:], block_view=True, block_fix=True)
    if script == "cli.py" or script.endswith("/maxilun/cli.py"):
        return bool(rest) and rest[0].lower() in _CLI_READ_SUBS and not _has_bad_flag(rest[1:], block_view=True, block_fix=True)
    return False


def _classify_mcp_call(args: dict) -> str:
    server = str(args.get("ServerName") or args.get("serverName") or args.get("server_name") or args.get("server") or "").strip().lower()
    tool = str(args.get("ToolName") or args.get("toolName") or args.get("tool_name") or args.get("tool") or "").strip()
    if tool and WRITE_TOOL.search(tool):
        return "deny"
    if server == "maxilun-kg" and tool.lower() in MCP_KG_READ_TOOLS:
        return "allow"
    return "ask"


def read_payload():
    try:
        data = json.load(sys.stdin)
        return data if isinstance(data, dict) else None
    except ValueError:
        return None


def _any_marker_on(roots: list) -> bool:
    for r in roots:
        if r and (Path(str(r)) / MARKER).is_file():
            return True
    return False


def hook() -> None:
    payload = read_payload()
    if payload is None:
        return
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or ".")
    if (root / MARKER).is_file():
        print(REMINDER)


def agy_hook() -> None:
    p = read_payload()
    fallback_roots = [os.environ.get("CLAUDE_PROJECT_DIR"), "."]
    if p is None:
        # Fail closed when hook payload is unreadable/malformed while council marker may be active.
        if _any_marker_on(fallback_roots):
            print(json.dumps({"decision": "deny", "reason": "Malformed hook payload while Maxilun council lock is active."}))
        else:
            print(json.dumps({"decision": "ask"}))
        return
    raw_ws = p.get("workspacePaths")
    ws_list = list(raw_ws) if isinstance(raw_ws, list) else []
    roots = [p.get("cwd")] + ws_list + fallback_roots
    on = _any_marker_on(roots)
    event = p.get("hookEventName")
    if event == "PreInvocation":
        print(json.dumps({"injectSteps": [{"systemMessage": {"systemMessage": REMINDER}}]} if on else {}))
        return
    # PreToolUse. "ask" leaves the user's own permission settings in charge.
    raw_call = p.get("toolCall")
    call = raw_call if isinstance(raw_call, dict) else {}
    name = str(call.get("name") or "")
    raw_args = call.get("args")
    if isinstance(raw_args, str):
        try:
            raw_args = json.loads(raw_args)
        except ValueError:
            raw_args = {}
    args = raw_args if isinstance(raw_args, dict) else {}
    raw_input = p.get("lastUserInput")
    user_text = raw_input if isinstance(raw_input, str) else ""
    approved = is_acc(user_text)
    if on and not approved and name.lower() in ("call_mcp_tool", "mcp_call"):
        print(json.dumps({"decision": _classify_mcp_call(args)}))
        return
    cmd = str(args.get("CommandLine") or args.get("command") or args.get("cmd") or "")
    stopping = bool(user_text and STOP_PHRASE.search(user_text)) and _is_stop_council_cmd(cmd, user_text)
    lname = name.lower()
    held = bool(WRITE_TOOL.search(name)) or (
        lname in _SHELL_TOOLS and (lname == "send_command_input" or not (_is_safe_read_cmd(cmd) or stopping))
    )
    if on and held and not approved:
        print(json.dumps({"decision": "deny", "reason": (
            "Maxilun council is on: no edits or state-changing commands before the user replies ACC. "
            "Finish the meeting minutes and synthesis, then end the turn.")}))
    elif on and READ_TOOL.match(name) and not held:
        print(json.dumps({"decision": "allow"}))
    else:
        print(json.dumps({"decision": "ask"}))


def _load_json_dict(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError) as exc:
        print(f"Warning: could not parse {path}: {exc}", file=sys.stderr)
        return {}


def toggle(on: bool, root: Path) -> None:
    marker, hooks_file = root / MARKER, root / AGY_HOOKS
    existed = hooks_file.is_file()
    data = _load_json_dict(hooks_file) if existed else {}
    if on:
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.touch()
        if not existed:
            # The hook holds this machine's paths; keep it out of the repo.
            ignore(root, ["/.maxilun/", "/.agents/hooks.json"])
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
    if not on and hooks_file.parent.is_dir() and not any(hooks_file.parent.iterdir()):
        hooks_file.parent.rmdir()
    print("council %s in %s" % ("on" if on else "off", root))


def ignore(root: Path, lines: list) -> None:
    if not (root / ".git").exists():
        return
    gi = root / ".gitignore"
    text = gi.read_text(encoding="utf-8") if gi.is_file() else ""
    missing = [ln for ln in lines if ln not in text.splitlines()]
    if missing:
        sep = "" if not text or text.endswith("\n") else "\n"
        gi.write_text(text + sep + "\n".join(missing) + "\n", encoding="utf-8")


def install() -> None:
    settings = Path.home() / ".claude" / "settings.json"
    data = _load_json_dict(settings)
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
