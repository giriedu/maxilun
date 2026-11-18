# Patterns

Starting structures per screen type, and the states every screen needs.
These are skeletons to reason from. The Brief decides the final shape; if
two projects end up with the same layout, one of them skipped the Brief.

Contents: dashboard · data table · form · detail page · landing page ·
Apps Script / single-file web app · states · responsive · accessibility floor

## Dashboard

Ask first: what decision does this screen support, and how often is it
opened? A dashboard nobody acts on is a poster.

- **One lead region** answering the Job (the trend, the queue, today's
  list). It takes the most area and the Spotlight.
- **Supporting figures** as a compact strip: label, value, comparison with
  its reference (`vs last month`, `dari 312 siswa`). Three to five. No icons,
  no mini charts, no coloured tiles.
- **A work list** (what needs attention) usually beats a second chart.
  People act on rows, not on bars.
- Supporting regions differ in kind and size from the lead: chart + list,
  not chart + chart.
- Page title is the scope and the period, with the period control next to it.
- Filters live in one row above the content they filter.

Avoid: the 4-cards / 2-charts / 1-table stack, greeting header, donut charts
for more than three slices, a "recent activity" feed added to fill space.

## Data table

- Columns ordered by what identifies the row first, what is acted on last.
- Text left, numbers right with tabular figures, dates in one format,
  status as a word with a small dot.
- Header: secondary text role, same size as the body or one step smaller,
  sentence case, sticky when the table scrolls.
- One separator style: hairlines between rows **or** zebra, not both.
- Row actions: at most one visible, the rest in a menu at the row end.
  Bulk actions appear in a bar when rows are selected.
- Search and filters above; count of results stated in words
  (`42 dari 318 siswa`).
- Long tables: pagination or virtual scroll, with the choice of page size.
- Narrow screens: turn each row into a stacked block showing the two or
  three most important fields; the rest behind a tap. Never a sideways
  scroll of twelve columns without a frozen first column.
- Empty filtered result is different from an empty table: say which filter
  hides everything and offer to clear it.

## Form

- One column. Two fields side by side only when they are one thought
  (`Tempat` + `Tanggal lahir`).
- Label above, always visible. Placeholder only for format examples.
- Group related fields under a plain heading with space, not in boxes.
- Mark the minority: if most fields are required, mark the optional ones.
- Field width hints at the expected length (NISN is short, address is wide).
- Use the right input: date picker, select for ≤ 7 fixed options shown as
  radios when ≤ 4, numeric keyboard for numbers (`inputmode="numeric"`).
- Validate on blur, not on every key. Error text sits under the field, says
  what is wrong and what to type instead, and is linked for screen readers.
- One primary button, labelled with the outcome, at the end of the reading
  line (left-aligned under the fields). Destructive actions are separate.
- Long forms: sections with progress that can be saved and resumed; never
  lose typed data on error.
- After submit: say what happened and what happens next.

## Detail page

- Header: the object's name, its key status, and the one or two actions
  that apply to it.
- Body: facts as a definition list (label left or above, value prominent),
  grouped by meaning. Not a grid of cards with one value each.
- Related lists below, each with its own empty state.
- Edits happen in place or in a side panel; avoid full-page modals.

## Landing page

- First screen states what it is, who it is for and the one action. If a
  visitor reads only the headline, they should be able to repeat what the
  product does.
- Show the real thing: a product view built in code with plausible data, a
  photo, or a real document from the Origin. One visual, given real size.
- Every section must earn its place by answering a question a visitor
  actually has: what is it, is it for me, how does it work, what does it
  cost, can I trust it, how do I start. Delete sections that answer none.
- Proof is specific and sourced, or absent.
- One primary action repeated, not five different ones.
- Vary section composition; do not alternate image-left / image-right
  mechanically.

## Apps Script / single-file web app

Common for school and office tools. Constraints: one HTML file, slow
networks, old Android phones, users who are not technical.

- System font stack or one self-hosted-size font; no icon font, inline the
  few SVG icons used.
- All tokens in one `:root` block at the top of the `<style>`.
- Design phone-first at 360px; most parents and teachers open it from a
  chat link.
- Big, labelled steps: choose class → find name → verify → edit → confirm.
  One step per screen on phones, with a visible way back.
- Every server call (`google.script.run`) has a visible pending state on
  the control that triggered it, a success message, and a failure message
  with a retry. Disable the button while pending.
- Confirm before saving changes to official data, and show what changed
  (old value → new value).
- Plain Bahasa Indonesia, no technical words (`Gagal menyimpan. Periksa
  koneksi lalu coba lagi.` not `Error 500`).

## States

Design these for every data region, not only the full one.

| State | Must contain |
|---|---|
| **Loading** | A skeleton shaped like the real content for > 300ms waits; nothing for shorter; never a spinner over the whole page for partial loads |
| **Empty (first use)** | What will appear here, why it is useful, the action to create the first one |
| **Empty (filtered)** | Which filter caused it, a way to clear it |
| **Error** | What failed in plain words, whether data is safe, a retry |
| **Partial / stale** | What is missing or how old the data is |
| **Too much** | Truncation with a way to see all; long names wrap or ellipsize with a title |
| **Success** | Quiet confirmation near where the action happened; toast only for things that happened elsewhere |
| **No permission** | What is restricted and who can grant access |

Also check extremes: 0, 1 and 1,000 items; a 60-character name; a number
with nine digits; a missing photo.

## Responsive

Decide per breakpoint what **changes**, not just what shrinks.

- ≤ 480: one column, navigation in a bottom bar (≤ 5 items) or a menu,
  primary action reachable by thumb, tables become stacked rows.
- 481–1024: navigation collapses to icons with labels on demand or a top
  bar; two columns only where both stay readable.
- > 1024: full shell. Cap the content width; extra space becomes margin,
  not wider text.
- Use `clamp()` for page gutters and display sizes, container queries for
  components that live in differently sized regions.

## Accessibility floor

Not optional and not a later phase.

- Semantic elements: `button` for actions, `a` for navigation, real
  headings in order, `label` tied to every input, `table` for tabular data.
- Everything works by keyboard; focus is visible and never trapped except
  inside an open dialog, which returns focus on close.
- Contrast 4.5:1 for text, 3:1 for large text and control boundaries.
- Hit targets 44×44 on touch, 24×24 minimum on pointer.
- Icons without text have an accessible name. Decorative images have
  empty `alt`.
- Status changes are announced (`aria-live="polite"`), errors are linked to
  their fields (`aria-describedby`).
- Page language set (`<html lang="id">`).
- Zoom to 200% without loss of content.
