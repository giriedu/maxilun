#!/usr/bin/env python3
"""component_lookup.py - CLI tool to search the 220+ component & 84 registry ecosystem.

Part of maxilun-craft. Indexes and searches skills/maxilun-craft/references/component-ecosystem.md.

Usage:
  python component_lookup.py search <query>     Search components by keyword
  python component_lookup.py get <name>         Get details for a component
  python component_lookup.py registries         List all 84 community registries
  python component_lookup.py categories         List all 16 component categories
"""
import argparse
import os
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
REFERENCE_FILE = REPO_ROOT / "skills" / "maxilun-craft" / "references" / "component-ecosystem.md"

if not REFERENCE_FILE.exists():
    REFERENCE_FILE = Path(__file__).resolve().parent.parent / "references" / "component-ecosystem.md"


def load_ecosystem() -> str:
    if not REFERENCE_FILE.exists():
        print(f"Error: {REFERENCE_FILE} not found.", file=sys.stderr)
        sys.exit(1)
    with open(REFERENCE_FILE, encoding="utf-8", errors="ignore") as f:
        return f.read()


def cmd_search(query: str):
    text = load_ecosystem()
    lines = text.split("\n")
    results = []
    current_category = "General"

    for line in lines:
        if line.startswith("### "):
            current_category = line.replace("###", "").strip()
        elif line.startswith("| **`") and query.lower() in line.lower():
            # Parse table row: | **`name`** | Purpose | Capabilities |
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) >= 2:
                name = parts[0].replace("**`", "").replace("`**", "").replace("**", "")
                purpose = parts[1]
                details = parts[2] if len(parts) > 2 else ""
                results.append((current_category, name, purpose, details))
        elif line.strip().startswith("- **") and query.lower() in line.lower():
            results.append((current_category, line.strip(), "", ""))

    if not results:
        print(f"No components found matching '{query}'.")
        return

    print(f"\n🔍 Found {len(results)} component(s) matching '{query}':\n" + "=" * 65)
    for cat, name, purpose, details in results:
        print(f"[{cat}]")
        print(f"  • {name} — {purpose}")
        if details:
            print(f"    {details}")
        print()


def cmd_get(name: str):
    text = load_ecosystem()
    lines = text.split("\n")
    found = False

    for line in lines:
        if (line.startswith("| **`") or line.strip().startswith("- **")) and name.lower() in line.lower():
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) >= 2:
                comp_name = parts[0].replace("**`", "").replace("`**", "").replace("**", "")
                purpose = parts[1]
                details = parts[2] if len(parts) > 2 else ""
                print(f"\nComponent: {comp_name}")
                print(f"Purpose:   {purpose}")
                if details:
                    print(f"Details:   {details}")
                print(f"Source:    skills/maxilun-craft/references/component-ecosystem.md\n")
                found = True
            else:
                print(f"\n{line.strip()}\n")
                found = True

    if not found:
        print(f"Component '{name}' not found.")


def cmd_registries():
    text = load_ecosystem()
    match = re.search(r"## 2\. The 84 Curated Community Registries.*?(?=##|\Z)", text, re.DOTALL)
    if not match:
        print("Registries section not found.")
        return

    regs = re.findall(r"-\s*\[([^\]]+)\]\(([^)]+)\)\s*[-—:]\s*([^\n]+)", match.group(0))
    print(f"\n📦 Curated Community Registries ({len(regs)} total):\n" + "=" * 65)
    for name, url, desc in regs:
        print(f"• {name.ljust(24)} : {desc.strip()} ({url})")
    print()


def cmd_categories():
    text = load_ecosystem()
    cats = re.findall(r"### ([A-P]\.\s*[^\n]+)", text)
    print(f"\n📂 Specialized Component Categories ({len(cats)} total):\n" + "=" * 65)
    for c in cats:
        print(f"  {c}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Maxilun Component Ecosystem Lookup CLI")
    subparsers = parser.add_subparsers(dest="command")

    search_p = subparsers.add_parser("search", help="Search components by keyword")
    search_p.add_argument("query", help="Keyword (e.g. table, modal, calendar, credenza)")

    get_p = subparsers.add_parser("get", help="Get component details")
    get_p.add_argument("name", help="Component name (e.g. credenza, adapttable)")

    subparsers.add_parser("registries", help="List all 84 community registries")
    subparsers.add_parser("categories", help="List all 16 component categories")

    args = parser.parse_args()
    if args.command == "search":
        cmd_search(args.query)
    elif args.command == "get":
        cmd_get(args.name)
    elif args.command == "registries":
        cmd_registries()
    elif args.command == "categories":
        cmd_categories()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
