# Auto-Clip Pipeline: Long Footage to Platform-Ready Shorts

<!-- metadata:
  version: "1.3.0"
  sync_target: "skills/maxilun-cinecode/SKILL.md"
  origin: "Maxilun CineCode Engine"
-->

Decision rules for turning one long recording (interview, podcast, talk, stream) into several short, captioned, reframed, platform-specific clips with covers and post copy, while keeping model cost, wall-clock time, and local CPU load bounded. It complements `video-production-pipeline.md` (authored motion graphics) by covering the footage-led, transcript-driven case.

---

## 1. Boundary and Tool Choice

| Situation | Primary tool | Why |
|---|---|---|
| Cut, reframe, burn captions, normalize audio on existing footage | FFmpeg filter graph | Native, no browser, one decode per clip, cheapest per output |
| Authored overlays (animated title, lower third, progress bar, end card) on a clip | Remotion composition with the clip as footage layer | Frame-driven overlays, Studio review, typed props per clip |
| Batch of hundreds of clips with identical packaging | FFmpeg for the cut plus one pre-rendered alpha overlay per template | Browser capture per clip multiplies cost without visual gain |

- Do not start a browser render for a job FFmpeg alone can finish. Reach for Remotion only when the packaging needs authored motion.
- Discovery (which moments deserve a clip) and packaging (how a chosen moment is shaped for a destination) are separate modules with separate inputs. A platform preset must never influence which moment is selected, only how it is cut, framed, and dressed.

## 2. Stage Graph and Artifacts

```
ingest -> transcript -> chunk -> discover -> snap boundaries -> score + select
       -> reframe -> caption -> package (title, cover, copy) -> render -> QA -> export
```

1. Every stage writes a durable artifact (JSON, SRT, media) keyed by project and stage. A rerun resumes from the first missing or invalidated artifact.
2. Cache raw model responses per chunk, then always replay them through the same parser and validator used for live responses. A cached response that fails validation marks the chunk failed; it is never a silent licence to make a new paid call.
3. Each stage emits a small report of counts and stable codes only (`input`, `output`, `dropped`, `merged`, `fallback`). No transcript text, keys, or paths in reports, so they can be shared for diagnosis.
4. Keep stable clip IDs assigned at discovery. Later stages re-rank but never renumber, so UI state, caches, and user edits survive a rerun.

## 3. Transcript First

- Prefer captions the source already carries (author-uploaded or platform captions). They skip transcription time and cost entirely. Treat auto-generated platform captions as ASR quality, not author quality.
- When transcribing, choose local ASR (zero marginal cost, CPU-bound, slow on long audio) or cloud ASR (billed by audio duration, parallel upload, fast). Expose the choice; do not hide a paid path behind a default.
- Require word-level timestamps when the engine offers them. Row-level cues are enough for discovery, but boundary QA (Section 14) needs word edges.
- Normalize every cue to `(start_sec, end_sec, text)` floats once, sorted, empty rows removed. All later stages work in seconds, never in formatted timestamp strings.

## 4. Chunking and Candidate Discovery

1. Split the transcript into chunks by character budget, cutting only on cue boundaries. Size chunks so a chunk plus instructions fits the model context with room for the response; smaller chunks raise call count, larger chunks raise per-call latency and parse failure blast radius.
2. Process chunks in parallel with a bounded pool, then merge results in chunk order. Determinism of the merged list matters more than throughput.
3. Ask the model to quote cue timestamps or cue indices for each candidate, never to compute times. Validate every returned range: it must lie inside the chunk's time span, have `start < end`, and match an existing cue edge within a small tolerance.
4. On a parse or validation failure, retry with a corrective instruction a bounded number of times. Transport retries already happen inside the client; do not nest a second retry loop that multiplies the request budget.
5. Prefer one discovery call that returns topic, range, and a draft title together over a chain of sequential calls per topic. Fewer round trips is the largest single latency win in this pipeline.

## 5. Duration Profile from Source Length

Clip length targets should scale with the source. A ten-minute talk cannot yield the same count or length as a three-hour podcast. Derive a profile once from total duration and append it to every discovery prompt as the authoritative parameter block, so it overrides any fixed numbers in the base prompt.

| Source length | Min clip | Target band | Hard max | Candidates kept |
|---|---|---|---|---|
| Under 10 min | 15 s | 25-75 s | 120 s | 2-5 |
| 10-45 min | 30 s | 45-150 s | 240 s | 3-8 |
| Over 45 min | 45 s | 60-240 s | 360 s | scales with hours, capped |

These are Maxilun starting points, chosen so a short clip still completes one idea (roughly one question and its answer) and a long-source clip stays under typical short-form hard caps after trimming. Tune them from a regression set of real sources, and record why each change was made.

## 6. Boundary Snapping

Model-proposed ranges land on cue edges, and cue edges are often half sentences. Snap every range before scoring:

1. **Start**: move back to the start of the sentence that contains the proposed start, but no further than a lead limit (about 15-20 s). If the clip opens on an answer, include the question that prompted it when it fits inside the lead limit.
2. **End**: move forward to the sentence end that finishes the running thought, within a tail limit (about 20-25 s). If a cue contains a sentence end in its middle, cut inside the cue at that offset, estimating time proportionally across the cue's characters.
3. **Unpunctuated transcripts** (common for some ASR languages): treat a silence gap of roughly 0.5-0.7 s, or an explicit speaker-turn marker, as a sentence end.
4. **Trailing question**: if a new question starts near the end and only a short stub of its answer follows, end before that question. It belongs to the next clip.
5. **Optional model refinement**: show the model the rows around each cut and let it choose a better start or end. Validate the choice against the same rules; anything outside the allowed extension or not on a sentence edge falls back to the deterministic result.
6. Merge two candidates when they overlap by more than half of the shorter one; extend or drop candidates below the profile minimum.

## 7. Scoring and Selection

- Score on a rubric the model can apply from text: hook in the first seconds, self-contained (no unresolved references to earlier context), concrete payoff, specificity, emotional or surprising beat. Ask for a 0-1 score plus a one-line reason per candidate.
- Send the transcript excerpt of the snapped range with each candidate, not only the topic label; scores from labels alone reward good titles, not good clips.
- Align returned scores by candidate ID, never by list position. Unmatched candidates get a recorded fallback score instead of dropping the whole batch.

```ts
type Scored = { id: string; startSec: number; score: number; selectedBy?: 'threshold' | 'fallback' };

function selectClips(items: Scored[], threshold: number, minKeep: number, maxKeep: number): Scored[] {
  const ranked = [...items].sort((a, b) => b.score - a.score);
  const picked = ranked.filter((c) => c.score >= threshold).map((c) => ({ ...c, selectedBy: 'threshold' as const }));
  for (const c of ranked) {
    if (picked.length >= minKeep) break;
    if (!picked.some((p) => p.id === c.id)) picked.push({ ...c, selectedBy: 'fallback' });
  }
  return picked.slice(0, maxKeep).sort((a, b) => a.startSec - b.startSec);
}
```

Mark fallback picks visibly in the UI. A user should know which clips cleared the bar and which were kept only to avoid an empty result.

## 8. Platform Presets

Keep one table as the single source of truth for every destination. Each preset carries canvas, layout mode, hard duration limit, recommended duration, caption style, cover size, and audience language.

| Destination class | Canvas | Default layout | Duration rule |
|---|---|---|---|
| Vertical short (Shorts, Reels, TikTok-style) | 1080x1920 | crop to speaker, fit when several people | Respect each platform's hard cap; YouTube Shorts is capped at 3 minutes |
| Note-style feed with 3:4 cards | 1080x1440 cover, 9:16 or 3:4 video | crop or fit | Recommended only |
| Landscape long-form | 1920x1080 | keep original framing | No trimming |

- **Hard limit vs recommendation**: a hard limit trims at a sentence boundary (Section 6 rules, applied backward). A recommended length is shown as guidance and is never enforced by cutting.
- Platform limits change. Store the date each limit was checked beside the table and re-verify before relying on it.
- Social UI overlays cover the top and bottom of vertical video; keep captions and titles inside the safe area defined in `video-production-pipeline.md`.

## 9. Reframing Landscape Footage to Vertical

1. Work per shot, not per clock tick. Detect hard cuts first (an FFmpeg scene-change score threshold around 0.3 is a common start), ignore "shots" shorter than about 0.4 s as flashes or transitions.
2. Inside each shot, sample about one frame per second and detect faces. Classify the shot:
   - one relevant face that fits the window: **crop** centered on it;
   - several people who must all stay visible, or only a turned-away listener: **fit** the whole frame over a blurred or tinted backdrop;
   - no usable face (slides, screen recordings, quote cards): **fit**.
3. When several faces are visible, follow the active speaker: speaker labels from the transcript first, mouth motion second. The back of a head is never the crop center.
4. Camera window motion: jump on a hard cut, ease when the speaker changes inside a shot, otherwise hold still. A window that oscillates reads as a glitch; a window that drifts reads as wobble.
5. Ship a lightweight face model on demand rather than in the base install; most users who only export landscape never need it.

## 10. Captions

- At most two lines per screen at the output size. Break lines at punctuation first, then at natural joints (before conjunctions, after particles), never mid-word.
- Measure width in display units: count a full-width CJK glyph as 1 and a Latin character as roughly 0.5-0.6. Pixel measurement with the real font is better when available.
- Do not end a line on a short function word (`a`, `the`, `of`, `to`, `and`) and do not start a line with closing punctuation.
- Share a cue's time across its screens in proportion to displayed width, so long screens stay up longer.
- Strip disfluencies (`uh`, `um`) and speaker-turn markers from burned text; keep them in the stored transcript.
- Always export a sidecar `.srt` or `.vtt` in addition to burned captions. Burned captions serve muted autoplay; the sidecar serves accessibility and platform indexing.
- When translating captions, translate cue-by-cue by index and reject any response that merges, splits, or adds cues.

## 11. Cover and Post Copy

- **Cover frame**: pick from frames where the subject's face is large, eyes open, mouth not mid-word, and not motion-blurred. A local heuristic (face size times sharpness) is a fine default; a vision model is an opt-in upgrade that needs the user's consent to send frames out.
- **Cover sizes** follow each destination's cover slot, not the video canvas: a 3:4 feed card, a 16:10 or 16:9 landscape thumbnail, a 9:16 vertical poster.
- **Title on cover**: reuse the clip title and the clip's palette so cover and video read as one package. Keep cover text short enough to read at thumbnail size.
- **Post copy**: generate title, description, and tags for every selected platform of a clip in one model call. Enforce per-platform rules (length caps, tag count, language) in code after the call; never trust the model to obey them. If copy is missing or malformed, fall back to the clip title so publishing is never blocked.
- Copy must not claim facts the transcript does not contain.

## 12. Cost and Latency Control for Cloud Models

| Control | Rule |
|---|---|
| Call count | Track calls per stage; collapsing sequential per-topic calls into per-chunk calls is the main lever |
| Per-chunk cap | A fixed ceiling on model calls per chunk across all retries, shared by retry and fallback paths |
| Job wall-clock budget | One budget per clip job covering every provider call; pause it during local CPU work (ASR, encode) so slow hardware is not mistaken for a slow provider |
| Error classes | Rate limit: back off, then try a same-provider fallback model. Quota or billing exhausted: stop and tell the user; never fall back silently to a different paid path |
| Usage ledger | Append tokens in/out, model, stage, and latency per call to a project-local log; derive cost from the ledger, not from estimates |
| Fallback order | Deterministic and documented; never ranked by commercial relationships |

- Show the user an estimated cost before the run and the measured cost after it.
- A balance or quota probe may run before paid calls, but it must fail open as `unavailable`, never block a run on a probe error, and never log balance values.

## 13. Render and Encode

1. Render each clip from an immutable snapshot of its draft (range, framing, captions, packaging), so a later edit cannot change a render already in flight.
2. One FFmpeg invocation per clip where possible: seek input, crop or fit, overlay, burn captions (ASS for styled captions), loudness-normalize, encode.

```bash
ffmpeg -ss 754.20 -to 821.90 -i source.mp4 \
  -filter_complex "[0:v]crop=ih*9/16:ih:x=640:y=0,scale=1080:1920,subtitles=clip.ass[v];[0:a]loudnorm=I=-14:TP=-1:LRA=11[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -pix_fmt yuv420p -preset medium -crf 20 -c:a aac -b:a 160k -movflags +faststart clip.mp4
```

3. Probe for a hardware encoder (NVENC, QSV, AMF, VideoToolbox) once per session; on any failure retry the clip with `libx264`. Never ship a partial file from a failed encode; delete it.
4. Authored overlays render once per template as an alpha intermediate (ProRes 4444 or another alpha codec) and are composited by FFmpeg, unless they depend on per-clip data, in which case render them per clip in Remotion.
5. Queue renders one at a time on desktop, cap FFmpeg thread counts, and lower process priority (`nice` on POSIX, below-normal priority class on Windows) so a batch does not freeze the user's machine.

## 14. Output QA Gate

Run these checks on every exported clip before it is marked ready:

- **Ending**: using word timestamps, fail when the clip end falls inside a word, or when the last word is not sentence-final and the next word starts within about 0.6 s.
- **Loudness**: integrated loudness near -14 LUFS with true peak at or below -1 dBTP, the common normalization target of major streaming and social platforms.
- **A/V sync**: cross-correlate sampled windows of output audio against the source at the mapped time. A container start-time match is not proof of sync. Keep the median offset well inside the commonly cited lip-sync detectability window (about 45 ms audio-early, 125 ms audio-late); a 40 ms gate is a safe default.
- **Framing stability**: fail on crop-window reversals (large jump undone within a second) and on residual jitter in shots that are not intentional pans.
- **Frame 0 and captions**: first frame is a usable thumbnail; no caption exceeds two lines or leaves the safe area.

## 15. Rejected Patterns

- Hard-coded duration rules inside prompts, patched later by appending overrides: keep durations in one profile object and render the prompt from it.
- Many coexisting versions of the same renderer or title-art module: keep one owner per capability and delete superseded versions.
- Provider fallback ranked by sponsorship: Maxilun ranks by capability and cost evidence only.
- Crash reporting or analytics on by default in a local-first tool: opt-in, with the scope written down.
- Emoji in captions, covers, or UI chrome as decoration.
