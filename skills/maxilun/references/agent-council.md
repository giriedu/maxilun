# Multi-Agent Council & Deliberation Protocol (Roundtable Mode)

The Multi-Agent Council is Maxilun's collaborative deliberation protocol. It enables specialist agents to visibly discuss, pitch creative ideas, debate technical trade-offs, and synthesize a cohesive blueprint before any code is modified, giving the user full oversight to review and approve ("ACC") the plan.

---

## 1. Trigger Conditions

Activate Council Mode whenever:
1. **Explicit command**: `/maxilun council`, `/maxilun roundtable`, `diskusi agent`, `rembug agent`, `openbot`, `agent ngobrol`, `tanya dewan`, or `musyawarah agent`.
2. **Type 1 Redesign & Greenfield Strategy**: When the user asks for a total overhaul, new architecture, or visual revamp with open creative possibilities.
3. **Multi-Domain Trade-off**: When UX aesthetics, 3D/motion graphics, and backend performance pull in competing directions.

---

## 2. Council Roster & Domain Personas

During deliberation, each specialist speaks in character using their explicit domain tag:

| Tag | Specialist | Deliberation Focus |
|---|---|---|
| `[maxilun-ui-designer]` | UI/UX Architecture | Visual Archetype, font pairings, OKLCH tokens, layout topology (Bento, Ledger, Spotlight), dismantling card monotony (`LAY-008`). |
| `[maxilun-ui-motion]` | 3D & Motion Choreography | WebGL/Three.js interactive canvas, analytical springs, scroll blur reveals, GPU frame budgets, ambient micro-interactions. |
| `[maxilun-coder-frontend]` | Frontend Engineering | Next.js 15 App Router topology, RSC vs Client Islands, dynamic imports for 3D shaders, hydration performance, zero CLS. |
| `[maxilun-architect]` | System Architecture | API data contracts, module seams, state isolation, database load, security boundaries. |
| `[maxilun-ui-reviewer]` | Quality & Purity Gate | Banning generic AI tells (`CMP-003` zero emoji, `HDR-001` no breadcrumb slop, `LAY-008` no 3-card triads), mobile 375px overflow, `slopscan.py` 0-error gate. |

---

## 3. Deliberation Turn Sequence

A Council session executes in 4 structured phases:

### Phase 1: Creative Exploration & Pitches
Specialists propose bold domain solutions tailored to the product purpose:
- **`[maxilun-ui-designer]`**: Proposes visual archetype (e.g. *Technical Data-Dense* or *Warm Editorial*), font pairings (e.g. Space Grotesk + JetBrains Mono), and asymmetric layout topology.
- **`[maxilun-ui-motion]`**: Proposes 3D ambient visual layer (e.g. interactive particle wave or geometric mesh in React Three Fiber) and scroll-triggered physics.

### Phase 2: Technical & Feasibility Critique
Specialists challenge and optimize each other's ideas:
- **`[maxilun-coder-frontend]`**: Analyzes bundle impact—demands lazy-loading / Client Island boundaries for Three.js canvas so initial HTML FCP remains instant (<1.2s).
- **`[maxilun-architect]`**: Ensures client-side state transitions do not cause waterfall API requests.
- **`[maxilun-ui-reviewer]`**: Verifies compliance against strict mechanical purity rules—rejects symmetrical cards, checks WCAG contrast, and confirms mobile responsive layout.

### Phase 3: Consensus Blueprint
The Master Orchestrator gathers all contributions and outputs a crisp **Consensus Blueprint**:
- **Design Archetype & Fonts**: Declared archetype and Google Font CDN pairing.
- **Layout Topology**: Asymmetric Bento 2:1, Tabular Ledger, or Spotlight Pairing.
- **3D & Motion Layer**: Interactive WebGL shader/canvas, spring physics parameters.
- **Technical Architecture**: RSC layout with dynamic client island for 3D/motion.
- **Verification Gates**: Commands and criteria for exit code 0 (`slopscan.py`, build, test).

### Phase 4: User Approval Gate ("ACC Gate")
**Strict Stop Rule**: The agents DO NOT write or edit code files until the user reviews and approvals the plan. The Orchestrator ends the round with:
> *"Rencana hasil diskusi dewan agent telah selesai dirumuskan. Silakan review dan berikan **ACC (Approve)** atau sampaikan arahan/revisi sebelum kami mulai eksekusi kode!"*

Once the user approves ("ACC", "Lanjut", "Gas", or custom notes), Wave 1 and Wave 2 implementation begins immediately.

