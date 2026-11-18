# IoT Connectivity & Protocol Engineering (MQTT, BLE, Modbus, OTA)

Implementation guide for telemetry protocols, IoT wireless networking, industrial buses, and secure firmware updates.

## 1. MQTT Telemetry Protocol (TLS & LWT State)

### 1.1 Connection Pattern & Keep-Alive
- **Last Will and Testament (LWT)**: Register a will message when initializing the MQTT connection, so the broker publishes an `offline` status automatically if the device dies suddenly or loses signal.
- **QoS levels**:
  - Use `QoS 0` for high-frequency sensor telemetry (per-second temperature, where losing 1 packet is not fatal).
  - Use `QoS 1` for alarm status, command events, or configuration acknowledgements.
  - Avoid `QoS 2` on memory-constrained microcontrollers unless it is truly required.
- **TLS encryption**: Use TLS port `8883` and validate the broker's root CA certificate, to prevent credential interception on public networks.

---

## 2. Bluetooth Low Energy (BLE GATT)

- **GATT profile design**: Group functionality into separate Service UUIDs (for example Device Info Service, Sensor Data Service, Configuration Service).
- **Characteristic properties**:
  - Use `Notify` for one-way data streaming instead of constant polling by the mobile client.
  - Limit payload size to the negotiated MTU (default 23 bytes; negotiate up to 512 bytes for fast data transfer).

---

## 3. Industrial Bus: Modbus RTU & RS-485

- **Transceiver direction pin control (DE/RE)**:
  On half-duplex RS-485, assert the Driver Enable pin before sending the first byte and deassert it immediately after the last byte leaves the hardware UART shift register (check the `TEMT` / transmitter empty bit, not just the `TXE` buffer empty bit).
- **Modbus frame validation**:
  Compute and verify the Modbus CRC-16 (polynomial `0xA001`) on every incoming packet. Discard a packet that fails validation without processing its register contents.

---

## 4. Over-The-Air (OTA) Firmware Updates & Rollback

Use dual-boot A/B partitions (`ota_0` and `ota_1`) with an anti-bricking mechanism:
1. Download the new firmware payload over a secure HTTPS connection.
2. Write the binary to the inactive partition.
3. Set the next boot partition to the new partition.
4. Reboot the device.
5. **Self-test**: Check sensor communication and the server connection within the first 30 seconds:
   - If it passes: call `esp_ota_mark_app_valid_cancel_rollback()`.
   - If it fails or a watchdog timeout occurs: the bootloader automatically cancels the update and rolls back to the old, stable firmware partition.
