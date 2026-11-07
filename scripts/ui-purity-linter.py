#!/usr/bin/env python3
"""
Maxilun UI Purity Linter (ui-purity-linter.py)

Deterministic AST and regex scanner detecting 45 AI design tells
across HTML, CSS, TSX, JSX, Vue, Svelte, Swift, and Kotlin files.
Adheres strictly to references/purity-catalog.md and maxilun-craft standards.

The audit is the ceiling, this linter is the floor.
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


@dataclass
class TellViolation:
    rule_id: str
    category: str
    message: str
    severity: str  # "ERROR" or "WARNING"
    file_path: str
    line_number: int
    snippet: str
    remedy: str


@dataclass
class ScanResult:
    total_files: int = 0
    scanned_lines: int = 0
    violations: List[TellViolation] = field(default_factory=list)
    score: float = 100.0

    @property
    def passed(self) -> bool:
        error_count = sum(1 for v in self.violations if v.severity == "ERROR")
        return error_count == 0 and self.score >= 85.0

    def calculate_score(self):
        if self.scanned_lines == 0:
            self.score = 100.0
            return
        penalty = 0.0
        for v in self.violations:
            penalty += 5.0 if v.severity == "ERROR" else 2.0
        self.score = max(0.0, min(100.0, 100.0 - penalty))


class UIPurityLinter:
    """Deterministic scanner for the 45 AI Design Tells taxonomy."""

    TELL_RULES: List[Tuple[str, str, str, str, str, re.Pattern]] = [
        # --- 1-5: Warna (Color) ---
        (
            "CLR-TEL-01", "Warna", "ERROR",
            "Cliche AI gradient detected (purple-blue or rainbow text-gradient on headings)",
            "Ganti dengan warna solid material fisik dunia nyata domain subjek (OKLCH).",
            re.compile(r"(?:from-purple-|from-violet-|to-indigo-|#667eea|#764ba2|#8b5cf6|linear-gradient\([^)]*(?:#667eea|#764ba2|purple|violet)|(?:bg-clip-text\s+text-transparent|text-transparent\s+bg-clip-text))", re.IGNORECASE)
        ),
        (
            "CLR-TEL-02", "Warna", "ERROR",
            "Saturated neon glow drop-shadow or saturated colored container border",
            "Gunakan hairline border 1px netral atau bayangan kontak alami beropasitas rendah.",
            re.compile(r"(?:shadow-(?:purple|indigo|pink|cyan|fuchsia)-\d+|box-shadow:[^;]*(?:rgba\(\s*(?:139|124|168|236|59)\s*,[^;]*\b(?:20|25|30)px\b)|border-(?:purple|cyan|pink|fuchsia)-(?:400|500|600))", re.IGNORECASE)
        ),
        (
            "CLR-TEL-03", "Warna", "WARNING",
            "Status indicator relying solely on color dot without text/icon accompaniment",
            "Wajib tambahkan teks atau ikon semantik pendamping (aksesibilitas).",
            re.compile(r"""<(?:span|div)[^>]*class=["'][^"']*\b(?:bg-green-500|bg-red-500|bg-emerald-500)\b[^"']*\b(?:rounded-full|w-2|h-2|w-3|h-3)\b[^"']*["']\s*(?:/>|></(?:span|div)>)""", re.IGNORECASE)
        ),
        (
            "CLR-TEL-04", "Warna", "ERROR",
            "High chroma oversaturated container background",
            "Redam kroma latar belakang utama agar mata pengguna tidak lelah (chroma <= 0.04 di OKLCH).",
            re.compile(r"""\b(?:bg-pink-600|bg-purple-700|bg-fuchsia-600)\b""", re.IGNORECASE)
        ),
        (
            "CLR-TEL-05", "Warna", "WARNING",
            "Uncalibrated raw pure black text (#000000) on pure white canvas",
            "Gunakan tinta gelap terkalibrasi terhadap suhu permukaan (misal: oklch(0.20 0.01 hue)).",
            re.compile(r"(?:color:\s*#000000|text-black)\b[^;]*\b(?:background(?:-color)?:\s*#ffffff|bg-white)\b", re.IGNORECASE)
        ),

        # --- 6-12: Tata Letak (Layout) ---
        (
            "LAY-TEL-01", "Tata Letak", "ERROR",
            "Monotonous centered hero stack (badge -> H1 -> p -> 2 twin buttons)",
            "Gunakan tata letak asimetris atau penataan editorial bertingkat alami.",
            re.compile(r"""(?:\btext-center\b[^\n]*\bitems-center\b[^\n]*\bjustify-center\b[^\n]*\brounded-full\b[^\n]*\btracking-wid)""", re.IGNORECASE)
        ),
        (
            "LAY-TEL-02", "Tata Letak", "WARNING",
            "Symmetrical 3-card triad without role differentiation (grid-cols-3)",
            "Ganti sesuai sifat konten: tabel perbandingan faktual, alur langkah, atau split showcase.",
            re.compile(r"""\bgrid-cols-1\s+md:grid-cols-3\b[^\n]*\brounded-2xl\b""", re.IGNORECASE)
        ),
        (
            "LAY-TEL-03", "Tata Letak", "ERROR",
            "4 floating KPI metric cards strip with decorative percent badge",
            "Tampilkan metrik langsung di konteks data atau tabel operasional tanpa kartu mengambang palsu.",
            re.compile(r"""\bgrid-cols-4\b[^\n]*\b(?:\+12\.5%|\+24%|\+8\.4%|text-emerald-500)\b""", re.IGNORECASE)
        ),
        (
            "LAY-TEL-04", "Tata Letak", "ERROR",
            "Twin solid primary buttons competing for focus in the same view",
            "Tetapkan tepat satu tombol beraksen solid per tampilan; tombol pendamping wajib sekunder/outline.",
            re.compile(r"""<button[^>]*class=["'][^"']*\bbg-(?:blue|indigo|emerald|violet)-600\b[^"']*["'][^>]*>[^<]*</button>\s*<button[^>]*class=["'][^"']*\bbg-(?:blue|indigo|emerald|violet)-600\b""", re.IGNORECASE)
        ),
        (
            "LAY-TEL-05", "Tata Letak", "WARNING",
            "Card-inside-a-card wrapper nesting abuse",
            "Gunakan spasi 2x (spatial rhythm) alih-alih menambah kotak garis batas bersarang.",
            re.compile(r"""<(?:div|section|article)[^>]*class=["'][^"']*\b(?:card|border\b[^"']*\brounded-[a-z0-9]+)\b[^"']*["'][^>]*>\s*<(?:div|section|article)[^>]*class=["'][^"']*\b(?:card|border\b[^"']*\brounded-[a-z0-9]+)\b""", re.IGNORECASE)
        ),
        (
            "LAY-TEL-06", "Tata Letak", "ERROR",
            "Dark SaaS Bento Grid forced on non-technical domain",
            "Sesuaikan arsitektur layout dengan dokumen kerja riil domain bersangkutan.",
            re.compile(r"""\bbento\b[^\n]*\bbg-zinc-950\b|\bcol-span-2\b[^\n]*\brow-span-2\b[^\n]*\bbg-black\b""", re.IGNORECASE)
        ),
        (
            "LAY-TEL-07", "Tata Letak", "WARNING",
            "Unbounded paragraph line length (> 75ch without max-w constraint)",
            "Terapkan max-w-[65ch] atau max-w-prose dan text-wrap: pretty.",
            re.compile(r"""<p[^>]*class=["'][^"']*\b(?:max-w-none|w-full)\b[^"']*["'][^>]*>[^<]{120,}""", re.IGNORECASE)
        ),

        # --- 13-20: Komponen (Components) ---
        (
            "CMP-TEL-01", "Komponen", "ERROR",
            "Floating pill badge with glowing dot stamped above heading",
            "Hapus kapsul dekoratif; integrasikan konteks langsung ke dalam judul atau navigasi.",
            re.compile(r"""(?:rounded-full[^"']*\b(?:px-[2-6]|py-[0-3])\b[^"']*(?:uppercase|tracking-wid)[^"']*["'][^>]*>(?:\s*(?:•|\*)|[^<]*[•·\*]|<span[^>]*bg-(?:emerald|green|indigo|cyan)-500))""", re.IGNORECASE)
        ),
        (
            "CMP-TEL-02", "Komponen", "WARNING",
            "Fake Cmd+K / Ctrl+K keyboard shortcut badge on landing page",
            "Gunakan input pencarian fungsional; jangan pasang shortcut keyboard palsu di luar aplikasi kerja.",
            re.compile(r"""(?:<kbd[^>]*>(?:⌘K|Cmd\s*\+\s*K|Ctrl\s*\+\s*K)</kbd>)""", re.IGNORECASE)
        ),
        (
            "CMP-TEL-03", "Komponen", "ERROR",
            "Dead interactive button or control without click handler",
            "Setiap tombol interaktif wajib memiliki fungsi/state nyata atau dihilangkan.",
            re.compile(r"""(?:onClick=\{\(\)\s*=>\s*\{\}\}|href="#"|href=""|action=\{\(\)\s*=>\s*\{\}\})""", re.IGNORECASE)
        ),
        (
            "CMP-TEL-04", "Komponen", "WARNING",
            "Nested border-radius ignoring concentric formula (R_inner = R_outer - Padding)",
            "Gunakan radius konsentris eksak agar sudut tidak bertabrakan optik.",
            re.compile(r"""p-4\s+rounded-2xl[^\n]*rounded-2xl|p-6\s+rounded-xl[^\n]*rounded-xl""", re.IGNORECASE)
        ),
        (
            "CMP-TEL-05", "Komponen", "WARNING",
            "Redundant shallow breadcrumb on flat page (Home > Dashboard)",
            "Gunakan judul halaman tunggal atau tautan kembali; simpan breadcrumb untuk taksonomi >= 3 level.",
            re.compile(r"""(?:Home\s*>\s*Dashboard|Home\s*/\s*Settings)\b""", re.IGNORECASE)
        ),
        (
            "CMP-TEL-06", "Komponen", "ERROR",
            "Emoji used as UI functional buttons, headings, badges, or list icons (AI slop)",
            "Gunakan ikon SVG semantik yang terstandarisasi optik (lulus 1-Bit Monochrome Test).",
            re.compile(r"""<(?:button|a|h[1-6]|span|li|div|p)[^>]*>(?:[^<]*)(?:🚀|✨|🔥|🎉|💡|⚡|⭐|✅|❌|⚠️|👉|💎|🌟|🤖)(?:[^<]*)</(?:button|a|h[1-6]|span|li|div|p)>""", re.IGNORECASE)
        ),
        (
            "CMP-TEL-07", "Komponen", "WARNING",
            "Numbers, prices, or financial metrics without tabular-nums",
            "Wajib tambahkan font-variant-numeric: tabular-nums (atau class tabular-nums).",
            re.compile(r"""<(?:span|div|p)[^>]*class=["'](?!.*tabular-nums)[^"']*(?:font-mono|text-[0-9a-z]+)[^"']*["'][^>]*>[\$€£Rp]\s*[0-9]+""", re.IGNORECASE)
        ),
        (
            "CMP-TEL-08", "Komponen", "ERROR",
            "Centered bare spinner loader isolated in screen without geometry skeleton",
            "Gunakan skeleton geometri proporsional 1:1 (CLS = 0) alih-alih spinner kosong.",
            re.compile(r"""\b(?:animate-spin|border-t-transparent)\b[^\n]*\b(?:w-8\s+h-8|w-12\s+h-12)\b[^\n]*\bmx-auto\b""", re.IGNORECASE)
        ),

        # --- 21-28: Tipografi (Typography) ---
        (
            "TYP-TEL-01", "Tipografi", "WARNING",
            "Default uncalibrated system sans-serif for unique heritage/editorial subject",
            "Pilih typeface yang memiliki akar historis/geografis dengan karakter produk.",
            re.compile(r"""font-family:\s*(?:'Inter'|Inter|'Geist'|Geist)[^;]*;""", re.IGNORECASE)
        ),
        (
            "TYP-TEL-02", "Tipografi", "WARNING",
            "Title Case used in descriptive sentences or body headings",
            "Terapkan sentence case alami pada judul dan keterangan deskriptif.",
            re.compile(r"""<h[1-4][^>]*>[A-Z][a-z]{2,}\s+[A-Z][a-z]{2,}\s+[A-Z][a-z]{2,}\s+[A-Z][a-z]{2,}</h[1-4]>""")
        ),
        (
            "TYP-TEL-03", "Tipografi", "ERROR",
            "Uppercase tracking-widest stamped blindly across every section label",
            "Batasi huruf kapital lebar hanya untuk label metadata teknis atau satuan ukur.",
            re.compile(r"""\buppercase\b[^\n]*\btracking-wid(?:est|er)\b[^\n]*\btext-xs\b""", re.IGNORECASE)
        ),
        (
            "TYP-TEL-04", "Tipografi", "ERROR",
            "Low contrast faint gray text (< 4.5:1 ratio)",
            "Tingkatkan kontras warna teks terhadap permukaan sesuai standar WCAG AA.",
            re.compile(r"""\b(?:text-gray-300|text-zinc-400|text-slate-400)\b[^\n]*\b(?:bg-white|bg-slate-50)\b""", re.IGNORECASE)
        ),
        (
            "TYP-TEL-05", "Tipografi", "ERROR",
            "Mobile input font-size smaller than 16px (triggers iOS auto-zoom)",
            "Atur font-size input minimal 16px (text-base) pada layar mobile.",
            re.compile(r"""<input[^>]*class=["'][^"']*\b(?:text-xs|text-sm|text-\[1[0-4]px\])\b[^"']*["']""", re.IGNORECASE)
        ),
        (
            "TYP-TEL-06", "Tipografi", "WARNING",
            "Headline text without text-wrap: balance (risk of orphaned words)",
            "Pasang text-wrap: balance pada seluruh judul halaman dan modal.",
            re.compile(r"""<h[1-3][^>]*class=["'](?!.*(?:text-balance|text-wrap:\s*balance))[^"']*["']""", re.IGNORECASE)
        ),
        (
            "TYP-TEL-07", "Tipografi", "WARNING",
            "Typography scale chaos (> 5 unscaled arbitrary font sizes in one view)",
            "Gunakan skala tipe matematis terukur (misal: rasio 1.250 Major Third).",
            re.compile(r"""text-\[1[13579]px\]|text-\[2[137]px\]""", re.IGNORECASE)
        ),
        (
            "TYP-TEL-08", "Tipografi", "WARNING",
            "Monospace font forced on non-technical prose or descriptions",
            "Simpan font monospace hanya untuk kode, token, atau koordinat.",
            re.compile(r"""<p[^>]*class=["'][^"']*\b(?:font-mono|font-\['Courier'\])\b[^"']*["'][^>]*>[A-Za-z\s]{50,}""", re.IGNORECASE)
        ),

        # --- 29-35: Mobile Native ---
        (
            "MOB-TEL-01", "Mobile Native", "ERROR",
            "Ignoring SafeArea insets on mobile screen container",
            "Pastikan konten interaktif berada dalam safe area insets (safeAreaPadding / insets).",
            re.compile(r"""\.ignoresSafeArea\(\)\s*(?!\.background)""", re.IGNORECASE)
        ),
        (
            "MOB-TEL-02", "Mobile Native", "ERROR",
            "Touch target size below 44pt (iOS) or 48dp (Android)",
            "Bungkus tombol/kontrol interaktif dengan target sentuh minimal 44x44pt.",
            re.compile(r"""<(?:button|a)[^>]*class=["'][^"']*\b(?:w-6\s+h-6|w-7\s+h-7|w-8\s+h-8|w-\[3\dpx\])\b[^"']*["']|\.frame\(\s*(?:width|minWidth):\s*(?:[1-3]\d|[1-9])\s*,\s*(?:height|minHeight):\s*(?:[1-3]\d|[1-9])\s*\)""", re.IGNORECASE)
        ),
        (
            "MOB-TEL-03", "Mobile Native", "WARNING",
            "Hijacking native platform navigation stack with non-standard custom header",
            "Utamakan pola NavigationStack / UINavigationBar / TopAppBar native.",
            re.compile(r"""class=["'][^"']*\bfixed\s+top-0\s+left-0\s+w-full\s+z-50\b[^"']*["'][^>]*>\s*<button[^>]*Back</button>""", re.IGNORECASE)
        ),
        (
            "MOB-TEL-04", "Mobile Native", "WARNING",
            "Hardcoded font points ignoring Dynamic Type scaling in mobile app",
            "Gunakan text styles semantik bawaan sistem (.title, .headline, .body).",
            re.compile(r"""\.font\(\.system\(size:\s*\d{2,}\)\)""", re.IGNORECASE)
        ),
        (
            "MOB-TEL-05", "Mobile Native", "ERROR",
            "Mobile input form without keyboard avoidance padding (imePadding)",
            "Pasang imePadding (Android) atau keyboard avoidance auto-scroll.",
            re.compile(r"""TextField\(|OutlinedTextField\(|TextInput\b(?!.*(?:imePadding|keyboardAvoiding))""", re.IGNORECASE)
        ),
        (
            "MOB-TEL-06", "Mobile Native", "WARNING",
            "Repetitive confirmation modal cascade instead of reversible undo toast",
            "Ganti modal konfirmasi dengan Undo Toast berbatas waktu 5-8 detik.",
            re.compile(r"""(?:Are you sure you want to delete|Apakah Anda yakin ingin menghapus)""", re.IGNORECASE)
        ),
        (
            "MOB-TEL-07", "Mobile Native", "ERROR",
            "Disabling native interactive swipe back gesture",
            "Pertahankan navigasi gestur usap kembali alami platform.",
            re.compile(r"""navigationBarBackButtonHidden\(true\)(?!.*ToolbarItem)""", re.IGNORECASE)
        ),

        # --- 36-41: Konten & Copy ---
        (
            "CPY-TEL-01", "Konten", "ERROR",
            "Cliche AI promotional hero slogan formula",
            "Tulis tindakan fungsional spesifik yang nyata dapat dilakukan pengguna.",
            re.compile(r"""(?:Revolutionize\s+Your|Unlock\s+Your\s+Potential|Supercharge\s+Your|The\s+Ultimate\s+All-in-One|Di\s+era\s+digital\s+yang\s+serba\s+cepat|Solusi\s+terpadu\s+untuk)""", re.IGNORECASE)
        ),
        (
            "CPY-TEL-02", "Konten", "ERROR",
            "Invented statistical rating or fake social proof count",
            "Hapus klaim statistik dan rating fiktif (purity invariant).",
            re.compile(r"""(?:★\s*4\.9\s*/\s*5|4\.98\s*\/\s*5\.0|10\,?000\+\s*happy\s*users|Trusted\s+by\s+10k\+|10\.000\+\s*tim\s*percaya)""", re.IGNORECASE)
        ),
        (
            "CPY-TEL-03", "Konten", "ERROR",
            "Forbidden AI buzzword detected in user-facing copy",
            "Ganti dengan kata kerja bahasa manusia yang langsung dan jujur.",
            re.compile(r"""\b(?:delve|tapestry|synergy|holistic|leverage|seamlessly|robust|cutting-edge|game-changer|supercharge|dive\s+in|menyelami|merajut\s+harmoni|sinergi)\b""", re.IGNORECASE)
        ),
        (
            "CPY-TEL-04", "Konten", "ERROR",
            "Fabricated marketing testimonial quotation",
            "Hanya tampilkan ulasan riil yang tersimpan di basis data produksi.",
            re.compile(r"""(?:This\s+app\s+completely\s+changed\s+my\s+life|Aplikasi\s+ini\s+benar-benar\s+mengubah\s+hidup\s+saya)""", re.IGNORECASE)
        ),
        (
            "CPY-TEL-05", "Konten", "WARNING",
            "Generic ambiguous button action verb (Submit / Get Started)",
            "Gunakan label spesifik kata kerja + objek (mis. 'Kirim Tagihan', 'Periksa Tanggal').",
            re.compile(r"""<(?:button|a)[^>]*>(?:\s*)(?:Submit|Get\s+Started|Click\s+Here|Mulai\s+Sekarang)(?:\s*)</(?:button|a)>|(?:Button|Text)\(\s*["'](?:Submit|Get\s+Started|Click\s+Here|Mulai\s+Sekarang)["']\s*\)""", re.IGNORECASE)
        ),
        (
            "CPY-TEL-06", "Konten", "WARNING",
            "Conversational opening fluff filler sentence",
            "Langsung sebutkan entitas produk dan instruksi fungsional langkah berikutnya.",
            re.compile(r"""(?:In\s+today's\s+fast-paced\s+world|Dalam\s+dunia\s+modern\s+yang\s+dinamis|As\s+an\s+AI\s+language\s+model)""", re.IGNORECASE)
        ),

        # --- 42-45: Gerak & Aksesibilitas (Motion & A11y) ---
        (
            "ANI-TEL-01", "Gerak", "ERROR",
            "Animating layout reflow properties (width, height, top, left, margin)",
            "Animasikan hanya transform dan opacity untuk menjaga 60/120 FPS tanpa layout thrashing.",
            re.compile(r"""transition(?:-all)?:\s*[^;]*(?:width|height|top|left|margin|padding)""", re.IGNORECASE)
        ),
        (
            "ANI-TEL-02", "Gerak", "WARNING",
            "Infinite continuous distracting animation loop on interactive controls",
            "Batasi animasi interaksi hanya saat event hover/active/load selesai.",
            re.compile(r"""\b(?:animate-bounce|animate-pulse)\b[^\n]*\b(?:rounded-full|btn|button)\b""", re.IGNORECASE)
        ),
        (
            "ANI-TEL-03", "Gerak", "ERROR",
            "CSS animation lacking prefers-reduced-motion media query fallback",
            "Wajib tambahkan @media (prefers-reduced-motion: reduce) { ... }.",
            re.compile(r"""@keyframes\s+[a-zA-Z0-9_-]+\s*\{(?![^}]*prefers-reduced-motion)""", re.IGNORECASE)
        ),
        (
            "ANI-TEL-04", "Gerak", "WARNING",
            "Sluggish micro-interaction transition duration (> 300ms)",
            "Batasi respon mikro-interaksi tombol dan kontrol pada durasi 100-200ms.",
            re.compile(r"""transition-duration:\s*(?:[4-9]\d{2}|[1-9]\d{3})ms\b|duration-(?:500|700|1000)\b""", re.IGNORECASE)
        ),
    ]

    SUPPORTED_EXTENSIONS = {
        ".html", ".htm", ".css", ".scss", ".tsx", ".jsx",
        ".vue", ".svelte", ".swift", ".kt", ".md"
    }

    def scan_file(self, file_path: Path) -> List[TellViolation]:
        violations: List[TellViolation] = []
        if file_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            return violations
        if "design-md" in file_path.parts:
            return violations

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return violations

        lines = content.splitlines()
        is_md = file_path.suffix.lower() == ".md"
        in_code_block = False

        for idx, line in enumerate(lines, start=1):
            if is_md:
                if line.strip().startswith("```"):
                    in_code_block = not in_code_block
                    continue
                if not in_code_block:
                    continue

            for rule_id, category, severity, msg, remedy, pattern in self.TELL_RULES:
                # Avoid scanning self definition files
                if file_path.name in ("ui-purity-linter.py", "purity-catalog.md", "SKILL.md") and "TELL_RULES" in line:
                    continue
                match = pattern.search(line)
                if match:
                    snippet = line.strip()
                    if len(snippet) > 90:
                        snippet = snippet[:87] + "..."
                    violations.append(TellViolation(
                        rule_id=rule_id,
                        category=category,
                        message=msg,
                        severity=severity,
                        file_path=str(file_path),
                        line_number=idx,
                        snippet=snippet,
                        remedy=remedy,
                    ))
        return violations

    def scan_path(self, target_path: Path) -> ScanResult:
        result = ScanResult()
        files_to_scan: List[Path] = []

        if target_path.is_file():
            if "design-md" not in target_path.parts:
                files_to_scan.append(target_path)
        elif target_path.is_dir():
            for root, dirs, files in os.walk(target_path):
                # Ignore node_modules, .git, venv, build, and design-md reference archive
                dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "venv", ".venv", "build", "dist", ".next", "__pycache__", "design-md")]
                for f in files:
                    p = Path(root) / f
                    if p.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                        files_to_scan.append(p)

        result.total_files = len(files_to_scan)
        for f in files_to_scan:
            try:
                line_count = len(f.read_text(encoding="utf-8", errors="ignore").splitlines())
                result.scanned_lines += line_count
            except Exception:
                pass
            v = self.scan_file(f)
            result.violations.extend(v)

        result.calculate_score()
        return result


def format_report(result: ScanResult, verbose: bool = False) -> str:
    status_icon = "✅ PASS" if result.passed else "❌ FAIL"
    err_count = sum(1 for v in result.violations if v.severity == "ERROR")
    warn_count = sum(1 for v in result.violations if v.severity == "WARNING")

    lines = [
        "============================================================",
        f"  Maxilun UI Purity Gate: {status_icon} (Score: {result.score:.1f}/100)",
        f"  Files Scanned: {result.total_files} | Lines: {result.scanned_lines}",
        f"  Violations Found: {len(result.violations)} (Errors: {err_count}, Warnings: {warn_count})",
        "============================================================"
    ]

    if result.violations:
        lines.append("\nDetected AI Design Tells:")
        for v in result.violations:
            loc = f"{Path(v.file_path).name}:{v.line_number}"
            lines.append(f"  [{v.severity}] [{v.rule_id}] {v.message} ({loc})")
            lines.append(f"      Code:   `{v.snippet}`")
            lines.append(f"      Remedy: {v.remedy}")
    else:
        lines.append("\n  Zero AI design tells detected. Surface is clean and authentic.")

    return "\n".join(lines)


def run_self_test() -> bool:
    """Self-test validating that the 45 tell rules work deterministically."""
    print("🧪 Running UIPurityLinter self-test on synthetic test cases...")
    linter = UIPurityLinter()

    bad_sample = """
    <div class="from-purple-600 to-indigo-600 shadow-purple-500 rounded-full px-3 py-1 uppercase tracking-widest">
      <span>✨</span> Revolutionize Your Experience with our 10,000+ happy users!
      <button onClick={() => {}} class="bg-blue-600">Submit</button>
      <button class="bg-blue-600">Get Started</button>
      <input class="text-xs" />
    </div>
    """
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".tsx", delete=False, encoding="utf-8") as f:
        f.write(bad_sample)
        temp_bad = Path(f.name)

    good_sample = """
    <div class="bg-stone-50 border border-stone-200 p-6 rounded-xl">
      <h2 class="text-stone-900 font-serif text-2xl text-balance">Available rooms for your stay</h2>
      <p class="text-stone-600 text-base max-w-prose">Restored 1840 stone farmhouse bordered by hundred-year cork oaks.</p>
      <span class="tabular-nums font-medium text-stone-900">€285 / night</span>
      <button onClick={handleCheckDates} class="bg-emerald-900 text-stone-100 h-12 px-6 rounded-lg">Check dates</button>
    </div>
    """
    with tempfile.NamedTemporaryFile("w", suffix=".tsx", delete=False, encoding="utf-8") as f:
        f.write(good_sample)
        temp_good = Path(f.name)

    try:
        bad_res = linter.scan_path(temp_bad)
        good_res = linter.scan_path(temp_good)

        assert len(bad_res.violations) >= 5, f"Expected >=5 violations on bad sample, got {len(bad_res.violations)}"
        assert not bad_res.passed, "Bad sample should fail purity check"
        assert len(good_res.violations) == 0, f"Expected 0 violations on good sample, got {len(good_res.violations)}"
        assert good_res.passed, "Good sample should pass purity check"
        print(f"  ✅ Caught {len(bad_res.violations)} tells in bad sample (Score: {bad_res.score:.1f}/100)")
        print(f"  ✅ Clean sample passed perfectly (Score: {good_res.score:.1f}/100)")
        print("  🎉 Self-test passed successfully.")
        return True
    finally:
        if temp_bad.exists():
            temp_bad.unlink()
        if temp_good.exists():
            temp_good.unlink()


def main():
    parser = argparse.ArgumentParser(description="Maxilun UI Purity Linter — 45 AI Design Tells Scanner")
    parser.add_argument("target", nargs="?", default=".", help="Target file or directory to scan")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--strict", action="store_true", help="Fail if any warning or error is found")
    parser.add_argument("--self-test", action="store_true", help="Run deterministic self-test suite")

    args = parser.parse_args()

    if args.self_test:
        success = run_self_test()
        sys.exit(0 if success else 1)

    target_path = Path(args.target).resolve()
    if not target_path.exists():
        print(f"Error: Target path '{target_path}' does not exist.", file=sys.stderr)
        sys.exit(1)

    linter = UIPurityLinter()
    result = linter.scan_path(target_path)

    if args.json:
        payload = {
            "passed": result.passed,
            "score": result.score,
            "total_files": result.total_files,
            "scanned_lines": result.scanned_lines,
            "violations": [
                {
                    "rule_id": v.rule_id,
                    "category": v.category,
                    "severity": v.severity,
                    "message": v.message,
                    "file_path": v.file_path,
                    "line_number": v.line_number,
                    "snippet": v.snippet,
                    "remedy": v.remedy
                }
                for v in result.violations
            ]
        }
        print(json.dumps(payload, indent=2))
    else:
        print(format_report(result))

    if args.strict:
        sys.exit(0 if len(result.violations) == 0 else 1)
    else:
        sys.exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()
