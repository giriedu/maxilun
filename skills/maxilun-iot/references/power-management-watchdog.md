# Power Management, Watchdog Timers & Hardware Resilience

Engineering standards for ultra-low power modes, RTC memory persistence, hardware watchdog timers (WDT), and brownout protection in embedded microcontrollers.

---

## 1. Microcontroller Power Modes & Sleep Cycles

For battery-operated and edge sensor nodes (ESP32, STM32, RP2040):

| Sleep Mode | Typical ESP32 Current | Clock Domain | Wakeup Sources | Restored State |
|---|---|---|---|---|
| **Active** | 80–240 mA | All CPUs & Radios on | N/A | Full execution state |
| **Modem-sleep** | 20–40 mA | CPU active, Wi-Fi/BT paused | Network DTIM beacon | CPU registers & RAM intact |
| **Light-sleep** | 0.8–3 mA | CPU clock gated, RAM retained | Timer, GPIO, UART | Resumes immediately from sleep call |
| **Deep-sleep** | 10–150 µA | CPU & RAM off, RTC domain active | RTC Timer, EXT0/EXT1 GPIO | Reboots through `app_main`; RAM reset |

### State Retention via RTC Fast/Slow Memory
To preserve sensor readings, boot counts, or calibration offsets across deep-sleep cycles without wearing out internal flash:

```c
// ESP32: Store variable in RTC slow memory (persists across deep-sleep)
RTC_DATA_ATTR static uint32_t boot_count = 0;
RTC_DATA_ATTR static float last_temperature = 0.0f;

void app_main(void) {
    boot_count++;
    // Perform sensor read and MQTT transmission
    esp_sleep_enable_timer_wakeup(60ULL * 1000000ULL); // 60 seconds
    esp_deep_sleep_start();
}
```

---

## 2. Hardware Watchdog Timers (WDT) & Reset Handling

Never deploy embedded firmware with disabled watchdog timers.

1. **Task Watchdog Timer (TWDT)**:
   - Supervise high-priority worker threads. If a thread starves for CPU time or hangs in a blocking network call, trigger a deterministic reset.
   ```c
   // Initialize TWDT with 5-second timeout
   esp_task_wdt_config_t twdt_config = {
       .timeout_ms = 5000,
       .idle_core_mask = (1 << 0), // Monitor Core 0 idle task
       .trigger_panic = true,
   };
   esp_task_wdt_init(&twdt_config);
   esp_task_wdt_add(NULL); // Add current task
   ```
2. **Periodic Feeding Invariant**:
   - Call `esp_task_wdt_reset()` only after successful completion of a work loop, never from a blind periodic timer that masks real application deadlocks.
3. **Interrupt Watchdog Timer (IWDT)**:
   - Catches ISRs that exceed execution budget (e.g. `> 300 µs`). All ISRs must exit within microseconds.

---

## 3. Brownout Detection & Voltage Collapse Mitigation

When Wi-Fi or cellular modems transmit, transient current spikes can drop VDD below the minimum operating threshold:

1. **Hardware Brownout Detector**:
   - Set brownout threshold voltage to trip before RAM corruption occurs (e.g. 2.7V for a 3.3V system).
   - In battery-powered nodes, execute an emergency shutdown in the brownout ISR: close open flash handles and flush telemetry buffers.
2. **Capacitive Buffering**:
   - Ensure power rails provide at least $10\mu\text{F}$ to $100\mu\text{F}$ low-ESR ceramic capacitors close to the microcontroller VDD pins to absorb transmission burst transients.
