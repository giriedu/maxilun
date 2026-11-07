# Android Native Engineering Playbook (Kotlin, Jetpack Compose, Gradle)

Panduan rekayasa aplikasi Android native modern berbasis Kotlin, deklaratif Jetpack Compose, arsitektur teruji, dan build packaging produksi.

## 1. Arsitektur Antarmuka Jetpack Compose

### 1.1 Kestabilan Rekomposisi & State
- **Rekomposisi Terukur**: Hindari pembuatan objek instan di dalam body composable tanpa `remember`.
- **`derivedStateOf`**: Gunakan `derivedStateOf` saat state turunan berubah lebih sering daripada kebutuhan render antarmuka (misalnya pemantauan scroll position list).
- **State Hoisting**: Buat composable tanpa state (*stateless*) untuk kemudahan pengujian dan penggunaan ulang. Kirim event ke atas via lambda callback.

### 1.2 Pola ViewModel & Coroutine Lifecycle
```kotlin
@HiltViewModel
class OrderViewModel @Inject constructor(
    private val orderRepository: OrderRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow<OrderUiState>(OrderUiState.Loading)
    val uiState: StateFlow<OrderUiState> = _uiState.asStateFlow()

    fun fetchOrder(orderId: String) {
        viewModelScope.launch(Dispatchers.IO) {
            orderRepository.getOrderFlow(orderId)
                .catch { err -> _uiState.value = OrderUiState.Error(err.message ?: "Unknown error") }
                .collect { order -> _uiState.value = OrderUiState.Success(order) }
        }
    }
}
```

---

## 2. Persistensi Offline & Sinkronisasi (Room)

- **Indeks Kolom**: Setiap foreign key atau kolom yang sering di-filter wajib memiliki `@Index` eksplisit di entitas Room.
- **Migrasi Skema**: Jangan gunakan `fallbackToDestructiveMigration()` di lingkungan produksi. Wajib sediakan `Migration(from, to)` teruji:
  ```kotlin
  val MIGRATION_1_2 = object : Migration(1, 2) {
      override fun migrate(db: SupportSQLiteDatabase) {
          db.execSQL("ALTER TABLE orders ADD COLUMN tracking_number TEXT DEFAULT '' NOT NULL")
      }
  }
  ```

---

## 3. Background Work & Izin Sistem

- **WorkManager**: Gunakan untuk tugas background persisten yang wajib selesai meskipun aplikasi ditutup. Pasang constraint baterai dan jaringan:
  ```kotlin
  val constraints = Constraints.Builder()
      .setRequiredNetworkType(NetworkType.CONNECTED)
      .setRequiresBatteryNotLow(true)
      .build()
  ```
- **Izin Runtime (Android 13+)**: Tangani izin `POST_NOTIFICATIONS` dan izin lokasi (`ACCESS_FINE_LOCATION`) dengan alur penjelasan kontekstual sebelum menampilkan dialog sistem.

---

## 4. Keamanan & Optimasi Ukuran (R8 / ProGuard)

- **Aturan R8**: Pertahankan model serialisasi JSON (Kotlinx Serialization, Moshi, Gson) agar tidak terhapus (*stripped*) atau rusak saat obfuscation:
  ```proguard
  -keepclassmembers class * {
      @com.google.gson.annotations.SerializedName <fields>;
  }
  ```
- **Penyimpanan Kunci**: Gunakan `MasterKey` dan `EncryptedSharedPreferences` atau Android KeyStore untuk menyimpan token autentikasi. Dilarang menyimpan token di plain SharedPreferences.
