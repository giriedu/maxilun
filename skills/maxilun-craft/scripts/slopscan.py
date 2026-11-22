#!/usr/bin/env python3
"""slopscan - mechanical check for machine-averaged UI. Part of maxilun-craft.

Usage:
  slopscan.py <file-or-dir> [more paths]   scan UI source files
  slopscan.py <path> --json                machine-readable output
  slopscan.py <path> --strict              warnings also fail (exit 1)
  slopscan.py --contrast <fg> <bg>         WCAG contrast of two hex colours

Scans .html .htm .css .scss .jsx .tsx .js .ts .vue .svelte .astro .gs.html
No dependencies. Exit code 1 when errors are found (or warnings with --strict).

It only finds what can be found by pattern. Structure, hierarchy and taste
need a person or a screenshot: see references/tells.md.
"""
import json
import os
import re
import sys

EXT = (".html", ".htm", ".css", ".scss", ".jsx", ".tsx", ".js", ".ts",
       ".vue", ".svelte", ".astro")
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

# (id, level, regex, message, fix)
LINE_RULES = [
    ("gradient-cool", E,
     re.compile(r"(?:from|via|to)-" + COOL + r"-\d{2,3}.*(?:from|via|to)-\w+-\d{2,3}"
                r"|linear-gradient\([^)]*(?:purple|violet|indigo|#[67a][0-9a-f]5[0-9a-f]f[0-9a-f])", re.I),
     "hue-to-hue gradient in the blue/violet/pink family",
     "flat surface from the neutral ramp; accent only on the Spotlight"),
    ("gradient", W,
     re.compile(r"(?:linear|radial|conic)-gradient\([^)]*#[0-9a-f]{3,8}[^)]*#[0-9a-f]{3,8}"
                r"|\bbg-(?:gradient|linear)-to-\w+\b", re.I),
     "gradient surface", "allowed only as a small tone shift inside one neutral; otherwise flat"),
    ("gradient-text", E,
     re.compile(r"bg-clip-text|background-clip\s*:\s*text|-webkit-background-clip\s*:\s*text", re.I),
     "gradient-filled text", "solid text colour; hierarchy from size"),
    ("glow", E,
     re.compile(r"shadow-\[0_0_|drop-shadow-\[0_0_|shadow-" + COOL + r"-\d{3}"
                r"|box-shadow\s*:[^;]*\b0(?:px)?\s+0(?:px)?\s+\d{2,}px[^;]*(?:rgba?\((?!0,\s*0,\s*0)|#(?!000))", re.I),
     "glow or coloured shadow", "surface step + hairline; neutral shadow only for floating layers"),
    ("transition-all", W,
     re.compile(r"\btransition-all\b|transition\s*:\s*all\b", re.I),
     "transition on all properties", "name the properties (colour, opacity, transform)"),
    ("loop-motion", W,
     re.compile(r"\banimate-(?:pulse|ping|bounce)\b|animation[^;:]*:[^;]*\binfinite\b", re.I),
     "looping animation", "keep only if the thing is really live or loading"),
    ("hover-scale", W,
     re.compile(r"hover:scale-(?!100\b)\d+|:hover\s*\{[^}]*transform\s*:\s*scale\(1\.[0-9]", re.I),
     "scale on hover", "surface or border step on hover; tiny scale-down on press"),
    ("heavy-weight", W,
     re.compile(r"\bfont-(?:extrabold|black)\b|font-weight\s*:\s*[89]00", re.I),
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
     re.compile(r"text-transform\s*:\s*uppercase", re.I),
     "uppercase transform", "confirm it is not a tracked micro-label"),
    ("breadcrumb-header", W,
     re.compile(r">\s*(?:Home|Dashboard|Overview|App|Pages)\s*[/›>»]\s*(?:Dashboard|Analytics|Overview|Settings|Features|Home)\s*<", re.I),
     "breadcrumb-like header on flat surface (HDR-001)", "domain-authentic masthead; keep breadcrumbs for >=3 deep hierarchies"),
    ("pill-tagline", W,
     re.compile(r"rounded-full[^\"'>]*border[^\"'>]*(?:bg-|text-)[^\"'>]*>\s*(?:[•·\|\/]\s*)?[A-Z0-9_\s-]{3,24}(?:\s*[•·\|\/]\s*[A-Z0-9_\s-]{3,24})*\s*<", re.I),
     "floating pill tagline capsule with bullets above headline (CMP-015)", "unbordered sentence-case text eyebrow or integrate context directly into headline"),
    ("pastel-badge", W,
     re.compile(r"(?:bg-(?:blue|indigo|sky|purple|emerald|amber|violet|teal|cyan|pink|rose)-50\b[^\"'>\n]*\brounded\b|\brounded\b[^\"'>\n]*bg-(?:blue|indigo|sky|purple|emerald|amber|violet|teal|cyan|pink|rose)-50\b)", re.I),
     "icon or badge inside a pastel rounded square (CMP-021)", "monochrome text-colour icon or clean neutral surface badge"),
]

OFFGRID_TW = re.compile(r"(?<![\w-])-?" + SPACING_PREFIX + r"-\[(\d+(?:\.\d+)?)px\]")
OFFGRID_CSS = re.compile(r"(?:padding|margin|gap|row-gap|column-gap)(?:-\w+)?\s*:\s*([^;{}]+)", re.I)
HEX = re.compile(r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
TW_SIZE = re.compile(r"(?<![\w-])text-(xs|sm|base|lg|xl|[2-9]xl|\[\d+(?:\.\d+)?(?:px|rem)\])")
CSS_SIZE = re.compile(r"font-size\s*:\s*([\d.]+(?:px|rem|em))", re.I)
TW_HUE = re.compile(r"(?:bg|text|border|from|to|via|ring|fill|stroke)-"
                    r"(red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|"
                    r"indigo|violet|purple|fuchsia|pink|rose)-\d{2,3}")


def is_comment(line):
    s = line.strip()
    return s.startswith(("//", "/*", "*", "<!--", "#!"))


def scan_file(path):
    findings, stats = [], {}
    try:
        text = open(path, encoding="utf-8", errors="ignore").read()
    except OSError:
        return findings, stats
    lines = text.split("\n")

    def add(rule, level, ln, msg, fix, sample=""):
        findings.append({"file": path, "line": ln, "rule": rule, "level": level,
                         "message": msg, "fix": fix, "sample": sample.strip()[:90]})

    emoji_lines, offgrid = [], []
    for n, line in enumerate(lines, 1):
        if is_comment(line) or len(line) > 2000:
            continue
        for rid, lvl, rx, msg, fix in LINE_RULES:
            m = rx.search(line)
            if m:
                add(rid, lvl, n, msg, fix, m.group(0))
        if EMOJI.search(line):
            emoji_lines.append(n)
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
    blur = len(re.findall(r"backdrop-blur|backdrop-filter\s*:\s*blur", text))
    if blur > 2:
        add("glass", W, 1, "backdrop blur used %d times" % blur,
            "solid surfaces; blur only behind one floating layer")
    pills = len(re.findall(r"\brounded-full\b|border-radius\s*:\s*(?:9999px|999px|50rem)", text))
    if pills > 8:
        add("pill-everything", I, 1, "fully rounded shape used %d times" % pills,
            "one radius decision; pills only for tags and toggles")

    white_cards = len(re.findall(r"\bbg-white\b[^\"'>\n]*(?:\brounded-(?:lg|xl|2xl)\b[^\"'>\n]*\bborder-(?:gray|slate)-(?:100|200)\b|\bborder-(?:gray|slate)-(?:100|200)\b[^\"'>\n]*\brounded-(?:lg|xl|2xl)\b)", text))
    if white_cards > 3:
        add("white-box-monoculture", W, 1,
            "%d generic white rounded cards with gray borders (LAY-014)" % white_cards,
            "declare an authentic archetype (e.g. Technical Ledger, Deep Space Obsidian, Swiss High-Contrast); avoid generic white boxes on light-gray background")

    stats["motion"] = bool(re.search(r"transition|animation|@keyframes|animate-|motion\.", text))
    stats["reduced"] = bool(re.search(r"prefers-reduced-motion|motion-reduce:|motion-safe:|"
                                      r"useReducedMotion|reducedMotion", text))
    stats["interactive"] = bool(re.search(r"<button|<a\s|<input|onClick", text))
    stats["focus"] = bool(re.search(r"focus-visible|:focus|focus:", text))
    stats["tokens"] = bool(re.search(r"--[\w-]+\s*:|@theme|theme\.extend|tailwind\.config", text))
    stats["inter_only"] = bool(re.search(r"font-family[^;]*\bInter\b|['\"]Inter['\"]", text))
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
                         "focus": False, "tokens": False, "inter_only": False}
    for f in files:
        fs, st = scan_file(f)
        findings += fs
        for k in agg:
            agg[k] = agg[k] or st.get(k, False)

    def project(rule, level, msg, fix):
        findings.append({"file": "(project)", "line": 0, "rule": rule, "level": level,
                         "message": msg, "fix": fix, "sample": ""})
    if agg["motion"] and not agg["reduced"]:
        project("no-reduced-motion", W, "motion present but no reduced-motion handling",
                "add the global prefers-reduced-motion guard")
    if agg["interactive"] and not agg["focus"]:
        project("no-focus-style", W, "interactive elements but no focus styles found",
                "add a visible :focus-visible ring")
    if not agg["tokens"]:
        project("no-tokens", W, "no design tokens found (custom properties or theme)",
                "lock tokens before components: references/tokens.md")
    if agg["inter_only"]:
        project("default-font", I, "Inter in use", "confirm it was chosen for the Voice, or replace")

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
