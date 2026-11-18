# Android Native Engineering Playbook (Kotlin, Jetpack Compose, Gradle)

Engineering guide for modern native Android apps: Kotlin, declarative Jetpack Compose, tested architecture, and production build packaging.

## 1. Jetpack Compose UI Architecture

### 1.1 Recomposition Stability & State
- **Bounded recomposition**: Do not instantiate objects inside a composable body without `remember`.
- **`derivedStateOf`**: Use `derivedStateOf` when a derived state changes more often than the UI needs to render (for example, tracking a list's scroll position).
- **State hoisting**: Write stateless composables so they are easy to test and reuse. Send events upward through lambda callbacks.

### 1.2 ViewModel Pattern & Coroutine Lifecycle
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

## 2. Offline Persistence & Sync (Room)

- **Column indexes**: Give every foreign key and every frequently filtered column an explicit `@Index` in the Room entity.
- **Schema migrations**: Do not use `fallbackToDestructiveMigration()` in production. Provide a tested `Migration(from, to)`:
  ```kotlin
  val MIGRATION_1_2 = object : Migration(1, 2) {
      override fun migrate(db: SupportSQLiteDatabase) {
          db.execSQL("ALTER TABLE orders ADD COLUMN tracking_number TEXT DEFAULT '' NOT NULL")
      }
  }
  ```

---

## 3. Background Work & System Permissions

- **WorkManager**: Use it for persistent background work that must finish even if the app is closed. Set battery and network constraints:
  ```kotlin
  val constraints = Constraints.Builder()
      .setRequiredNetworkType(NetworkType.CONNECTED)
      .setRequiresBatteryNotLow(true)
      .build()
  ```
- **Runtime permissions (Android 13+)**: Handle `POST_NOTIFICATIONS` and location permission (`ACCESS_FINE_LOCATION`) with a contextual explanation flow before showing the system dialog.

---

## 4. Security & Size Optimization (R8 / ProGuard)

- **R8 rules**: Keep JSON serialization models (Kotlinx Serialization, Moshi, Gson) so they are not stripped or broken by obfuscation:
  ```proguard
  -keepclassmembers class * {
      @com.google.gson.annotations.SerializedName <fields>;
  }
  ```
- **Key storage**: Use `MasterKey` with `EncryptedSharedPreferences`, or the Android KeyStore, to store authentication tokens. Never store a token in plain SharedPreferences.
