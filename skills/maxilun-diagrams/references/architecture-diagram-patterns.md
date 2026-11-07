# Architecture & Sequence Diagramming Patterns

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-diagrams/SKILL.md"
  origin: "Maxilun Diagrams Engine"
-->

Panduan penyusunan diagram arsitektur perangkat lunak, diagram sekuens transaksional, dan visualisasi relasi data menggunakan sintaks Mermaid murni.

---

## 1. Diagram Sekuens Transaksional (Sequence Diagram)

Gunakan diagram sekuens untuk memetakan alur panggilan antar-layanan atau interaksi klien-server dengan penomoran otomatis:

```mermaid
sequenceDiagram
    autonumber
    actor User as Pengguna
    participant Client as Frontend (Next.js)
    participant API as Backend Service (Go)
    participant DB as Basis Data (PostgreSQL)

    User->>Client: Klik "Kirim Pembayaran"
    Client->>API: POST /api/v1/orders (Idempotency-Key)
    API->>DB: BEGIN TRANSACTION
    API->>DB: SELECT saldo FOR UPDATE
    alt Saldo Mencukupi
        API->>DB: INSERT INTO payments (status='PAID')
        API->>DB: COMMIT
        API-->>Client: 200 OK (Payment Receipt)
        Client-->>User: Tampilkan Konfirmasi Sukses
    else Saldo Tidak Cukup
        API->>DB: ROLLBACK
        API-->>Client: 422 Unprocessable (Saldo Kurang)
        Client-->>User: Tampilkan Pesan Pemulihan Inline
    end
```

---

## 2. Diagram Relasi Entitas (ER Diagram)

Gunakan diagram ER untuk memetakan skema tabel, tipe kunci (PK, FK), dan kardinalitas relasi:

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

## 3. Invarian Keterbacaan Diagram

1. **Arah Aliran Konsisten**: Gunakan orientasi `TD` (Top-Down) atau `LR` (Left-Right) secara konsisten di satu diagram.
2. **Tanpa Dekorasi Berlebih**: Hindari warna-warni sembarang tanpa makna semantik; gunakan warna hanya untuk membedakan batasan sistem internal vs eksternal.
