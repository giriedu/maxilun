# Embedded Systems & Microcontroller Engineering Playbook

Production embedded engineering guide for microcontrollers (ESP32, STM32, Arduino, Raspberry Pi Pico), FreeRTOS, and hardware bus protocols.

## 1. Memory Architecture & ISR (Interrupt Service Routine) Rules

### 1.1 Interrupt Handling (ISR) Invariant
- **Zero heap allocation**: Never use dynamic allocation (`malloc`, `free`, `new`, `delete`) inside an ISR.
- **Shared variables (`volatile`)**: Declare every variable that is read in the main loop and modified in an ISR as `volatile` (or use C11/C++20 atomics).
- **Deferred processing**:
  An ISR only records a flag or sends a message to a FreeRTOS queue (`xQueueSendFromISR`), then signals a yield (`portYIELD_FROM_ISR`). Run long computation in a regular worker task.

### 1.2 FreeRTOS Tasks & Stack Budget
- Size each task stack deliberately (for example 2048 to 4096 words).
- Monitor the memory high-water mark with `uxTaskGetStackHighWaterMark()`. A stack overflow causes an immediate fatal crash.
- Assign task priorities correctly: high-speed I/O tasks get higher priority than background telemetry logging.

---

## 2. Hardware Bus Drivers (I2C, SPI, UART, GPIO)

### 2.1 I2C Bus
- Fit physical pull-up resistors (typically 2.2kΩ to 4.7kΩ) on the SDA and SCL lines.
- Give every sensor register read a timeout. Do not use an unbounded `while(!flag)` loop; it freezes the microprocessor permanently when a sensor cable comes loose:
  ```c
  esp_err_t err = i2c_master_cmd_begin(I2C_NUM_0, cmd, pdMS_TO_TICKS(50));
  if (err != ESP_OK) {
      ESP_LOGE(TAG, "I2C read timeout or NACK: %s", esp_err_to_name(err));
      i2c_driver_delete(I2C_NUM_0);
      i2c_param_config(I2C_NUM_0, &conf);
      i2c_driver_install(I2C_NUM_0, conf.mode, 0, 0, 0);
  }
  ```

### 2.2 SPI Bus & DMA
- Use Direct Memory Access (DMA) transfers for large payloads (for example a TFT display or external SPI flash reads) to free CPU core cycles.
- Deassert the Chip Select (CS) pin when the transfer completes.

### 2.3 GPIO & Debouncing
- Debounce buttons in hardware (RC capacitor) or software (timer of at least 20–50ms) before triggering an action event.

---

## 3. Watchdog Timer (WDT) & Low-Power Modes

1. **Task Watchdog Timer (TWDT)**:
   Register every continuous task with the Watchdog Timer. Feed the watchdog (`esp_task_wdt_reset()`) on every iteration of the main loop.
2. **Deep sleep & power consumption profile**:
   Turn off unused peripherals, disconnect Wi-Fi/Bluetooth cleanly, and configure the wake-up pin before entering deep sleep:
   ```c
   esp_sleep_enable_ext0_wakeup(GPIO_NUM_33, 0); // Wake on LOW level
   esp_deep_sleep_start();
   ```
3. **NVS / flash storage endurance**:
   Use an NVS partition with wear leveling for configuration storage. Avoid periodic per-second writes to internal flash.
