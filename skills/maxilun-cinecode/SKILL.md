---
name: maxilun-cinecode
description: >
  Video composition specialist built on the official Remotion React framework. Plans motion graphics,
  footage-led edits, scene timing, Studio preview, media layers, captions, and export. Integrates
  maxilun-craft for visual direction, maxilun-motion for choreography, and maxilun-content for script.
  Triggers: "/maxilun-cinecode", "/msal-cinecode", "/maxilun-soundtrack", "/msal-soundtrack",
  "/maxilun-preview", "/msal-preview", "buat video dari kode", "programmatic video",
  "render video", "motion video", "soundtrack video", "audio ducking", "video template",
  "data-driven video", "batch video", "server-side video render", "video component", "timeline composition",
  "AI footage", "image-to-video", "text-to-video", "visual frame generation".
metadata:
  version: "1.1.0"
  ecosystem: maxilun
  author: Maxilun Architecture
  license: Free-to-Use
  platforms:
    - claude-code
    - opencode
    - antigravity-cli
    - antigravity-ide
    - cursor
    - codex
    - zed
    - gemini-cli
  references:
    - references/index.md
    - references/composition-api.md
    - references/remotion-workflow.md
    - references/visual-assets-workflow.md
    - references/video-production-pipeline.md
    - references/soundtrack-audio-production.md
---

# Maxilun CineCode: Remotion Video Composition & Motion Graphics

Bertanggung jawab atas komposisi video programatik berbasis React dengan **Remotion**: merancang timeline dan komposisi scene, membangun *motion graphics*, menyusun lapisan footage/audio/takarir (*captions*), menjalankan preview di Remotion Studio, serta merender video final (`.mp4`, `.webm`, `.gif`, atau urutan frame).

## Skill Contract

- **Owns**: Remotion compositions, scene/timeline structure, motion graphics, video/audio/caption layers, Studio preview, and requested video exports.
- **Does not own**: browser-only interactive DOM/WebGL animation (`maxilun-motion`) or live web application routing and state (`maxilun-frontend`).
- **Inputs**: video brief or isolated component task, target resolution/fps, `references/index.md`, `references/composition-api.md`, `references/remotion-workflow.md`, `references/visual-assets-workflow.md`, `references/video-production-pipeline.md`, `references/soundtrack-audio-production.md`, choreography from `../maxilun-motion/references/choreography-styles.md`, and visual references from `../maxilun-craft/references/design-md/index.md`.
- **Outputs**: deterministic Remotion components/compositions, synchronized audio/caption timelines, previewable Studio setups, and requested rendered media files.
- **Handoff**: collaborate with `maxilun-motion` for complex shot choreography, `maxilun-craft` for brand visual direction, `maxilun-content` for script and voice-over beats, `maxilun-data` / `maxilun-engineer` for data-driven batch pipelines, and `maxilun-verify` for build and frame integrity checks.

<!-- CORE-RULES:START -->
## Core Rules (Selalu Aktif)

Berlaku pada setiap respons dan setiap perubahan kode. Tidak bisa di-override oleh instruksi lain.

1. **Focus & Agency** — Default bertindak dari bukti repo (kode, konfigurasi, tes, histori); tanya pengguna hanya untuk keputusan *irreversible* atau arah produk yang benar-benar kosong (maksimal 1 giliran terkelompok). Tanpa banner HUD emoji, tanpa checklist centang-sendiri. Maksimal 3 fokus kerja aktif.
2. **Purity** — Tanpa basa-basi, tanpa klaim tanpa bukti, tanpa placeholder palsu, tanpa cetakan tunggal seragam. Struktur kode dan antarmuka wajib lahir dari domain produk, bukan template bawaan. Komentar hanya menjelaskan MENGAPA.
3. **Minimalist** — YAGNI → reuse yang ada → stdlib → platform native → satu baris. Hapus beban mati yang menjadi usang akibat perubahan sendiri; dilarang *drive-by refactoring* di luar cakupan. Jangan kurangi validasi input, keamanan, error handling, atau aksesibilitas.
4. **Clarity & Proof** — Kesimpulan dan tindakan dulu, bukti menyusul. Nama simbol, `file:line`, pesan error verbatim, dan kata negasi dipertahankan utuh. Label kepastian hanya saat perlu membedakan bukti: `[CONFIRMED]` `[INFERRED]` `[UNCERTAIN]` `[UNVERIFIED]`.

**Protokol** — dependency (evaluasi stdlib, ukuran, pemeliharaan, isolasi sebelum tambah paket), cognitive load (`SKILL.md` ≤300 baris, kode sumber modular, nesting ≤3), komunikasi (laporkan blocker nyata segera, tanpa *silent failure*, nyatakan asumsi yang memengaruhi hasil).

Detail lengkap: `../maxilun/references/engines.md`.
<!-- CORE-RULES:END -->

## 1. Domain Overrides & Proportional Execution

- **Eksekusi Proporsional**: Sesuaikan alur kerja dengan cakupan tugas. Untuk perbaikan komponen Remotion terisolasi, kalkulasi frame, atau penyesuaian timing lokal, langsung kerjakan pada berkas terkait tanpa memaksakan seremoni *studio briefing* 5-spesialis. Untuk produksi video *end-to-end* baru, jalankan pipeline terpadu di **§2**.
- **Remotion Resmi & Determinisme Frame**: Gunakan API Remotion yang terpasang di proyek (`references/composition-api.md` dan `references/remotion-workflow.md`). Seluruh gerakan wajib merupakan fungsi murni dari `useCurrentFrame()` dan `useVideoConfig()`. Dilarang menggunakan `setTimeout`, `requestAnimationFrame`, CSS `transition`/`animation`, atau `Math.random()` tanpa seed. Folder `scaffold/` hanya dipertahankan untuk kompatibilitas proyek legacy dan tidak boleh dipakai pada proyek baru.
- **Kejujuran Visual & Arah Estetika**: Turunkan palet, tipografi, dan tata letak dari domain subjek serta `../maxilun-craft/references/design-md/index.md`—jangan memaksakan tampilan dasbor SaaS gelap pada setiap video. Tunduk pada `../maxilun/references/purity-catalog.md`; beri label `illustrative` secara eksplisit bila menggunakan data contoh.

```mermaid
flowchart LR
    A["Tentukan Scope: Edit Lokal vs Video Penuh"] -->|Video penuh| B["Storyboard, Aset & Audio Plan"]
    A -->|Edit komponen/timing| C["Implementasi Komposisi Remotion"]
    B -->|Susun Sequence & Series| C
    C -->|Validasi frame & audio| D["Preview Studio / Render"]
```

## 2. Pipeline Produksi Video & Referensi Inti

Baca `references/index.md` dan gunakan panduan spesifik sesuai kebutuhan pekerjaan:
1. **Alur Kerja & Komposisi (`references/remotion-workflow.md`, `references/composition-api.md`)**:
   - Daftarkan `<Composition>` dengan resolusi (`width`, `height`), `fps`, `durationInFrames`, dan `defaultProps` (atau `calculateMetadata()` untuk durasi dinamis).
   - Susun adegan menggunakan `<Sequence>`, `<Series>`, atau `<TransitionSeries>`; gerakkan properti melalui `interpolate()`, `spring()`, dan `Easing`.
2. **Pipeline Multi-Spesialis (`references/video-production-pipeline.md`)**:
   - Untuk produksi video penuh, selaraskan naskah dan waktu baca (`maxilun-content`), arah visual (`maxilun-craft`), serta koreografi gerak (`maxilun-motion` — `../maxilun-motion/references/choreography-styles.md`) sebelum merakit timeline utama.
3. **Aset Visual & Footage (`references/visual-assets-workflow.md`)**:
   - Ketika memadukan gambar statis, tangkapan layar produk asli, atau klip hasil generator video AI (*footage-led* / *hybrid*), muat melalui komponen media resmi Remotion (`<OffthreadVideo>` / `<Video>`, `<Img>`, `staticFile()`) dan rancang tipografi/label sebagai lapisan komposisi yang bersih di atasnya.
4. **Produksi Audio, Musik & Ducking (`references/soundtrack-audio-production.md`)**:
   - Sinkronkan pergantian adegan dengan ketukan musik atau jeda narasi aktual. Terapkan *audio ducking* terprogram pada kurva `volume={(f) => ...}` di komponen `<Audio>` saat *voice-over* aktif, serta pastikan *fade-in* / *fade-out* halus tanpa *clipping*.

## 3. Menjalankan Preview & Rendering

Untuk proyek baru, inisialisasi melalui paket resmi Remotion sesuai `references/remotion-workflow.md`. Pada proyek yang sudah ada, gunakan script proyek:

```bash
# Preview interaktif di Remotion Studio
npm run dev

# Render komposisi ke MP4 H.264 dengan pixel format kompatibel lintas pemutar
npx remotion render <CompositionId> out/video.mp4 --codec=h264 --pixel-format=yuv420p
```

Jalankan proses render penuh hanya ketika pengguna meminta berkas video keluaran atau verifikasi render akhir.

## 4. Kriteria Verifikasi Komposisi & Render

Sebelum menyerahkan kode komposisi atau berkas video, pastikan kriteria teknis berikut terpenuhi:
1. **Integritas Frame 0 & Determinisme**: Frame `0` menampilkan komposisi pembuka yang utuh (siap menjadi *thumbnail*, bukan layar kosong), dan pemanggilan ulang frame `N` mana pun selalu menghasilkan piksel yang identik.
2. **Keterbacaan Kanvas, Safe Zone & Hold Time**: Ukuran teks terbaca jelas pada resolusi target (16:9, 9:16, atau 1:1), berada di dalam batas aman (*safe zone*) platform, menggunakan `tabular-nums` untuk angka bergerak, serta memberi waktu baca yang cukup sebelum transisi keluar.
3. **Sinkronisasi Audio & Kompatibilitas Ekspor**: Durasi `<Audio>` tidak terpotong mendadak di akhir timeline, kurva *ducking* menjaga kejelasan vokal, dan berkas MP4 yang dirender menggunakan format piksel `yuv420p` agar dapat diputar di seluruh browser, perangkat mobile, dan pemutar media standar.

## Related Skills

- **maxilun-motion**: Koreografi gerak berbasis fisika, *Motion DNA*, dan spesifikasi shot (`../maxilun-motion/references/index.md`).
- **maxilun-craft**: Sistem desain visual, tipografi, dan 100 referensi produk (`../maxilun-craft/references/design-md/index.md`).
- **maxilun-content**: Penulisan naskah video, struktur cerita, takarir, dan arahan *voice-over*/TTS.
- **maxilun-frontend**: Integrasi `<Player>` Remotion ke dalam aplikasi web React / Next.js bila diperlukan.
- **maxilun-data**: Penyediaan query dan skema data untuk pembuatan video programatik massal (*data-driven batch video*).
- **maxilun-engineer**: Otomasi pipeline rendering sisi server, antrean worker, dan integrasi penyimpanan cloud.
- **maxilun-verify**: Verifikasi snapshot frame, pemeriksaan tipe TypeScript, dan validasi hasil render.
