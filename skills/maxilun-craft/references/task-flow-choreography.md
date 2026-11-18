# Task Flow Choreography: User Mental Pathways & Friction Reduction

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-craft/SKILL.md"
  origin: "Maxilun Craft Engine"
-->

Choreograph user task flows (*task flow choreography*) to minimize cognitive load and cut navigation friction points. Do not rely on abstract flow diagrams. Focus on how efficiently real screen transitions complete the primary task.

---

## 1. Deconstructing User Mental Pathways

Every user task in an application consists of 4 discrete mental stages:

```text
[Context Orientation] ──> [Option Evaluation] ──> [Action Confirmation] ──> [Result Verification]
```

1. **Context Orientation (< 2 seconds)**:
   - Users understand where they are and what the current page is for.
   - Show a clear title in *sentence case* and identify the main work entity.
2. **Option Evaluation**:
   - Limit the options presented at one time (Hick's Law).
   - Show the most decisive parameters first (for example: price, date availability, or order status) before secondary settings.
3. **Action Confirmation**:
   - Label the primary action button with a specific verb + object (for example: *"Confirm Reservation"*, *"Send Report"*).
   - Avoid buttons with generic labels (*"Submit"*, *"OK"*, *"Next"*).
4. **Result Verification**:
   - Show visual proof that the system recorded the action (immediate status change, transaction receipt summary, or reference number).

---

## 2. Eliminating Screen Bounce

*Screen bounce* happens when users are forced onto a full separate screen only to enter one small piece of data, and then return to the original screen.

Replace it with the **In-Place Choreography** pattern:

| Interaction Case | Conventional Pattern (Many Bounces) | Maxilun Choreography Pattern (No Bounce) |
|---|---|---|
| **Data Filtering & Sorting** | Move to a separate filter page. | Use a drawer panel (*bottom sheet*) or an inline filter directly above the data table. |
| **Single-Row Editing** | Move to a full-screen edit form. | Apply inline editing (*click-to-edit*) or a non-intrusive side drawer. |
| **Item Detail Preview** | Move to a new route, then press the back button. | Apply a split preview (*master-detail pane*) on desktop or accordion expansion on mobile. |

---

## 3. Progressive Disclosure Discipline

1. **80/20 Rule**:
   - Show the 80% of common parameters that most users need directly on the main surface.
   - Hide the 20% of *advanced settings* behind a progressive disclosure control (*disclosure toggle* or secondary tab).
2. **Persistent Context**:
   - When users open the advanced option details, keep the summary of the earlier main parameters visible as a comparison anchor.

---

## 4. Running the Subtraction Pass in a Workflow

Use this subtraction checklist before finalizing a task flow:

1. **Redundancy Check**: Is there instruction text that the input label already makes clear? (If yes, delete that instruction text.)
2. **Divider Check**: Can 2x spacing (*spatial rhythm*) alone achieve the visual separation, instead of a new divider line or card? (If yes, delete the line/card.)
3. **Click Check**: Can any steps in the flow be merged without burdening user comprehension? (If yes, cut the number of steps.)
