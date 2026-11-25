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
from typing import List, Dict, Optional, Tuple, Any

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
            re.compile(r"(?:shadow-(?:purple|indigo|pink|cyan|fuchsia)-\d+|shadow-\[0_0_|(?:box-shadow|boxShadow):\s*[^;\n]*(?:rgba\(\s*(?:16|139|124|168|236|59)\s*,[^;\n]*\b(?:1[2-9]|[2-9]\d)px\b)|border-(?:purple|cyan|pink|fuchsia)-(?:400|500|600))", re.IGNORECASE)
        ),
        (
            "CLR-TEL-03", "Warna", "WARNING",
            "Status indicator relying solely on color dot without text/icon accompaniment",
            "Wajib tambahkan teks atau ikon semantik pendamping (aksesibilitas).",
            re.compile(r"""<(?:span|div)[^>]*class(?:Name)?=["'][^"']*\b(?:bg-green-500|bg-red-500|bg-emerald-500)\b[^"']*\b(?:rounded-full|w-2|h-2|w-3|h-3)\b[^"']*["']\s*(?:/>|></(?:span|div)>)""", re.IGNORECASE)
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
            "LAY-TEL-02", "Tata Letak", "ERROR",
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
            re.compile(r"""<button[^>]*class(?:Name)?=["'][^"']*\bbg-(?:blue|indigo|emerald|violet)-600\b[^"']*["'][^>]*>[^<]*</button>\s*<button[^>]*class(?:Name)?=["'][^"']*\bbg-(?:blue|indigo|emerald|violet)-600\b""", re.IGNORECASE)
        ),
        (
            "LAY-TEL-05", "Tata Letak", "WARNING",
            "Card-inside-a-card wrapper nesting abuse",
            "Gunakan spasi 2x (spatial rhythm) alih-alih menambah kotak garis batas bersarang.",
            re.compile(r"""<(?:div|section|article)[^>]*class(?:Name)?=["'][^"']*\b(?:card|border\b[^"']*\brounded-[a-z0-9]+)\b[^"']*["'][^>]*>\s*<(?:div|section|article)[^>]*class(?:Name)?=["'][^"']*\b(?:card|border\b[^"']*\brounded-[a-z0-9]+)\b""", re.IGNORECASE)
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
            re.compile(r"""<p[^>]*class(?:Name)?=["'][^"']*\b(?:max-w-none|w-full)\b[^"']*["'][^>]*>[^<]{120,}""", re.IGNORECASE)
        ),
        (
            "LAY-TEL-08", "Tata Letak", "ERROR",
            "Symmetrical 4 or 5 KPI card strip without role differentiation (LAY-017)",
            "Urutkan konten: satu yang paling penting memimpin, sisanya jadi baris ledger yang tenang, tabel, atau master-detail.",
            re.compile(r"""\b(?:grid-cols-4|grid-cols-5|md:grid-cols-4|md:grid-cols-5)\b[^\n]*(?:\brounded-(?:lg|xl|2xl)\b|card)""", re.IGNORECASE)
        ),
        (
            "LAY-TEL-09", "Tata Letak", "ERROR",
            "Centered hero stack with floating capsule badge (LAY-018)",
            "Terapkan tata letak start-aligned editorial atau split hero dengan working console artifact.",
            re.compile(r"""\btext-center\b[^\n]*\b(?:mx-auto|items-center)\b[^\n]*\brounded-full\b""", re.IGNORECASE)
        ),

        # --- 13-20: Komponen (Components) ---
        (
            "CMP-TEL-01", "Komponen", "ERROR",
            "Floating pill badge with glowing dot stamped above heading",
            "Hapus kapsul dekoratif; integrasikan konteks langsung ke dalam judul atau navigasi.",
            re.compile(r"""(?:rounded-full[^"']*\b(?:px-[2-6]|py-[0-3])|\b(?:px-[2-6]|py-[0-3])\b[^"']*rounded-full)[^"']*["'][^>]*>(?:\s*(?:•|\*)|[^<]*[•·\*]|[\s\n]*<span[^>]*bg-(?:emerald|green|indigo|cyan)-500)""", re.IGNORECASE)
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
            re.compile(r"""<(?:[a-zA-Z0-9_\.\-]+)[^>]*>[^<]*(?:[\U0001F300-\U0001FAFF]|[\u2600-\u27BF]|[\u2300-\u23FF]|[\u2B50\u2B55]|🚀|✨|🔥|🎉|💡|⚡|⭐|✅|❌|⚠️|👉|💎|🌟|🤖)""", re.UNICODE | re.IGNORECASE)
        ),
        (
            "CMP-TEL-07", "Komponen", "WARNING",
            "Numbers, prices, or financial metrics without tabular-nums",
            "Wajib tambahkan font-variant-numeric: tabular-nums (atau class tabular-nums).",
            re.compile(r"""<(?:span|div|p)[^>]*class(?:Name)?=["'](?!.*tabular-nums)[^"']*(?:font-mono|text-[0-9a-z]+)[^"']*["'][^>]*>[\$€£Rp]\s*[0-9]+""", re.IGNORECASE)
        ),
        (
            "CMP-TEL-08", "Komponen", "ERROR",
            "Centered bare spinner loader isolated in screen without geometry skeleton",
            "Gunakan skeleton geometri proporsional 1:1 (CLS = 0) alih-alih spinner kosong.",
            re.compile(r"""\b(?:animate-spin|border-t-transparent)\b[^\n]*\b(?:w-8\s+h-8|w-12\s+h-12)\b[^\n]*\bmx-auto\b""", re.IGNORECASE)
        ),
        (
            "CMP-TEL-09", "Komponen", "ERROR",
            "Pill badge overload / decorative capsule proliferation across view (CMP-022)",
            "Hilangkan kapsul rounded-full dekoratif; gunakan tipografi polos dan tabular-nums.",
            re.compile(r"""\brounded-full\b[^\n]*\b(?:text-xs|px-2)\b[^\n]*>(?:\s*(?:•|\*)|[^<]*(?:LIVE|HOST|AI|NORMAL|VALID|AKTIF|STATUS|KKTP))""", re.IGNORECASE)
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
            re.compile(r"""<input[^>]*class(?:Name)?=["'][^"']*\b(?:text-xs|text-sm|text-\[1[0-4]px\])\b[^"']*["']""", re.IGNORECASE)
        ),
        (
            "TYP-TEL-06", "Tipografi", "WARNING",
            "Headline text without text-wrap: balance (risk of orphaned words)",
            "Pasang text-wrap: balance pada seluruh judul halaman dan modal.",
            re.compile(r"""<h[1-3][^>]*class(?:Name)?=["'](?!.*(?:text-balance|text-wrap:\s*balance))[^"']*["']""", re.IGNORECASE)
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
            re.compile(r"""<p[^>]*class(?:Name)?=["'][^"']*\b(?:font-mono|font-\['Courier'\])\b[^"']*["'][^>]*>[A-Za-z\s]{50,}""", re.IGNORECASE)
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
            re.compile(r"""<(?:button|a)[^>]*class(?:Name)?=["'][^"']*\b(?:w-6\s+h-6|w-7\s+h-7|w-8\s+h-8|w-\[3\dpx\])\b[^"']*["']|\.frame\(\s*(?:width|minWidth):\s*(?:[1-3]\d|[1-9])\s*,\s*(?:height|minHeight):\s*(?:[1-3]\d|[1-9])\s*\)""", re.IGNORECASE)
        ),
        (
            "MOB-TEL-03", "Mobile Native", "WARNING",
            "Hijacking native platform navigation stack with non-standard custom header",
            "Utamakan pola NavigationStack / UINavigationBar / TopAppBar native.",
            re.compile(r"""class(?:Name)?=["'][^"']*\bfixed\s+top-0\s+left-0\s+w-full\s+z-50\b[^"']*["'][^>]*>\s*<button[^>]*Back</button>""", re.IGNORECASE)
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
            re.compile(r"""(?:TextField\(|OutlinedTextField\(|TextInput\b)(?!.*(?:imePadding|keyboardAvoiding))""", re.IGNORECASE)
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
            re.compile(r"""transition(?:-all)?:\s*[^;\n]*(?:width|height|top|left|margin|padding)|\btransition-all\b[^\n>]*style=\{\{[^}\n]*(?:width|height|top|left|margin|padding)""", re.IGNORECASE)
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
            re.compile(r"""transition-duration:\s*(?:[4-9]\d{2}|[1-9]\d{3})ms\b|duration-(?:500|700|1000)\b|transition(?:-duration)?:\s*[^;\n]*\b0\.[4-9]\d*s\b""", re.IGNORECASE)
        ),
    ]

    SUPPORTED_EXTENSIONS = {
        ".html", ".htm", ".css", ".scss", ".tsx", ".jsx",
        ".vue", ".svelte", ".astro", ".swift", ".kt", ".md", ".svg"
    }

    SVG_SATURATED_FONTS = re.compile(
        r"(?:font-family\s*=\s*|font-family\s*:\s*)[\"']?(?:Inter|Roboto|Open[ _+]Sans|Poppins|Montserrat|Lato|Nunito|"
        r"Space[ _+]Grotesk|Plus[ _+]Jakarta[ _+]Sans|DM[ _+]Sans|Outfit|Manrope|Sora|Geist|"
        r"Satoshi|Urbanist|Lexend|Playfair[ _+]Display|Instrument[ _+]Serif|Fraunces|Syne|"
        r"Clash[ _+]Display|JetBrains[ _+]Mono|Fira[ _+]Code|Space[ _+]Mono)\b",
        re.IGNORECASE,
    )
    SVG_EMOJI = re.compile(
        r"[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002300-\U000023FF"
        r"\U00002B50\U00002B55\U00002705\U0000274C\U00002728\U000026A1]"
    )

    @staticmethod
    def _strip_block_comments(text: str, keep_examples: bool = False) -> str:
        def _blank(m: re.Match) -> str:
            return "".join("\n" if c == "\n" else " " for c in m.group(0))
        out = re.sub(r"\{/\*[\s\S]*?\*/\}", _blank, text)
        out = re.sub(r"/\*[\s\S]*?\*/", _blank, out)
        if not keep_examples:
            out = re.sub(r"<!--(?!\s*/?maxilun-example:)[\s\S]*?-->", _blank, out)
        return out

    @staticmethod
    def _balanced_css_classes(text: str) -> set:
        """Extracts CSS class selectors whose rules declare `text-wrap: balance`."""
        balanced = set()
        for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", text):
            if re.search(r"text-wrap\s*:\s*balance", m.group(2), re.IGNORECASE):
                for cls in re.findall(r"\.([a-zA-Z0-9_-]+)", m.group(1)):
                    balanced.add(cls)
                for htag in re.findall(r"\b(h[1-3])\b", m.group(1), re.IGNORECASE):
                    balanced.add(htag.lower())
        return balanced

    @staticmethod
    def _circular_hue_span(hues: List[float]) -> float:
        if len(hues) < 2:
            return 0.0
        s = sorted(hues)
        gaps = [s[i + 1] - s[i] for i in range(len(s) - 1)] + [360.0 - s[-1] + s[0]]
        return 360.0 - max(gaps)

    @staticmethod
    def _hex_hue_sat(hexc: str):
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
            hue = 60.0 * (((g - b) / d) % 6)
        elif mx == g:
            hue = 60.0 * ((b - r) / d + 2)
        else:
            hue = 60.0 * ((r - g) / d + 4)
        return hue, sat

    def _scan_svg(self, file_path: Path, content: str, inline: bool = False, line_offset: int = 1, doc_text: str = "") -> List[TellViolation]:
        violations: List[TellViolation] = []
        fp_str = str(file_path)
        full_doc = doc_text or content

        if not inline:
            first_line = content.splitlines()[0][:87] if content else "<svg>"
            if not re.search(r"<title\b", content, re.IGNORECASE):
                violations.append(TellViolation(
                    rule_id="SVG-TEL-01", category="Aksesibilitas SVG", severity="ERROR",
                    message="Standalone SVG missing <title> accessible summary",
                    remedy="Tambahkan <title id='...-title'> dan <desc> di awal <svg>.",
                    file_path=fp_str, line_number=line_offset, snippet=first_line,
                ))
            if 'role="img"' not in content and "aria-hidden=" not in content:
                violations.append(TellViolation(
                    rule_id="SVG-TEL-01", category="Aksesibilitas SVG", severity="ERROR",
                    message="Standalone SVG missing role='img' or aria-hidden='true'",
                    remedy="Tambahkan role='img' + aria-labelledby (atau aria-hidden='true' jika dekoratif).",
                    file_path=fp_str, line_number=line_offset, snippet=first_line,
                ))

        unsafe_rx = re.compile(r"<script\b|<foreignObject\b|\bon[a-z]+\s*=|javascript:|https?://[^\s\"']+\.(?:css|woff2?|ttf|otf)", re.IGNORECASE)
        heavy_rx = re.compile(r"(?:font-weight\s*=\s*[\"']?|font-weight\s*:\s*)[89]00\b", re.IGNORECASE)
        grad_text_rx = re.compile(r"<text[^>]*?(?:fill\s*=\s*[\"']url\(|fill\s*:\s*url\()", re.IGNORECASE)
        blur_rx = re.compile(r"<feGaussianBlur[\s\S]{0,160}?stdDeviation\s*=\s*[\"']?(?:1[6-9]|[2-9]\d|\d{3,})", re.IGNORECASE)
        smil_rx = re.compile(r"<animate(?:Motion|Transform)?[\s\S]{0,200}?repeatCount\s*=\s*[\"']indefinite[\"']", re.IGNORECASE)
        has_reduced = bool(re.search(r"@media\s*\([^)]*prefers-reduced-motion", full_doc, re.IGNORECASE))

        for rx, rid, cat, sev, msg, rem in (
            (unsafe_rx, "SVG-TEL-02", "Keamanan SVG", "ERROR",
             "SVG contains script, foreignObject, event handler, javascript:, or external font/CSS URL",
             "Hapus <script>/<foreignObject>/on* dan gunakan system font stack tanpa tautan eksternal."),
            (heavy_rx, "SVG-TEL-03", "Tipografi SVG", "ERROR",
             "Heavy 800-900 font-weight in SVG typography",
             "Gunakan bobot 500-700 dengan skala ukuran dan kontras warna."),
            (grad_text_rx, "SVG-TEL-03", "Tipografi SVG", "ERROR",
             "Gradient-filled SVG <text> (TYPO-008)",
             "Gunakan fill warna tinta solid dengan kontras >= 4.5:1."),
            (blur_rx, "SVG-TEL-03", "Permukaan SVG", "ERROR",
             "Large SVG Gaussian blur blob (CMP-016)",
             "Hapus efek blur dekoratif; gunakan permukaan solid atau objek Origin konkret."),
            (self.SVG_EMOJI, "SVG-TEL-04", "Komponen SVG", "ERROR",
             "Emoji character inside SVG markup (CMP-003)",
             "Ganti emoji dengan path SVG monokrom atau teks editorial."),
            (self.SVG_SATURATED_FONTS, "SVG-TEL-05", "Tipografi SVG", "WARNING",
             "Saturated default font-family attribute in SVG",
             "Gunakan system-ui stack aman untuk <img> atau font Origin spesifik."),
        ):
            for m in rx.finditer(content):
                ln = line_offset + content[:m.start()].count("\n")
                violations.append(TellViolation(
                    rule_id=rid, category=cat, severity=sev, message=msg, remedy=rem,
                    file_path=fp_str, line_number=ln, snippet=m.group(0).splitlines()[0].strip()[:87],
                ))

        if not has_reduced:
            for m in smil_rx.finditer(content):
                ln = line_offset + content[:m.start()].count("\n")
                violations.append(TellViolation(
                    rule_id="ANI-TEL-03", category="Gerak", severity="ERROR",
                    message="Infinite SMIL SVG animation lacking prefers-reduced-motion guard",
                    remedy="Tambahkan guard @media (prefers-reduced-motion: reduce) atau hapus repeatCount='indefinite'.",
                    file_path=fp_str, line_number=ln, snippet=m.group(0).splitlines()[0].strip()[:87],
                ))

        for gm in re.finditer(r"<(?:linear|radial)Gradient\b[^>]*>[\s\S]*?</(?:linear|radial)Gradient>", content, re.IGNORECASE):
            stops = re.findall(r"#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b", gm.group(0))
            chroma = [hs[0] for hx in stops for hs in (self._hex_hue_sat(hx),) if hs and hs[1] >= 0.25]
            if len(chroma) >= 2 and self._circular_hue_span(chroma) >= 18:
                ln = line_offset + content[:gm.start()].count("\n")
                violations.append(TellViolation(
                    rule_id="CLR-TEL-01", category="Warna", severity="ERROR",
                    message="Chromatic multi-hue SVG gradient detected (CLR-001)",
                    remedy="Gunakan permukaan solid netral atau pergeseran nada satu hue.",
                    file_path=fp_str, line_number=ln, snippet=gm.group(0).splitlines()[0].strip()[:87],
                ))

        rect_dims = []
        for rm in re.finditer(r"<rect\b[^>]*>", content, re.IGNORECASE):
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
                violations.append(TellViolation(
                    rule_id="LAY-TEL-08", category="Tata Letak", severity="ERROR",
                    message=f"Symmetrical {count}-card strip inside SVG ({top_dim[0]}x{top_dim[1]}, rx={top_dim[2]}) (LAY-017)",
                    remedy="Ganti strip kartu identik dengan komposisi asimetris atau fokus tunggal.",
                    file_path=fp_str, line_number=line_offset, snippet=f"{count}x rect {top_dim[0]}x{top_dim[1]} rx={top_dim[2]}",
                ))
        return violations

    def scan_file(self, file_path: Path) -> List[TellViolation]:
        violations: List[TellViolation] = []
        if file_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            return violations
        if "design-md" in file_path.parts:
            return violations

        try:
            raw_content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return violations

        is_md = file_path.suffix.lower() == ".md"
        content = self._strip_block_comments(raw_content, keep_examples=is_md)
        if file_path.suffix.lower() == ".svg":
            return self._scan_svg(file_path, content, inline=False, line_offset=1, doc_text=content)

        lines = content.splitlines()
        balanced_css_classes = self._balanced_css_classes(content)
        has_reduced_motion = bool(re.search(r"@media\s*\([^)]*prefers-reduced-motion|useReducedMotion|motion-reduce:", content, re.IGNORECASE))
        in_code_block = False
        in_bad_example = False
        seen_keys = set()

        def _add_v(rule_id, category, severity, msg, remedy, ln, snip):
            key = (rule_id, ln)
            if key in seen_keys:
                return
            seen_keys.add(key)
            s = snip.strip()
            if len(s) > 90:
                s = s[:87] + "..."
            violations.append(TellViolation(
                rule_id=rule_id, category=category, message=msg, severity=severity,
                file_path=str(file_path), line_number=ln, snippet=s, remedy=remedy,
            ))

        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            if "<!-- maxilun-example:bad -->" in stripped:
                in_bad_example = True
                continue
            if "<!-- /maxilun-example:bad -->" in stripped:
                in_bad_example = False
                continue
            if is_md:
                if stripped.startswith("```"):
                    in_code_block = not in_code_block
                    continue
                if not in_code_block or in_bad_example:
                    continue
            elif in_bad_example:
                continue

            for rule_id, category, severity, msg, remedy, pattern in self.TELL_RULES:
                if file_path.name in ("ui-purity-linter.py", "purity-catalog.md", "SKILL.md") and "TELL_RULES" in line:
                    continue
                if rule_id == "ANI-TEL-03" and has_reduced_motion:
                    continue
                if rule_id == "ANI-TEL-01" and "interpolate-size" in content:
                    continue
                match = pattern.search(line)
                if match:
                    if rule_id == "TYP-TEL-06":
                        htag_m = re.match(r"<(h[1-3])\b[^>]*class(?:Name)?=[\"']([^\"']*)[\"']", match.group(0), re.IGNORECASE)
                        if htag_m:
                            elem_classes = set(htag_m.group(2).split()) | {htag_m.group(1).lower()}
                            if elem_classes & balanced_css_classes:
                                continue
                    _add_v(rule_id, category, severity, msg, remedy, idx, line)

        # Inline <svg> and multiline JSX/HTML tag checks for non-Markdown files
        if not is_md:
            for svg_m in re.finditer(r"<svg\b[\s\S]*?</svg>", content, re.IGNORECASE):
                ln = content[:svg_m.start()].count("\n") + 1
                for sv in self._scan_svg(file_path, svg_m.group(0), inline=True, line_offset=ln, doc_text=content):
                    _add_v(sv.rule_id, sv.category, sv.severity, sv.message, sv.remedy, sv.line_number, sv.snippet)

            # Flatten multiline opening HTML/JSX tags (<tag\n ... >) to single lines for rule parity.
            for tag_m in re.finditer(r"<(?:button|a|input|span|div|p|h[1-4])\b[^>]*\n[^>]*>(?:[^<]{0,200}</(?:button|a|h[1-4]|p|span)>)?", content, re.IGNORECASE):
                ln = content[:tag_m.start()].count("\n") + 1
                flat = re.sub(r"\s*\n\s*", " ", tag_m.group(0))
                for rule_id, category, severity, msg, remedy, pattern in self.TELL_RULES:
                    if rule_id in ("ANI-TEL-03", "ANI-TEL-01"):
                        continue
                    if pattern.search(flat):
                        _add_v(rule_id, category, severity, msg, remedy, ln, flat)

        # Multi-line checks for split JSX/HTML elements
        if not is_md:
            multiline_pill = re.search(
                r"""(?:rounded-full[^"']*\b(?:px-[2-6]|py-[0-3])|\b(?:px-[2-6]|py-[0-3])\b[^"']*rounded-full)[^"']*["'][^>]*>[\s\S]{0,180}?(?:<span[^>]*bg-(?:emerald|green|indigo|cyan)-500|•|\*|&bull;)[\s\S]{0,180}?(?:[A-Z0-9_\/-]{4,}\s*\/\/\s*[A-Z0-9_\/-]{4,}|STANDAR|MULTI-TENANT|SAAS)""",
                content, re.IGNORECASE
            )
            if multiline_pill:
                ln = content[:multiline_pill.start()].count("\n") + 1
                if not any(v.rule_id == "CMP-TEL-01" for v in violations):
                    snippet = multiline_pill.group(0).replace("\n", " ").strip()
                    if len(snippet) > 90:
                        snippet = snippet[:87] + "..."
                    violations.append(TellViolation(
                        rule_id="CMP-TEL-01",
                        category="Komponen",
                        severity="ERROR",
                        message="Floating pill badge with glowing dot stamped above heading",
                        remedy="Hapus kapsul dekoratif; integrasikan konteks langsung ke dalam judul atau navigasi.",
                        file_path=str(file_path),
                        line_number=ln,
                        snippet=snippet
                    ))

            multiline_hero = re.search(
                r"""text-center[^\n]*mx-auto[\s\S]{0,400}?rounded-full[\s\S]{0,400}?<h1""",
                content, re.IGNORECASE
            )
            if multiline_hero:
                ln = content[:multiline_hero.start()].count("\n") + 1
                if not any(v.rule_id == "LAY-TEL-09" for v in violations):
                    snippet = multiline_hero.group(0).replace("\n", " ").strip()
                    if len(snippet) > 90:
                        snippet = snippet[:87] + "..."
                    violations.append(TellViolation(
                        rule_id="LAY-TEL-09",
                        category="Tata Letak",
                        severity="ERROR",
                        message="Centered hero stack with floating capsule badge (LAY-018)",
                        remedy="Terapkan tata letak start-aligned editorial atau split hero dengan working console artifact.",
                        file_path=str(file_path),
                        line_number=ln,
                        snippet=snippet
                    ))

        # Multiline checks for Symmetrical 4/5 KPI Card Strip across parent/child nodes (LAY-017)
        if not is_md:
            for m_kpi in re.finditer(r"""\b(?:md:|lg:|xl:)?grid-cols-(?:4|5)\b[\s\S]{0,650}""", content, re.IGNORECASE):
                window = m_kpi.group(0)
                if not re.search(r"""\bcol-span-(?:2|3|4|5|6|7|8)\b""", window):
                    if len(re.findall(r"""\brounded-(?:lg|xl|2xl|3xl)\b""", window)) >= 2:
                        ln = content[:m_kpi.start()].count("\n") + 1
                        if not any(v.rule_id == "LAY-TEL-08" for v in violations):
                            snippet = window.splitlines()[0].strip()[:87]
                            violations.append(TellViolation(
                                rule_id="LAY-TEL-08",
                                category="Tata Letak",
                                severity="ERROR",
                                message="Symmetrical 4 or 5 KPI card strip without role differentiation (LAY-017)",
                                remedy="Urutkan konten: satu yang paling penting memimpin, sisanya jadi baris ledger yang tenang, tabel, atau master-detail.",
                                file_path=str(file_path),
                                line_number=ln,
                                snippet=snippet
                            ))
                        break

        return violations

    def scan_path(self, target_path: Path) -> ScanResult:
        result = ScanResult()
        files_to_scan: List[Path] = []

        if target_path.is_file():
            if "design-md" not in target_path.parts:
                files_to_scan.append(target_path)
        elif target_path.is_dir():
            for root, dirs, files in os.walk(target_path):
                # Ignore node_modules, .git, venv, build, fixtures, and design-md reference archive
                dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "venv", ".venv", "build", "dist", ".next", "__pycache__", "design-md", "fixtures")]
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

    def fix_file(self, file_path: Path) -> Tuple[bool, List[str]]:
        """
        Automatically remediates common high-confidence AI purity violations:
        - Replaces raw decorative emojis with clean SVG or text.
        - Converts heading rainbow gradients to solid text.
        - Fixes raw hex background #06090e to OKLCH tokens.
        - Strips fake glowing dot bullets in capsule pills.
        """
        fixes_applied = []
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            return False, fixes_applied

        original = content

        # 1. Fix gradients in headings/text
        gradient_pat = re.compile(
            r'\b(?:bg-clip-text\s+text-transparent|text-transparent\s+bg-clip-text)\s+bg-gradient-to-[a-z0-9-]+\s+from-[a-z0-9-]+\s+to-[a-z0-9-]+(?:\s+via-[a-z0-9-]+)?',
            re.IGNORECASE
        )
        if gradient_pat.search(content):
            content = gradient_pat.sub('text-foreground font-semibold', content)
            fixes_applied.append("Replaced AI rainbow text-gradient with solid text")

        # 2. Fix decorative emojis in spans or inline headings without gluing adjacent words
        emoji_chars = r'(?:[\U0001F300-\U0001FAFF]|[\u2600-\u27BF]|[\u2300-\u23FF]|[\u2B50\u2B55]|🚀|✨|🔥|💡|🎉|⭐|👉|💎|🌟|🤖|💬|🏫|🎓|🕒)'
        emoji_span_pat = re.compile(
            rf'<(?:span|badge|div|p|h[1-6]|button)[^>]*>\s*{emoji_chars}+\s*</(?:span|badge|div|p|h[1-6]|button)>|[ \t]*{emoji_chars}+[ \t]*',
            re.UNICODE,
        )
        if emoji_span_pat.search(content):
            def _clean_emoji(m: re.Match) -> str:
                txt = m.group(0)
                return "" if txt.startswith("<") else (" " if txt.startswith((" ", "\t")) and txt.endswith((" ", "\t")) else "")
            content = emoji_span_pat.sub(_clean_emoji, content)
            fixes_applied.append("Removed decorative emojis")
        # 3. Replace checkmark / cross emojis with clean SVG icons
        cls_attr = "className" if file_path.suffix.lower() in (".tsx", ".jsx") else "class"
        if '✅' in content:
            svg_check = f'<svg {cls_attr}="w-4 h-4 text-emerald-500 inline-block align-middle" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>'
            content = content.replace('✅', svg_check)
            fixes_applied.append("Replaced emoji ✅ with monochrome SVG checkmark")

        if '❌' in content:
            svg_cross = f'<svg {cls_attr}="w-4 h-4 text-red-500 inline-block align-middle" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>'
            content = content.replace('❌', svg_cross)
            fixes_applied.append("Replaced emoji ❌ with monochrome SVG cross")

        # 4. Replace raw hex background #06090e with var(--canvas)
        if '#06090e' in content.lower():
            content = re.sub(r'#06090e', 'var(--canvas, oklch(0.12 0.008 250))', content, flags=re.IGNORECASE)
            fixes_applied.append("Replaced raw hex #06090e with OKLCH token var(--canvas)")

        # 5. Fix floating pill badge with glowing dot pattern
        pill_pat = re.compile(
            r'(<span[^>]*class=["\'][^"\']*\brounded-full\b[^"\']*["\'][^>]*>)\s*(?:•|\*|&bull;)\s*',
            re.IGNORECASE
        )
        if pill_pat.search(content):
            content = pill_pat.sub(r'\1', content)
            fixes_applied.append("Removed fake glowing dot bullet in capsule pill")

        if content != original:
            file_path.write_text(content, encoding="utf-8")
            return True, fixes_applied

        return False, fixes_applied

    def fix_path(self, target_path: Path) -> Dict[str, Any]:
        files_to_fix: List[Path] = []
        if target_path.is_file():
            if "design-md" not in target_path.parts:
                files_to_fix.append(target_path)
        elif target_path.is_dir():
            for root, dirs, files in os.walk(target_path):
                dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "venv", ".venv", "build", "dist", ".next", "__pycache__", "design-md", "fixtures")]
                for f in files:
                    p = Path(root) / f
                    if p.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                        files_to_fix.append(p)

        fixed_count = 0
        details = {}
        for f in files_to_fix:
            modified, fixes = self.fix_file(f)
            if modified:
                fixed_count += 1
                details[str(f)] = fixes

        return {
            "total_files": len(files_to_fix),
            "fixed_files": fixed_count,
            "details": details
        }


def format_report(result: ScanResult, verbose: bool = False) -> str:
    status_icon = "[PASS]" if result.passed else "[FAIL]"
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
    """Self-test validating that the tell rules (web + SVG) work deterministically."""
    print("Running UIPurityLinter self-test on synthetic test cases...")
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

    bad_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 400">
      <defs><linearGradient id="g"><stop stop-color="#22d3ee"/><stop stop-color="#a855f7"/></linearGradient></defs>
      <text x="40" y="80" font-family="Inter, sans-serif" font-weight="800" fill="url(#g)">🚀 Banner</text>
      <rect x="40" y="140" width="240" height="120" rx="12"/>
      <rect x="300" y="140" width="240" height="120" rx="12"/>
      <rect x="560" y="140" width="240" height="120" rx="12"/>
      <rect x="820" y="140" width="240" height="120" rx="12"/>
    </svg>"""
    with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False, encoding="utf-8") as f:
        f.write(bad_svg)
        temp_bad_svg = Path(f.name)

    good_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 420" role="img" aria-labelledby="t d">
      <title id="t">System ledger</title>
      <desc id="d">Deterministic engineering diagram</desc>
      <rect width="1280" height="420" fill="#090d16"/>
      <rect x="48" y="48" width="640" height="324" rx="8" fill="#101624" stroke="#232d42"/>
      <text x="80" y="120" font-family="'Instrument Sans', system-ui, sans-serif" font-weight="700" font-size="36" fill="#f8fafc">System Architecture</text>
    </svg>"""
    with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False, encoding="utf-8") as f:
        f.write(good_svg)
        temp_good_svg = Path(f.name)

    try:
        bad_res = linter.scan_path(temp_bad)
        good_res = linter.scan_path(temp_good)
        bad_svg_res = linter.scan_path(temp_bad_svg)
        good_svg_res = linter.scan_path(temp_good_svg)

        assert len(bad_res.violations) >= 5, f"Expected >=5 violations on bad sample, got {len(bad_res.violations)}"
        assert not bad_res.passed, "Bad sample should fail purity check"
        assert len(good_res.violations) == 0, f"Expected 0 violations on good sample, got {len(good_res.violations)}"
        assert good_res.passed, "Good sample should pass purity check"
        assert not bad_svg_res.passed and len(bad_svg_res.violations) >= 3, (
            f"Expected >=3 violations on bad SVG, got {len(bad_svg_res.violations)}"
        )
        assert good_svg_res.passed and len(good_svg_res.violations) == 0, (
            f"Expected 0 violations on clean SVG, got {good_svg_res.violations}"
        )
        print(f"  [PASS] Caught {len(bad_res.violations)} tells in bad sample (Score: {bad_res.score:.1f}/100)")
        print(f"  [PASS] Clean sample passed perfectly (Score: {good_res.score:.1f}/100)")
        print(f"  [PASS] SVG bad failed ({len(bad_svg_res.violations)} tells); SVG clean passed")
        print("  Self-test passed successfully.")
        return True
    finally:
        for tmp in (temp_bad, temp_good, temp_bad_svg, temp_good_svg):
            if tmp.exists():
                tmp.unlink()


def main():
    parser = argparse.ArgumentParser(description="Maxilun UI Purity Linter — 45 AI Design Tells Scanner", allow_abbrev=False)
    parser.add_argument("target", nargs="?", default=".", help="Target file or directory to scan")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--strict", action="store_true", help="Fail if any warning or error is found")
    parser.add_argument("--fix", action="store_true", help="Automatically remediate detected purity violations where safe")
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
    if args.fix:
        fix_res = linter.fix_path(target_path)
        if not args.json:
            print(f"Purity Auto-Fixer: Remediated {fix_res['fixed_files']} / {fix_res['total_files']} files.")
            for fp, fixes in fix_res['details'].items():
                print(f"   - {Path(fp).name}: {', '.join(fixes)}")
            print()

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
