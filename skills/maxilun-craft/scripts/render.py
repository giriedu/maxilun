#!/usr/bin/env python3
"""Render a page to PNG screenshots so the designer can look at what it built.

Code misreports what people see. Run this, then open every PNG it prints (the Read
tool shows images) and critique the pixels, not the markup.

    python render.py <file-or-url> [--out DIR] [--widths 320,768,1440] [--height 900]

Backends, best first:
  1. Playwright (if importable): full-page shots plus a horizontal-overflow probe.
  2. Headless Chrome / Edge / Chromium CLI: first-viewport shots only, no overflow probe.
Override the browser binary with MAXILUN_BROWSER. Exit 2 when nothing can render.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FOLD_HEIGHT = {320: 720, 360: 760, 390: 844, 768: 1024}
MIN_WINDOW = 600


def to_url(target: str) -> str:
    if "://" in target:
        return target
    return Path(target).resolve().as_uri()


def find_browser() -> str | None:
    env = os.environ.get("MAXILUN_BROWSER")
    if env and Path(env).exists():
        return env
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome", "msedge", "microsoft-edge"):
        hit = shutil.which(name)
        if hit:
            return hit
    pf = [os.environ.get(k, "") for k in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA")]
    candidates = [Path(p) / rel for p in pf if p for rel in (
        "Google/Chrome/Application/chrome.exe", "Microsoft/Edge/Application/msedge.exe", "Chromium/Application/chrome.exe")]
    candidates += [Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
                   Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
                   Path("/Applications/Chromium.app/Contents/MacOS/Chromium")]
    return next((str(c) for c in candidates if c.exists()), None)


def with_playwright(url: str, widths, height: int, out: Path) -> bool:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for w in widths:
            page = browser.new_page(viewport={"width": w, "height": FOLD_HEIGHT.get(w, height)})
            page.goto(url, wait_until="networkidle")
            png = out / f"render-{w}.png"
            page.screenshot(path=str(png), full_page=True)
            overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            note = f"  HORIZONTAL OVERFLOW {overflow}px" if overflow > 0 else "  no horizontal overflow"
            print(f"{png}  ({w}px, full page){note}")
            page.close()
        browser.close()
    return True


def with_cli(url: str, widths, height: int, out: Path) -> bool:
    exe = find_browser()
    if not exe:
        return False
    profile = tempfile.mkdtemp(prefix="maxilun-render-")
    try:
        for w in widths:
            h = FOLD_HEIGHT.get(w, height)
            png = out / f"render-{w}.png"
            shot_url, win_w, note = url, w, ""
            if w < MIN_WINDOW:
                # Headless windows cannot be narrower than ~500px, so a real w-px viewport is an iframe.
                frame = Path(profile) / f"frame-{w}.html"
                frame.write_text(f'<!doctype html><body style="margin:0;background:#6b6b6b">'
                                 f'<iframe src="{url}" style="display:block;width:{w}px;height:{h}px;border:0;background:#fff">'
                                 f'</iframe></body>', encoding="utf-8")
                shot_url, win_w, note = frame.as_uri(), MIN_WINDOW, f"; page is the left {w}px, grey is outside it"
            subprocess.run([exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                            "--allow-file-access-from-files", f"--user-data-dir={profile}", "--virtual-time-budget=4000",
                            f"--window-size={win_w},{h}", f"--screenshot={png}", shot_url],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90, check=False)
            if not png.exists():
                print(f"could not render {w}px with {exe}", file=sys.stderr)
                return False
            print(f"{png}  ({w}x{h}, first viewport only; overflow not probed{note})")
    finally:
        shutil.rmtree(profile, ignore_errors=True)
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", help="HTML file path or http(s) URL (serve SPAs and dev builds over HTTP)")
    ap.add_argument("--out", default=None, help="output folder (default: a temp folder)")
    ap.add_argument("--widths", default="320,768,1440")
    ap.add_argument("--height", type=int, default=900, help="viewport height for widths without a preset")
    a = ap.parse_args()
    widths = [int(w) for w in a.widths.split(",") if w.strip()]
    out = Path(a.out or tempfile.mkdtemp(prefix="maxilun-shots-"))
    out.mkdir(parents=True, exist_ok=True)
    url = to_url(a.target)
    if with_playwright(url, widths, a.height, out) or with_cli(url, widths, a.height, out):
        print("Now open every PNG above and critique what you see (see maxilun-craft SKILL.md §7).")
        return 0
    print("[UNVERIFIED] no renderer: install Playwright (pip install playwright && playwright install chromium) "
          "or Chrome/Edge, or set MAXILUN_BROWSER.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
