# Multilingual Voice Synthesis & Narration Direction

Voiceover specification for `maxilun-content` and `maxilun-cinecode` (compatible with zero-shot multilingual TTS and SSML pipelines).

## 1. Speaker Profile Attributes
Define a consistent voice brief per project:
- **Language / Dialect**: explicit BCP-47 tag (e.g., `id-ID`, `en-US`).
- **Voice Design**: gender, age range, pitch, pace (WPM), and timbre (e.g., `calm-technical`, `warm-editorial`).

## 2. Beat-Synced Script & Non-Verbal Cues
- Keep spoken beats aligned to `maxilun-cinecode` frame timelines ($\le 8$ words per visual beat; ~2.5 words/sec natural pace).
- Use explicit pause markers (`[pause:300ms]`) and non-verbal cues (`[laughter]`, `[sigh]`) sparingly only where the product tone calls for it.
- Supply phoneme or phonetic spelling overrides for domain acronyms, brand names, and mixed-language terms.

