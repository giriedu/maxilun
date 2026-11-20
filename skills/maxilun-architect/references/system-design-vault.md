# System Design Vault: Scalable Distributed Architecture

A comprehensive reference vault for designing resilient, high-throughput, low-latency distributed systems. Grounded in the industry-standard foundations of Donne Martin's System Design Primer.

---

## 1. Scalability Dimensions & Trade-offs

| Dimension | Description | Typical Strategy |
|---|---|---|
| **Vertical Scaling (Scale Up)** | Increasing CPU, RAM, or IOPS of a single server. | Simple, no distributed state complexity, but hits hardware ceilings and creates single points of failure. |
| **Horizontal Scaling (Scale Out)** | Adding more commodity instances behind a load balancer. | Linear capacity expansion, requires stateless service tiers and distributed data management. |
| **Latency vs Throughput** | Latency is time to service one request; throughput is requests serviced per unit time. | Optimize for latency with caching and non-blocking I/O; optimize for throughput with batching and parallel pipelines. |

---

## 2. Consistency & CAP / PACELC Theorems

### CAP Theorem
In a distributed system with network partitions ($P$ is unavoidable):
- **CP (Consistency + Partition Tolerance)**: Rejects writes or returns errors if nodes cannot achieve quorum consensus (e.g., Raft, Paxos, Spanner, ZooKeeper). Used for financial ledgers and auth tokens.
- **AP (Availability + Partition Tolerance)**: Accepts writes locally and syncs asynchronously; nodes may return stale data during partitions (e.g., Cassandra, DynamoDB). Used for social feeds, metrics, and carts.

### PACELC Theorem
If partition ($P$), trade-off is Availability ($A$) vs Consistency ($C$); **Else** ($E$), trade-off is Latency ($L$) vs Consistency ($C$):
- *PC/EC*: MongoDB, Postgres synchronously replicated.
- *PA/EL*: DynamoDB, Cassandra with weak consistency.

---

## 3. Load Balancing & Reverse Proxies

- **Layer 4 (Transport Layer)**: Routes traffic based on IP address and TCP/UDP port (e.g., HAProxy, AWS NLB). Extremely high throughput, cannot inspect HTTP headers or cookies.
- **Layer 7 (Application Layer)**: Inspects HTTP headers, paths, cookies, and TLS SNI (e.g., Nginx, Envoy, AWS ALB). Enables path-based routing, SSL termination, and rate limiting.
- **Balancing Algorithms**:
  - *Round Robin / Weighted Round Robin*: Equal capacity instances.
  - *Least Connections*: High request duration variance.
  - *Consistent Hashing*: Preserves cache locality across node additions and removals ($O(1/N)$ key redistribution).

---

## 4. Caching Topologies & Invariants

### Caching Patterns
1. **Cache-Aside (Lazy Loading)**: Application reads cache. On miss, reads DB, writes to cache, and returns. Cache only holds requested data; handles cache failures gracefully.
2. **Write-Through**: Application writes to cache; cache synchronously writes to DB before returning. Prevents stale reads at the cost of higher write latency.
3. **Write-Behind (Write-Back)**: Application writes to cache; cache asynchronously batches writes to DB. Ultra-fast writes, but risks data loss on cache node crash.
4. **Refresh-Ahead**: Cache automatically reloads frequently accessed keys before expiration based on access patterns.

### Cache Eviction & Failure Mitigations
- **Eviction Policies**: LRU (Least Recently Used), LFU (Least Frequently Used), FIFO.
- **Cache Stampede (Dog-Piling / Thundering Herd)**: Occurs when a high-traffic key expires, causing thousands of requests to hit the database simultaneously.
  - *Mitigation*: Distributed Mutex (Redis `SETNX`), or Probabilistic Early Expiration (XFetch algorithm: expire early if $t - \beta \ln(\text{rand}()) > \text{TTL}$).

---

## 5. Database Partitioning & Storage Selection

| Storage Class | Engines | Best Used For | Anti-Patterns |
|---|---|---|---|
| **Relational (RDBMS)** | PostgreSQL, MySQL, SQLite | ACID transactions, strict schemas, relational joins, financial ledgers. | Highly unstructured hierarchical JSON blobs at massive scale. |
| **Key-Value Store** | Redis, DynamoDB | Session storage, rate limiter counters, high-throughput caching. | Complex relational multi-table queries. |
| **Document Store** | MongoDB, DocumentDB | Catalogues, CMS articles, polymorphic schemas. | Distributed transactions across multiple collections. |
| **Wide-Column Store** | Cassandra, ScyllaDB | Append-heavy time-series, event logs, high-write telemetry. | Dynamic ad-hoc filtering across arbitrary columns. |
| **Graph Store** | Neo4j, Amazon Neptune | Social networks, fraud detection graphs, knowledge bases. | High-frequency bulk append logging. |

### Relational Scaling Strategies
- **Read Replicas**: Master takes writes and replicates asynchronously to read replicas. Watch out for replication lag on read-after-write flows (route immediate reads to master).
- **Database Sharding**: Partitioning tables across database nodes.
  - *Hash-based*: Even distribution (`hash(user_id) % N`).
  - *Range-based*: Based on date or alphabetical boundaries.
  - *Directory-based*: Lookup service maps entity ID to shard ID.

---

## 6. Asynchronous Processing & Message Brokers

- **Task Queues vs Event Streams**:
  - *Task Queues (RabbitMQ, Celery)*: Push-based, tracks individual message acknowledgment, ideal for discrete worker jobs (sending email, rendering video).
  - *Event Streams (Kafka, Redpanda)*: Pull-based, append-only partitioned log with replayable offsets, ideal for event sourcing and event stream processing.
- **Idempotency Invariant**: Distributed networks guarantee *at-least-once* delivery. Consumers MUST be idempotent:
  - Maintain a `processed_messages (message_id, processed_at)` table within the database transaction.
