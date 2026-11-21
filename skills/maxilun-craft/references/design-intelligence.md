# Product Design Intelligence & Context Invariants

> **Status**: Reference Document  
> **Specialist**: `maxilun-craft` & `maxilun-scaffold`  
> **Source Attribution**: Synthesized from Design Intelligence principles (MIT License, see `CREDITS.md`)

This document defines the core heuristics that elevate AI coding assistants from mere component generators into disciplined product designers. It enforces factual grounding, prevents business hallucination, and establishes a deterministic design lifecycle.

---

## 1. The "Ask Before You Design" Protocol

AI models often rush into writing frontend markup based on vague prompts, inventing requirements that contradict actual user intent. 

### Mandatory Context Checklist
Before generating or redesigning screens, verify these three anchors from repository facts (`docs/PRD.md`, schema files, or explicit user brief):
1. **Primary User Goal**: What single operational outcome must the user achieve on this viewport?
2. **Data Shape & Boundaries**: What real fields exist in the database schema or API contract?
3. **Irreversible Business Rules**: Are there specific permissions, multi-tenant boundaries, or regulatory constraints?

*If any irreversible business logic is ambiguous and cannot be confirmed from repository evidence, pause and clarify before writing code.*

---

## 2. Invariant: Zero Invented Business Facts

Generic AI interfaces frequently suffer from "speculative feature injection." The following practices are strictly prohibited:

- **No Fabricated Pricing Tiers**: Never invent arbitrary plan names (e.g., "Enterprise Platinum Plus"), prices, or billing cycles not present in repository contracts.
- **No Fictional Promo Mechanics**: Never add countdown timers, fake discount badges, or artificial urgency mechanisms unless explicitly specified in the product requirement.
- **No Hallucinated Policies**: Do not invent fake refund terms, compliance badges, or security guarantees.
- **No Fake Social Proof**: Ban placeholder testimonials with stock avatars and fictional company quotes (`TEST-001`).

---

## 3. Resilient Surface Topology: The 6-State Standard

Professional product design treats state transitions and failure modes as first-class citizens, not afterthoughts. Every interactive surface must implement all 6 states:

| State | Implementation Standard | Failure To Avoid |
| :--- | :--- | :--- |
| **1. Idle** | Resting state with clean visual hierarchy, neutral hairline borders, and single focal action. | Over-decorated borders or competing neon buttons. |
| **2. Loading** | Dimensionally stable skeletons matching exact component height/width (Zero CLS). | Shifting content boxes or generic full-screen spinners. |
| **3. Populated** | Realistic data density, sentence-case headings, and `tabular-nums` right-aligned on numerical columns. | Centered numbers or truncated text without tooltips. |
| **4. Empty + CTA** | Informative empty state explaining *why* it is empty and providing a primary action button to populate it. | Dead-end screens ("No data found") without a clear next step. |
| **5. Pending** | Immediate optimistic UI response with disabled duplicate triggers to prevent double-submit. | Unresponsive clicks causing user confusion. |
| **6. Error + Recovery** | Human-readable error message explaining root cause, paired with a non-destructive "Try Again" action. | Raw JSON stack traces or silent failures. |

---

## 4. The 5-Stage Product Design Lifecycle

Every interface task must progress through five structured stages:

```
[Phase 1: Analyze] ──> [Phase 2: Frame] ──> [Phase 3: Build] ──> [Phase 4: Critique] ──> [Phase 5: Verify]
```

1. **Analyze**: Ingest domain context, examine user constraints, and review existing component architecture.
2. **Frame**: Choose the appropriate layout topology (Asymmetric Bento Grid, Operational Tabular Ledger, or Master-Detail Split) instead of generic symmetrical card grids (`LAY-008`).
3. **Build**: Lock the OKLCH semantic token ramp, apply mathematical concentric radii ($R_{inner} = R_{outer} - padding$), and compose accessible headless primitives.
4. **Critique**: Subject the interface to directional tuning commands:
   - `bolder`: Strengthen contrast and focal hierarchy.
   - `quieter`: Eliminate unnecessary border visual noise.
   - `typeset`: Format sentence case, text balance, and font weights.
   - `polish`: Refine micro-spring physics and hover states.
   - `harden`: Stress-test 320px mobile viewport reflow and text overflow.
5. **Verify**: Execute `python scripts/slopscan.py` to mechanically confirm zero AI tells, WCAG AAA contrast, and keyboard focus visibility.

