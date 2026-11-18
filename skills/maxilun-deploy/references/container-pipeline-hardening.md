# Container & Pipeline Hardening Playbook

<!-- metadata:
  version: "1.3.0"
  sync_target: "skills/maxilun-deploy/SKILL.md"
  origin: "Maxilun Deploy Engine"
-->

How to build minimal Docker containers, harden production images, and optimize CI/CD pipelines.

---

## 1. Docker Multi-Stage Build Discipline

Separate the build stage from the runtime stage to minimize image size and keep the compile toolchain out of production:

```dockerfile
# Stage 1: Builder
FROM node:22.12.0-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Minimal production runner
FROM node:22.12.0-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

# Run as a non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 appuser

COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist

USER appuser
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

### Container Security Invariants:
1. **Non-root user required**: Never run the application process inside the container as `root`.
2. **Clean the package manager cache**: Always clean the package manager cache in the same layer (for example: `rm -rf /var/cache/apk/*` or `apt-get clean`).
3. **Pin a specific image version**: Never use the `:latest` tag in production. Use an explicit semantic tag (for example: `node:22.12.0-alpine`) or a SHA digest.

---

## 2. CI/CD Pipeline Cache Optimization

1. **Dependency cache keying**:
   - Cache the dependency directories (`~/.npm`, `~/.cache/pip`, `~/.m2`) keyed on the hash of the lockfile (`package-lock.json`, `poetry.lock`, `go.sum`).
   - GitHub Actions standard cache step:
   ```yaml
   - name: Cache dependencies
     uses: actions/cache@v4
     with:
       path: ~/.npm
       key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
       restore-keys: |
         ${{ runner.os }}-node-
   ```
2. **Fail fast & parallel sharding**:
   - Run linter and code format checks as the earliest step, before the heavy test suite.
   - Split integration test cases into several parallel shards when total execution time exceeds 10 minutes.

### 2.1 Hardened Nginx Reverse Proxy Configuration
```nginx
server {
    listen 80;
    server_name example.com;
    server_tokens off;

    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60s;
    }
}
```
---

## 3. SRE SLO Alerting: Multi-Window Multi-Burn-Rate

Move production monitoring away from raw threshold alerts (for example: CPU > 80% or Memory > 85%, which often cause *alert fatigue*) to **Symptom-Based Alerting** driven by the **SLO Error Budget**.

### 3.1 Burn Rate Formula
If the availability SLO target is $99.9\%$ over a 30-day window (Error Budget = $0.1\% = 0.001$):
- **Burn Rate 1.0**: Consumes 100% of the error budget in exactly 30 days (normal consumption).
- **Burn Rate 14.4**: Consumes 2% of the error budget in just 1 hour ($100\% / (30 \times 24 / 14.4)$) $\to$ critical emergency (*Critical Outage*).

### 3.2 Multi-Window Multi-Burn-Rate Alerting Matrix

Combine a long window (to detect a degradation trend) with a short window (to suppress false alerts during recovery):

| Severity | Budget Consumption | Long Window | Short Window | Burn Rate | Response Target & Action |
|---|---|---|---|---|---|
| **P1 - Critical (Pager)** | 2% of budget consumed in 1 hour | 1 Hour | 5 Minutes | **14.4x** | Page on-call immediately. Active outage or massive 5xx spike. Link directly to the rollback / failover runbook. |
| **P2 - High (Urgent)** | 5% of budget consumed in 6 hours | 6 Hours | 30 Minutes | **6.0x** | Urgent notification to the team. Investigate within 30 minutes. Check for database or third-party API degradation. |
| **P3 - Medium (Ticket)** | 10% of budget consumed in 3 days | 3 Days | 6 Hours | **1.0x** | Automatic ticket in the active sprint backlog. Slow degradation that erodes system reliability. |

### 3.3 Alert Operating Rules
1. **Runbook link required**: Every alert sent to a pager or Slack/Discord must include the URL of its specific operational runbook. An alert without a runbook must not be active in production.
2. **Automatic reset condition**: An emergency alert clears only when the short window drops back below the burn rate threshold, which proves the fix/rollback has stopped the budget burn.
