#!/usr/bin/env python3
"""lessons.py - Deterministic memory & repository lessons manager for Maxilun.

Manages persistent lessons in .maxilun/lessons.jsonl to maintain continuous learning
and prevent repeated errors across agent turns.

Usage:
  python scripts/lessons.py list                    List all confirmed lessons
  python scripts/lessons.py search <query>          Search lessons by keyword
  python scripts/lessons.py add --trigger <kw> --action <policy> --evidence <reason>
  python scripts/lessons.py validate               Validate schema integrity of .maxilun/lessons.jsonl
"""
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LESSONS_FILE = REPO_ROOT / ".maxilun" / "lessons.jsonl"


def load_lessons():
    if not LESSONS_FILE.exists():
        return []
    lessons = []
    with open(LESSONS_FILE, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                lessons.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"Warning: Line {i} is invalid JSON: {e}", file=sys.stderr)
    return lessons


def save_lessons(lessons):
    LESSONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LESSONS_FILE, "w", encoding="utf-8") as f:
        for item in lessons:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def cmd_list(args):
    lessons = load_lessons()
    if not lessons:
        print("No lessons recorded in .maxilun/lessons.jsonl.")
        return
    print(f"\nPersistent Repository Lessons ({len(lessons)} total):\n" + "=" * 70)
    for l in lessons:
        lid = l.get("id", "L-???")
        trigger = l.get("trigger", "")
        action = l.get("action", "")
        conf = l.get("confidence", 0.9)
        date = l.get("last_confirmed", "")
        print(f"- [{lid}] ({conf:.2f}) Trigger: {trigger}")
        print(f"    Action: {action}")
        print(f"    Date: {date}\n")


def cmd_search(args):
    query = args.query.lower()
    lessons = load_lessons()
    matched = [
        l for l in lessons
        if query in l.get("trigger", "").lower()
        or query in l.get("action", "").lower()
        or any(query in ev.lower() for ev in l.get("evidence", []))
    ]
    if not matched:
        print(f"No lessons matching '{args.query}'.")
        return
    print(f"\nFound {len(matched)} matching lesson(s) for '{args.query}':\n" + "=" * 70)
    for l in matched:
        print(f"- [{l.get('id')}] Trigger: {l.get('trigger')}")
        print(f"    Action: {l.get('action')}")
        print(f"    Evidence: {', '.join(l.get('evidence', []))}\n")


def cmd_add(args):
    lessons = load_lessons()
    max_num = max(
        (int(l["id"].split("-")[1]) for l in lessons if str(l.get("id", "")).startswith("L-") and l["id"].split("-")[1].isdigit()),
        default=0,
    )
    lid = f"L-{max_num + 1:03d}"
    today = datetime.now().strftime("%Y-%m-%d")

    evidence = [args.evidence] if isinstance(args.evidence, str) else args.evidence

    new_lesson = {
        "id": lid,
        "trigger": args.trigger,
        "action": args.action,
        "evidence": evidence,
        "confidence": float(args.confidence),
        "scope": args.scope,
        "last_confirmed": today
    }

    lessons.append(new_lesson)
    save_lessons(lessons)
    print(f"[OK] Added lesson [{lid}] to .maxilun/lessons.jsonl:")
    print(f"   Trigger : {args.trigger}")
    print(f"   Action  : {args.action}")


def cmd_validate(args):
    if not LESSONS_FILE.exists():
        print("[OK] .maxilun/lessons.jsonl does not exist yet (clean).")
        return
    lessons = load_lessons()
    required = ["id", "trigger", "action", "evidence", "confidence", "scope", "last_confirmed"]
    errors = []
    for idx, l in enumerate(lessons, 1):
        for field in required:
            if field not in l:
                errors.append(f"Lesson {idx} ([{l.get('id', 'unknown')}]) missing required field '{field}'")
    if errors:
        print(f"[FAIL] Validation failed with {len(errors)} error(s):")
        for err in errors:
            print(f"   - {err}")
        sys.exit(1)
    else:
        print(f"[OK] Validated {len(lessons)} lessons in .maxilun/lessons.jsonl: 100% compliant.")


def main():
    parser = argparse.ArgumentParser(description="Maxilun Persistent Lessons Manager")
    subparsers = parser.add_subparsers(dest="command")

    # list
    subparsers.add_parser("list", help="List all confirmed lessons")

    # search
    search_p = subparsers.add_parser("search", help="Search lessons by keyword")
    search_p.add_argument("query", help="Keyword to search in triggers or actions")

    # add
    add_p = subparsers.add_parser("add", help="Add a new repository lesson")
    add_p.add_argument("--trigger", required=True, help="Trigger keyword or file pattern")
    add_p.add_argument("--action", required=True, help="Mandatory action or policy to take")
    add_p.add_argument("--evidence", required=True, help="Reason or user correction evidence")
    add_p.add_argument("--confidence", default=0.9, type=float, help="Confidence score (0.0 to 1.0)")
    add_p.add_argument("--scope", default="repo", help="Scope of lesson (repo or global)")

    # validate
    subparsers.add_parser("validate", help="Validate schema of .maxilun/lessons.jsonl")

    args = parser.parse_args()
    if args.command == "list":
        cmd_list(args)
    elif args.command == "search":
        cmd_search(args)
    elif args.command == "add":
        cmd_add(args)
    elif args.command == "validate":
        cmd_validate(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

