# Game Feel & Juice: Tactile Physicality & Combat Feedback

> **Status**: Reference Document  
> **Specialist**: `maxilun-game` & `maxilun-motion`  
> **Source Attribution**: Synthesized from Game Feel Prompts (see `CREDITS.md`)

"Juice" is the non-functional audiovisual feedback that gives digital interactions tangible weight, visceral satisfaction, and physical momentum. Without juice, mechanics feel dry, clinical, and unresponsive. This reference documents implementation recipes across Godot 4, Unity, and interactive WebGL/Canvas runtimes.

---

## 1. Combat & Impact Feedback

### A. Hit Stop (Frame Freeze)
When a weapon connects with a target, freezing execution for 3–6 frames (50ms–100ms) conveys physical resistance and destructive force before continuing animation:

#### Godot 4 GDScript
```gdscript
# Autoload or CombatManager.gd
func hit_stop(duration_sec: float = 0.08, time_scale: float = 0.05) -> void:
    Engine.time_scale = time_scale
    await get_tree().create_timer(duration_sec * time_scale).timeout
    Engine.time_scale = 1.0
```

### B. Camera Shake (Trauma Model)
Linear camera shake feels like cheap vibration. The polynomial trauma model creates natural, organic impacts that decay gracefully:

$$\text{trauma} = \max(0, \text{trauma} - \text{recovery\_rate} \times \Delta t)$$
$$\text{offset} = \text{max\_offset} \times (\text{trauma})^2 \times \text{noise}(t)$$

#### Godot 4 GDScript
```gdscript
extends Camera2D

@export var decay: float = 1.2
@export var max_offset: Vector2 = Vector2(16, 12)
@export var max_roll: float = 0.05
var trauma: float = 0.0
var noise = FastNoiseLite.new()
var noise_y: float = 0.0

func _ready() -> void:
    randomize()
    noise.seed = randi()
    noise.frequency = 0.5

func add_trauma(amount: float) -> void:
    trauma = min(trauma + amount, 1.0)

func _process(delta: float) -> void:
    if trauma > 0.0:
        trauma = max(trauma - decay * delta, 0.0)
        noise_y += delta * 50.0
        var shake = trauma * trauma # Quadratic curve for natural feel
        offset.x = max_offset.x * shake * noise.get_noise_2d(noise.seed, noise_y)
        offset.y = max_offset.y * shake * noise.get_noise_2d(noise.seed + 1, noise_y)
        rotation = max_roll * shake * noise.get_noise_2d(noise.seed + 2, noise_y)
    else:
        offset = Vector2.ZERO
        rotation = 0.0
```

---

## 2. Platforming & Control Polish

### A. Coyote Time & Jump Buffering
Strict collision physics frustrates players when jumping off ledges. Coyote Time and Jump Buffering deliver responsive, forgiving movement:

- **Coyote Time (100ms–150ms)**: Allows the player to jump briefly after stepping off a platform.
- **Jump Buffering (100ms)**: Stores a jump press input right before landing, triggering the jump on the exact landing frame.

#### Godot 4 GDScript
```gdscript
const COYOTE_TIME_SEC: float = 0.12
const JUMP_BUFFER_SEC: float = 0.10

var coyote_timer: float = 0.0
var jump_buffer_timer: float = 0.0

func _physics_process(delta: float) -> void:
    if is_on_floor():
        coyote_timer = COYOTE_TIME_SEC
    else:
        coyote_timer -= delta

    if Input.is_action_just_pressed("jump"):
        jump_buffer_timer = JUMP_BUFFER_SEC
    else:
        jump_buffer_timer -= delta

    # Execute jump when both conditions align
    if jump_buffer_timer > 0.0 and coyote_timer > 0.0:
        velocity.y = JUMP_VELOCITY
        jump_buffer_timer = 0.0
        coyote_timer = 0.0
        apply_squash_and_stretch(Vector2(0.8, 1.25)) # Stretch upward on launch
```

### B. Squash and Stretch
Physical characters compress before launching and flatten on impact:

- **Jump Launch**: $X = 0.8, Y = 1.25$ (Stretch upward).
- **Hard Landing**: $X = 1.3, Y = 0.7$ (Squash downward).
- Rebound to $1.0$ within 120ms via an exponential damped spring.

---

## 3. UI & HUD Juice

### A. Delayed Health Bar Chip (Fighting Game Standard)
When health drops, the primary bar drains instantly while a ghost white bar lingers for 300ms before smoothly catching up:

```tsx
"use client";

import * as React from "react";

export function JuicyHealthBar({ currentHp, maxHp }: { currentHp: number; maxHp: number }) {
  const percentage = Math.max(0, Math.min(100, (currentHp / maxHp) * 100));
  const [chipPercentage, setChipPercentage] = React.useState(percentage);

  React.useEffect(() => {
    const timer = setTimeout(() => {
      setChipPercentage(percentage);
    }, 350); // 350ms delay before ghost bar catches up
    return () => clearTimeout(timer);
  }, [percentage]);

  return (
    <div className="relative w-64 h-4 bg-neutral-900 rounded-full overflow-hidden border border-neutral-800 p-0.5">
      {/* Delayed Ghost Chip Bar */}
      <div
        className="absolute inset-0.5 origin-left bg-neutral-200/60 rounded-full transition-transform duration-200 ease-out"
        style={{ transform: `scaleX(${chipPercentage / 100})` }}
      />
      {/* Primary Immediate HP Bar */}
      <div
        className="relative h-full w-full origin-left bg-emerald-500 rounded-full transition-transform duration-100 ease-linear ring-1 ring-emerald-400/40"
        style={{ transform: `scaleX(${percentage / 100})` }}
      />
    </div>
  );
}
```

---

## 4. Accessibility Invariant

All dynamic screen shakes and flashing lights MUST respect the global accessibility preference:
- In Web runtimes: check `@media (prefers-reduced-motion: reduce)` and cap camera offset at `Vector2.ZERO`.
- In Native Game Engines: provide an in-game "Screen Shake: [Off / 50% / 100%]" toggle in accessibility options.

