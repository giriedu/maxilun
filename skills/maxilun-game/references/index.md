# Maxilun Game References Index

Index of the reference library for game studio architecture, multi-engine engineering (Godot, Unity, Unreal Engine), gameplay design, and the game production lifecycle.

## Domain Reference Files

1. **`game-design-lifecycle.md`**:
   The standard 8-section Game Design Document (GDD) structure, mathematical formulation of economy and combat balancing, the damage mitigation formula, time-to-kill (TTK), prototyping and vertical slice methodology, and frame rate budgets (CPU/GPU/draw calls).

2. **`godot-playbook.md`**:
   Godot 4.x engineering: GDScript 2.0 static typing, `@abstract` classes and methods, variadic arguments, lambda capture-by-value semantics, data-driven custom Resources, C++ module integration through GDExtension, 3D Jolt Physics, the shader pipeline, MultiplayerAPI, and gdUnit4 automated testing with orphan node prevention.

3. **`unity-playbook.md`**:
   Modern Unity 6 LTS engineering: data-oriented DOTS/ECS architecture (Burst-compatible `ISystem`, `IComponentData`, `SystemAPI.Query`), asynchronous Addressables memory management, Netcode for GameObjects (NGO) replication, Universal Render Pipeline (URP), New Input System, and NUnit PlayMode/EditMode testing.

4. **`unreal-engine-playbook.md`**:
   Unreal Engine 5.x engineering: the C++20 standard, the `TObjectPtr<T>` smart pointer, the `UPROPERTY()` memory lifecycle, the Gameplay Ability System (GAS) based on Gameplay Tags, Enhanced Input Mapping Contexts, Nanite virtualized geometry, Lumen GI, Chaos physics substepping, authoritative netcode replication, and Unreal Automation Tool testing.

## File Loading Guide
Load a specific file only when the task domain touches the related engine or phase:
- GDD design, economy/combat balancing, or game sprint planning → read `references/game-design-lifecycle.md`.
- Godot Engine projects (GDScript/GDExtension/gdUnit4) → read `references/godot-playbook.md`.
- Unity projects (C#/DOTS/URP/Addressables) → read `references/unity-playbook.md`.
- Unreal Engine projects (C++/Blueprint/GAS/Replication) → read `references/unreal-engine-playbook.md`.
