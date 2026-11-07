# Maxilun IoT & Embedded References Index

Indeks pustaka rekayasa sistem embedded, mikrokontroler, protokol telemetri, dan komunikasi nirkabel.

## Berkas Referensi Domain

1. **`embedded-systems-playbook.md`**:
   Aturan arsitektur mikrokontroler (ESP32 ESP-IDF, STM32 HAL, Arduino/PlatformIO), zero-heap ISR, FreeRTOS task & stack budgeting, driver bus I2C/SPI/UART/GPIO, hardware watchdog timer (WDT), dan manajemen mode deep sleep.
2. **`iot-protocols-connectivity.md`**:
   Protokol telemetri MQTT (QoS, TLS, LWT), profil BLE GATT (Notify, MTU), industri Modbus RTU / RS-485 transceiver timing, dan alur pembaruan firmware Over-The-Air (OTA) dengan dual-partition rollback.

## Panduan Pemuatan
- Tugas mikrokontroler, FreeRTOS, driver sensor, atau pin GPIO → baca `references/embedded-systems-playbook.md`.
- Tugas jaringan IoT, MQTT, BLE, Modbus, atau firmware OTA → baca `references/iot-protocols-connectivity.md`.
