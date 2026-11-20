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

Invite only the 2-5 agents whose domains the decision actually crosses, in the order their outputs depend on each other (structure before pixels before runtime before review). The UI roster below is the default for a visual overhaul; a backend or mobile decision invites `maxilun-architect`, `maxilun-coder-backend`, `maxilun-coder-mobile`, `maxilun-security-auditor`, or `maxilun-verifier` instead.

| Tag | Specialist | Deliberation Focus |
|---|---|---|
| `[maxilun-ui-designer]` | UI/UX Architecture | Visual Archetype, font pairings, OKLCH tokens, layout topology (Bento, Ledger, Spotlight), dismantling card monotony (`LAY-008`). |
| `[maxilun-ui-motion]` | 3D & Motion Choreography | WebGL/Three.js interactive canvas, analytical springs, scroll blur reveals, GPU frame budgets, ambient micro-interactions. |
| `[maxilun-coder-frontend]` | Frontend Engineering | Next.js 15 App Router topology, RSC vs Client Islands, dynamic imports for 3D shaders, hydration performance, zero CLS. |
| `[maxilun-architect]` | System Architecture | API data contracts, module seams, state isolation, database load, security boundaries. |
| `[maxilun-ui-reviewer]` | Quality & Purity Gate | Banning generic AI tells (`CMP-003` zero emoji, `HDR-001` no breadcrumb slop, `LAY-008` no 3-card triads), mobile 375px overflow, `slopscan.py` 0-error gate. |

---

## 3. Deliberation Turn Sequence

### 3.1 How the meeting runs

Every turn is a separately dispatched agent, so each specialist reasons with its own skill and persona; one model writing all the voices is not a meeting. Dispatch by host:

| Host | How each turn is dispatched |
|---|---|
| Maxilun harness | `convene_meeting` tool (`harness/engine/meeting.py`) runs the whole loop, or `python -m harness.cli meeting "<agenda>" --with <agents>` from a terminal |
| Claude Code | Task tool, `subagent_type: maxilun-<agent>` (agents installed in `~/.claude/agents`) |
| OMP / Termul | `task` tool, `agent: maxilun-<agent>` (agents installed in `~/.omp/agent/agents`) |
| OpenCode | its agent dispatcher (agents installed in `~/.config/opencode/agents`) |

On the host paths the orchestrator is the loop: dispatch one speaker, append the reply verbatim to the minutes, dispatch the next speaker with the updated minutes, and stop on a round with no objection or after round 3. Each dispatch prompt carries the agenda, the full minutes, the five-line format below, and "read-only: do not edit files".

1. **Turn-taking.** Speakers talk one at a time in roster order. Each speaker receives the agenda and the full minutes so far, so the second speaker answers the first and round 2 answers round 1.
2. **Fixed turn format.** Every turn is five lines: `POSITION`, `AGREE: @agent`, `OBJECT: @agent + evidence`, `PROPOSE`, `ASK: @agent`. Questions addressed with `@name` must be answered first in that agent's next turn. An objection needs `file:line` evidence or the label `[UNVERIFIED]`.
3. **Read-only.** During the meeting, speakers can only read files, query the knowledge graph, and read the bus. Writing, shell, and delegation are blocked, so nobody changes code before the decision is made.
4. **Closing.** A round with no `OBJECT` closes the meeting with consensus. Otherwise it continues up to 3 rounds and returns the open objections. An objection is withdrawn by writing `OBJECT: none`.
5. **Minutes.** Every turn is posted to the agent bus as one thread (`meeting_open` → `meeting_turn` → `meeting_close`), with `reply_to` linking each turn to the one before it, and saved to `maxilun-out/agent_bus.json`. Later `delegate_task` handoffs carry the meeting outcome, not the full transcript.

Without any dispatcher (Cursor, Gemini CLI, Codex without agents), say so in one sentence, then run the same format in order within one message, reading each `agents/<name>.md` for its voice. Label those minutes `[simulated]`; they must still use the five lines per turn, answer every `ASK`, and stop on a round with no objections.

### 3.1.1 Minutes shown to the user

```text
Agenda: <one line>
**@maxilun-architect** (R1): POSITION ... / OBJECT ... / ASK @maxilun-coder-backend ...
**@maxilun-coder-backend** (R1): POSITION ... (answers the ASK first) / AGREE @maxilun-architect ...
Synthesis (chair): decision, who settled each objection, open questions
```

### 3.2 Phase content

A Council session moves through 4 phases:

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
The Master Orchestrator turns the minutes into a crisp **Consensus Blueprint**. Each open objection must state who resolved it and how (by the contract owner: `maxilun-architect` for structure, `maxilun-craft` for rendered surfaces, `maxilun-data` for schema, `maxilun-sentinel` for trust boundaries), or it goes to the user as an open question:
- **Design Archetype & Fonts**: Declared archetype, font pairing, and delivery (project loader or self-hosted; CDN only for a requested prototype).
- **Layout Topology**: Asymmetric Bento 2:1, Tabular Ledger, or Spotlight Pairing.
- **3D & Motion Layer**: Interactive WebGL shader/canvas, spring physics parameters.
- **Technical Architecture**: RSC layout with dynamic client island for 3D/motion.
- **Verification Gates**: Commands and criteria for exit code 0 (`slopscan.py`, build, test).

### Phase 4: User Approval Gate ("ACC Gate")
**Strict Stop Rule**: The agents DO NOT write or edit code files until the user reviews and approvals the plan. The Orchestrator ends the round with:
> *"Rencana hasil diskusi dewan agent telah selesai dirumuskan. Silakan review dan berikan **ACC (Approve)** atau sampaikan arahan/revisi sebelum kami mulai eksekusi kode!"*

Once the user approves ("ACC", "Lanjut", "Gas", or custom notes), Wave 1 and Wave 2 implementation begins immediately.

