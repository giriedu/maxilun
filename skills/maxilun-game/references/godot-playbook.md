# Godot Engine 4.x Architecture & Playbook

Godot 4.x engineering standards: GDScript 2.0, GDExtension C++ modules, scene and node based architecture, shaders, MultiplayerAPI, and deterministic testing with gdUnit4.

---

## 1. GDScript 2.0 Language Standards

### 1.1 Static Typing & `@abstract`

Apply full static typing to every variable, function parameter, and return type:

```gdscript
class_name CombatEntity extends CharacterBody3D

@export var config: CharacterConfigResource
var current_health: float = 100.0

@abstract func execute_ability(ability_id: StringName, target_position: Vector3) -> bool
```

### 1.2 Lambda Capture-by-Value Semantics

In Godot 4, a lambda captures local variables *by-value* at the moment the lambda is created. Mutating a primitive variable inside the lambda does not affect the caller's variable:

```gdscript
# WRONG: hit stays false in the caller
var hit: bool = false
timer.timeout.connect(func(): hit = true)

# RIGHT: use a reference-type container (Dictionary / Object / Array)
var event_state: Dictionary = {"hit": false}
timer.timeout.connect(func(): event_state["hit"] = true)
```

### 1.3 Variadic Parameters

Declare a variadic parameter in the last position of the function with the `...` syntax:

```gdscript
func dispatch_game_event(event_name: StringName, ...args: Array) -> void:
    for arg in args:
        print_verbose("[EVENT %s]: %s" % [event_name, str(arg)])
```

---

## 2. Data-Driven Architecture & UI Separation

Store all stat data and mechanic configuration in Resource files (`.tres`). Do not hardcode them in node logic:

```gdscript
class_name WeaponDataResource extends Resource

@export var weapon_id: StringName = &"plasma_rifle"
@export var base_damage: float = 35.0
@export var fire_rate_seconds: float = 0.15
@export var projectile_speed: float = 45.0
@export var energy_cost: float = 8.0
```

### Coupling-Free Communication with Signals:
Gameplay systems must not call visual or UI components directly:

```gdscript
# Gameplay logic emits signals
signal health_depleted(entity: CharacterBody3D)
signal damage_received(current: float, max: float, delta: float)

func take_damage(amount: float) -> void:
    current_health = maxf(0.0, current_health - amount)
    damage_received.emit(current_health, config.max_health, amount)
    if current_health <= 0.0:
        health_depleted.emit(self)
```

HUD UI components connect to these signals declaratively, through the editor or a scene controller script.

---

## 3. Physics & Game Loop

1. **Jolt Physics 3D**: Use the Jolt physics engine for more stable collisions and higher determinism in 3D.
2. **Delta Time Invariant**:
   - Every time-based translation in `_physics_process(delta)` must multiply the speed parameter by `delta`.
   - Use `move_and_slide()` for `CharacterBody3D`; its internal `velocity` is already expressed per second.

```gdscript
func _physics_process(delta: float) -> void:
    if not is_on_floor():
        velocity.y -= gravity * delta

    var input_dir: Vector2 = Input.get_vector(&"move_left", &"move_right", &"move_forward", &"move_back")
    var direction: Vector3 = (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()

    if direction != Vector3.ZERO:
        velocity.x = direction.x * config.move_speed
        velocity.z = direction.z * config.move_speed
    else:
        velocity.x = move_toward(velocity.x, 0, config.friction * delta)
        velocity.z = move_toward(velocity.z, 0, config.friction * delta)

    move_and_slide()
```

---

## 4. Multiplayer & Authoritative Netcode

Use `MultiplayerAPI` with an authoritative server role. The client sends input or action command RPCs. The server validates the logic and synchronizes state through RPC:

```gdscript
@rpc("any_peer", "call_local", "reliable")
func request_fire_weapon(aim_target: Vector3) -> void:
    var sender_id: int = multiplayer.get_remote_sender_id()
    # Only the server may validate and process the projectile
    if not multiplayer.is_server():
        return

    if not _validate_ammo_and_cooldown(sender_id):
        return

    _spawn_projectile_authoritative(aim_target)
    notify_weapon_fired.rpc(aim_target)

@rpc("authority", "call_local", "unreliable")
func notify_weapon_fired(aim_target: Vector3) -> void:
    _play_fire_fx(aim_target)
```

---

## 5. Automated Testing with gdUnit4

Every gameplay unit test must avoid memory leaks and orphan nodes by using the `auto_free()` wrapper:

```gdscript
class_name TestCombatHealth extends GdUnitTestSuite

func test_take_damage_reduces_health_accurately() -> void:
    var entity: CombatEntity = auto_free(CombatEntity.new())
    var mock_config: CharacterConfigResource = auto_free(CharacterConfigResource.new())
    mock_config.max_health = 100.0
    entity.config = mock_config
    entity.current_health = 100.0

    entity.take_damage(25.0)

    assert_float(entity.current_health).is_equal_approx(75.0, 0.001)

func test_lethal_damage_triggers_depleted_signal() -> void:
    var entity: CombatEntity = auto_free(CombatEntity.new())
    var mock_config: CharacterConfigResource = auto_free(CharacterConfigResource.new())
    mock_config.max_health = 50.0
    entity.config = mock_config
    entity.current_health = 50.0

    var signal_monitor: SignalMonitor = monitor_signals(entity)
    entity.take_damage(60.0)

    await assert_signal(signal_monitor).is_emitted("health_depleted")
```

Headless CLI run:
```bash
godot --headless --path . -s addons/gdUnit4/bin/GdUnitCmdTool.gd --test-dir tests/
```
