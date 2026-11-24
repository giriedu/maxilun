# Multi-Agent Council & Deliberation Protocol (Roundtable Mode)

The Multi-Agent Council is Maxilun's collaborative deliberation protocol. It enables specialist agents to visibly discuss, pitch creative ideas, debate technical trade-offs, and synthesize a cohesive blueprint before any code is modified, giving the user full oversight to review and approve ("ACC") the plan.

---

## 0. Persistence and Edit Lock per Host

**Council persists until stopped.** On `/maxilun council` (or an alias) run `<python> "<skill-dir>/scripts/council_hook.py" --on` from the project root; on any deactivation phrase run it with `--off`. `--on` creates the marker `.maxilun/council` and, for Antigravity, adds a `maxilun-council` entry to `.agents/hooks.json` that re-injects council mode before every model call and denies file writes and state-changing commands until the user's message is an ACC. Without Python, create or delete `.maxilun/council` by hand. While it exists, `scripts/council_hook.py` (a Claude Code `UserPromptSubmit` hook, installed by `<python> "<skill-dir>/scripts/council_hook.py" --install`; on Claude Code run that once at activation when `~/.claude/settings.json` has no `council_hook.py` entry, it is idempotent and repairs a path copied from another machine) re-injects council mode into every message, so it survives compaction and new sessions. Other modes are not persisted. **Hosts without that hook** (Cursor, Codex, Gemini CLI, Antigravity, OpenCode, or Claude Code where it was never installed): at the start of every turn check whether `.maxilun/council` exists in the project root and, if it does, run the turn as council. The marker, not the hook, is the switch. When a council dispatch fails because the agents are missing (`~/.claude/agents/maxilun-*.md` or the host's equivalent), say so in one sentence, name the installer to re-run, and continue `[simulated]` per §5.1 step 6.

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
| Maxilun harness (source repo only, not shipped with the skills) | `convene_meeting` tool (`harness/engine/meeting.py`) runs the whole loop, or `python -m harness.cli meeting "<agenda>" --with <agents>` from that repo root. Anywhere else use the host row below. |
| Claude Code | Task tool, `subagent_type: maxilun-<agent>` (agents installed in `~/.claude/agents`) |
| OMP / Termul | `task` tool, `agent: maxilun-<agent>` (agents installed in `~/.omp/agent/agents`) |
| OpenCode | its agent dispatcher (agents installed in `~/.config/opencode/agents`) |

On the host paths the orchestrator is the loop: dispatch one speaker, append the reply verbatim to the minutes, dispatch the next speaker with the updated minutes, and stop on a round with no objection or after round 3. Each dispatch prompt carries the agenda, the full minutes, the five-line format below, and "read-only: do not edit files".

1. **Turn-taking.** Speakers talk one at a time in roster order. Each speaker receives the agenda and the full minutes so far, so the second speaker answers the first and round 2 answers round 1.
2. **Fixed turn format.** Every turn is five lines: `POSITION`, `AGREE: @agent`, `OBJECT: @agent + evidence`, `PROPOSE`, `ASK: @agent`. Questions addressed with `@name` must be answered first in that agent's next turn. An objection needs `file:line` evidence or the label `[UNVERIFIED]`.
3. **Read-only.** During the meeting, speakers can only read files, query the knowledge graph, and read the bus. Writing, shell, and delegation are blocked, so nobody changes code before the decision is made.
4. **Closing.** A round with no `OBJECT` closes the meeting with consensus. Otherwise it continues up to 3 rounds and returns the open objections. An objection is withdrawn by writing `OBJECT: none`.
5. **Minutes.** On the Maxilun harness, every turn is posted to the agent bus as one thread (`meeting_open` → `meeting_turn` → `meeting_close`), with `reply_to` linking each turn to the one before it, and saved to `maxilun-out/agent_bus.json`. Later `delegate_task` handoffs carry the meeting outcome, not the full transcript.

Without any dispatcher (Antigravity IDE without a subagent tool, Cursor, Gemini CLI, Codex without agents), say so in one sentence, then run the same format in order within one message, reading each `agents/<name>.md` for its voice. Label those minutes `[simulated]`; they must still use the five lines per turn, answer every `ASK`, and stop on a round with no objections. Each speaker after the first opens by replying to a named earlier speaker; a round where nobody objects to anything on a cross-domain question is a sign the voices were not separated, so the reviewer looks again before closing.

**Edit lock.** Until the user's own message approves, speakers and the chair read only: no file writes, no state-changing commands, no partial implementation. On Antigravity, `scripts/council_hook.py --on` enforces this with a `PreToolUse` hook in `.agents/hooks.json`.

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
- **`[maxilun-ui-designer]`**: Proposes a direction derived from the product Origin, a font pairing chosen per `../maxilun-craft/SKILL.md` §4.3 (a saturated default such as Inter, Space Grotesk, Geist, Plus Jakarta Sans, or JetBrains Mono needs a written Origin reason), and a layout topology ranked from the content.
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

