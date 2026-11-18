# Headless Blender (`bpy`) & Provable 3D Export Pipeline

Standards for `maxilun-motion` and `maxilun-ui-motion` when generating 3D assets, renders, or animations via headless Blender (`blender --background --python script.py`).

## 1. Deterministic `bpy` Scene Discipline
- Clear default scene (`bpy.ops.wm.read_factory_settings(use_empty=True)`) at script start.
- Pack PBR textures into ORM channels (R=AO, G=Roughness, B=Metallic) before GLB export to cut GPU VRAM.
- Set explicit render engine (`CYCLES` or `BLENDER_EEVEE_NEXT`), resolution, samples, and color management (`AgX` / `Standard`) in script rather than relying on user preferences.

## 2. Provable Output Verification (Never Trust File Size)
Every headless render or export must pass a deterministic verification check before reporting `[CONFIRMED]`:
- **PNG/WebP Render**: Verify non-zero dimensions and non-blank pixel variance (reject solid black/transparent frames).
- **GLB/glTF Export**: Verify magic header (`glTF`), valid JSON chunk, non-zero mesh/node count, and animation/skin presence when rigged.
- **MP4/Video Export**: Verify valid container header (`ftyp`) and non-zero frame/stream count via `ffprobe`.

