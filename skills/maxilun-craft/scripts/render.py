#!/usr/bin/env python3
"""Render a page to PNG screenshots so the designer can look at what it built.

Code misreports what people see. Run this, then open every PNG it prints (the Read
tool shows images) and critique the pixels, not the markup.

    python render.py <file-or-url> [--out DIR] [--widths 320,768,1440] [--height 900]
    python render.py <banner.svg> --preset banner [--out DIR]

Backends, best first:
  1. Playwright (if importable): full-page shots plus a horizontal-overflow probe.
  2. Headless Chrome / Edge / Chromium CLI: first-viewport shots only, no overflow probe.
Override the browser binary with MAXILUN_BROWSER. Exit 2 when nothing can render.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse

FOLD_HEIGHT = {320: 720, 360: 760, 390: 844, 768: 1024}
BANNER_PRESETS = {
    "og": (1200, 630),
    "github": (1280, 640),
    "banner": (1280, 420),
    "linkedin": (1584, 396),
    "x": (1500, 500),
    "square": (1080, 1080),
}
MIN_WINDOW = 600


def to_url(target: str) -> str:
    if "://" in target:
        return target
    return Path(target).resolve().as_uri()


def _svg_dimensions(svg_path: Path):
    text = svg_path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(
        r'viewBox\s*=\s*["\']\s*[-.\d]+[\s,]+[-.\d]+[\s,]+(\d+(?:\.\d+)?)[\s,]+(\d+(?:\.\d+)?)\s*["\']',
        text,
    )
    if m:
        return int(round(float(m.group(1)))), int(round(float(m.group(2))))
    mw = re.search(r'<svg[^>]*\bwidth\s*=\s*["\']\s*(\d+(?:\.\d+)?)(?:px)?\s*["\']', text, re.I)
    mh = re.search(r'<svg[^>]*\bheight\s*=\s*["\']\s*(\d+(?:\.\d+)?)(?:px)?\s*["\']', text, re.I)
    if mw and mh:
        return int(round(float(mw.group(1)))), int(round(float(mh.group(1))))
    return 1280, 420


def _wrap_svg(svg_path: Path, width: int, height: int, workdir: Path) -> str:
    svg_text = svg_path.read_text(encoding="utf-8", errors="replace")
    wrapper = workdir / f"svg-wrap-{width}x{height}.html"
    wrapper.write_text(
        f'<!doctype html><html><head><meta charset="utf-8">'
        f'<style>html,body{{margin:0;padding:0;width:{width}px;height:{height}px;background:transparent}}'
        f'svg{{display:block;width:100%;height:100%}}</style></head><body>{svg_text}</body></html>',
        encoding="utf-8",
    )
    return wrapper.as_uri()


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


def _viewport_height(width: int, height: int | None, is_svg: bool, is_preset: bool) -> int:
    if is_svg or is_preset:
        return height or 420
    if height is not None:
        return height
    return FOLD_HEIGHT.get(width, 900)


def with_playwright(url: str, widths, height: int | None, out: Path, is_svg: bool = False, is_preset: bool = False) -> bool:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for w in widths:
            h = _viewport_height(w, height, is_svg, is_preset)
            page = browser.new_page(viewport={"width": w, "height": h})
            page.goto(url, wait_until="networkidle")
            png = out.resolve() / f"render-{w}.png"
            page.screenshot(path=str(png), full_page=not (is_svg or is_preset))
            overflow = page.evaluate("""() => {
                const ph = document.documentElement.style.overflowX;
                const pb = document.body ? document.body.style.overflowX : '';
                document.documentElement.style.setProperty('overflow-x', 'visible', 'important');
                if (document.body) document.body.style.setProperty('overflow-x', 'visible', 'important');
                const diff = document.documentElement.scrollWidth - document.documentElement.clientWidth;
                document.documentElement.style.overflowX = ph;
                if (document.body) document.body.style.overflowX = pb;
                return diff;
            }""")
            note = f"  HORIZONTAL OVERFLOW {overflow}px" if overflow > 0 else "  no horizontal overflow"
            if is_svg:
                svg_metrics = page.evaluate("""() => {
                    const svg = document.querySelector('svg');
                    const sr = svg ? svg.getBoundingClientRect() : {left: 0, top: 0, right: window.innerWidth, bottom: window.innerHeight};
                    const boxes = [...document.querySelectorAll('svg text')].map(el => ({
                        t: (el.textContent || '').trim().slice(0, 24), r: el.getBoundingClientRect()
                    })).filter(b => b.t && b.r.width > 0 && b.r.height > 0);
                    const hit = (a, b) => a.left < b.right && b.left < a.right && a.top < b.bottom && b.top < a.bottom;
                    const clashes = [];
                    const clipped = [];
                    for (let i = 0; i < boxes.length; i++) {
                        const r = boxes[i].r;
                        if (r.left < sr.left - 1 || r.right > sr.right + 1 || r.top < sr.top - 1 || r.bottom > sr.bottom + 1)
                            clipped.push(boxes[i].t);
                        for (let j = i + 1; j < boxes.length; j++)
                            if (hit(r, boxes[j].r)) clashes.push([boxes[i].t, boxes[j].t]);
                    }
                    return {clashes: clashes.length, clipped: clipped.length};
                }""")
                note += f"  svg_text_clashes={svg_metrics['clashes']} svg_text_clipped={svg_metrics['clipped']}"
            print(f"{png}  ({w}x{h}){note}")
            page.close()
        browser.close()
    return True


def with_cli(url: str, widths, height: int | None, out: Path, is_svg: bool = False, is_preset: bool = False) -> bool:
    exe = find_browser()
    if not exe:
        return False
    profile = tempfile.mkdtemp(prefix="maxilun-render-")
    try:
        for w in widths:
            h = _viewport_height(w, height, is_svg, is_preset)
            png = out.resolve() / f"render-{w}.png"
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
    ap.add_argument("target", help="HTML/SVG file path or http(s) URL (serve SPAs and dev builds over HTTP)")
    ap.add_argument("--out", default=None, help="output folder (default: a temp folder)")
    ap.add_argument("--widths", default="320,768,1440")
    ap.add_argument("--height", type=int, default=None, help="explicit viewport height (overrides per-width fold heights)")
    ap.add_argument("--preset", choices=sorted(BANNER_PRESETS), default=None,
                    help="fixed banner/OG canvas size (og=1200x630, github=1280x640, banner=1280x420, linkedin=1584x396, x=1500x500, square=1080x1080)")
    a = ap.parse_args()
    out = Path(a.out or tempfile.mkdtemp(prefix="maxilun-shots-")).resolve()
    out.mkdir(parents=True, exist_ok=True)
    is_url = "://" in a.target
    is_svg = Path(urlparse(a.target).path if is_url else a.target).suffix.lower() == ".svg"

    tmp_wrap = None
    try:
        if a.preset:
            pw, ph = BANNER_PRESETS[a.preset]
            widths, height = [pw], ph
        elif is_svg:
            if not is_url and Path(a.target).is_file():
                sw, sh = _svg_dimensions(Path(a.target))
                widths, height = [sw], sh
            else:
                widths, height = [1280], 420
        else:
            widths = [int(w) for w in a.widths.split(",") if w.strip()]
            height = a.height

        if is_svg and not is_url:
            tmp_wrap = Path(tempfile.mkdtemp(prefix="maxilun-svgwrap-"))
            url = _wrap_svg(Path(a.target).resolve(), widths[0], height or 420, tmp_wrap)
        else:
            url = to_url(a.target)

        if with_playwright(url, widths, height, out, is_svg=is_svg, is_preset=bool(a.preset)) or with_cli(url, widths, height, out, is_svg=is_svg, is_preset=bool(a.preset)):
            print("Now open every PNG above and critique what you see (see maxilun-craft SKILL.md §7).")
            return 0
    finally:
        if tmp_wrap:
            shutil.rmtree(tmp_wrap, ignore_errors=True)

    print("[UNVERIFIED] no renderer: install Playwright (pip install playwright && playwright install chromium) "
          "or Chrome/Edge, or set MAXILUN_BROWSER.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
