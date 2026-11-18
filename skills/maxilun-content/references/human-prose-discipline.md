# Human Prose & Anti-AI-Slop Writing Standard

Eliminate statistically detectable AI writing patterns across product copy, microcopy, READMEs, articles, emails, and reports while preserving the author's real voice.

## 1. Two Operating Modes
- **Edit (default)**: Make the minimum effective edit to fix AI patterns, repetition, and unclear abstractions. Preserve the writer's natural cadence, humor, and personal phrasing. Return the edited draft plus a brief `What changed` summary.
- **Detect (audit only)**: Quote each offending line, name the exact pattern below, and give a short fix without rewriting or guessing an AI-detector score.

## 2. Core Prose Principles
- **Lead with the point**: Cut generic throat-clearing ("In today's fast-paced..."). Keep personal context only when it adds tension or clarity.
- **Active voice & concrete nouns**: "The team shipped Tuesday" beats "the decision emerged." Replace vague abstractions ("improved efficiency") with numbers, names, and mechanisms ("cut deploy time from 40m to 4m").
- **Sentence variety**: Break uniform 15–20 word rhythm; mix short direct statements with longer explanatory sentences.
- **Action-oriented UI copy**: Name the exact action on buttons ("Save invoice", not "Submit" or "Continue") and pair every error notice with a concrete recovery step.

## 3. Banned AI Vocabulary
Avoid unless quoting or required as a literal technical term:
- `delve`, `tapestry`, `landscape` (figurative), `testament`, `vibrant`, `pivotal`, `crucial`, `intricate` / `intricacies`, `meticulous` / `meticulously`, `bolster`, `garner`, `underscore`, `interplay`, `multifaceted`, `nuanced` (as filler), `foster`, `leverage` (as verb), `utilize` (use `use`), `commence` (use `start`), `facilitate`, `encompass`, `paramount`, `groundbreaking`, `cutting-edge`, `game-changer` / `game-changing`, `transformative`, `revolutionize`, `seamless` / `seamlessly`, `robust` (outside engineering), `comprehensive` (describing own output), `endeavor`, `aforementioned`, `harnessing`, `spearheading`, `navigating` (figurative), `showcasing`, `highlighting`, `emphasizing`, `enhancing`, `unprecedented`, `remarkable`, `stunning`, `profound`, `epic` (non-literal), `in essence`, `thought leader`, `synergy`, `pain points`, `value proposition` (casual), `moving forward`, `circle back`, `rest assured`.

## 4. Banned Phrases & Openers
- **Openers**: `Certainly,`, `Moreover,`, `Additionally,`, `Furthermore,`, `Notably,`, `Interestingly,`, `Importantly,`, `Significantly,`, `Indeed,`, `Undoubtedly,`, `In conclusion,`, `Overall,`.
- **Phrases**: `"In today's [adj] [noun]..."`, `"It's worth noting that..."`, `"It's important to note that..."`, `"Let's dive in"`, `"At its core..."`, `"In the realm of..."`, `"When it comes to..."`, `"A testament to..."`, `"Not just X, but Y"`, `"It's not just about X — it's about Y"`, `"Whether you're a [X] or a [Y]..."`, `"From X to Y"` (range opener), `"At the end of the day..."`, `"The bottom line is..."`, `"Without further ado..."`, `"In a nutshell..."`, `"Take it to the next level"`, `"Unlock the power of..."`, `"Bridge the gap"`, `"Move the needle"`.

## 5. Structural, Punctuation & Accuracy Tells
- **Rule of three**: Do not force every list or clause into three parallel adjectives/clauses.
- **Binary contrast & colon reveals**: Cut `"It's not X; it's Y"` and faux-insight `"Here's the truth: ..."` setups.
- **Fake-profound kickers & recap endings**: End on a concrete point, fact, or next step — never a summary-recap paragraph.
- **Punctuation**: Limit em dashes (`—`) to 0 in short UI copy and at most 1–2 in long drafts; use sentence case after colons unless a proper noun or code requires otherwise; avoid exclamation spam and emoji bullets.
- **Zero fabrication**: Never invent statistics, quotes, or anecdotes; flag missing data for the user.
