# Design Decision Records (DDR): Adversarial Direction Justification

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-craft/SKILL.md"
  origin: "Maxilun Craft Engine"
-->

Write Design Decision Records (DDR) from an adversarial evaluation of competing directions. For every new interface design or visual overhaul, document why the direction was chosen before writing the first line of code.

---

## 1. Order of Operations

Before deciding layout and color palette:

1. **Research 3 Real Category Leaders**:
   - Study the best implementations in the relevant field (for example: boutique lodging reservations -> inspect *Airbnb Luxe*, *Mr & Mrs Smith*, *Plum Guide*).
   - Identify the industry's conventional patterns and decide one main point of differentiation: a convention you deliberately reject.
2. **Extract a Real-World Physical Palette**:
   - Do not pick arbitrary hex values from generic internet palettes.
   - Take colors from physical materials that actually exist in the product subject's environment:
     - Print shop / typography: dense offset ink, cold cast type metal, steel lubricating oil.
     - Artisan coffee shop: dark roasted beans, natural filter paper, glazed clay ceramic.
     - Rural lodging: stone-wall lime wash, local forest leaf green, fired terracotta floor tile.
3. **Living Typography Catalog**:
   - Choose a display typeface with a historical or geographic link to the product's character (for example: *Lusitana* for Portuguese architecture, *Fraunces* for organic editorial typography).
   - Pair it with a neutral functional sans-serif for operational text, tabular data, and forms.
4. **Audit the Old Design Locks Before a Redesign (Design Lock Assessment)**:
   - When the task is a *redesign*, inspect the existing `:root` tokens, layout shell, and primitive components.
   - Identify any dull variable or narrow wrapper that locks the UI to the old template.
   - Decide the *cutover point* where the lock is dismantled before reworking leaf JSX.
---

## 2. Three Competing Directions

Design three contrasting concepts to prevent the AI model's automatic bias:

| Direction | Concept Definition | Key Characteristics | Risk / Evaluation Rationale |
|---|---|---|---|
| **Direction 1: The Generic AI Trap** | The first instinctive pattern an automatic generator usually picks. | Symmetric card stacks, floating hero pill badge, two twin solid buttons, monotonous center-aligned layout. | Identify it so you can deliberately reject it or cut it entirely. |
| **Direction 2: Authentic Domain Artifact** | An interface structure centered on the subject's work object or material identity. | Builds the interface around one main interactive object (*The Object IS the Interface*), proportional editorial hierarchy, calibrated physical palette. | Sells the subject's character and the experience of use before asking for a transaction. |
| **Direction 3: Radical Utility & Density** | An approach focused on speed and high task efficiency. | Measured tabular data density, high-contrast monochrome, direct navigation without secondary visual ornament. | Very efficient for daily work tools; evaluate whether it fits this product's audience. |

---

## 3. Comparison Matrix & Winner Justification

Compare the three directions against objective criteria:

1. **Fit with the User's Mental Model**: Does the visual flow match how users process this information in the real world?
2. **Functional Honesty**: Does every visual element carry a real function, or is it only decoration?
3. **Cross-Device Resilience**: Does the interface geometry hold from a 375px mobile screen to a wide desktop without scroll leaks?

### DDR Documentation Format

Document the decision in this concise 3-paragraph format:

```markdown
### DDR-001: [Screen / Component Name]
- **Context & Physical Entities**: [Real-world physical materials and the chosen typefaces]
- **Chosen Direction**: Direction 2 ([Direction Name])
- **Why It Won**: [2 factual sentences on why this direction best serves the primary task]
- **Rejected Elements**: [List of components from Direction 1 & 3 deliberately discarded, with the argument for each rejection]
```

### Redesign & Lock Dismantling Documentation Format (DDR-DL)

Use this format when redesigning an interface that was previously locked:

```markdown
### DDR-DL-001: [Screen / Redesign Area Name]
- **Design Locks Dismantled**: [Old `:root` tokens, narrow layout wrappers, or obsolete primitives removed]
- **New Foundation Installed**: [OKLCH palette from the domain's physical materials, display/sans typography, free canvas layout]
- **Patchwork Prevention**: [Evidence that old/zombie CSS was removed cleanly and no styling collisions remain]
```

---

## 4. Interface Subtraction Protocol (Subtraction Pass)

After the interface draft is assembled:

1. Remove one visual element (a divider line, a decorative badge, a double card wrapper, or a repeated caption).
2. Check whether user comprehension or data readability drops.
3. Repeat until the next removal starts to damage comprehension or navigation.
4. Restore that last element. The number of elements left is the optimal limit (*pure density*).
