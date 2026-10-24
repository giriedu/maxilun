# Maxilun Purity Catalog

<!-- metadata:
  version: "1.0.0"
  last_updated: "2026-10-22"
  sync_target: "scripts/test-suite.py:BANNED_BUZZWORDS"
  origin: "Maxilun Purity Engine"
  enhancement: "Documented Review Checklist + Contextual Critique Checks"
-->

Katalog penolakan pola generik (*Purity Catalog*) yang mengikat seluruh skill Maxilun. Tiga domain: **Konten/Teks**, **Desain Website**, dan **Teknis**. Aturan ini menjadi panduan review agent; repository ini tidak menyertakan executable detector untuk daftar di bawah. Setiap temuan harus dinilai dalam konteks sebelum dihapus atau diganti.

> **Sinkronisasi Test Suite**: Daftar kata terlarang di bawah ini terikat langsung dengan `BANNED_BUZZWORDS` di `scripts/test-suite.py`. Setiap penambahan kosakata terlarang baru wajib diperbarui serentak di dokumen ini dan di test suite untuk menjaga kepatuhan CI.

> **Maxilun Purity Engine**: Katalog ini menetapkan heuristik review kualitas konten, desain, dan kode berbasis konteks. Daftar ini adalah panduan review agen, bukan klaim jumlah rule yang dijalankan oleh pemindai biner otomatis.

---

## A. Pola Klise Generik pada Konten & Teks

Konten wajib ditulis ulang bila memenuhi salah satu kriteria di bawah (menolak jika ≥1 cocok):

1. **Generik tanpa jangkar** — bisa berlaku untuk topik apa pun tanpa berubah. Wajib ada entitas spesifik (nama produk, angka, audiens, kasus).
2. **Panjang, poin sedikit** — banyak kata, sedikit informasi. Rasio: setiap kalimat harus menambah satu fakta/keputusan baru, jika tidak, hapus.
3. **Judul heboh, isi dangkal** — klaim superlatif di judul tanpa bukti di badan. Judul dilarang menjanjikan lebih dari yang dibuktikan isi.
4. **Tanpa data/sumber/contoh/sudut pandang** — wajib ada minimal satu: angka nyata, sumber tertaut, contoh konkret, atau posisi yang jelas. Jika tidak tersedia, nyatakan eksplisit ("data belum tersedia"), jangan dikarang.
5. **Daftar Kosakata Terlarang Kanonik (Banned Vocabulary)** — kata/frasa AI buzzword yang dilarang keras digunakan dalam konteks positif:
   - Bahasa Inggris: `delve`, `tapestry`, `synergy`, `holistic`, `leverage`, `seamlessly`, `robust`, `cutting-edge`, `game-changer`, `revolutionary`, `supercharge`, `dive in`, `elevate`, `empower`, `unlock`, `transformative`, `next-level`, `state-of-the-art`, `best-in-class`, `paradigm shift`.
   - Padanan Bahasa Indonesia: `menyelami`, `merajut harmoni`, `sinergi`, `holistik`, `memanfaatkan secara mulus`, `solusi mutakhir/terdepan`, `pengubah permainan`, `revolusioner`, `meningkatkan ke level berikutnya`, `mari selami`, `memberdayakan`, `membuka potensi`, `transformatif`, `kelas dunia`, `pergeseran paradigma`.
6. **Frasa template pamungkas** — larangan frasa klise: *"Revolutionize Your Workflow"*, *"Unlock Your Potential"*, *"Di era digital yang serba cepat"*, *"Solusi all-in-one terpercaya"*, *"Elevate your experience"*, *"Empowering innovation"*.
7. **Tidak menjawab kebutuhan pembaca** — setiap paragraf harus menjawab pertanyaan nyata pembaca sasaran. Konten yang bercerita tentang diri sendiri tanpa manfaat pembaca ditolak.

### Gerbang Konten (Content Gate)
Sebelum menyerahkan teks, jawab 3 pertanyaan; satu gagal = tulis ulang:
- Bisakah kalimat ini dipakai di topik lain tanpa perubahan? (jika ya → generik, gagal)
- Adakah satu fakta/angka/contoh nyata di dalamnya? (jika tidak → gagal)
- Apakah ini menjawab kebutuhan pembaca spesifik? (jika tidak → gagal)

---

## B. Pola Klise Visual pada Desain Website (Visual Anti-Patterns)

Setiap elemen berikut dilarang ditambahkan tanpa fungsi nyata. Jika muncul tanpa alasan desain, hapus.

### B1. Typography & Font Issues
1. **Overused fonts** — Arial, Inter, Roboto, system defaults tanpa modifikasi. Wajib custom typeface atau minimal font pairing yang disengaja.
2. **Gray text on colored backgrounds** — teks abu-abu (#666, #888) di atas background berwarna. Kontras wajib ≥4.5:1 dengan tinted colors.
3. **Pure black/gray without tint** — #000000, #333333, #666666 murni. Selalu tint ke brand hue (oklch recommended).
4. **Inconsistent font sizes** — lebih dari 5 size variants tanpa modular scale. Wajib type scale (1.250 atau 1.333 ratio).
5. **Line length violations** — body text >75ch atau <45ch. Optimal: 60-70ch untuk readability.
6. **Missing font smoothing** — tidak ada `-webkit-font-smoothing: antialiased` untuk light-on-dark themes.

### B2. Color & Gradient Issues
7. **Purple-to-blue gradients everywhere** — gradien #667eea→#764ba2 atau serupa sebagai default AI aesthetic. Gradien hanya untuk semantic meaning.
8. **Rainbow/multi-color chaos** — >3 hue families tanpa sistem warna. Wajib OKLCH/HSL color system dengan ≤3 base hues.
9. **Low contrast text** — rasio kontras <4.5:1 (AA) atau <7:1 (AAA). Test dengan automated tools.
10. **Color-only status indicators** — status conveyed by color alone tanpa icon/text label. Redundant cues wajib.
11. **Dark mode afterthought** — dark mode ditambahkan belakangan tanpa token system. Wajib design tokens dari awal.
12. **Saturated backgrounds** — background dengan chroma >0.1 di OKLCH. Backgrounds should be subtle (chroma ≤0.05).

### B3. Layout & Spacing Issues
13. **Card nesting overload** — cards within cards within cards. Max 2 levels of containment.
14. **Everything in cards** — plain text wrapped in card containers tanpa grouping need. Cards only for discrete units.
15. **Inconsistent spacing** — padding/margin values tidak mengikuti spatial scale (4px/8px grid). Wajib design token spacing.
16. **Cramped touch targets** — interactive elements <44x44px di mobile, <24x24px di desktop. WCAG 2.2 minimum.
17. **Whitespace as filler** — large empty spaces tanpa rhythm/hierarchy purpose. Whitespace marks grouping, not fills pages.
18. **Grid misalignment** — elements tidak snap ke baseline/grid. Optical alignment ±1px acceptable, random placement tidak.
19. **Overflow issues** — horizontal scroll unintended, text truncation tanpa ellipsis, content clipping.

### B4. Component & Pattern Issues
20. **Breadcrumb Navigation (AI-Generated Web Tell — DILARANG DEFAULT)** — `Home > Section > Page` atau `Dashboard / Settings / Profile` di bagian atas halaman adalah salah satu sinyal terkuat bahwa sebuah website di-generate oleh template AI. **DILARANG merender komponen breadcrumb secara default** pada landing page, SaaS dashboard, form, login/register, 404, maupun aplikasi web modern. Gunakan navigasi kembali kontekstual (`← Kembali ke Daftar Tagihan`), command palette (`Cmd+K`), atau tab/header langsung. Pengecualian hanya jika pengguna secara eksplisit meminta breadcrumb untuk katalog e-commerce/dokumentasi bersarang `>= 4` level.
21. **Badge inflation** — badges labeled "Powerful", "AI-Powered", "New" tanpa factual basis. Badges only for status (version, count, state).
22. **Emoji as icons** — emoji menggantikan professional icon set. Icons wajib dari satu family (Lucide, Phosphor, etc.) dengan consistent weight.
23. **Uniform border radius** — semua elements rounded sama (e.g., all 8px). Nested radii: child ≤ parent, concentric hierarchy.
24. **Hero cliché** — bombastic headline + generic subtitle + dual CTAs tanpa clear primary. One primary CTA; hero explains value, not sensation.
25. **Fake statistics** — "99.9% Accuracy", "10k+ happy users" tanpa source. Numbers require citation or deletion.
26. **Decorative components** — buttons/tabs/dropdowns/search that don't function. If non-functional, don't render.
27. **Tab bar bloat** — >5 tabs di mobile nav. Mobile tab bars: 3-5 items max dengan icons + labels.
28. **Modal abuse** — modals untuk content yang bisa inline. Modals only for interrupts requiring focus.
29. **Login page decoration** — gradient backgrounds, floating shapes, fake product screenshots, marketing copy, atau testimonials pada halaman login/register. Login page fokus pada form functionality, bukan visual impressiveness. Background boleh textured/subtle tapi tidak boleh mengganggu readability form.
30. **Generic menu names** — sidebar/nav menggunakan "Dashboard", "Settings", "Profile", "Admin" tanpa konteks produk. Menu names wajib mencerminkan struktur informasi aktual: "Patient Records" bukan "Dashboard", "Notification Preferences" bukan "Settings", "Clinic Profile" bukan "Profile".

### B5. Animation & Motion Issues
29. **Animation overload** — glow, floating, parallax, hover effects tanpa functional purpose. Motion clarifies cause-effect only.
30. **Bounce/elastic easing** — cubic-bezier dengan overshoot (bounce, elastic) terasa dated. Use spring physics or ease-out.
31. **Layout property animation** — animating top/left/width/height causes reflow. Only animate transform + opacity.
32. **Non-interruptible animations** — animations yang tidak bisa di-cancel oleh user input. All motion must be interruptible.
33. **Autoplay without control** — auto-playing animations/media tanpa pause control. User must control timing.
34. **Missing reduced-motion** — tidak ada `@media (prefers-reduced-motion: reduce)` variant. Required for accessibility.
35. **Flash/seizure triggers** — >3 flashes per second, rapid strobing. WCAG 2.3.1 compliance mandatory.

### B6. Visual Hierarchy & Clarity
36. **Shadow overdose** — shadows on every card/button/section. Layered shadows (ambient + direct) only for elevated elements.
37. **Glassmorphism stacking** — multiple frosted glass layers bertumpuk. Max 1 glass layer per view.
38. **Dark glow borders** — glowing borders di semua interactive elements. Borders should be subtle, glows reserved for focus states.
39. **Side-tab borders** — vertical tabs dengan heavy left borders. Use subtle indicators, not thick borders.
40. **Icon inconsistency** — mixing emoji, SVG, different icon families. One set, one style, one stroke width.
41. **Generic UI text** — "Click here", "Learn more", "Submit" tanpa context. Labels must be specific ("Download report", "Save profile").
42. **Template layout** — structure identical to thousands of AI sites. Structure follows content needs, not default patterns.

### Visual Gate Checklist
Prinsip tunggal: **jangan menambahkan elemen hanya agar terlihat canggih.** Setiap komponen wajib punya:
1. Fungsi nyata
2. Alasan desain yang documented
3. Relevansi terhadap kebutuhan pengguna

Jika salah satu absen → hapus. No exceptions.

---

## C. Documented Quality Checks (Agent-Assisted Review)

Gunakan ID berikut untuk menyebut temuan secara konsisten. Nilai source, preview, dan konteks produk; jangan menyatakan pemeriksaan otomatis lulus atau gagal. Tidak ada CLI, pre-commit hook, CI job, waiver parser, atau auto-fix yang disediakan katalog ini.

### C1. Typography Checks
| ID | Check | Severity | Suggested action |
|----|------|----------|----------|
| TYPO-001 | Overused font family detected (Arial, Inter, Roboto, system-ui) | ERROR | ❌ |
| TYPO-002 | Gray text (#666, #888, #999) on colored background | ERROR | ✅ Suggest tinted alternative |
| TYPO-003 | Pure black (#000000) or pure gray without hue tint | WARNING | ✅ Apply brand hue tint |
| TYPO-004 | Body text line length >75ch or <45ch | WARNING | ❌ |
| TYPO-005 | More than 5 font size variants without scale | ERROR | ❌ |
| TYPO-006 | Missing font-smoothing for light-on-dark | WARNING | ✅ Add antialiased |
| TYPO-007 | Font size <16px on mobile inputs | ERROR | ✅ Set min 16px |

### C2. Color & Contrast Checks
| ID | Check | Severity | Suggested action |
|----|------|----------|----------|
| CLR-001 | Purple-to-blue gradient (#667eea→#764ba2 pattern) | ERROR | ❌ |
| CLR-002 | Text contrast ratio <4.5:1 (WCAG AA) | ERROR | ✅ Suggest compliant color |
| CLR-003 | Text contrast ratio <7:1 (WCAG AAA for body) | WARNING | ✅ Suggest compliant color |
| CLR-004 | Status indicator using color only (no icon/text) | ERROR | ❌ |
| CLR-005 | Background chroma >0.1 in OKLCH | WARNING | ✅ Reduce saturation |
| CLR-006 | More than 3 hue families without system | ERROR | ❌ |
| CLR-007 | Dark mode without color-scheme: dark | ERROR | ✅ Add declaration |

### C3. Layout & Spacing Checks
| ID | Check | Severity | Suggested action |
|----|------|----------|----------|
| LAY-001 | Card nesting >2 levels deep | WARNING | ❌ |
| LAY-002 | Plain text wrapped in card container | WARNING | ❌ |
| LAY-003 | Spacing value not in spatial scale (4px grid) | ERROR | ✅ Snap to nearest |
| LAY-004 | Touch target <44x44px (mobile) or <24x24px (desktop) | ERROR | ✅ Expand hit area |
| LAY-005 | Horizontal overflow detected (overflow-x: hidden hack) | ERROR | ❌ |
| LAY-006 | Element misaligned from baseline grid >2px | WARNING | ❌ |
| LAY-007 | Text truncation without ellipsis/title attribute | WARNING | ✅ Add overflow handling |

### C4. Component Checks
| ID | Check | Severity | Suggested action |
|----|------|----------|----------|
| CMP-001 | Breadcrumb rendered by default (strong AI-generated website tell; use contextual back link `← Back to [Parent]` instead) | ERROR | ❌ Remove breadcrumb |
| CMP-002 | Badge with marketing adjective ("Powerful", "New") | ERROR | ❌ |
| CMP-003 | Emoji used as functional icon | ERROR | ✅ Replace with icon component |
| CMP-004 | Uniform border-radius across all elements | WARNING | ❌ |
| CMP-005 | Non-functional interactive element (button/link without action) | ERROR | ❌ |
| CMP-006 | Modal for content displayable inline | WARNING | ❌ |
| CMP-007 | Tab bar with >5 items (mobile) | ERROR | ❌ |
| CMP-008 | Login/register page with decorative gradient background | WARNING | ❌ |
| CMP-009 | Login/register page with marketing copy or testimonials | ERROR | ❌ |
| CMP-010 | Generic menu name ("Dashboard", "Settings", "Profile") without product context | WARNING | ❌ |
| CMP-011 | `Home > ...` or `Dashboard / ...` trail on landing, app, auth, or dashboard screen | ERROR | ❌ Remove breadcrumb |

### C5. Animation & Performance Checks
| ID | Check | Severity | Suggested action |
|----|------|----------|----------|
| ANI-001 | Bounce/elastic easing detected | WARNING | ✅ Suggest spring/ease-out |
| ANI-002 | Animating layout properties (top/left/width/height) | ERROR | ✅ Convert to transform |
| ANI-003 | Missing prefers-reduced-motion media query | ERROR | ✅ Add fallback |
| ANI-004 | Flash rate >3Hz (seizure risk) | ERROR | ❌ |
| ANI-005 | Autoplay media without pause control | ERROR | ❌ |
| ANI-006 | transition: all (performance anti-pattern) | WARNING | ✅ List specific properties |
| ANI-007 | Animation duration >1000ms for micro-interactions | WARNING | ✅ Cap at 300ms |

### C6. Accessibility Checks
| ID | Check | Severity | Suggested action |
|----|------|----------|----------|
| A11Y-001 | Interactive element missing accessible name | ERROR | ❌ |
| A11Y-002 | Image without alt text or aria-label | ERROR | ❌ |
| A11Y-003 | Form input without associated label | ERROR | ✅ Wrap with label |
| A11Y-004 | Focus outline removed without replacement | ERROR | ✅ Add :focus-visible |
| A11Y-005 | Heading hierarchy skip (h1→h3 without h2) | WARNING | ❌ |
| A11Y-006 | Link text "click here" or "read more" without context | WARNING | ✅ Make descriptive |
| A11Y-007 | Color contrast fail in :hover/:focus states | ERROR | ✅ Increase contrast |

### Example Configuration Shape (Not Read by This Repository)
```json
{
  "detector": {
    "enabled": true,
    "failOnSeverity": "ERROR",
    "ignoreRules": ["TYPO-003"],
    "ignoreFiles": ["legacy/**", "vendor/**"],
    "ignoreValues": {
      "CLR-001": ["brand-gradient-primary"]
    },
    "designSystem": {
      "enabled": true,
      "tokenPath": ".maxilun/design-tokens.json"
    }
  }
}
```

### Example Waiver Comments (Not Parsed Automatically)
Komentar berikut hanya mendokumentasikan alasan pengecualian bagi reviewer:
```css
/* maxilun-disable CLR-001: brand identity requires this gradient */
.hero-background {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* maxilun-disable-next-line TYPO-002 */
.caption { color: #888; } /* intentional muted style for decorative element */
```

---

## D. Contextual Critique Checks

Checks ini memerlukan human/AI judgment dan harus dilaporkan sebagai review, bukan hasil pemindaian:

1. **Emotional resonance** — Does the design evoke appropriate feeling for brand/audience?
2. **Cultural appropriateness** — Are symbols/colors/language appropriate for target locale?
3. **Brand consistency** — Does visual language align with established brand DNA?
4. **Information hierarchy clarity** — Can user scan and understand priority in <3 seconds?
5. **Cognitive load assessment** — Is complexity justified by task requirements?
6. **Delight vs distraction balance** — Do moments of joy enhance or detract from goals?
7. **Contextual relevance** — Does design serve specific use case, not generic template?
8. **Long-term maintainability** — Can team extend this system without breaking coherence?

### Critique Workflow
Minta review melalui skill `/maxilun-craft critique <target>` saat tersedia. Ini adalah instruksi untuk agent, bukan executable CLI.

---

## E. Uji Akhir (Pre-Submit Self-Check)

Sebelum menyerahkan hasil konten atau UI, jawab cepat:
- Terasa dibuat untuk **algoritma** atau untuk **manusia**? Jika demi algoritma → tulis ulang.
- Adakah satu elemen yang bisa dihapus tanpa kehilangan informasi/fungsi? Jika ada → hapus.
- Apakah semua temuan severity ERROR sudah diperbaiki atau dijustifikasi?
- Apakah LLM critique checks menunjukkan no critical issues?

### Pre-Submit Review
Minta agent meninjau source/preview, rangkum temuan dengan ID, severity, lokasi, alasan, dan usulan perubahan. Perbaikan hanya diterapkan setelah diminta pengguna.

---

## F. Integration dengan Maxilun Ecosystem

### Token System Binding
Review checklist may be compared manually against `.maxilun/design-tokens.json` when that file exists:
- Spacing values checked against defined spatial scale
- Colors validated against semantic color system
- Typography checked against modular scale
- Border radius validated against nested hierarchy rules

### Automation Status
Repository ini belum menyediakan audit executable, CI workflow, atau file-save hook untuk katalog ini. Jangan menambahkan konfigurasi yang memanggil `scripts/audit.js` sebelum tool tersebut benar-benar tersedia.
