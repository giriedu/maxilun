# Embedded Systems & Microcontroller Engineering Playbook

Panduan rekayasa sistem embedded tingkat produksi untuk mikrokontroler (ESP32, STM32, Arduino, Raspberry Pi Pico), FreeRTOS, dan protokol bus perangkat keras.

## 1. Arsitektur Memori & Aturan ISR (Interrupt Service Routine)

### 1.1 Invarian Penanganan Interupsi (ISR)
- **Zero Heap Allocation**: Dilarang menggunakan alokasi dinamis (`malloc`, `free`, `new`, `delete`) di dalam ISR.
- **Variabel Bersama (`volatile`)**: Setiap variabel yang dibaca di main loop dan dimodifikasi di ISR wajib dideklarasikan `volatile` (atau gunakan atomic C11/C++20).
- **Penundaan Eksekusi (Deferred Processing)**:
  ISR hanya bertugas mencatat flag atau mengirim pesan ke antrean FreeRTOS (`xQueueSendFromISR`), kemudian memberikan sinyal yield (`portYIELD_FROM_ISR`). Logika komputasi panjang dijalankan di task worker biasa.

### 1.2 FreeRTOS Task & Anggaran Stack
- Tentukan ukuran stack task secara cermat (misalnya 2048 s/d 4096 words).
- Pantau water mark memori dengan `uxTaskGetStackHighWaterMark()`. Stack overflow langsung memicu crash fatal.
- Berikan prioritas task yang tepat: task I/O berkecepatan tinggi mendapat prioritas lebih tinggi daripada logging telemetri latar belakang.

---

## 2. Driver Bus Perangkat Keras (I2C, SPI, UART, GPIO)

### 2.1 Bus I2C
- Pasang resistor pull-up fisik (umumnya 2.2kΩ s/d 4.7kΩ) pada jalur SDA dan SCL.
- Setiap pembacaan register sensor wajib memiliki batas waktu (*timeout*). Jangan gunakan loop `while(!flag)` tanpa batas yang dapat menyebabkan mikroprosesor freeze permanen saat kabel sensor terlepas:
  ```c
  esp_err_t err = i2c_master_cmd_begin(I2C_NUM_0, cmd, pdMS_TO_TICKS(50));
  if (err != ESP_OK) {
      ESP_LOGE(TAG, "I2C read timeout or NACK: %s", esp_err_to_name(err));
      i2c_driver_delete(I2C_NUM_0);
      i2c_param_config(I2C_NUM_0, &conf);
      i2c_driver_install(I2C_NUM_0, conf.mode, 0, 0, 0);
  }
  ```

### 2.2 Bus SPI & DMA
- Gunakan transfer Direct Memory Access (DMA) untuk payload berukuran besar (misalnya display TFT atau pembacaan flash SPI eksternal) guna membebaskan siklus inti CPU.
- Pastikan pin Chip Select (CS) dinonaktifkan kembali saat transfer selesai.

### 2.3 GPIO & Debouncing
- Terapkan debouncing tombol secara perangkat keras (kapasitor RC) atau perangkat lunak (timer minimal 20–50ms) sebelum memicu event aksi.

---

## 3. Watchdog Timer (WDT) & Mode Daya Rendah

1. **Task Watchdog Timer (TWDT)**:
   Daftarkan setiap task berkelanjutan ke Watchdog Timer. Beri makan watchdog (`esp_task_wdt_reset()`) di setiap iterasi loop utama.
2. **Deep Sleep & Profil Konsumsi Daya**:
   Matikan periferal yang tidak digunakan, putuskan koneksi Wi-Fi/Bluetooth dengan rapi, dan konfigurasi pin wake-up sebelum memasuki deep sleep:
   ```c
   esp_sleep_enable_ext0_wakeup(GPIO_NUM_33, 0); // Bangun saat level LOW
   esp_deep_sleep_start();
   ```
3. **Ketahanan NVS / Flash Storage**:
   Gunakan partisi NVS dengan mekanisme *wear leveling* untuk penyimpanan konfigurasi. Hindari penulisan berkala per detik ke flash internal.
