# Production n8n Workflow Patterns & Architecture Recipes

This reference details canonical architecture recipes for n8n workflow automation in the Maxilun ecosystem.

---

## 1. Webhook Ingress with HMAC-SHA256 Signature Verification

When receiving webhooks from payment gateways (Stripe, Midtrans, Xendit) or third-party webhooks, always implement constant-time signature verification.

```json
{
  "name": "Webhook Ingress with HMAC Verification",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "payment-callback",
        "options": {}
      },
      "id": "node-webhook-1",
      "name": "Webhook Ingress",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [250, 300]
    },
    {
      "parameters": {
        "jsCode": "const crypto = require('crypto');\nconst secret = $env.WEBHOOK_SECRET || '';\nconst signature = $json.headers['x-callback-signature'] || '';\nconst payload = JSON.stringify($json.body);\nconst expected = crypto.createHmac('sha256', secret).update(payload).digest('hex');\nconst valid = crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expected));\nif (!valid) throw new Error('Invalid webhook HMAC signature');\nreturn [{ json: { verified: true, body: $json.body } }];"
      },
      "id": "node-code-verify",
      "name": "Verify HMAC Signature",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [480, 300]
    },
    {
      "parameters": {
        "operation": "executeQuery",
        "query": "UPDATE orders SET status = $1, updated_at = NOW() WHERE id = $2 RETURNING id, status;"
      },
      "id": "node-postgres-update",
      "name": "Update Order Status",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 2.4,
      "position": [720, 300],
      "credentials": {
        "postgres": {
          "id": "prod-postgres-cred"
        }
      }
    }
  ],
  "connections": {
    "Webhook Ingress": {
      "main": [
        [{ "node": "Verify HMAC Signature", "type": "main", "index": 0 }]
      ]
    },
    "Verify HMAC Signature": {
      "main": [
        [{ "node": "Update Order Status", "type": "main", "index": 0 }]
      ]
    }
  }
}
```

---

## 2. Document & Industrial Data ETL Pipeline

Parse incoming CSV, Excel, or tabular data, map columns with paired item semantics, and load into PostgreSQL.

```json
{
  "name": "Document & Industrial ETL Pipeline",
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [{ "field": "cronExpression", "expression": "0 2 * * *" }]
        }
      },
      "id": "node-schedule-trigger",
      "name": "Nightly Schedule",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1.2,
      "position": [250, 300]
    },
    {
      "parameters": {
        "url": "https://api.internal.com/reports/daily-export.csv",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth"
      },
      "id": "node-fetch-report",
      "name": "Fetch CSV Report",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [480, 300]
    },
    {
      "parameters": {
        "options": {
          "delimiter": ",",
          "headerRow": true
        }
      },
      "id": "node-parse-csv",
      "name": "Parse CSV",
      "type": "n8n-nodes-base.spreadsheetFile",
      "typeVersion": 2,
      "position": [720, 300]
    }
  ],
  "connections": {
    "Nightly Schedule": {
      "main": [
        [{ "node": "Fetch CSV Report", "type": "main", "index": 0 }]
      ]
    },
    "Fetch CSV Report": {
      "main": [
        [{ "node": "Parse CSV", "type": "main", "index": 0 }]
      ]
    }
  }
}
```

---

## 3. Two-Way Webhook Glue-Code Templates

### Next.js 15 Server Action (Outbound to n8n)
```typescript
import crypto from "crypto";

export async function triggerN8nWorkflow(payload: Record<string, unknown>) {
  const secret = process.env.N8N_WEBHOOK_SECRET!;
  const body = JSON.stringify(payload);
  const signature = crypto.createHmac("sha256", secret).update(body).digest("hex");

  const res = await fetch(process.env.N8N_WEBHOOK_URL!, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Callback-Signature": signature,
    },
    body,
  });

  if (!res.ok) {
    throw new Error(`n8n webhook failed with HTTP status ${res.status}`);
  }
  return res.json();
}
```

### PHP 8+ cURL (Outbound to n8n)
```php
<?php
function trigger_n8n_workflow(array $data, string $webhookUrl, string $secret): array {
    $body = json_encode($data, JSON_UNESCAPED_SLASHES);
    $signature = hash_hmac('sha256', $body, $secret);

    $ch = curl_init($webhookUrl);
    curl_setopt_array($ch, [
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => $body,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => [
            'Content-Type: application/json',
            'X-Callback-Signature: ' . $signature
        ],
        CURLOPT_TIMEOUT => 10
    ]);
    $res = curl_exec($ch);
    $code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($code >= 400) {
        throw new RuntimeException("n8n webhook failed with status: $code");
    }
    return json_decode($res, true) ?: [];
}
```

