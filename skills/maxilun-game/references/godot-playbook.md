# Godot Engine 4.x Architecture & Playbook

Standar rekayasa Godot 4.x: GDScript 2.0, modul GDExtension C++, arsitektur berbasis scene & node, shader, MultiplayerAPI, dan pengujian deterministik dengan gdUnit4.

---

## 1. Standar Bahasa GDScript 2.0

### 1.1 Static Typing & `@abstract`

Wajib gunakan static typing penuh pada seluruh variabel, parameter fungsi, dan return type:

```gdscript
class_name CombatEntity extends CharacterBody3D

@export var config: CharacterConfigResource
var current_health: float = 100.0

@abstract func execute_ability(ability_id: StringName, target_position: Vector3) -> bool
```

### 1.2 Semantik Lambda Capture-by-Value

Di Godot 4, lambda menangkap variabel lokal secara *by-value* saat pembuatan lambda. Mutasi variabel primitif di dalam lambda tidak memengaruhi variabel pemanggil:

```gdscript
# SALAH: hit tetap bernilai false pada pemanggil
var hit: bool = false
timer.timeout.connect(func(): hit = true)

# BENAR: Gunakan container tipe referensi (Dictionary / Object / Array)
var event_state: Dictionary = {"hit": false}
timer.timeout.connect(func(): event_state["hit"] = true)
```

### 1.3 Variadic Parameters

Parameter variadic dideklarasikan di posisi akhir fungsi menggunakan sintaks `...`:

```gdscript
func dispatch_game_event(event_name: StringName, ...args: Array) -> void:
    for arg in args:
        print_verbose("[EVENT %s]: %s" % [event_name, str(arg)])
```

---

## 2. Arsitektur Data-Driven & Pemisahan UI

Semua data statistik dan konfigurasi mekanik disimpan dalam berkas Resource (`.tres`), bukan di-hardcode dalam logika node:

```gdscript
class_name WeaponDataResource extends Resource

@export var weapon_id: StringName = &"plasma_rifle"
@export var base_damage: float = 35.0
@export var fire_rate_seconds: float = 0.15
@export var projectile_speed: float = 45.0
@export var energy_cost: float = 8.0
```

### Komunikasi Bebas Coupling dengan Signal:
Sistem gameplay dilarang memanggil komponen visual atau UI secara langsung:

```gdscript
# Logika gameplay memancarkan signal
signal health_depleted(entity: CharacterBody3D)
signal damage_received(current: float, max: float, delta: float)

func take_damage(amount: float) -> void:
    current_health = maxf(0.0, current_health - amount)
    damage_received.emit(current_health, config.max_health, amount)
    if current_health <= 0.0:
        health_depleted.emit(self)
```

Komponen UI HUD terhubung ke signal tersebut secara deklaratif via editor atau skrip scene controller.

---

## 3. Fisika & Game Loop

1. **Jolt Physics 3D**: Gunakan mesin fisika Jolt untuk stabilitas tumbukan dan determinisme yang lebih tinggi pada 3D.
2. **Delta Time Invariant**:
   - Seluruh translasi berbasis waktu di `_physics_process(delta)` wajib mengalikan parameter kecepatan dengan `delta`.
   - Gunakan `move_and_slide()` untuk `CharacterBody3D` di mana `velocity` internal sudah memperhitungkan satuan detik.

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

Gunakan `MultiplayerAPI` dengan peran server yang otoritatif. Klien mengirim input atau RPC perintah aksi, server mengeksekusi validasi logika dan menyinkronkan state via RPC:

```gdscript
@rpc("any_peer", "call_local", "reliable")
func request_fire_weapon(aim_target: Vector3) -> void:
    var sender_id: int = multiplayer.get_remote_sender_id()
    # Hanya server yang berhak memvalidasi dan memproses peluru
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

## 5. Pengujian Otomasi dengan gdUnit4

Semua pengujian unit gameplay wajib menghindari memory leak dan orphan node menggunakan wrapper `auto_free()`:

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

Eksekusi CLI headless:
```bash
godot --headless --path . -s addons/gdUnit4/bin/GdUnitCmdTool.gd --test-dir tests/
```
