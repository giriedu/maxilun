"""Zero-dependency Iconify SVG Search & Fetch CLI for Maxilun Craft.

Searches 200+ open-source icon sets (Lucide, Tabler, Heroicons, Phosphor, etc.)
and retrieves clean monochrome SVG markup so agents never invent broken paths
or inject Unicode emojis (CMP-003).
"""

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path


API_BASE = "https://api.iconify.design"


def search_icons(query: str, prefix: str = "", limit: int = 10) -> dict:
    params = {"query": query, "limit": str(limit)}
    if prefix:
        params["prefix"] = prefix
    url = f"{API_BASE}/search?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "maxilun-craft-icon-lookup/1.3.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_icon_svg(icon_id: str, size: int = 24) -> str:
    if ":" not in icon_id:
        raise ValueError("icon_id must use 'prefix:name' format (e.g. 'lucide:arrow-right')")
    prefix, name = icon_id.split(":", 1)
    safe_prefix = urllib.parse.quote(prefix.strip(), safe="")
    safe_name = urllib.parse.quote(name.strip(), safe="")
    url = f"{API_BASE}/{safe_prefix}/{safe_name}.svg?width={int(size)}&height={int(size)}"
    req = urllib.request.Request(url, headers={"User-Agent": "maxilun-craft-icon-lookup/1.3.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        svg = resp.read().decode("utf-8")
    # Ensure monochrome currentColor hygiene when not already set
    if 'stroke="currentColor"' not in svg and 'fill="currentColor"' not in svg:
        svg = re.sub(r"<svg\b", '<svg fill="currentColor"', svg, count=1)
    return svg


def main() -> int:
    parser = argparse.ArgumentParser(description="Maxilun Craft SVG Icon Lookup (Iconify API)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_search = sub.add_parser("search", help="Search icons by keyword")
    p_search.add_argument("query", help="Search keyword (e.g. 'arrow', 'dashboard')")
    p_search.add_argument("--prefix", default="", help="Optional collection prefix (e.g. 'lucide', 'tabler')")
    p_search.add_argument("--limit", type=int, default=10, help="Max results (default: 10)")

    p_get = sub.add_parser("get", help="Fetch clean SVG markup for an icon id")
    p_get.add_argument("icon_id", help="Icon ID in 'prefix:name' format (e.g. 'lucide:check')")
    p_get.add_argument("--size", type=int, default=24, help="Width/height in px (default: 24)")
    p_get.add_argument("--out", default="", help="Optional output .svg file path")

    args = parser.parse_args()
    try:
        if args.cmd == "search":
            data = search_icons(args.query, prefix=args.prefix, limit=args.limit)
            icons = data.get("icons", [])
            print(json.dumps({"query": args.query, "count": len(icons), "icons": icons}, indent=2))
        elif args.cmd == "get":
            svg = get_icon_svg(args.icon_id, size=args.size)
            if args.out:
                out_path = Path(args.out)
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(svg, encoding="utf-8")
                print(f"Saved {args.icon_id} -> {out_path}")
            else:
                print(svg)
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

