# Remotion Workflow for Maxilun CineCode

Use Remotion itself as the video runtime. The old CineCode renderer under `scaffold/` is a legacy implementation; do not base new videos on its custom frame hooks, renderer, or encoder. Keep it only when maintaining an existing project that already depends on it.

## 1. Inspect and set up

1. Inspect the target folder, including hidden files. If it already contains a Remotion project, preserve its package manager, versions, entry points, and user changes.
2. If no video project exists and the target folder is empty, scaffold in that folder. If it contains meaningful files, scaffold into a new child folder. Never overwrite an existing project to make a Remotion project.
3. Use the official starter:

   ```bash
   npx create-video@latest --yes --blank --no-tailwind video-project
   cd video-project
   npm install
   npx remotion skills add
   npm run dev
   ```

   Adapt `./video-project` and package-manager commands to the workspace. If the CLI's skill installer is unavailable, use current official Remotion documentation and the official skills repository as references; do not invent framework APIs.
4. Check the applicable [Remotion license terms](https://www.remotion.dev/docs/license). Remotion is source-available with a proprietary license; eligibility depends on user and organization status.

## 2. Preview-first production

- Start Remotion Studio and open its exact local URL as soon as the project runs. Keep the preview available while building so the user can review progress.
- Register video compositions in the project's Remotion root using the official `<Composition>` API. Set the real `width`, `height`, `fps`, and `durationInFrames`; calculate metadata when duration or dimensions depend on input props.
- Build a storyboard and shot list before detailed scene code. For a timeline of media clips, represent independently editable clips as separate authored JSX elements.
- Use `<Sequence>`, `<Series>`, and `<TransitionSeries>` from the installed Remotion packages where appropriate. Child frame timing follows Remotion's official sequence semantics; do not add a parallel homegrown sequence clock.
- Use `useCurrentFrame()`, `useVideoConfig()`, `interpolate()`, `spring()`, and `Easing` from the installed Remotion version. Drive all rendered animation from the frame; avoid CSS transitions, timers, and runtime randomness.
- Use Remotion's media and asset components/helpers (`<Video>`/`<Audio>` from `@remotion/media`, `<Img>` and `staticFile()` from `remotion`, `delayRender()`/`continueRender()`) when their documented behavior fits. Check the installed version's official docs before using newer APIs.
- Build motion graphics as authored React/SVG/CSS layers with clear depth, timing, and visual hierarchy. Treat generated video as footage, then compose deliberate graphic overlays in Remotion; Remotion is the compositor, not the photoreal video generator.
- If generated artwork or footage is needed, follow `visual-assets-workflow.md`: define each shot and its continuity anchors, use only tools available in the user's environment, review every returned asset, then build the edit around usable media. Do not let a generator's default length or rhythm dictate the final edit.

## 3. Visual direction and review

1. Write the production brief, choose `motion graphics`, `footage-led / AI video`, or `hybrid`, and lay out each shot's purpose, subject, framing, action, camera move, transition, copy, audio, and duration.
2. Ground product screens, names, logos, and data in user-provided or verified assets. Label conceptual diagrams and sample data as `illustrative`.
3. Design for video, not a web page: one dominant read per shot, generous safe areas, hierarchy scaled to the output dimensions, and no redundant labels or decorative motion.
4. Use the Studio preview to inspect the opening, representative motion frames, transitions, and end frame. Watch the full timeline when the task is motion-led or footage-led; check continuity, typography, crop, overlays, pacing, and audio sync.
5. Do not render/export an MP4 by default. Render only when the user asks for the output file or when their request clearly includes exporting it.

## 4. Maxilun collaboration

- `maxilun-content`: short script beats and narration grounded in supplied facts.
- `maxilun-craft`: visual system and type/color decisions when brand direction is missing.
- `maxilun-motion`: shot choreography, motion grammar, and motion-graphics direction.
- `maxilun-cinecode`: Remotion composition, media timing, preview, and export.
- `maxilun-verify`: requested implementation checks and visual regression review.

The storyboard owns the creative decisions. Do not force a fixed number of scenes, a fixed hook, continuous motion, one of the preset signatures, or a metric chart into every brief.

## Official references

- [Remotion Agent Skills](https://www.remotion.dev/docs/ai/skills)
- [Remotion Best Practices skill source](https://github.com/remotion-dev/remotion/blob/main/packages/skills/skills/remotion-best-practices/SKILL.md)
- [Remotion Create skill source](https://github.com/remotion-dev/remotion/blob/main/packages/skills/skills/remotion-create/SKILL.md)
- [Create a project](https://www.remotion.dev/docs)
- [Core idea and compositions](https://www.remotion.dev/docs/idea)
- [Timing and trimming](https://www.remotion.dev/docs/timing)
- [Animating properties](https://www.remotion.dev/docs/animating-properties)
- [Rendering](https://www.remotion.dev/docs/render)
- [License](https://www.remotion.dev/docs/license)
