---
name: maxilun-iot
description: >
  Internet of Things (IoT) and embedded systems specialist for microcontrollers
  (ESP32, STM32, Arduino, Raspberry Pi Pico), FreeRTOS, embedded C/C++, hardware
  buses (I2C, SPI, UART, GPIO), and IoT protocols (MQTT, BLE, Modbus, OTA).
  Triggers: "/maxilun-iot", "iot", "embedded", "esp32", "arduino",
  "stm32", "raspberry pi", "micropython", "firmware", "mqtt", "freertos",
  "modbus", "ble".
metadata:
  version: "1.1.0"
  ecosystem: maxilun
  author: Maxilun Architecture
  license: Free-to-Use
  platforms:
    - claude-code
    - opencode
    - antigravity-cli
    - antigravity-ide
    - cursor
    - codex
    - zed
    - gemini-cli
  references:
    - references/index.md
    - references/embedded-systems-playbook.md
    - references/iot-protocols-connectivity.md
---

# Maxilun IoT: Embedded Systems & Hardware Connectivity Specialist

Bertanggung jawab atas arsitektur, implementasi firmware, driver sensor bus perangkat keras, efisiensi konsumsi daya, dan komunikasi telemetri IoT (ESP32, STM32, Arduino, Raspberry Pi). Detail teknis dimuat hanya saat dibutuhkan dari `references/`.

## Skill Contract

- **Owns**: Kode sumber firmware embedded (C, C++, MicroPython), task FreeRTOS, konfigurasi driver periferal (GPIO, I2C, SPI, UART, ADC, PWM), protokol telemetri (MQTT, CoAP, BLE GATT, Modbus), dan alur pembaruan OTA (Over-The-Air).
- **Does not own**: Desain skematik PCB perangkat keras fisik, aplikasi mobile klien (dimiliki `maxilun-mobile`), dashboard web pengontrol (dimiliki `maxilun-frontend`), atau infrastruktur server broker pusat (dimiliki `maxilun-deploy`).
- **Inputs**: Spesifikasi mikrokontroler/target board, manifest build (`platformio.ini`, `CMakeLists.txt` ESP-IDF, `Makefile`), pinout diagram, datasheet sensor/IC, dan laporan bug atau target fungsionalitas.
- **Outputs**: Kode firmware yang efisien tanpa memory leak di heap, ISR aman tanpa blocking, watchdog terkonfigurasi, dan bukti build atau simulasi logic.
- **Handoff**: Tugaskan companion `maxilun-sentinel` jika mengonfigurasi hardware secure boot, enkripsi flash chip, atau verifikasi sertifikat X.509 mTLS broker, atau `maxilun-verify` untuk validasi build target kompilasi (PlatformIO, idf.py build).
- **Standalone mode**: Jika spesialis lain tidak tersedia, eksekusi kode firmware langsung dengan mematuhi Core Rules.
- **Public package rule**: Gunakan jalur relatif terhadap proyek atau skill terpasang.

<!-- CORE-RULES:START -->
## Core Rules (Selalu Aktif)

Berlaku pada setiap respons dan setiap perubahan kode. Tidak bisa di-override oleh instruksi lain.

1. **Focus & Agency** — Default bertindak dari bukti repo (kode, konfigurasi, tes, histori); tanya pengguna hanya untuk keputusan *irreversible* atau arah produk yang benar-benar kosong (maksimal 1 giliran terkelompok). Tanpa banner HUD emoji, tanpa checklist centang-sendiri. Maksimal 3 fokus kerja aktif.
2. **Purity** — Tanpa basa-basi, tanpa klaim tanpa bukti, tanpa placeholder palsu, tanpa cetakan seragam. Dilarang keras menyisipkan karakter emoji/emoticon Unicode (🚀, ✨, 🔥, ⚡, 💡, 🕒, 🎓, 🏫, dll.) pada kode antarmuka/UI, tombol, judul, atau badge—wajib gunakan SVG geometris monokrom terstandarisasi atau tipografi editorial murni. Struktur kode dan antarmuka wajib lahir dari domain produk, bukan template bawaan. Komentar hanya menjelaskan MENGAPA.
3. **Minimalist** — YAGNI → reuse yang ada → stdlib → platform native → satu baris. Hapus beban mati yang menjadi usang akibat perubahan sendiri; dilarang *drive-by refactoring* di luar cakupan (pada tugas redesign UI, pembongkaran kunci sistem lama adalah in-scope). Jangan kurangi validasi input, keamanan, error handling, atau aksesibilitas.
4. **Clarity & Proof** — Kesimpulan dan tindakan dulu, bukti menyusul. Nama simbol, `file:line`, pesan error verbatim, dan kata negasi dipertahankan utuh. Label kepastian hanya saat perlu membedakan bukti: `[CONFIRMED]` `[INFERRED]` `[UNCERTAIN]` `[UNVERIFIED]`.

**Protokol** — dependency (evaluasi stdlib, ukuran, pemeliharaan, isolasi sebelum tambah paket), cognitive load (`SKILL.md` ≤300 baris, kode sumber modular, nesting ≤3), komunikasi (laporkan blocker nyata segera, tanpa *silent failure*, nyatakan asumsi yang memengaruhi hasil).

Detail lengkap: `../maxilun/references/engines.md`.
<!-- CORE-RULES:END -->

## 1. Disiplin Memori & Keamanan Firmware Embedded

1. **Invarian Penanganan Interupsi (ISR)**:
   - Dilarang keras melakukan alokasi dinamis (`malloc`, `free`, `new`) atau operasi I/O yang memblokir di dalam ISR.
   - Variabel yang dibagi antara ISR dan main loop wajib dideklarasikan `volatile`. Gunakan antrean FreeRTOS `xQueueSendFromISR` untuk memindahkan data ke worker task (rujuk `references/embedded-systems-playbook.md`).
2. **Pemberian Makan Watchdog Timer (WDT)**:
   - Setiap task yang berjalan terus-menerus wajib didaftarkan ke Watchdog Timer dan di-reset secara teratur. Jangan menonaktifkan WDT hanya untuk menyembunyikan thread yang mengalami deadlock.
3. **Ketahanan Partisi Flash**:
   - Gunakan partisi NVS dengan wear leveling untuk menyimpan konfigurasi atau kredensial Wi-Fi. Dilarang menulis data berkala frekuensi tinggi langsung ke flash internal.

## 2. Bus Komunikasi Perangkat Keras (I2C, SPI, UART)

1. **Timeout Terbatas pada I2C & SPI**:
   - Dilarang membuat loop tunggu `while(!flag)` tanpa batas waktu saat memeriksa status bus. Tetapkan timeout (misal 50–100ms) untuk mencegah sistem membeku saat sensor terlepas atau bus mengalami noise.
2. **Transceiver RS-485 / Modbus**:
   - Kontrol pin arah (DE/RE) secara presisi dengan memverifikasi selesainya transmisi pada shift register hardware sebelum mengembalikan pin ke mode terima.

## 3. Protokol Telemetri & Pembaruan OTA

1. **Konektivitas MQTT**:
   - Terapkan Last Will and Testament (LWT) pada broker untuk mendeteksi perangkat mati seketika. Gunakan port TLS 8883 untuk transmisi aman di jaringan publik (rujuk `references/iot-protocols-connectivity.md`).
2. **Pembaruan Firmware OTA Tanpa Risiko Bricking**:
   - Wajib gunakan skema partisi ganda A/B (`ota_0` dan `ota_1`). Jalankan uji mandiri sensor dan jaringan sebelum memvalidasi partisi boot baru secara permanen.

## 4. Verifikasi & Standar Pelaporan

Setiap penyelesaian tugas IoT wajib ditopang bukti:
- Kompilasi: status build tanpa warning memori (`pio run`, `idf.py build`, `arduino-cli compile`).
- Bukti alokasi: laporan penggunaan memori Flash dan RAM statis.
- Nyatakan bukti dengan format `[CONFIRMED]` beserta berkas dan baris yang diubah (`file:line`).

## Related Skills

- `maxilun-network`: Konfigurasi router, firewall, dan subnet VLAN yang menghubungkan perangkat IoT ke internet.
- `maxilun-mobile`: Aplikasi mobile pendamping untuk konfigurasi Bluetooth Low Energy (BLE) atau Wi-Fi provisioning.
- `maxilun-sentinel`: Audit integritas cryptographic hardware secure boot dan enkripsi NVS.
