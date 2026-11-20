# Deterministic HTML Frame Rendering

<!-- metadata:
  version: "1.3.0"
  sync_target: "skills/maxilun-cinecode/SKILL.md"
  origin: "Maxilun CineCode Engine"
-->

How a browser page becomes a frame-exact video: the seek contract, time virtualization, readiness gates, media handling, capture, parallel workers, and encoding. Remotion stays the CineCode runtime; this reference explains the mechanics underneath any browser-based renderer so that third-party web animation can be embedded in a Remotion composition without drift, and so render failures can be diagnosed from first principles.

---

## 1. Boundary

- New CineCode videos use Remotion (`remotion-workflow.md`). Do not build a parallel homegrown capture renderer; the legacy `scaffold/` renderer stays legacy.
- Read this file when: a composition embeds a GSAP, Lottie, Web Animations, CSS keyframe, canvas, or WebGL animation authored outside React; preview and render disagree; a render is non-reproducible across runs or worker counts; or an encode fails on dimensions, color, or concatenation.
- The same rules apply whatever renderer captures the page. Remotion enforces them by making every value a function of `useCurrentFrame()`. A seek-driven HTML renderer enforces them by pausing every animation and moving it to an exact time before capture.

## 2. Seek, Never Play

A renderer never plays a page. For each output frame it computes a time, moves every animated thing to that time, waits for the page to settle, and captures.

| Contract item | Rule |
|---|---|
| Time base | `t = frame / fps`, computed from integers. For NTSC rates use the rational form (`30000/1001`), not `29.97` |
| Idempotent seek | Seeking to the same frame twice yields identical state |
| Order independence | Forward, backward, and random-order seeks all work; parallel workers depend on it |
| Settle before capture | Any async work a seek triggers resolves before the frame is captured; nothing resolves after |
| Finite length | Duration is known before frame 0 and never changes during the render |
| Locked geometry | `fps`, width, height, and input props are fixed before frame 0 |
| Lifecycle | `init` once, `seek` many times, `destroy` releases listeners, timers, GPU contexts |

A screen recorder that watches the wall clock drops frames when a frame is expensive. A seek-driven render never drops a frame; it only gets slower. Preview stutter is therefore not a render defect, but a render that differs from preview is.

## 3. Sources of Nondeterminism

| Source | Failure | Fix |
|---|---|---|
| `Date.now()`, `new Date()`, `performance.now()` | Output depends on render speed | Derive time from the frame; or virtualize (Section 4) |
| `requestAnimationFrame`, `setTimeout`, `setInterval` | Motion runs on wall time, differs per worker | Drive from frame; timers only for setup |
| `Math.random()`, `crypto.getRandomValues()` | Different layout every run | Seeded PRNG keyed by a stable seed, or Remotion `random(seed)` |
| CSS `transition` / running `@keyframes` | Captured mid-flight at arbitrary phase | Pause and set phase explicitly (Section 5) |
| Native `<video>` playback | Seek lands on the nearest decodable frame, not the requested one | Pre-extract frames (Section 7) |
| Network fetch after frame 0 | Missing asset in some frames | Load everything before the ready signal (Section 6) |
| Web fonts, lazy images | Fallback font or blank box on early frames | Readiness gate waits for fonts and decoded images |
| Locale, timezone, `prefers-reduced-motion`, device pixel ratio | Differs per machine | Pin them in the browser launch and the container |
| Tween values resolved on first render | Worker that starts mid-film computes a different start value | Make every worker replay frame 0 setup before its first frame |

## 4. Time Virtualization (When Code Cannot Be Rewritten)

When an embedded page reads the clock and cannot be rewritten to read the frame, replace the page's time sources before any of its scripts run:

1. Install a shim at document start that holds a single `virtualNowMs`. `Date.now`, `performance.now`, and argument-less `new Date()` return it.
2. Queue `requestAnimationFrame` callbacks and flush them once per seek with `virtualNowMs` as the timestamp.
3. Until the page reports ready, timers keep real time, because setup code may legitimately wait on them. After ready, timers register on film time; each seek fires every timer due up to the target time, in due order, setting `virtualNowMs` to each timer's due time as it fires.
4. A timer scheduled from inside a firing timer waits at least 1 ms of film time, so a zero-delay chain cannot spin forever inside one seek.
5. Reseed `Math.random` and `crypto.getRandomValues` from the seek time, so the same frame draws the same numbers on every run and every worker.
6. A worker whose first assigned frame is past zero performs a seek to frame 0 first, so setup-time timers and first-render values match a single-worker render.

Virtualization is a compatibility layer for foreign code, not an authoring style. Code written for CineCode reads the frame directly.

## 5. Driving Foreign Animation from a Remotion Frame

Every seekable runtime exposes a pause plus an absolute position setter. Drive it from `useCurrentFrame()` inside a layout effect so the DOM is updated before capture.

```tsx
import { useLayoutEffect, useRef } from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { gsap } from 'gsap';

export const SeekedReveal: React.FC<{ label: string }> = ({ label }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const root = useRef<HTMLDivElement>(null);
  const timeline = useRef<gsap.core.Timeline | null>(null);

  useLayoutEffect(() => {
    const ctx = gsap.context(() => {
      timeline.current = gsap
        .timeline({ paused: true })
        .from('.word', { yPercent: 110, stagger: 0.08, duration: 0.6, ease: 'power3.out' });
    }, root);
    return () => ctx.revert();
  }, []);

  useLayoutEffect(() => {
    timeline.current?.seek(frame / fps, false);
  }, [frame, fps]);

  return (
    <AbsoluteFill ref={root} style={{ justifyContent: 'center', alignItems: 'center', overflow: 'hidden' }}>
      {label.split(' ').map((w, i) => (
        <span key={i} className="word" style={{ display: 'inline-block', marginRight: '0.3em' }}>{w}</span>
      ))}
    </AbsoluteFill>
  );
};
```

| Runtime | Pause | Position at time `t` seconds |
|---|---|---|
| GSAP timeline | `paused: true` | `tl.seek(t, false)` (suppress events) |
| Web Animations API | `anim.pause()` | `anim.currentTime = t * 1000` |
| CSS `@keyframes` | `animation-play-state: paused` | `animation-delay: -${t}s` |
| Lottie | official Remotion Lottie package, or `goToAndStop(frame, true)` | frame index, not seconds |
| Canvas / WebGL loop | remove the loop | call the draw function with `t` |

Guard the seek with the timeline's own duration and let Remotion `<Sequence>` own the start offset; do not add a second clock.

## 6. Readiness Gate

Capture must not start until every input that frame 0 needs has settled.

- **Fonts**: wait for `document.fonts.ready`, then confirm the specific faces with `document.fonts.check('700 84px "Brand Sans"')`. A ready promise alone resolves before faces that were never requested.
- **Images**: `await img.decode()` for every image visible in the first scene; `complete` is not proof of decode.
- **Media**: video and audio at `HAVE_FUTURE_DATA` or after their first `seeked` event.
- **Data**: props and remote JSON resolved before render, through `calculateMetadata()` in Remotion, never fetched inside a frame.
- In Remotion, wrap any remaining async setup in `delayRender()` / `continueRender()` with a timeout and a label, so a hang names its cause.
- Scope readiness. A first-frame gate lets preview start sooner; a full gate is required before a final render. Never let a readiness timeout silently start capture; fail with the list of pending inputs.

## 7. Video Inside a Captured Page

A browser `<video>` cannot be seeked frame-exactly; it lands on a nearby keyframe-derived frame and decodes asynchronously. Frame-exact renderers therefore decode source footage outside the page and hand each output frame the exact source image. Remotion's `<OffthreadVideo>` follows this model; prefer it over a plain `<video>` for rendered output.

- Map output slot `k` of a clip that starts at source time `s` to source time `s + k / fps_out`. For variable-frame-rate sources, pick the source frame on screen at that time; do not count source frames.
- Normalize odd probed rates to their exact rational form before computing slots, so a 23.976 source does not accumulate a drift of one frame every few hundred.
- Cache decoded frames with a bound on both entry count and bytes. Large frames (4K PNG as data URIs reach tens of megabytes) must bypass the cache rather than thrash it.
- Audio is never captured from the page. The renderer reads declared audio and video sources, their in/out points, and volume curves, then mixes them with FFmpeg in a separate pass.

## 8. Capture Methods

| Method | Behavior | Use |
|---|---|---|
| Compositor-driven frame (headless `BeginFrame` control) | Page paints exactly when asked; one atomic frame | Default for deterministic headless capture when supported |
| Screenshot per frame | Works everywhere; full redraw of damaged tiles | Fallback; always correct, slower |
| In-page element raster | Fastest; captures one subtree | Only for frames proven safe; verify against a screenshot sample |

- Probe the fast path once at session start with a short timeout. Some software-rasterized pages with many promoted layers never return the first compositor frame; route those renders to screenshots instead of hanging.
- When a fast path cannot reproduce specific effects, scan which frames contain them and capture only those ranges by screenshot, padded by one frame and with nearby ranges joined so capture does not alternate modes every few frames. If risky frames exceed a large share of the film, screenshot everything.
- Set the device scale factor and viewport to the exact output size. Disable background throttling for hidden tabs. Request a transparent background only when the output codec carries alpha.
- GPU raster and software raster can differ by a few pixel values. Pick one per project and keep it for every render that must match.

## 9. Parallel Workers

1. Split the frame range into contiguous chunks, one per worker. Each worker is a full browser process.
2. Size worker count by available memory first and cores second. A capturing browser commonly uses well over half a gigabyte; budgeting by cores alone overcommits small machines and produces black or truncated frames under memory pressure.
3. Two ways to assemble output:
   - **Ordered stream**: workers write into a reorder buffer that releases frames to one encoder's stdin strictly in sequence (image pipe input). One encode, no seams.
   - **Chunk encode plus concat**: each worker encodes its own segment, then segments are concatenated with stream copy. This requires closed GOPs with keyframes forced on a fixed cadence that divides the chunk length; otherwise a seam lands on a frame that references the previous segment.

```bash
# per-chunk H.264 encode whose segments can be joined with -c copy
ffmpeg -f image2pipe -framerate 30 -i - \
  -c:v libx264 -pix_fmt yuv420p -g 60 -keyint_min 60 -sc_threshold 0 \
  -x264-params "scenecut=0:open-gop=0:repeat-headers=1" chunk_003.mp4
```

4. A correct render is worker-count invariant: 1 worker and N workers must produce identical frames (Section 12).

## 10. Encode Pipeline

- **Even dimensions**: 4:2:0 chroma (`yuv420p`) requires even width and height. Pad an odd dimension by one pixel (`pad=ceil(iw/2)*2:ceil(ih/2)*2`); never scale, which resamples every pixel.
- **Color**: browser screenshots arrive full-range RGB. Convert explicitly to limited-range BT.709 and tag the stream (`-colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv`) so players do not shift contrast.
- **Alpha**: H.264 has no alpha. Use ProRes 4444 (`yuva444p10le`) for editor interchange or VP9 with `yuva420p` in WebM for web playback.
- **Delivery**: `-movflags +faststart` for progressive web playback; AAC audio for MP4, Opus for WebM.
- **Intermediate frames**: JPEG frames are fast but lossy twice (capture plus encode). Use PNG for text-heavy or gradient-heavy work where banding and ringing show.
- **Hardware encoders**: probe once, fall back to software on failure, and do not mix hardware and software segments in one concatenated output.

## 11. Remote Assets and Reproducibility

- Download every remote video, audio, image, and font into the render's work directory before frame 0, with limits on file size, attempt duration, minimum throughput, and free disk space. Sniff downloaded files as real media containers before decoding them.
- No script or style loads from a CDN at render time. Vendor pinned versions into the project, or install them as locked dependencies.
- Pin the browser build, font set, and FFmpeg build in a container when bit-exact reproducibility matters. Fonts and browser versions differ across machines; a local render can move by a pixel.
- Write a provenance record beside each output: renderer version, browser version, FFmpeg version, encode arguments, input prop hash, and worker count.

## 12. Verification Gate

| Check | Pass condition |
|---|---|
| Repeatability | Two renders of the same input produce identical frame hashes, or PSNR above an agreed threshold where codec noise is expected |
| Worker invariance | 1-worker and N-worker renders match frame for frame |
| Random-order seek | Seeking frames in shuffled order and capturing yields the same frames as sequential order |
| Preview parity | Representative frames from Studio and the final render match |
| Readiness | Frame 0 shows final fonts, decoded images, and first video frame; no fallback glyphs |
| Encode | `ffprobe` confirms codec, pixel format, color tags, even dimensions, duration equal to `frames / fps` |

## 13. Remotion and a Seek-Driven HTML Renderer Compared

| Concern | Remotion | Seek-driven HTML renderer |
|---|---|---|
| Authoring unit | React component reading the frame | HTML page with paused timelines registered for seeking |
| Determinism enforced by | Author discipline: pure function of frame | Runtime pausing and seeking, plus time shims for stray clocks |
| Existing web animation | Wrap and seek it (Section 5) | Drops in close to as-is |
| Typed inputs and schema | Built in | Page variables; validation is separate work |
| Failure mode | Visible: a non-frame value fails review | Quiet: an unregistered timeline renders as a still |
| Licensing | Source-available; company-size terms apply | Varies; check each tool |

CineCode keeps Remotion as the runtime and borrows the seek model only to embed foreign animation. Switching renderers is a project decision driven by source material and licensing, not novelty.

## 14. Rejected Patterns

- Wall-clock screen recording of a playing page as a render method.
- Loading animation libraries from a CDN during render.
- A second timing system beside `<Sequence>` and `useCurrentFrame()`.
- Silent fallback from a failed readiness gate into capture.
- Telemetry in render tooling that is on by default; opt-in only.
