package com.maxilun.mobile.scaffold

import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

/**
 * Maxilun Mobile: MVI Intent Reducer & Offline-First Repository Boundary
 */
class MainViewModel {
    private val _uiState = MutableStateFlow<UiState<List<TelemetryRecord>>>(UiState.Loading)
    val uiState: StateFlow<UiState<List<TelemetryRecord>>> = _uiState.asStateFlow()

    fun processIntent(intent: UserIntent) {
        when (intent) {
            is UserIntent.LoadInitialData -> loadData()
            is UserIntent.RefreshPull -> loadData()
            is UserIntent.UpdateItem -> updateItem(intent.id, intent.title)
        }
    }

    private fun loadData() {
        _uiState.value = UiState.Loading
        try {
            // Simulated local SQLite Room cache read
            val cachedData = listOf(
                TelemetryRecord("1", "Production Node A", "42.5 req/s", isSyncedLocally = true),
                TelemetryRecord("2", "Edge Broker Gateway", "1,200 msgs", isSyncedLocally = true)
            )
            _uiState.value = if (cachedData.isEmpty()) {
                UiState.Empty("No telemetry records found. Tap refresh to poll.")
            } else {
                UiState.Success(cachedData)
            }
        } catch (e: Exception) {
            _uiState.value = UiState.Error(e, retryIntent = UserIntent.LoadInitialData)
        }
    }

    private fun updateItem(id: String, title: String) {
        val current = _uiState.value
        if (current is UiState.Success) {
            val updated = current.data.map {
                if (it.id == id) it.copy(title = title, isSyncedLocally = false) else it
            }
            _uiState.value = UiState.Success(updated)
        }
    }
}
