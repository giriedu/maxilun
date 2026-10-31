# Interactive 3D Scene Workflow

Read this reference when the requested deliverable is a navigable or interactive 3D environment in a website/app (immersive landing page, explorable product world, 3D portfolio, or interactive scene). For isolated 3D accents or ordinary UI motion, use the main motion references instead.

## 1. Establish the scene contract

Before implementation, turn the brief into a compact scene contract. Use repository evidence and user-provided assets first. Record:

- **Purpose and audience**: what the world explains or helps the visitor do.
- **Scene graph**: environment, zones, primary objects, repeated objects, and which details are real product features versus visual metaphors.
- **Camera choreography**: initial framing, navigation points, transition triggers, and a stable way back to the overview.
- **Interactions**: what each hotspot does, what information appears, and how the same actions work without a pointer.
- **Assets and loading**: available model/texture/audio files, asset ownership, expected loading states, and intentional placeholders.
- **Runtime constraints**: existing framework, supported browsers/devices, performance target, and required fallback.

For a large scene, implement a coherent first pass with the whole navigable environment and one working interaction per core mechanic. Do not silently drop named zones. If time/asset constraints require reducing detail, preserve the complete scene layout and disclose which details are simplified.

## 2. Select the runtime from the project

- Preserve an existing 3D renderer and its established conventions when possible.
- In a React project, prefer React Three Fiber when its installed React major is compatible; use direct Three.js when the project is not React or the existing architecture favors imperative scene ownership.
- Do not add a renderer, controls, post-processing, physics, or asset libraries just for appearance. For each proposed dependency, confirm it is needed, maintained, compatible with the project's versions, and worth its bundle/runtime cost.
- Before relying on library APIs or adding packages, consult current official documentation (Context7 where available; otherwise official docs) for the exact installed or proposed versions.
- Treat WebGPU as an optional path only when project/browser support and a useful fallback are established; WebGL remains the compatibility path when required by the brief.

## 3. Build the world, not a screenshot

For immersive or cinematic scenes, omit breadcrumb navigation and any eyebrow/kicker/overline/category label immediately above the hero H1 (such as `GATEWAY WHATSAPP · SELF-HOSTED`). Start the hero with its main heading. Keep headings as clear content titles, not breadcrumb-like trails. If visitors need orientation between zones, provide a distinct scene selector/index rather than adding a label above the hero or turning a heading into navigation.

Separate the scene into understandable components: environment, zones/chambers, lighting, camera/navigation, interaction targets, and scene state. Keep text, navigation, dialogs, forms, and critical actions in accessible DOM UI layered over the canvas. A mesh click must have an equivalent keyboard-operable control; expose selected/active state and useful labels.

Use provided models when available. Use procedural geometry for simple shapes, diagrams, or deliberate low-poly art direction. A temporary primitive is acceptable during implementation, but never present it as a finished branded model; identify it as a placeholder and state what asset is needed. Do not download or invent licensed assets. Keep simulated visual effects (particles, telemetry, connection flows) distinct from live backend data, and label sample metrics as illustrative.

Coordinate one primary camera movement at a time. Make scroll choreography navigable through explicit buttons/links too, support touch without requiring device orientation permission, and provide a stable overview/reduced-motion path. Avoid combining continuous orbit, tilt, shake, and scroll camera movement in ways that cause disorientation.

## 4. Loading, failure, motion and performance

- Show useful loading progress when measurable; otherwise show an honest indeterminate loader. Handle model load errors with a visible recovery path.
- Detect renderer/context failure and show a meaningful HTML/2D fallback that preserves the scene's key information and navigation. Do not leave an empty canvas.
- Respect `prefers-reduced-motion`: remove autoplay/scroll-driven camera travel and continuous ambient motion; keep the same content available through static framing and direct selection.
- Profile representative desktop and mobile conditions. Reduce pixel ratio, shadow resolution, post-processing, particle count, and model detail as needed; pause or use demand rendering when the scene is idle. Use instancing for repeated geometry when profiling shows draw-call pressure, cull unseen objects, and avoid React state updates or new allocations on every frame.
- Dispose listeners, animation loops, controls, and GPU resources when the scene unmounts or assets are replaced.
- Treat a frame-rate figure (for example 60 FPS) as a measured target on named hardware/browser, never as a universal guarantee. Report the device, browser, scene quality, and measured result when making a performance claim.

## 5. Completion evidence

A scene is ready for review when:

1. Every named zone is present and reachable through the navigation methods promised in the scene contract.
2. Every promised interaction works; UI text and actions remain usable by keyboard and touch.
3. Loading, error, unsupported-WebGL/context-loss, and reduced-motion paths have meaningful behavior.
4. Sample/simulated data is visibly distinguished from live data.
5. The scene has been opened and reviewed at desktop and mobile viewport sizes; performance claims include measurement evidence.

If browser preview or representative hardware is unavailable, state that visual/device behavior is unverified instead of claiming it passed.
