#!/usr/bin/env python3
"""Keep Maxilun council mode alive across compaction and new sessions.

Council mode lives in the conversation, so a summarised or fresh session forgets it.
The marker file `.maxilun/council` in the project root is the durable switch: the
skill creates it on `/maxilun council` and deletes it on `stop council`.

    python council_hook.py            UserPromptSubmit hook: re-injects the mode while the marker exists
    python council_hook.py --install  registers the hook in ~/.claude/settings.json (idempotent)
"""

import json
import os
import sys
from pathlib import Path

MARKER = Path(".maxilun") / "council"
REMINDER = (
    "[maxilun] Council mode is ON for this project (marker: .maxilun/council). "
    "Run this message as a real council meeting per the maxilun skill §5.1 and "
    "references/agent-council.md: dispatch 2-5 relevant agents one at a time, show minutes "
    "and synthesis, and wait for user ACC before any coding. If the user says "
    "\"stop council\", \"stop maxilun\", or \"normal mode\", delete .maxilun/council and answer normally."
)


def hook() -> None:
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        payload = {}
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or ".")
    if (root / MARKER).is_file():
        print(REMINDER)


def install() -> None:
    settings = Path.home() / ".claude" / "settings.json"
    data = json.loads(settings.read_text(encoding="utf-8")) if settings.is_file() else {}
    command = f'python "{Path(__file__).resolve().as_posix()}"'
    entries = data.setdefault("hooks", {}).setdefault("UserPromptSubmit", [])
    if any("council_hook.py" in h.get("command", "") for e in entries for h in e.get("hooks", [])):
        print("council hook already registered")
        return
    entries.append({"hooks": [{"type": "command", "command": command}]})
    settings.parent.mkdir(parents=True, exist_ok=True)
    settings.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"council hook registered in {settings}")


if __name__ == "__main__":
    install() if "--install" in sys.argv else hook()
