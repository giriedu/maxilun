# OpenAPI 3.1, AsyncAPI 3.0 & API Contract Reference

Use this reference when writing API contract documentation (`docs/api.md`, `openapi.yaml`), an error catalog, a webhook specification, or an event broker schema.

---

## 1. REST API Contract Standard (OpenAPI 3.1 + RFC 9457)

Every production API specification must document:
1. **Explicit authentication and authorization** per operation (allowed roles/scopes and resource ownership rules).
2. **Idempotency** for financial or state-critical mutations (`Idempotency-Key` header).
3. **Cursor-based pagination** for large collections (avoids the poor performance of `OFFSET` on tables with millions of rows).
4. **A standardized error structure (RFC 9457 Problem Details — `application/problem+json`)**, not an ad-hoc error format per endpoint.

### Production OpenAPI 3.1 Template (`openapi.yaml`)

```yaml
openapi: 3.1.0
info:
  title: Order & Billing Service API
  version: "1.3.0"
  description: >
    Internal and partner API for invoice creation and payment settlement.
    All monetary values are represented in minor units (IDR integer) to prevent floating-point drift.
servers:
  - url: https://api.example.com/v1
    description: Production
  - url: http://localhost:8080/v1
    description: Local Development

security:
  - bearerAuth: []

paths:
  /invoices:
    get:
      operationId: listInvoices
      summary: List invoices with cursor pagination
      tags: [Invoices]
      parameters:
        - name: cursor
          in: query
          description: Opaque cursor returned from the previous page's `next_cursor`
          schema:
            type: string
        - name: limit
          in: query
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 25
        - name: status
          in: query
          schema:
            type: string
            enum: [DRAFT, PENDING_PAYMENT, PAID, EXPIRED, CANCELLED]
      responses:
        "200":
          description: Paginated invoice list
          content:
            application/json:
              schema:
                type: object
                required: [data, page_info]
                properties:
                  data:
                    type: array
                    items:
                      $ref: "#/components/schemas/Invoice"
                  page_info:
                    $ref: "#/components/schemas/CursorPageInfo"
        "401":
          $ref: "#/components/responses/UnauthorizedError"
        "429":
          $ref: "#/components/responses/RateLimitError"

    post:
      operationId: createInvoice
      summary: Create a new invoice (idempotent)
      tags: [Invoices]
      parameters:
        - name: Idempotency-Key
          in: header
          required: true
          description: Client-generated UUID v4; keys are retained for 24 hours per tenant.
          schema:
            type: string
            format: uuid
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateInvoiceRequest"
      responses:
        "201":
          description: Invoice created
          headers:
            Location:
              schema:
                type: string
              description: Canonical URL of the created invoice
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Invoice"
        "400":
          $ref: "#/components/responses/BadRequestError"
        "401":
          $ref: "#/components/responses/UnauthorizedError"
        "403":
          $ref: "#/components/responses/ForbiddenError"
        "409":
          $ref: "#/components/responses/ConflictError"
        "422":
          $ref: "#/components/responses/ValidationError"

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    CreateInvoiceRequest:
      type: object
      required: [customer_id, items, due_date]
      additionalProperties: false
      properties:
        customer_id:
          type: string
          format: uuid
        due_date:
          type: string
          format: date
        items:
          type: array
          minItems: 1
          maxItems: 100
          items:
            type: object
            required: [sku, quantity, unit_price_idr]
            properties:
              sku:
                type: string
                minLength: 1
                maxLength: 64
              quantity:
                type: integer
                minimum: 1
              unit_price_idr:
                type: integer
                minimum: 0

    Invoice:
      type: object
      required: [id, customer_id, total_amount_idr, status, created_at]
      properties:
        id:
          type: string
          format: uuid
        customer_id:
          type: string
          format: uuid
        total_amount_idr:
          type: integer
          example: 450000
        status:
          type: string
          enum: [DRAFT, PENDING_PAYMENT, PAID, EXPIRED, CANCELLED]
        created_at:
          type: string
          format: date-time

    CursorPageInfo:
      type: object
      required: [has_next_page, next_cursor]
      properties:
        has_next_page:
          type: boolean
        next_cursor:
          type: [string, "null"]

    ProblemDetails:
      type: object
      description: RFC 9457 Problem Details for HTTP APIs
      required: [type, title, status, detail]
      properties:
        type:
          type: string
          format: uri
          example: https://api.example.com/errors/validation-failed
        title:
          type: string
          example: Validation Failed
        status:
          type: integer
          example: 422
        detail:
          type: string
          example: Request payload contains 1 invalid field.
        instance:
          type: string
          example: /v1/invoices
        trace_id:
          type: string
          example: 01HV8X9Z2K4M7N8P9Q0R1S2T3U
        errors:
          type: array
          items:
            type: object
            required: [field, code, message]
            properties:
              field:
                type: string
                example: items[0].unit_price_idr
              code:
                type: string
                example: MIN_VALUE_VIOLATION
              message:
                type: string
                example: Must be greater than or equal to 0

  responses:
    BadRequestError:
      description: Malformed JSON or invalid header
      content:
        application/problem+json:
          schema:
            $ref: "#/components/schemas/ProblemDetails"
    UnauthorizedError:
      description: Missing or expired authentication token
      content:
        application/problem+json:
          schema:
            $ref: "#/components/schemas/ProblemDetails"
    ForbiddenError:
      description: Authenticated user lacks required permission or resource ownership
      content:
        application/problem+json:
          schema:
            $ref: "#/components/schemas/ProblemDetails"
    ConflictError:
      description: Idempotency key reused with different payload or state conflict
      content:
        application/problem+json:
          schema:
            $ref: "#/components/schemas/ProblemDetails"
    ValidationError:
      description: Semantic validation failure on input fields
      content:
        application/problem+json:
          schema:
            $ref: "#/components/schemas/ProblemDetails"
    RateLimitError:
      description: Rate limit exceeded
      headers:
        Retry-After:
          schema:
            type: integer
          description: Seconds until the client may retry
      content:
        application/problem+json:
          schema:
            $ref: "#/components/schemas/ProblemDetails"
```

---

## 2. Webhook Contract Documentation (Inbound / Outbound)

Every webhook document must explain how to verify the signature, how replay attacks are prevented, and the retry rules:

```markdown
## Webhook: `invoice.paid`

- **Delivery Method**: `POST <merchant_webhook_url>`
- **Timeout**: `5000ms` per attempt
- **Retry Schedule**: Exponential backoff (`15s`, `1m`, `5m`, `30m`, `2h`, `6h` — max 6 attempts)
- **Idempotency**: Consumers must deduplicate on the `X-Webhook-Id` header (a unique UUID per event).

### Security Headers
| Header | Example | Description |
|---|---|---|
| `X-Webhook-Id` | `evt_01HV8Y2A9B...` | Unique event ID for deduplication |
| `X-Webhook-Timestamp` | `1730000000` | Unix epoch seconds; reject when it differs by `> 300 seconds` from server time |
| `X-Webhook-Signature` | `v1=8f4a2c...` | `HMAC-SHA256(secret, "${timestamp}.${raw_body}")` |

### Signature Verification Example (Node.js)
```typescript
import { createHmac, timingSafeEqual } from 'node:crypto';

export function verifyWebhookSignature(
  rawBody: string,
  timestampHeader: string,
  signatureHeader: string,
  secret: string
): boolean {
  const nowSeconds = Math.floor(Date.now() / 1000);
  const timestamp = Number(timestampHeader);
  if (!Number.isInteger(timestamp) || Math.abs(nowSeconds - timestamp) > 300) {
    return false;
  }
  const expected = `v1=${createHmac('sha256', secret).update(`${timestamp}.${rawBody}`).digest('hex')}`;
  const a = Buffer.from(expected, 'utf8');
  const b = Buffer.from(signatureHeader, 'utf8');
  return a.length === b.length && timingSafeEqual(a, b);
}
```
```
