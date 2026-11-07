# PowerBuilder & Enterprise Desktop Engineering Playbook

Panduan rekayasa mendalam untuk pemeliharaan, refaktor, dan modernisasi aplikasi PowerBuilder (Appeon / Sybase PB 9 s/d 2022+), DataWindow engine, PowerScript, dan integrasi enterprise.

## 1. Arsitektur Objek & Transaksi PowerBuilder

### 1.1 Siklus Hidup Transaksi & `SQLCA`
- **Inisialisasi**: Hubungkan `SQLCA` hanya sekali per sesi kerja atau gunakan koneksi terisolasi untuk proses batch latar belakang.
- **`SetTransObject` vs `SetTrans`**:
  - Gunakan `dw_1.SetTransObject(SQLCA)`: Mengizinkan aplikasi mengontrol transaksi (`CONNECT`, `COMMIT`, `ROLLBACK`) dan menjaga koneksi tetap terbuka.
  - Jangan gunakan `dw_1.SetTrans(SQLCA)` untuk transaksi beruntun karena memutus dan menyambung koneksi setiap kali `Retrieve()` dijalankan.
- **Pola Transaksi Aman**:
  ```powerscript
  // Eksekusi transaksi dengan validasi kode status
  dw_order.AcceptText()
  IF dw_order.Update(True, False) = 1 THEN
      IF dw_details.Update(True, False) = 1 THEN
          COMMIT USING SQLCA;
          dw_order.ResetUpdate()
          dw_details.ResetUpdate()
      ELSE
          ROLLBACK USING SQLCA;
          MessageBox("Error", "Gagal memperbarui rincian: " + SQLCA.SQLErrText, StopSign!)
      END IF
  ELSE
      ROLLBACK USING SQLCA;
      MessageBox("Error", "Gagal memperbarui header: " + SQLCA.SQLErrText, StopSign!)
  END IF
  ```

### 1.2 Hirarki Objek PB
- **Application (`.sra`)**: Entry point; tangani `open`, `close`, dan `systemerror`. Tangkap error fatal di `systemerror` untuk logging ke berkas sebelum crash.
- **Window (`.srw`)**: Tipe window (`Main!`, `Response!`, `Child!`, `Popup!`). Pastikan response window selalu modal dan membebaskan memori saat ditutup.
- **User Object (`.sru`)**: Pisahkan logika bisnis ke Custom Non-Visual Object (NVO). Dilarang menempatkan query kompleks langsung di event tombol window.
- **Menu (`.srm`)**: Sinkronkan hak akses menu dengan role pengguna saat login.

---

## 2. Standar DataWindow Engine

### 2.1 Manajemen Buffer DataWindow
DataWindow mengelola 4 buffer internal. Jangan manipulasi buffer secara spekulatif:
1. **`Primary!`**: Baris data aktif yang terlihat dan dapat diedit oleh pengguna.
2. **`Filter!`**: Baris yang disaring keluar melalui ekspresi filter `dw_1.SetFilter()`.
3. **`Delete!`**: Baris yang dihapus melalui `dw_1.DeleteRow()`. Baris ini dikonversi menjadi perintah `DELETE` SQL saat `dw_1.Update()`.
4. **`Original!`**: Nilai awal kolom sebelum diubah, digunakan untuk verifikasi *concurrency conflict* pada klausa `WHERE`.

### 2.2 Penanganan Event Kritis
- **`ItemChanged`**:
  - Gunakan data argumen `data` bukan `GetItem...` karena buffer belum diperbarui.
  - Nilai balik:
    - `0`: Terima nilai dan ubah data.
    - `1`: Tolak nilai dan jangan izinkan fokus berpindah.
    - `2`: Tolak nilai tetapi izinkan fokus berpindah (kembalikan ke nilai lama).
- **`ItemError`**: Cegah dialog sistem bawaan yang membingungkan pengguna dengan mengembalikan nilai `1` atau `3` setelah menampilkan pesan error terstruktur.
- **`RetrieveStart` / `RetrieveEnd`**: Gunakan `dw_1.SetRedraw(False)` sebelum manipulasi visual banyak baris dan `dw_1.SetRedraw(True)` di akhir.

### 2.3 Sintaks Definisi DataWindow (`.srd`)
Format berkas `.srd` adalah spesifikasi deklaratif internal. Saat mengaudit atau memperbaiki `.srd`:
- Periksa konsistensi tipe data kolom di blok `table(...)` dengan tipe database.
- Hindari hardcode koneksi database di dalam properti DataWindow.
- Validasi edit style DropDownDataWindow (`DDDW`) agar kolom display dan data match dengan tabel referensi.

---

## 3. Integrasi Modern & Interoperabilitas

1. **REST API & JSON**:
   Gunakan komponen native Appeon PB `HTTPClient`, `JSONParser`, dan `JSONGenerator` untuk menghubungkan aplikasi legacy ke microservices modern.
2. **Panggilan DLL Native (C/C++)**:
   Deklarasikan library eksternal dengan konvensi pemanggilan tepat (`alias for ...` dan tipe parameter pas: `long` 32-bit vs `longlong` 64-bit pada PB 64-bit).
3. **PFC (PowerBuilder Foundation Class)**:
   Saat bekerja pada sistem berbasis PFC, hormati arsitektur service-oriented (`pfc_u_dw`, `pfc_n_cst_dwsrv`). Aktifkan service yang dibutuhkan saja (`of_SetUpdateChecks`, `of_SetSort`).
