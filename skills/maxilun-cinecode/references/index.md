# CineCode Reference Index

`maxilun-cinecode` uses the official Remotion React framework for new video projects. Its own guidance layers Maxilun's brief, art direction, motion choreography, and factuality requirements on top of Remotion's APIs and Agent Skills.

| Reference | Purpose | When to read |
|---|---|---|
| `remotion-workflow.md` | Project setup, official skill routing, preview-first production, storyboard, export boundary, licensing reminder | Every new video project or significant video edit |
| `visual-assets-workflow.md` | Original Maxilun process for still/footage briefs, continuity, asset review, and compositing | When creating or sourcing visual assets or footage |
| `composition-api.md` | Remotion `Composition`, `Sequence`, frame-driven animation, media, assets, Studio, and render orientation | Before writing or changing Remotion compositions |
| `video-production-pipeline.md` | Brief, production mode, art direction, shot list, motion-graphics quality and factuality gates | Complete promo, demo, explainer, or data-storytelling work |
| `soundtrack-audio-production.md` | Audio planning, score direction, narration, mix and timing | When the brief includes music, voice-over, or audio treatment |
| `../maxilun-motion/references/choreography-styles.md` | Motion language, signature catalog, and frame choreography concepts | When a video needs authored motion direction |
| `../maxilun-craft/references/design-md/index.md` | Brand and visual-system references | When supplied brand tokens/references do not cover the brief |

## Framework boundary

- The `scaffold/` folder at this skill path is a legacy Maxilun frame renderer. Do not use it for a new video project.
- New projects use the official `create-video` starter or the Remotion project already present in the target workspace.
- Remotion is source-available under a proprietary license. See `remotion-workflow.md` and the current official license terms for eligibility.
- Remotion composes and renders code-defined media. AI video footage must come from a separate generator or user-provided assets, then be edited and overlaid in Remotion.
