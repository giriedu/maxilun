# Cinematic Scriptwriting, Spoken Pacing & Google Cloud TTS Integration

Use this reference when writing a video narration script, directing vocal intonation, writing SSML annotations, or producing voice-over with Google Cloud Text-to-Speech for a `maxilun-cinecode` video.

---

## 1. Spoken Narration Philosophy: Write for the Ear, Not the Eye

Web copy is read with the eyes (scannable, non-linear). Video narration is heard with the ears (sequential, temporal, rhythmic):

| Aspect | Web Copy (`maxilun-content`) | Spoken Video Narration |
|---|---|---|
| **Medium** | Eyes read text on a screen | Ears hear sound waves |
| **Pace control** | The reader sets the scroll | The narrator sets pauses and emotion |
| **Density** | Compact, structured paragraphs | Short, spaced sentences (1 idea per breath) |
| **Silence** | Visual white space | Audio pause (`0.4s - 1.2s`) to let an idea land |
| **Output** | DOM typography elements | Synced audio file + cue metadata |

### 5 Principles of Cinematic Narration
1. **Read-aloud test**: Speak every line out loud before approving it. If the tongue trips or the breath breaks, split the sentence in two.
2. **Rhythm over rigid grammar**: Sentence fragments are allowed when they deliver the right emotional stress.
3. **Concrete replaces adjective**: Avoid empty adjectives. Replace them with a factual number or a direct comparison.
4. **Sync points**: Every narration sentence must pair with a relevant visual moment on the video frame timeline.
5. **Loudness balance**: Target voice-over at `-16 LUFS` integrated mono as a default baseline (adjusted per destination spec and measured via EBU R128), with the background music *ducked* while the voice is active.

---

## 2. Narration & Timeline Data Structure

```typescript
export interface NarrationSegment {
  id: string;
  sceneId: string;
  text: string;                  // Clean text without markup
  ssmlText: string;              // SSML-annotated text for the TTS engine
  startFrame: number;            // First frame on the timeline
  endFrame: number;              // Last frame of the vocal duration
  durationSeconds: number;
  emotion: 'authoritative' | 'urgent' | 'confident' | 'warm';
  pauseAfterMs: number;          // Silent pause after the sentence
  visualCue: string;             // Description of the visual event it triggers
  syncPoint?: {
    frame: number;
    event: string;
  };
}
```

---

## 3. Google Cloud TTS Integration & Voice Guide

### 3.1 Recommended Voices

| Voice ID | Language | Gender | Engine | Voice Characteristics |
|---|---|---|---|---|
| `id-ID-Wavenet-B` | Indonesian | Male | WaveNet | Authoritative, firm, formal articulation |
| `id-ID-Wavenet-A` | Indonesian | Female | WaveNet | Warm, professional, clear |
| `id-ID-Neural2-A` | Indonesian | Female | Neural2 | Modern, clear for technical instructions |
| `en-US-Journey-D` | English (US) | Male | Journey | Cinematic, storytelling, dynamic |
| `en-US-Neural2-D` | English (US) | Male | Neural2 | Precise, confident, steady tempo |

### 3.2 SSML Syntax Format (Speech Synthesis Markup Language)

Indonesian-language example (for an `id-ID` voice). The text means: "A business's first impression is now ninety-four percent decided on a digital screen."

```xml
<speak>
  <prosody rate="medium" pitch="+0st">
    Kesan pertama bisnis kini
    <emphasis level="strong">sembilan puluh empat persen</emphasis>
    ditentukan di layar digital.
    <break time="450ms"/>
  </prosody>
</speak>
```

SSML usage rules:
- `<break time="300ms"/>` for a pause between clauses.
- `<break time="600ms"/>` for a scene change or to stress an important point.
- `<emphasis level="strong">` for the one keyword that carries the main message.
- `<prosody rate="slow">` when stating numeric data or an action instruction.

---

## 4. Narration Quality Checklist Before Handoff to CineCode

- **Word Count**: Stay at or below 2.2 words per second at normal tempo (at most 65 words for a 30-second video).
- **Numbers written phonetically**: Write a number such as "94%" in words in the SSML script, in the narration language, so the TTS reading does not get the intonation wrong. Indonesian example: "sembilan puluh empat persen"; English example: "ninety-four percent".
- **Breath Marks & Holds**: Leave at least 1.5 seconds of silence at the end of the video before the file ends, so the CTA can be read in full.
- **Beat sync**: The vocal `startFrame` timing aligns with the bars of the background music.
