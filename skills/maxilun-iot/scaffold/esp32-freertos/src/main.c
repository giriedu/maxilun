/**
 * Maxilun IoT: Production ESP32 FreeRTOS Telemetry Starter
 * Invariants: Zero-heap ISR, Hardware Task Watchdog, Stack Budgeting
 */

#include <stdio.h>
#include <stdint.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "driver/gpio.h"
#include "esp_task_wdt.h"
#include "esp_log.h"

#define TAG "MAXILUN_IOT"
#define INTERRUPT_PIN GPIO_NUM_4
#define TELEMETRY_QUEUE_LEN 16
#define TASK_STACK_SIZE 4096

typedef struct {
    uint32_t timestamp_ms;
    uint32_t event_count;
    int32_t sensor_value;
} telemetry_event_t;

static QueueHandle_t s_telemetry_queue = NULL;
static volatile uint32_t s_raw_event_counter = 0;

// Zero-heap interrupt service routine (ISR)
static void IRAM_ATTR gpio_isr_handler(void* arg) {
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;
    telemetry_event_t event = {
        .timestamp_ms = (uint32_t)(xTaskGetTickCountFromISR() * portTICK_PERIOD_MS),
        .event_count = ++s_raw_event_counter,
        .sensor_value = 0
    };

    xQueueSendFromISR(s_telemetry_queue, &event, &xHigherPriorityTaskWoken);
    if (xHigherPriorityTaskWoken == pdTRUE) {
        portYIELD_FROM_ISR();
    }
}

// Telemetry processing task with watchdog monitoring
static void telemetry_worker_task(void* pvParameters) {
    ESP_LOGI(TAG, "Worker task initialized with 4KB stack budget");
    esp_task_wdt_add(NULL);

    telemetry_event_t event;
    while (1) {
        esp_task_wdt_reset();

        if (xQueueReceive(s_telemetry_queue, &event, pdMS_TO_TICKS(1000)) == pdTRUE) {
            ESP_LOGI(TAG, "Event processed: id=%lu, time=%lums",
                     (unsigned long)event.event_count,
                     (unsigned long)event.timestamp_ms);
        }
    }
}

void app_main(void) {
    ESP_LOGI(TAG, "Initializing Maxilun Embedded Subsystem...");

    // 1. Initialize queue with statically bounded buffer
    s_telemetry_queue = xQueueCreate(TELEMETRY_QUEUE_LEN, sizeof(telemetry_event_t));
    configASSERT(s_telemetry_queue != NULL);

    // 2. Configure GPIO ISR
    gpio_config_t io_conf = {
        .pin_bit_mask = (1ULL << INTERRUPT_PIN),
        .mode = GPIO_MODE_INPUT,
        .pull_up_en = GPIO_PULLUP_ENABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_NEGEDGE
    };
    gpio_config(&io_conf);
    gpio_install_isr_service(0);
    gpio_isr_handler_add(INTERRUPT_PIN, gpio_isr_handler, NULL);

    // 3. Spawn worker task with stack budgeting
    xTaskCreate(
        telemetry_worker_task,
        "telemetry_worker",
        TASK_STACK_SIZE,
        NULL,
        configMAX_PRIORITIES - 2,
        NULL
    );

    ESP_LOGI(TAG, "Maxilun IoT subsystem online. Watchdog active.");
}
