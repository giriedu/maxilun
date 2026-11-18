# Game Design Lifecycle & Balancing Playbook

Method for writing a Game Design Document (GDD), formulating mathematical balancing models, staging studio production, and budgeting game runtime performance.

---

## 1. Standard GDD Specification (8 Required Sections)

Every game system design document must contain the eight deterministic sections below, so the engineering implementation has no logic ambiguity:

1. **Overview**: The system's function, its purpose in the game loop, and its target audience, in 2–3 plain sentences.
2. **Player Fantasy**: The mechanic's effect on player experience and agency (for example: "The player feels the tension of resource management when stamina runs out mid-attack").
3. **Detailed Rules**: Deterministic mechanic logic flow, state transitions, win/lose conditions, input mapping, and interactions between systems.
4. **Formulas**: Formal numeric calculations (damage, experience calculation, drop rates, cooldown scaling).
5. **Edge Cases**: Handling of extreme conditions (disconnection during a trade, a frame drop inside the input buffer window, simultaneous conflicting inputs, death while a skill animation is active).
6. **Dependencies**: The list of external module dependencies (UI HUD, audio triggers, persistent save system, inventory data, network replication).
7. **Tuning Knobs**: Numeric parameters a designer can adjust without touching code (base speed, multiplier, duration, tick rate).
8. **Acceptance Criteria**: Measurable conditions that validate feature completion and can be tested empirically through an automated test.

---

## 2. Mathematical Model & Balancing Formulas

### 2.1 Damage Mitigation Formula

Avoid pure flat stat subtraction ($Damage - Armor$). It tends to produce zero values or exploitable invulnerability. Use a *diminishing returns* curve model:

$$DamageTaken = RawDamage \times \left(\frac{K}{K + Armor}\right)$$

Where $K$ is the armor constant (for example $K = 100$).
- $Armor = 100 \implies \text{damage reduced by } 50\%$.
- $Armor = 300 \implies \text{damage reduced by } 75\%$.
- Each additional 1 point of Armor consistently raises Effective Health Pool (EHP) by $1/K$ of Base Health.

### 2.2 Level Progression & Experience Curve

Use a controlled polynomial or exponential for leveling progression:

$$XP_{Required}(Level) = A \times Level^B + C \times Level$$

Example parameters for a standard RPG curve: $A = 50, B = 2, C = 100$.
- Level 1 to 2: $50(1)^2 + 100(1) = 150 \text{ XP}$.
- Level 10 to 11: $50(10)^2 + 100(10) = 6000 \text{ XP}$.

### 2.3 Time-To-Kill (TTK) Budgeting Formula

The TTK budget sets the rhythm of combat:

$$TTK = \frac{TargetHealth}{DamagePerSecond \times (1 - MitigationRatio)}$$

- *Fast Paced Tactical*: Target TTK 0.2s – 0.6s.
- *Hero Shooter / Arena*: Target TTK 1.2s – 2.5s.
- *MMORPG / Raid Boss*: Target TTK 180s – 600s.

### 2.4 Closed Economy System (Sinks & Sources)

Every game currency or resource must have an equilibrium equation:

$$\Delta Currency = \sum Sources(Inflow) - \sum Sinks(Outflow)$$

- **Sources**: Missions, enemy drops, daily rewards, incoming trades.
- **Sinks**: Gear repair costs, market transaction tax, consumable upgrades, stat rerolls.
- Designer rule: Without a *sink* proportional to the *inflow*, the economy enters hyperinflation that breaks the long-term progression system.

---

## 3. Game Studio Production Stages

Run the studio production cycle in stages, each with an empirical evaluation gate:

```
[Concept / Brief] -> [Systems GDD] -> [Prototype] -> [Vertical Slice] -> [Production] -> [Polish & QA] -> [Gold Master]
```

1. **Concept / Game Brief**: A 1–2 page document that defines the *core hook*, game pillars, target platforms, and technical constraints.
2. **Systems GDD**: A detailed breakdown of every mechanic into the 8 GDD sections before any code is written.
3. **Prototype (Greybox)**: Validate the core mechanic (*game feel*, controls, responsiveness) with primitive geometry and no final assets. It answers the question: "Is the core mechanic fun to play?"
4. **Vertical Slice**: A 5–15 minute piece of the game at fully representative quality (graphics, audio, HUD, stable 60 FPS performance, save data). It serves as the *quality benchmark* for every later production phase.
5. **Production**: Scale content (levels, enemy variety, quests, balancing) on the architecture proven in the Vertical Slice.
6. **Polish & QA**: Frame pacing optimization, regression bug fixes, memory allocation profiling, audio mixing, and platform compliance.
7. **Gold Master / Release**: The finalized build that passes platform certification, cross-resolution smoke tests, and zero-crash verification.

---

## 4. Runtime Performance Budget & Frame Pacing

Set the target frame rate in the project's first phase, with a strict frame time budget allocation:

| Target FPS | Total Frame Budget | CPU Gameplay & Physics | Render & Draw Calls | GPU Shading & Post-Process |
|---|---|---|---|---|
| **60 FPS** | 16.67 ms | $\le 6.0\text{ ms}$ | $\le 4.5\text{ ms}$ | $\le 6.0\text{ ms}$ |
| **120 FPS** | 8.33 ms | $\le 3.0\text{ ms}$ | $\le 2.0\text{ ms}$ | $\le 3.3\text{ ms}$ |
| **30 FPS (Mobile)** | 33.33 ms | $\le 12.0\text{ ms}$ | $\le 8.0\text{ ms}$ | $\le 13.0\text{ ms}$ |

### Technical Performance Limits:
- **Draw Calls**: At most 500–1000 per frame for mid-range PC targets; at most 80–150 per frame for mobile devices.
- **Garbage Collection (GC) Allocation**: Must be 0 bytes per frame in the main loop (`_process`, `Update`, `Tick`). All dynamic instantiation must use a pre-allocated object pool.
- **Physics Ticks**: Run physics updates at a fixed frequency (for example 50 Hz or 60 Hz) with an isolated delta time accumulator to avoid *physics hitching*.
