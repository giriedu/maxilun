#!/usr/bin/env python3
"""slopscan - mechanical check for machine-averaged UI. Part of maxilun-craft.

Usage:
  slopscan.py <file-or-dir> [more paths]   scan UI source files
  slopscan.py <path> --json                machine-readable output
  slopscan.py <path> --strict              warnings also fail (exit 1)
  slopscan.py --contrast <fg> <bg>         WCAG contrast of two hex colours

Scans .html .htm .css .scss .jsx .tsx .js .ts .vue .svelte .astro .gs.html .svg
No dependencies. Exit code 1 when errors are found (or warnings with --strict).

It only finds what can be found by pattern. Structure, hierarchy and taste
need a person or a screenshot: see references/tells.md.
"""
import json
import os
import re
import sys

EXT = (".html", ".htm", ".css", ".scss", ".jsx", ".tsx", ".js", ".ts",
       ".vue", ".svelte", ".astro", ".svg")
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", "out",
             "vendor", "coverage", ".turbo", ".cache"}

E, W, I = "error", "warn", "info"
WEIGHT = {E: 6, W: 2, I: 1}

COOL = r"(?:purple|violet|indigo|fuchsia|pink|blue|sky|cyan)"
EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF"
    "\U00002B50\U00002B06\U00002705\U0000274C\U00002728\U000026A1]")
SPACING_PREFIX = (r"(?:p[xytrbl]?|m[xytrbl]?|gap(?:-[xy])?|space-[xy]|"
                  r"w|h|min-w|min-h|max-h|top|left|right|bottom|inset(?:-[xy])?)")

# What a model picks when nobody chose. Matched only as the primary family, so a
# system-stack fallback like `"Segoe UI", Roboto, sans-serif` stays quiet.
SATURATED_FONTS = (r"Inter|Roboto|Open[ _+]Sans|Poppins|Montserrat|Lato|Nunito|Space[ _+]Grotesk|"
                   r"Plus[ _+]Jakarta[ _+]Sans|DM[ _+]Sans|Outfit|Manrope|Sora|Geist(?:[ _+](?:Sans|Mono))?|"
                   r"Satoshi|Urbanist|Lexend|Playfair[ _+]Display|Instrument[ _+]Serif|Fraunces|Syne|"
                   r"Clash[ _+]Display|JetBrains[ _+]Mono|Fira[ _+]Code|Space[ _+]Mono")

# (id, level, regex, message, fix)
LINE_RULES = [
    ("default-font", W,
     re.compile(r"(?:font-family\s*:\s*|fontFamily\s*:\s*|family=|--[\w-]*font[\w-]*\s*:\s*|(?:sans|serif|mono|display|heading|body)\s*:\s*\[\s*)"
                r"['\"]?(?:" + SATURATED_FONTS + r")\b"
                r"|import\s*\{[^}]*\b(?:" + SATURATED_FONTS + r")\b[^}]*\}\s*from\s*['\"]next/font", re.I),
     "saturated default font (reads as machine-picked)",
     "derive the face from the Origin (SKILL.md 4.3), or state why only this product can claim it"),
    ("blur-blob", E,
     re.compile(r"\bblur-(?:2xl|3xl|\[\d{2,}px\])\b|filter\s*:\s*['\"]?blur\(\s*(?:[4-9]\d|\d{3,})px", re.I),
     "large blurred colour blob decoration (CMP-016)", "remove; show the product or an Origin object"),
    ("sparkle-icon", W,
     re.compile(r"<(?:Sparkles?|WandSparkles|Wand2|MagicWand|SparklesIcon)\b|\bi-(?:lucide|ph|mdi)[:-]sparkle", re.I),
     "sparkle or magic-wand icon (stock 'AI' signifier)", "an icon that names the action, or the verb alone"),
    ("gradient-cool", E,
     re.compile(r"(?:from|via|to)-" + COOL + r"-\d{2,3}.*(?:from|via|to)-\w+-\d{2,3}"
                r"|linear-gradient\([^)]*(?:purple|violet|indigo|#667eea|#764ba2|#[67a][0-9a-f][457][0-9a-f][ef][0-9a-f])", re.I),
     "hue-to-hue gradient in the blue/violet/pink family",
     "flat surface from the neutral ramp; accent only on the Spotlight"),
    ("gradient", W,
     re.compile(r"(?:linear|radial|conic)-gradient\([^)]*#[0-9a-f]{3,8}[^)]*#[0-9a-f]{3,8}"
                r"|\bbg-(?:gradient|linear)-to-\w+\b", re.I),
     "gradient surface", "allowed only as a small tone shift inside one neutral; otherwise flat"),
    ("gradient-text", E,
     re.compile(r"bg-clip-text|(?:-webkit-)?background-clip\s*:\s*['\"]?text|WebkitBackgroundClip\s*:\s*['\"]?text", re.I),
     "gradient-filled text", "solid text colour; hierarchy from size"),
    ("glow", E,
     re.compile(r"shadow-\[0_0_|drop-shadow-\[0_0_|shadow-" + COOL + r"-\d{3}"
                r"|(?:box-shadow|boxShadow)\s*:[^;}\n]*\b0(?:px)?\s+0(?:px)?\s+\d{2,}px[^;}\n]*(?:rgba?\((?!0,\s*0,\s*0)|#(?!000))", re.I),
     "glow or coloured shadow", "surface step + hairline; neutral shadow only for floating layers"),
    ("transition-all", W,
     re.compile(r"\btransition-all\b|(?:transition|transitionProperty)\s*:\s*['\"]?all\b", re.I),
     "transition on all properties", "name the properties (colour, opacity, transform)"),
    ("loop-motion", W,
     re.compile(r"\banimate-(?:pulse|ping|bounce)\b|animation[^;:}\n]*:\s*['\"]?[^;\n]*\binfinite\b", re.I),
     "looping animation", "keep only if the thing is really live or loading"),
    ("hover-scale", W,
     re.compile(r"hover:scale-(?!100\b)\d+|:hover\s*\{[^}]*transform\s*:\s*scale\(1\.[0-9]", re.I),
     "scale on hover", "surface or border step on hover; tiny scale-down on press"),
    ("heavy-weight", W,
     re.compile(r"\bfont-(?:extrabold|black)\b|(?:font-weight|fontWeight)\s*:\s*['\"]?[89]00\b", re.I),
     "800-900 weight", "500-600 plus size and space for hierarchy"),
    ("shout-label", W,
     re.compile(r"uppercase[^\"'`\n]*tracking-(?:wide|wider|widest)"
                r"|tracking-(?:wide|wider|widest)[^\"'`\n]*uppercase", re.I),
     "all-caps label with wide tracking", "sentence case in the secondary text role"),
    ("greeting", W,
     re.compile(r"welcome back|selamat datang kembali|good (?:morning|afternoon|evening),", re.I),
     "greeting headline", "name the page or the period instead"),
    ("hype", W,
     re.compile(r"\b(?:supercharge|seamless(?:ly)?|unlock (?:the|your)|effortless(?:ly)?|"
                r"revolutioni[sz]e|game[- ]chang|next[- ]gen|cutting[- ]edge|ai[- ]powered|"
                r"solusi terbaik|tingkatkan produktivitas|revolusioner|tanpa batas)\b", re.I),
     "hype vocabulary", "say what it does, for whom, in the users' words"),
    ("placeholder-data", W,
     re.compile(r"lorem ipsum|john doe|jane doe|example@(?:email|example)\.com|\b123[,.]456\b", re.I),
     "placeholder data left in", "plausible data for the domain and locale"),
    ("generic-button", I,
     re.compile(r">\s*(?:Submit|Click here|OK)\s*</(?:button|a)>", re.I),
     "generic button label", "verb + object, e.g. 'Simpan data siswa'"),
    ("exclaim", I,
     re.compile(r">[^<>{}]*[A-Za-z]!+\s*<"),
     "exclamation mark in interface text", "plain statement"),
    ("caps-css", I,
     re.compile(r"(?:text-transform|textTransform)\s*:\s*['\"]?uppercase", re.I),
     "uppercase transform", "confirm it is not a tracked micro-label"),
    ("breadcrumb-header", W,
     re.compile(r">\s*(?:Home|Dashboard|Overview|App|Pages)\s*[/›>»]\s*(?:Dashboard|Analytics|Overview|Settings|Features|Home)\s*<", re.I),
     "breadcrumb-like header on flat surface (HDR-001)", "domain-authentic masthead; keep breadcrumbs for >=3 deep hierarchies"),
    ("pill-tagline", E,
     re.compile(r"rounded-full[^\"'>]*border[^\"'>]*(?:bg-|text-)[^\"'>]*>\s*(?:[•·\|\/\*]\s*)?[A-Z0-9_\s\/-]{3,80}(?:\s*[•·\|\/\*]\s*[A-Z0-9_\s\/-]{3,80})*\s*<", re.I),
     "floating pill tagline capsule with bullets above headline (CMP-015)", "unbordered sentence-case text eyebrow or integrate context directly into headline"),
    ("pill-overload", E,
     re.compile(r"rounded-full[^>\n]*>[^<]*(?:LIVE|HOST|AI|KKTP|PIPELINE|VALID|NORMAL|AKTIF)", re.I),
     "scattered status pill badges used as micro-frames (CMP-022)", "use plain typography, tabular numbers, or a single live status indicator dot"),
    ("symmetric-kpi-strip", E,
     re.compile(r"\bgrid-cols-(?:4|5)\b[^\"'>\n]*(?:\brounded-(?:lg|xl|2xl)\b|card)", re.I),
     "symmetrical 4 or 5 KPI card strip without role differentiation (LAY-017)", "rank the metrics: let the one that matters lead (wider, alone, or as a chart) and set the rest as a quiet ledger row"),
    ("centered-hero-stack", E,
     re.compile(r"(?:text-center\b[^\n]*\b(?:items-center|mx-auto)\b[^\n]*\brounded-full|rounded-full\b[^\n]*\btext-center\b[^\n]*\b(?:items-center|mx-auto))", re.I),
     "centered hero stack with floating pill badge capsule (LAY-018)", "use an asymmetric start-aligned layout or split editorial composition"),
    ("pastel-badge", W,
     re.compile(r"(?:bg-(?:blue|indigo|sky|purple|emerald|amber|violet|teal|cyan|pink|rose)-50\b[^\"'>\n]*\brounded\b|\brounded\b[^\"'>\n]*bg-(?:blue|indigo|sky|purple|emerald|amber|violet|teal|cyan|pink|rose)-50\b)", re.I),
     "icon or badge inside a pastel rounded square (CMP-021)", "monochrome text-colour icon or clean neutral surface badge"),
]

OFFGRID_TW = re.compile(r"(?<![\w-])-?" + SPACING_PREFIX + r"-\[(\d+(?:\.\d+)?)px\]")
OFFGRID_CSS = re.compile(r"(?:padding|margin|gap|row-gap|column-gap)(?:-\w+)?\s*:\s*([^;{}]+)", re.I)
HEX = re.compile(r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
TW_SIZE = re.compile(r"(?<![\w-])text-(xs|sm|base|lg|xl|[2-9]xl|\[\d+(?:\.\d+)?(?:px|rem)\])")
CSS_SIZE = re.compile(r"(?:font-size|fontSize)\s*:\s*['\"]?([\d.]+(?:px|rem|em))", re.I)
TW_HUE = re.compile(r"(?:bg|text|border|from|to|via|ring|fill|stroke)-"
                    r"(red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|"
                    r"indigo|violet|purple|fuchsia|pink|rose)-\d{2,3}")


def _strip_block_comments(text: str) -> str:
    """Replaces /* ... */, <!-- ... -->, and {/* ... */} comments while preserving line numbers."""
    def _blank(m: re.Match) -> str:
        return "".join("\n" if c == "\n" else " " for c in m.group(0))
    out = re.sub(r"\{/\*[\s\S]*?\*/\}", _blank, text)
    out = re.sub(r"/\*[\s\S]*?\*/", _blank, out)
    out = re.sub(r"<!--[\s\S]*?-->", _blank, out)
    return out


def is_comment(line):
    s = line.strip()
    return s.startswith(("//", "/*", "*", "<!--", "#!"))


def _rgb_hue_sat(hexc):
    h = hexc.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) < 6:
        return None
    r, g, b = (int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    mx, mn = max(r, g, b), min(r, g, b)
    d = mx - mn
    sat = 0.0 if mx == 0 else d / mx
    if d == 0:
        hue = 0.0
    elif mx == r:
        hue = 60 * (((g - b) / d) % 6)
    elif mx == g:
        hue = 60 * ((b - r) / d + 2)
    else:
        hue = 60 * ((r - g) / d + 4)
    return hue, sat


def _circular_hue_span(hues):
    if len(hues) < 2:
        return 0.0
    s = sorted(hues)
    gaps = [s[i + 1] - s[i] for i in range(len(s) - 1)] + [360.0 - s[-1] + s[0]]
    return 360.0 - max(gaps)


def _scan_svg_block(svg_text, line_offset, add, full_doc_text, standalone=True):
    """Audits standalone SVG files or inline <svg> blocks inside HTML/JSX/Vue."""
    if standalone:
        if not re.search(r"<title\b", svg_text, re.IGNORECASE):
            add("svg-missing-title", E, line_offset, "standalone SVG missing <title> element",
                "add <title id='...-title'> and <desc> inside <svg>")
        if 'role="img"' not in svg_text and "aria-hidden=" not in svg_text:
            add("svg-missing-role", E, line_offset, "standalone SVG missing role='img' or aria-hidden='true'",
                "add role='img' with aria-labelledby (or aria-hidden='true' if decorative)")

    unsafe_rx = re.compile(r"<script\b|<foreignObject\b|\bon[a-z]+\s*=|javascript:|https?://[^\s\"']+\.(?:css|woff2?|ttf|otf)", re.IGNORECASE)
    heavy_rx = re.compile(r"(?:font-weight\s*=\s*[\"']?|font-weight\s*:\s*)[89]00\b", re.IGNORECASE)
    grad_text_rx = re.compile(r"<text[^>]*?(?:fill\s*=\s*[\"']url\(|fill\s*:\s*url\()", re.IGNORECASE)
    blur_rx = re.compile(r"<feGaussianBlur[\s\S]{0,160}?stdDeviation\s*=\s*[\"']?(?:1[6-9]|[2-9]\d|\d{3,})", re.IGNORECASE)
    svg_font_rx = re.compile(r"(?:font-family\s*=\s*|font-family\s*:\s*)[\"']?(?:" + SATURATED_FONTS + r")\b", re.IGNORECASE)
    smil_rx = re.compile(r"<animate(?:Motion|Transform)?[\s\S]{0,200}?repeatCount\s*=\s*[\"']indefinite[\"']", re.IGNORECASE)

    has_reduced = bool(re.search(r"@media\s*\([^)]*prefers-reduced-motion", full_doc_text, re.I))
    for rx, rid, lvl, msg, fix in (
        (unsafe_rx, "svg-unsafe", E, "SVG contains script, foreignObject, event handler, javascript:, or external font/CSS URL",
         "keep SVG self-contained with system font stack and zero scripting"),
        (heavy_rx, "heavy-weight", W, "800-900 font-weight in SVG",
         "use 500-700 weight plus size and space for hierarchy"),
        (grad_text_rx, "gradient-text", E, "gradient-filled SVG <text> (TYPO-008)",
         "use solid ink colour with >= 4.5:1 contrast"),
        (blur_rx, "blur-blob", E, "large SVG Gaussian blur blob (CMP-016)",
         "remove blur blob; show concrete Origin geometry"),
        (svg_font_rx, "default-font", W, "saturated default font-family in SVG",
         "use system-ui stack for <img> or an Origin display face"),
    ):
        for m in rx.finditer(svg_text):
            ln = line_offset + svg_text[:m.start()].count("\n")
            add(rid, lvl, ln, msg, fix, m.group(0).splitlines()[0])

    if not has_reduced:
        for m in smil_rx.finditer(svg_text):
            ln = line_offset + svg_text[:m.start()].count("\n")
            add("loop-motion", W, ln, "infinite SMIL SVG animation without prefers-reduced-motion guard",
                "wrap animation or add @media (prefers-reduced-motion: reduce) guard", m.group(0).splitlines()[0])

    for gm in re.finditer(r"<(?:linear|radial)Gradient\b[^>]*>[\s\S]*?</(?:linear|radial)Gradient>", svg_text, re.IGNORECASE):
        stops = HEX.findall(gm.group(0))
        chroma = []
        for hx in stops:
            hs = _rgb_hue_sat(hx)
            if hs and hs[1] >= 0.25:
                chroma.append(hs[0])
        if len(chroma) >= 2 and _circular_hue_span(chroma) >= 18:
            ln = line_offset + svg_text[:gm.start()].count("\n")
            add("gradient-cool", E, ln, "chromatic multi-hue SVG gradient (CLR-001)",
                "use flat neutral surfaces or a quiet single-ramp tonal shift", gm.group(0).splitlines()[0])

    rect_dims = []
    for rm in re.finditer(r"<rect\b[^>]*>", svg_text, re.IGNORECASE):
        tag = rm.group(0)
        mw = re.search(r'\bwidth\s*=\s*["\'](\d+(?:\.\d+)?)["\']', tag)
        mh = re.search(r'\bheight\s*=\s*["\'](\d+(?:\.\d+)?)["\']', tag)
        mrx = re.search(r'\brx\s*=\s*["\'](\d+(?:\.\d+)?)["\']', tag)
        if mw and mh and mrx:
            rect_dims.append((mw.group(1), mh.group(1), mrx.group(1)))
    if rect_dims:
        from collections import Counter
        top_dim, count = Counter(rect_dims).most_common(1)[0]
        if count >= 4 and float(top_dim[0]) >= 120 and float(top_dim[1]) >= 80:
            add("symmetric-kpi-strip", E, line_offset,
                f"symmetrical {count}-card strip inside SVG ({top_dim[0]}x{top_dim[1]}, rx={top_dim[2]}) (LAY-017)",
                "replace uniform cards with an asymmetric layout or single Spotlight")


def scan_file(path):
    findings, stats = [], {}
    try:
        raw_text = open(path, encoding="utf-8", errors="ignore").read()
    except OSError:
        return findings, stats
    text = _strip_block_comments(raw_text)
    lines = text.split("\n")
    is_svg = path.lower().endswith(".svg")

    def add(rule, level, ln, msg, fix, sample=""):
        findings.append({"file": path, "line": ln, "rule": rule, "level": level,
                         "message": msg, "fix": fix, "sample": sample.strip()[:90]})

    if is_svg:
        _scan_svg_block(text, 1, add, text, standalone=True)
    else:
        for svg_m in re.finditer(r"<svg\b[\s\S]*?</svg>", text, re.IGNORECASE):
            ln = text[:svg_m.start()].count("\n") + 1
            _scan_svg_block(svg_m.group(0), ln, add, text, standalone=False)

    emoji_lines, offgrid = [], []
    for n, line in enumerate(lines, 1):
        if is_comment(line):
            continue
        if is_svg:
            # Run text-level typography/hype/caps rules on SVG <text>/<style> content too.
            for rid, lvl, rx, msg, fix in LINE_RULES:
                if rid in ("hype", "greeting", "caps-css", "placeholder-data"):
                    m = rx.search(line)
                    if m:
                        add(rid, lvl, n, msg, fix, m.group(0))
        else:
            for rid, lvl, rx, msg, fix in LINE_RULES:
                m = rx.search(line)
                if m:
                    add(rid, lvl, n, msg, fix, m.group(0))
            for m in OFFGRID_TW.finditer(line):
                v = float(m.group(1))
                if v > 2 and v % 4:
                    offgrid.append((n, m.group(0)))
            for m in OFFGRID_CSS.finditer(line):
                for px in re.findall(r"(?<![\w.#-])(\d+(?:\.\d+)?)px", m.group(1)):
                    v = float(px)
                    if v > 2 and v % 4:
                        offgrid.append((n, m.group(0).strip()))
                        break
        if EMOJI.search(line):
            emoji_lines.append(n)

    if emoji_lines:
        add("emoji", E if len(emoji_lines) > 2 else W, emoji_lines[0],
            "emoji used in the interface (%d lines: %s%s)" % (
                len(emoji_lines), ", ".join(map(str, emoji_lines[:6])),
                "..." if len(emoji_lines) > 6 else ""),
            "one line-icon family, or words")
    if offgrid:
        add("off-grid", W if len(offgrid) > 3 else I, offgrid[0][0],
            "%d spacing values off the 4px grid (first: %s)" % (len(offgrid), offgrid[0][1]),
            "use steps from the spacing tokens")

    hexes = {h.lower() for h in HEX.findall(text)}
    if len(hexes) > 14:
        add("colour-sprawl", W, 1, "%d distinct hex colours in one file" % len(hexes),
            "reduce to ramp roles + one accent + status")
    hues = set(TW_HUE.findall(text))
    if len(hues) > 4:
        add("hue-sprawl", W, 1, "%d colour families used (%s)" % (len(hues), ", ".join(sorted(hues))),
            "one accent; categorical colour only as small marks")
    sizes = set(TW_SIZE.findall(text)) | set(CSS_SIZE.findall(text))
    if len(sizes) > 6:
        add("size-sprawl", W, 1, "%d distinct font sizes" % len(sizes),
            "at most six sizes from one ratio")
    blur = len(re.findall(r"backdrop-blur|(?:backdrop-filter|backdropFilter)\s*:\s*['\"]?blur", text))
    if blur > 2:
        add("glass", W, 1, "backdrop blur used %d times" % blur,
            "solid surfaces; blur only behind one floating layer")
    big_r = len(re.findall(r"\brounded-(?:2xl|3xl)\b|(?:border-radius|borderRadius)\s*:\s*['\"]?(?:1[6-9]|[23]\d)px", text))
    if big_r >= 8:
        add("radius-monotony", W, 1, "large radius repeated %d times" % big_r,
            "one radius decision from the Voice; nested radius = outer - padding")
    pills = len(re.findall(r"\brounded-full\b|(?:border-radius|borderRadius)\s*:\s*['\"]?(?:9999px|999px|50rem)", text))
    if pills > 4:
        add("pill-overload", E if pills >= 5 else W, 1, "fully rounded pill shape used %d times (CMP-022)" % pills,
            "one radius decision; pills only for tags and toggles, maximum 2 per screen")

    # Multiline Centered Hero Stack: text-center with mx-auto followed by rounded-full and h1
    m_hero = re.search(r"text-center[^\n]*mx-auto[\s\S]{0,400}?rounded-full[\s\S]{0,400}?<h1", text, re.I)
    if m_hero and not any(f["rule"] == "centered-hero-stack" for f in findings):
        ln = text[:m_hero.start()].count("\n") + 1
        add("centered-hero-stack", E, ln,
            "monotonous centered hero stack with floating pill capsule (LAY-018)",
            "use an asymmetric start-aligned layout or split editorial composition", m_hero.group(0)[:80])

    # Tagline pill capsule with explicit eyebrow markers (•, //, STANDAR, SAAS) rather than benign version chips.
    for m in re.finditer(r"rounded-full[^>]*>[\s\S]{0,250}?(?:STANDAR|MULTI-TENANT|SAAS|\b[A-Z0-9_\/-]{4,}\s*\/\/\s*[A-Z0-9_\/-]{4,})[\s\S]{0,100}?<\/(?:div|span)>", text, re.I):
        if len(m.group(0)) < 350:
            ln = text[:m.start()].count("\n") + 1
            if not any(f["rule"] == "pill-tagline" and f["line"] == ln for f in findings):
                add("pill-tagline", E, ln, "floating pill tagline capsule above headline (CMP-015)",
                    "unbordered sentence-case text eyebrow or integrate context directly into headline", m.group(0)[:80])

    m_pill = re.search(r"rounded-full[^>]*>\s*(?:[•·\|\/\*]\s*[A-Z0-9_\s\/-]{3,80}|[A-Z0-9_-]{3,}\s*//\s*[A-Z0-9_-]{3,})\s*</", text, re.I)
    if m_pill and not any(f["rule"] == "pill-tagline" for f in findings):
        ln = text[:m_pill.start()].count("\n") + 1
        add("pill-tagline", E, ln, "floating pill tagline capsule above headline (CMP-015)",
            "unbordered sentence-case text eyebrow or integrate context directly into headline", m_pill.group(0)[:80])

    white_cards = sum(
        1 for ln_str in lines
        if re.search(r"\bbg-white\b", ln_str)
        and re.search(r"\brounded-(?:lg|xl|2xl|3xl)\b", ln_str)
        and re.search(r"\bborder(?:-(?:gray|slate|zinc|neutral|stone)-(?:100|200|300))?\b|\bshadow-(?:sm|md|lg)\b", ln_str)
    )
    if white_cards > 3:
        add("white-box-monoculture", E if white_cards >= 4 else W, 1,
            "%d generic white rounded cards with light borders/shadows (LAY-014)" % white_cards,
            "declare an authentic archetype (e.g. Technical Ledger, Deep Space Obsidian, Swiss High-Contrast); avoid generic white boxes on light-gray background")

    # Multiline Symmetric 4/5 KPI Card Strip (LAY-017)
    for m_kpi in re.finditer(r"\b(?:md:|lg:|xl:)?grid-cols-(?:4|5)\b[\s\S]{0,650}", text, re.I):
        window = m_kpi.group(0)
        if not re.search(r"\bcol-span-(?:2|3|4|5|6|7|8)\b", window):
            card_children = len(re.findall(r"\brounded-(?:lg|xl|2xl|3xl)\b[^\"'>]*(?:p-|border|bg-|shadow)", window))
            if card_children >= 2 and not any(f["rule"] == "symmetric-kpi-strip" for f in findings):
                ln = text[:m_kpi.start()].count("\n") + 1
                add("symmetric-kpi-strip", E, ln,
                    "symmetrical 4 or 5 KPI card strip across parent/child nodes (LAY-017)",
                    "rank the metrics: let the one that matters lead (wider, alone, or as a chart) and set the rest as a quiet ledger row",
                    window.splitlines()[0][:80])

    # Multiline Symmetric 3-Card Triad (LAY-008)
    for m_tri in re.finditer(r"\b(?:md:|lg:)?grid-cols-3\b[\s\S]{0,800}", text, re.I):
        window = m_tri.group(0)
        first_line = window.splitlines()[0]
        if "tablist" in first_line or "<dl" in first_line:
            continue
        if not re.search(r"\bcol-span-(?:2|4|6|8)\b", window):
            tri_cards = len(re.findall(r"\brounded-(?:xl|2xl|3xl)\b[^\"'>]*(?:p-|border|bg-|shadow)", window))
            if tri_cards >= 3 and not any(f["rule"] == "symmetric-triad" for f in findings):
                ln = text[:m_tri.start()].count("\n") + 1
                add("symmetric-triad", W, ln,
                    "symmetrical 3-card triad without role differentiation (LAY-008)",
                    "let the content ranking decide: a comparison table, master-detail split, or one lead item with the rest secondary",
                    first_line[:80])

    # Multiline JSX/HTML generic action button detection
    for m_btn in re.finditer(r"<(?:button|a)\b[^>]*>\s*(?:Submit|Click here|OK)\s*</(?:button|a)>", text, re.I):
        ln = text[:m_btn.start()].count("\n") + 1
        if not any(f["rule"] == "generic-button" and f["line"] == ln for f in findings):
            add("generic-button", I, ln, "generic button label", "verb + object, e.g. 'Simpan data siswa'", m_btn.group(0)[:80])

    tactile_rx = re.compile(
        r"cubic-bezier\(0\.16,\s*1,\s*0\.3,\s*1\)|layoutId|useSpring|useAnimationControls|"
        r"staggerChildren|beforeChildren|dragConstraints|active:scale-|translate3d\(|"
        r"rotateX\(|radial-gradient\([^)]*circle at|gridTemplateRows|grid-template-rows|"
        r"requestAnimationFrame|@keyframes\s+\w+", re.I
    )
    has_tactile = bool(tactile_rx.search(text))
    is_interactive_view = bool(re.search(r"<button|<a\s|<input|onClick", text)) and len(lines) >= 45
    if is_interactive_view and not has_tactile and path.lower().endswith((".tsx", ".jsx", ".vue", ".svelte", ".html")):
        add("shallow-motion", I, 1,
            "no motion primitives found in an interactive screen",
            "check the renders: add motion only where a state change is otherwise hard to follow (ui-motion-recipes.md)")

    stats["motion"] = bool(re.search(r"(?:transition\s*:|@keyframes\b|\banimate-(?:pulse|ping|bounce|spin)|\bmotion\.)", text))
    stats["tactile_motion"] = has_tactile
    stats["reduced"] = bool(re.search(r"@media\s*\([^)]*prefers-reduced-motion|motion-reduce:|motion-safe:|"
                                      r"useReducedMotion|reducedMotion", text))
    stats["interactive"] = bool(re.search(r"<button|<a\s|<input|onClick", text))
    stats["focus"] = bool(re.search(r"focus-visible|:focus|focus:", text))
    stats["tokens"] = bool(re.search(r"--[\w-]+\s*:|@theme|theme\.extend|tailwind\.config", text))
    return findings, stats


def collect(paths):
    files = []
    for p in paths:
        if os.path.isfile(p):
            files.append(p)
        elif os.path.isdir(p):
            for root, dirs, names in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
                for nm in names:
                    if nm.lower().endswith(EXT) and not nm.endswith(".min.js") \
                            and not nm.endswith(".min.css"):
                        files.append(os.path.join(root, nm))
        else:
            print("not found: %s" % p, file=sys.stderr)
    return sorted(files)


def lum(hexc):
    h = hexc.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) < 6:
        raise ValueError(hexc)
    ch = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    ch = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in ch]
    return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]


def contrast(fg, bg):
    a, b = sorted((lum(fg), lum(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def main(argv):
    if "--contrast" in argv:
        i = argv.index("--contrast")
        try:
            r = contrast(argv[i + 1], argv[i + 2])
        except (IndexError, ValueError):
            print("usage: slopscan.py --contrast <fg hex> <bg hex>")
            return 2
        verdict = ("passes text (AA)" if r >= 4.5 else
                   "passes large text / UI only" if r >= 3 else "fails")
        print("%.2f:1  %s" % (r, verdict))
        return 0 if r >= 4.5 else 1

    as_json, strict = "--json" in argv, "--strict" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        print(__doc__)
        return 2
    files = collect(paths)
    if not files:
        print("no UI source files found")
        return 2

    findings, agg = [], {"motion": False, "reduced": False, "interactive": False,
                         "focus": False, "tokens": False}
    for f in files:
        fs, st = scan_file(f)
        findings += fs
        for k in agg:
            agg[k] = agg[k] or st.get(k, False)

    def project(rule, level, msg, fix):
        findings.append({"file": "(project)", "line": 0, "rule": rule, "level": level,
                         "message": msg, "fix": fix, "sample": ""})
    all_svg = all(f.lower().endswith(".svg") for f in files)
    if not all_svg and agg["motion"] and not agg["reduced"]:
        project("no-reduced-motion", W, "motion present but no reduced-motion handling",
                "add the global prefers-reduced-motion guard")
    if not all_svg and agg["interactive"] and not agg["focus"]:
        project("no-focus-style", W, "interactive elements but no focus styles found",
                "add a visible :focus-visible ring")
    if not all_svg and not agg["tokens"]:
        project("no-tokens", W, "no design tokens found (custom properties or theme)",
                "lock tokens before components: references/tokens.md")

    counts = {lvl: sum(1 for f in findings if f["level"] == lvl) for lvl in (E, W, I)}
    score = max(0, 100 - sum(WEIGHT[f["level"]] for f in findings))
    if as_json:
        print(json.dumps({"files": len(files), "score": score, "counts": counts,
                          "findings": findings}, indent=2, ensure_ascii=False))
    else:
        order = {E: 0, W: 1, I: 2}
        for f in sorted(findings, key=lambda x: (order[x["level"]], x["file"], x["line"])):
            loc = f["file"] if not f["line"] else "%s:%d" % (f["file"], f["line"])
            print("%-5s %-18s %s" % (f["level"].upper(), f["rule"], loc))
            print("      %s%s" % (f["message"], ("  [" + f["sample"] + "]") if f["sample"] else ""))
            print("      -> %s" % f["fix"])
        print("\n%d files | %d errors, %d warnings, %d notes | score %d/100" % (
            len(files), counts[E], counts[W], counts[I], score))
        if not findings:
            print("Nothing mechanical found. Now do the tests that need eyes: "
                  "squint, swap, greyscale, keyboard, narrow, states.")
        else:
            print("A clean scan is necessary, not sufficient. See references/tells.md.")
    return 1 if counts[E] or (strict and counts[W]) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
