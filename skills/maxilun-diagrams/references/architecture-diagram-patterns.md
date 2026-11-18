# Architecture & Sequence Diagramming Patterns

<!-- metadata:
  version: "1.3.0"
  sync_target: "skills/maxilun-diagrams/SKILL.md"
  origin: "Maxilun Diagrams Engine"
-->

A guide to building software architecture diagrams, transactional sequence diagrams, and data relationship visualizations in pure Mermaid syntax.

---

## 1. Transactional Sequence Diagram

Use a sequence diagram to map the call flow between services or a client-server interaction, with automatic numbering:

```mermaid
sequenceDiagram
    autonumber
    actor User as User
    participant Client as Frontend (Next.js)
    participant API as Backend Service (Go)
    participant DB as Database (PostgreSQL)

    User->>Client: Click "Submit Payment"
    Client->>API: POST /api/v1/orders (Idempotency-Key)
    API->>DB: BEGIN TRANSACTION
    API->>DB: SELECT balance FOR UPDATE
    alt Balance Sufficient
        API->>DB: INSERT INTO payments (status='PAID')
        API->>DB: COMMIT
        API-->>Client: 200 OK (Payment Receipt)
        Client-->>User: Show Success Confirmation
    else Balance Insufficient
        API->>DB: ROLLBACK
        API-->>Client: 422 Unprocessable (Insufficient Balance)
        Client-->>User: Show Inline Recovery Message
    end
```

---

## 2. Entity-Relationship Diagram (ER Diagram)

Use an ER diagram to map table schemas, key types (PK, FK), and relationship cardinality:

```mermaid
erDiagram
    USERS ||--o{ ORDERS : places
    ORDERS ||--|{ ORDER_ITEMS : contains
    PRODUCTS ||--o{ ORDER_ITEMS : referenced_by

    USERS {
        uuid id PK
        string email UK
        string full_name
        timestamp created_at
    }

    ORDERS {
        uuid id PK
        uuid user_id FK
        numeric total_amount
        string status
        timestamp created_at
    }

    ORDER_ITEMS {
        uuid id PK
        uuid order_id FK
        uuid product_id FK
        int quantity
        numeric unit_price
    }
```
---

## 3. C4 Container Diagram

Use a C4 Container diagram to map software systems, external dependencies, and transport protocols:

```mermaid
flowchart TB
    subgraph External ["External Actors & Providers"]
        User([Customer / Web Browser])
        Stripe[Stripe Payment Gateway]
    end

    subgraph Boundary ["Payment System Boundary"]
        SPA["Single-Page App\n[TypeScript, React]\nDelivers transactional UI"]
        API["API Application\n[Go, Chi]\nHandles payment & order orchestration"]
        Worker["Event Consumer Worker\n[Go]\nProcesses async webhooks & outbox"]
        DB[("Main Database\n[PostgreSQL]\nStores orders, accounts, outbox")]
        Queue[["Message Queue\n[Redis Stream / RabbitMQ]\nBuffers transaction events"]]
    end

    User -->|HTTPS / JSON| SPA
    SPA -->|HTTPS / REST API| API
    API -->|SQL queries / RLS| DB
    API -->|Publishes events| Queue
    Queue -->|Consumes messages| Worker
    Worker -->|HTTPS / Webhook| Stripe
    Worker -->|Updates status| DB
```

---

## 4. State Machine Diagram

Use `stateDiagram-v2` to model lifecycle states, valid transitions, and guard conditions:

```mermaid
stateDiagram-v2
    [*] --> Draft : Create order
    Draft --> PendingPayment : Checkout submitted
    Draft --> Cancelled : User abandons

    state PendingPayment {
        [*] --> AwaitingGateway
        AwaitingGateway --> Processing : Webhook received
        Processing --> GatewayTimeout : 30s elapsed
        GatewayTimeout --> AwaitingGateway : Retry attempt <= 3
    }

    PendingPayment --> Paid : Payment confirmed
    PendingPayment --> Failed : Card declined
    PendingPayment --> Cancelled : Expiration TTL reached

    Paid --> Fulfilled : Shipping complete
    Paid --> Refunded : Support dispute approved

    Fulfilled --> [*]
    Failed --> [*]
    Cancelled --> [*]
    Refunded --> [*]
```

---

## 5. Diagram Readability Invariants


1. **Consistent Flow Direction**: Use the `TD` (Top-Down) or `LR` (Left-Right) orientation consistently within one diagram.
2. **No Excess Decoration**: Avoid arbitrary color with no semantic meaning; use color only to distinguish internal from external system boundaries.
