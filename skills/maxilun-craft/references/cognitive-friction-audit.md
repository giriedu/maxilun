# Cognitive Friction Audit: Empirical Usability Invariants

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-craft/SKILL.md"
  origin: "Maxilun Craft Engine"
-->

Run cognitive-load audits and heuristic interface evaluations from concrete code evidence (*file:line*). Skip generic theoretical audits: check the 10 empirical usability invariants directly against the DOM structure, the components, and the interactions.

---

## 1. Ten Empirical Usability Invariants

1. **Real-Time System Status Visibility**:
   - Show visual feedback (pending state, deterministic progress indicator) for every operation that takes $> 150\text{ms}$.
   - Never leave users guessing whether the system registered their button click.
2. **Match with Real-World Objects**:
   - Use the nouns and workflows of the user's own domain in interface vocabulary (for example: invoice, tracking number, reservation slot). Do not use internal developer terms (*database_id*, *payload*, *record_entity*).
3. **User Control and Freedom (Explicit Cancel Path)**:
   - Give every modal dialog, sliding drawer, or multi-step flow a clear close control (*escape hatch*) that also responds to the keyboard `Esc` key.
4. **Token & Interface Pattern Consistency**:
   - Use the same semantic color and iconography for every status of the same kind (success, warning, error) on every screen. Allow no arbitrary variation.
5. **Error Prevention Before It Happens**:
   - Remove the chance of wrong input from the start (for example: disable past dates for future bookings, apply numeric masking to card numbers, validate as soon as the user finishes typing).
6. **Recognition over Recall**:
   - Keep important contextual information (such as the order summary, price per night, or transaction ID) visible throughout the confirmation flow. Users must not need to return to the previous screen.
7. **Contextual Accelerator Ergonomics**:
   - Provide keyboard shortcuts only in applications built for fast keyboard work (editors, terminals, data filing). Do not force fake shortcuts onto public marketing pages.
8. **Subtractive Minimalism & Signal Clarity**:
   - Remove every decorative element that does not help users understand content or make a decision.
9. **Error Diagnostics Near the Point of Failure**:
   - Make every failure message guide the next recovery step. Do not show only a raw HTTP error code (*"500 Internal Error"*).
10. **Timely Help Without Interrupting the Flow**:
    - Present help as micro tooltip text or a contextual link next to the input label that needs a technical explanation.

---

## 2. Physical Ergonomics: Fitts's Law & the Thumb Zone

When designing a mobile interface or a tablet touch screen:

1. **Reach Area Rule**:
   - Place the most frequently used primary actions (main navigation, flow-advance button, quick filters) in the bottom third of the screen (*natural thumb zone*).
   - Place destructive or rarely used actions in the upper area, where reaching them takes deliberate effort.
2. **Measured Minimum Touch Target**:
   - Give mobile controls an effective tap area of at least $44 \times 44\text{pt}$ (iOS) or $48 \times 48\text{dp}$ (Android), even when the visual icon inside is smaller (use invisible hit-box padding).
3. **Spacing Between Buttons**:
   - Keep a safe gap of at least $8\text{px}$ between adjacent controls to prevent mis-taps (*accidental activation*).

---

## 3. Cognitive Audit Report Format

Report every usability audit finding in this evidence-based format:

```markdown
### [HEURISTIC-AUDIT] file:line — Short Problem Description
- **Invariant Code**: [INV-01 to INV-10]
- **Friction Level**: [High / Medium / Low]
- **Code Evidence**: `file:line` the violating code snippet
- **Cognitive Impact**: [1-2 sentences explaining the user confusion or the mis-click risk]
- **Recommended Fix**: [Diff or concrete adjustment specification]
```
