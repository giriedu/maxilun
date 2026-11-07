# Maxilun Game References Index

Indeks pustaka arsitektur game studio, rekayasa multi-engine (Godot, Unity, Unreal Engine), perancangan gameplay, dan siklus hidup produksi game.

## Berkas Referensi Domain

1. **`game-design-lifecycle.md`**:
   Struktur standar 8 bagian Game Design Document (GDD), perumusan matematis balancing ekonomi dan combat, formula mitigasi damage, time-to-kill (TTK), metodologi prototyping dan vertical slice, serta anggaran frame rate (CPU/GPU/draw calls).

2. **`godot-playbook.md`**:
   Rekayasa Godot 4.x: GDScript 2.0 static typing, kelas dan method `@abstract`, variadic arguments, semantik lambda capture-by-value, custom Resources data-driven, integrasi modul C++ via GDExtension, 3D Jolt Physics, shader pipeline, MultiplayerAPI, dan pengujian otomasi gdUnit4 dengan pencegahan orphan nodes.

3. **`unity-playbook.md`**:
   Rekayasa modern Unity 6 LTS: arsitektur data-oriented DOTS/ECS (`ISystem` Burst-compatible, `IComponentData`, `SystemAPI.Query`), manajemen memori Addressables asinkron, Netcode for GameObjects (NGO) replication, Universal Render Pipeline (URP), New Input System, dan pengujian NUnit PlayMode/EditMode.

4. **`unreal-engine-playbook.md`**:
   Rekayasa Unreal Engine 5.x: standar C++20, smart pointer `TObjectPtr<T>`, siklus hidup memori `UPROPERTY()`, Gameplay Ability System (GAS) berbasis Gameplay Tags, Enhanced Input Mapping Contexts, Nanite virtualized geometry, Lumen GI, Chaos physics substepping, authoritative netcode replication, dan pengujian Unreal Automation Tool.

## Panduan Pemuatan Berkas
Muat berkas spesifik hanya saat domain tugas menyentuh mesin atau fase terkait:
- Perancangan GDD, balancing ekonomi/combat, atau pembagian sprint game → baca `references/game-design-lifecycle.md`.
- Proyek berbasis Godot Engine (GDScript/GDExtension/gdUnit4) → baca `references/godot-playbook.md`.
- Proyek berbasis Unity (C#/DOTS/URP/Addressables) → baca `references/unity-playbook.md`.
- Proyek berbasis Unreal Engine (C++/Blueprint/GAS/Replication) → baca `references/unreal-engine-playbook.md`.
