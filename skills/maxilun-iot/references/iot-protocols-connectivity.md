# IoT Connectivity & Protocol Engineering (MQTT, BLE, Modbus, OTA)

Panduan implementasi protokol telemetri, jaringan nirkabel IoT, bus industri, dan pembaruan firmware aman.

## 1. Protokol Telemetri MQTT (TLS & State LWT)

### 1.1 Pola Koneksi & Keep-Alive
- **Last Will and Testament (LWT)**: Daftarkan pesan wasiat saat inisialisasi koneksi MQTT agar broker mempublikasikan status `offline` secara otomatis jika perangkat mati mendadak atau kehilangan sinyal.
- **Tingkat QoS**:
  - Gunakan `QoS 0` untuk telemetri sensor berfrekuensi tinggi (suhu per detik di mana kehilangan 1 paket tidak fatal).
  - Gunakan `QoS 1` untuk status alarm, event perintah, atau pengakuan konfigurasi.
  - Hindari `QoS 2` pada mikrokontroler dengan memori terbatas jika tidak sungguh diperlukan.
- **Enkripsi TLS**: Wajib gunakan port TLS `8883` dengan validasi sertifikat root CA broker untuk mencegah penyadapan kredensial di jaringan publik.

---

## 2. Bluetooth Low Energy (BLE GATT)

- **Desain Profil GATT**: Kelompokkan fungsionalitas ke dalam Service UUID yang terpisah (misalnya Device Info Service, Sensor Data Service, Configuration Service).
- **Properti Karakteristik**:
  - Gunakan `Notify` untuk streaming data satu arah alih-alih polling konstan oleh klien mobile.
  - Batasi ukuran payload sesuai negotiated MTU (default 23 byte; negosiasikan hingga 512 byte untuk transfer data cepat).

---

## 3. Bus Industri: Modbus RTU & RS-485

- **Kontrol Pin Arah Transceiver (DE/RE)**:
  Pada RS-485 half-duplex, aktifkan pin Driver Enable sebelum mengirim byte pertama dan nonaktifkan kembali segera setelah byte terakhir keluar dari shift register UART hardware (periksa bit `TEMT` / transmitter empty, bukan hanya `TXE` buffer empty).
- **Validasi Frame Modbus**:
  Hitung dan verifikasi CRC-16 Modbus (polinomial `0xA001`) pada setiap paket yang masuk. Buang paket yang gagal validasi tanpa memproses isi register.

---

## 4. Pembaruan Firmware Over-The-Air (OTA) & Rollback

Terapkan partisi dual-boot A/B (`ota_0` dan `ota_1`) dengan mekanisme anti-bricking:
1. Unduh payload firmware baru melalui koneksi HTTPS aman.
2. Tulis binary ke partisi non-aktif.
3. Set partisi boot berikutnya ke partisi baru.
4. Lakukan reboot perangkat.
5. **Uji Mandiri (Self-Test)**: Jalankan pemeriksaan komunikasi sensor dan koneksi server dalam waktu 30 detik pertama:
   - Jika lulus: Panggil `esp_ota_mark_app_valid_cancel_rollback()`.
   - Jika gagal atau terjadi watchdog timeout: Bootloader secara otomatis membatalkan pembaruan dan memutar kembali (*rollback*) ke partisi firmware lama yang stabil.
