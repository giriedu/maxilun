---
name: maxilun-game
description: >
  Game studio systems, multi-engine architecture (Unreal Engine, Unity, Godot),
  gameplay engineering, physics & netcode, GDD specification, and production pipelines.
  Triggers: "/maxilun-game", "/maxilun-gamestudio", "game dev", "game engine",
  "godot", "unreal", "unity", "gdd", "game design", "gameplay", "game studio".
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
    - references/game-design-lifecycle.md
    - references/godot-playbook.md
    - references/unity-playbook.md
    - references/unreal-engine-playbook.md
---

# Maxilun Game: Game Studio & Multi-Engine Architecture Specialist

Bertanggung jawab atas arsitektur sistem game studio, rekayasa multi-engine (Godot GDScript/GDExtension, Unreal C++/GAS, Unity C#/DOTS), implementasi mekanik gameplay berbasis event, sinkronisasi fisika deterministik, authoritative netcode, spesifikasi Game Design Document (GDD), dan pengujian otomasi runtime game. Detail teknis dimuat hanya saat dibutuhkan dari `references/`.

## Skill Contract

- **Owns**: Logika game loop, arsitektur multi-engine (Godot GDScript/GDExtension, Unreal C++/GAS, Unity C#/DOTS), mekanik gameplay, sinkronisasi delta-time dan fisika deterministik, finite state machine dan behavior trees, netcode client-server authoritative dan replikasi, standar shader pipeline, spesifikasi Game Design Document (GDD) dan matriks balancing ekonomi, serta otomasi test game (gdUnit4, NUnit, Unreal Automation).
- **Does not own**: Desain visual antarmuka web atau aplikasi non-game (dimiliki `maxilun-craft` atau `maxilun-frontend`), video promosi render MP4/WebM (dimiliki `maxilun-cinecode`), atau deployment container cloud non-game (dimiliki `maxilun-deploy`).
- **Inputs**: Berkas konfigurasi mesin (project.godot, .uproject, ProjectSettings/), skrip gameplay (GDScript, C++, C#), shader (.gdshader, .shader, .usf), dokumen desain game (GDD/GDBrief), dan target platform atau anggaran frame rate.
- **Outputs**: Kode gameplay modular tanpa nilai hardcoded, sistem decoupled berbasis event/sinyal tanpa ketergantungan UI langsung, shader teroptimasi per target draw call, rumus balancing matematis yang terverifikasi, dan suite pengujian otomasi game yang lulus.
- **Handoff**: Tugaskan companion `maxilun-craft` jika mendesain HUD/UI game dan visual design token, `maxilun-motion` jika merancang koreografi kamera interaktif atau partikel 3D, atau `maxilun-verify` untuk validasi build target game runner.
- **Standalone mode**: Jika spesialis lain tidak tersedia, eksekusi kode game engine secara langsung dengan mematuhi Core Rules.
- **Public package rule**: Gunakan jalur relatif terhadap proyek atau skill terpasang.

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

## 1. Disiplin Rekayasa Gameplay & Arsitektur Game Loop

1. **Frame-Rate Independence**:
   - Seluruh translasi, rotasi, timer, dan kalkulasi fisika berbasis waktu wajib dikalikan dengan delta time (`delta` di Godot, `Time.deltaTime` di Unity, `DeltaTime` di Unreal).
2. **Data-Driven Decoupling**:
   - Nilai gameplay (base damage, walk speed, armor rating, drop rate) dilarang keras di-hardcode dalam skrip logika. Gunakan external data asset: Godot Resource (`.tres`), Unity `ScriptableObject`, atau Unreal `UDataAsset`.
3. **Pemisahan UI dan Komunikasi Berbasis Event**:
   - Kode gameplay dilarang memegang referensi langsung ke widget atau scene UI HUD. Gunakan event terisolasi (Godot signals, C# `event Action`, Unreal dynamic multicast delegates).
4. **Alokasi Memori Nol pada Game Loop**:
   - Hindari instansiasi dinamis (`new`, `instantiate()`, `SpawnActor()`) di dalam tick reguler. Terapkan pola object pooling untuk proyektil peluru, efek partikel, dan floating text.

## 2. Arsitektur Multi-Engine: Godot, Unity, & Unreal Engine

1. **Godot Engine 4.x**:
   - Terapkan static typing penuh pada GDScript 2.0. Waspadai semantik lambda capture-by-value saat menyambungkan callback sinyal.
   - Manfaatkan Jolt Physics 3D untuk determinisme tumbukan. Pisahkan logika komputasi berat ke modul GDExtension C++ (rujuk `references/godot-playbook.md`).
2. **Unity 6 LTS**:
   - Gunakan C# 9+ record struct untuk event data dan arsitektur data-oriented DOTS/ECS (`ISystem` Burst-compatible, `IComponentData`, `SystemAPI.Query`).
   - Kelola memori aset asinkron melalui Addressables. Gunakan Netcode for GameObjects (NGO) untuk sinkronisasi state jaringan multiplayer (rujuk `references/unity-playbook.md`).
3. **Unreal Engine 5.x**:
   - Gunakan standar C++20 modern dengan `TObjectPtr<T>` dan deklarasi `UPROPERTY()` yang disiplin untuk Garbage Collection.
   - Bangun arsitektur kemampuan berbasis Gameplay Ability System (GAS) dan tangani input melalui Enhanced Input System (rujuk `references/unreal-engine-playbook.md`).

## 3. Spesifikasi GDD & Model Balancing Matematika

1. **Struktur Standar 8 Bagian GDD**:
   - Setiap berkas desain mekanik wajib memuat: Overview, Player Fantasy, Detailed Rules, Formulas, Edge Cases, Dependencies, Tuning Knobs, dan Acceptance Criteria (rujuk `references/game-design-lifecycle.md`).
2. **Formula Mitigasi Kerusakan**:
   - Terapkan formula diminishing returns: $DamageTaken = RawDamage \times (\frac{K}{K + Armor})$ untuk menjamin penambahan Effective Health Pool (EHP) yang seimbang.
3. **Pacing Time-To-Kill (TTK) & Ekonomi Tertutup**:
   - Tetapkan anggaran TTK sesuai ritme genre. Pastikan setiap inflow mata uang diimbangi outflow sink yang proporsional untuk mencegah degradasi ekonomi game.

## 4. Standar Shader, Netcode Otoritatif, & Verifikasi Game

1. **Standar Pipeline Shader**:
   - Beri prefix tipe engine yang jelas (`spatial_` pada Godot, `SG_` pada Unity, `M_` pada Unreal).
   - Hindari dynamic branching di fragment shader; gunakan fungsi bawaan GPU (`step`, `smoothstep`, `mix` / `lerp`). Batasi sampling tekstur sesuai anggaran draw call platform.
2. **Authoritative Server & Client Prediction**:
   - Server berwenang penuh memvalidasi input, cooldown, dan status pemain. Klien menjalankan local prediction dengan rekonsiliasi rollback saat terjadi misprediction.
3. **Verifikasi Faktual**:
   - Jalankan otomasi pengujian mesin via CLI headless: gdUnit4 untuk Godot, NUnit untuk Unity, dan Unreal Automation Tool untuk Unreal.
   - Laporkan hasil dengan format `[CONFIRMED]` beserta berkas skrip dan baris yang diubah (`file:line`).

## Related Skills

- `maxilun-craft`: Desain visual HUD, tipografi display skor, layout inventaris, dan art direction UI game.
- `maxilun-motion`: Koreografi kamera dinamis, scene partikel 3D, dan transisi visual interaktif.
- `maxilun-verify`: Integrasi test runner otomasi game (gdUnit4, NUnit, Unreal Automation) ke CI pipeline.
