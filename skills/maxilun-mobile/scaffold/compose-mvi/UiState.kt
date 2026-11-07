package com.maxilun.mobile.scaffold

/**
 * Maxilun Mobile: 4-State UI Contract
 * Invariant: Every screen MUST support Loading, Empty, Populated, and Error recovery.
 */
sealed interface UiState<out T> {
    data object Loading : UiState<Nothing>
    data class Empty(val message: String) : UiState<Nothing>
    data class Success<T>(val data: T) : UiState<T>
    data class Error(val throwable: Throwable, val retryIntent: UserIntent) : UiState<Nothing>
}

sealed interface UserIntent {
    data object LoadInitialData : UserIntent
    data object RefreshPull : UserIntent
    data class UpdateItem(val id: String, val title: String) : UserIntent
}

data class TelemetryRecord(
    val id: String,
    val title: String,
    val valueFormatted: String,
    val isSyncedLocally: Boolean
)
