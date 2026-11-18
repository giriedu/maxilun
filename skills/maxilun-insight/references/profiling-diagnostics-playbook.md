# Systems Profiling & Deep Diagnostics Playbook

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-insight/SKILL.md"
  origin: "Maxilun Insight Engine"
-->

Guide to system performance diagnostics, *memory leak* tracing, and CPU/IO saturation analysis.

---

## 1. CPU Flamegraph Analysis

1. **Identify the hot path**:
   - Check the bar width (*plateau*) in the flamegraph. A wide bar marks the function that consumes the most CPU execution time.
2. **Distinguish CPU bound from IO bound**:
   - If CPU usage is near 100% and the graph shows repeated calculation, optimize the algorithm or apply memoization.
   - If wait time is high but CPU is low, check the latency of external database queries or downstream network HTTP calls.

---

## 2. Memory Leak Tracing (Heap Profiling)

1. **Take 3 snapshots in sequence**:
   - Take a memory snapshot at startup (*Baseline*).
   - Trigger the system operation repeatedly (*Stress Test*).
   - Take the second snapshot, force a garbage collection, then take the third snapshot (*Comparison*).
2. **Detect retained objects (Retained Size)**:
   - Compare the object difference between snapshot 1 and snapshot 3. Objects that keep growing and are never cleaned up indicate a reference leak (for example: an event listener that is never unregistered, an unbounded cache map, or a closure holding a reference to a large object).

---

## 3. Deadlock & Connection Contention Investigation

1. **Monitor the connection pool**:
   - If latency spikes sharply when traffic rises, check whether the database connection pool queue has run out of slots (*pool exhaustion*).
2. **Keep lock ordering consistent (Lock Ordering)**:
   - To prevent deadlocks in multi-table transactions, make every code path lock rows or tables in the same order (for example: always sort IDs ascending before running `SELECT ... FOR UPDATE`).

---

## 4. Systemic Diagnostic Triage Matrix (Hangs, Leaks, Exhaustion, Disruption)

When a system shows a runtime anomaly in a test or production environment, use the structured triage matrix to isolate the root cause into one of 4 failure classes:

| Failure Class | Observed Signals | Root Cause Mechanism | Evidence & Verification Instruments |
|---|---|---|---|
| **1. Hang & Process Stall** | High event-loop lag, process does not answer `/health` while CPU is low, frozen thread pool | Mutex/row lock deadlock, synchronous I/O call in an async loop, `idle in transaction` database transaction without a timeout, or a distributed lock without auto-expiry | Node `perf_hooks.monitorEventLoopDelay()`, Python `py-spy dump`, Go `pprof/goroutine` (goroutine leak detection), `pg_stat_activity` (filter `state = 'idle in transaction'`) |
| **2. Memory Leak & OOM Killer** | RSS memory climbs monotonically after GC, stop-the-world GC pauses grow, process dies suddenly with exit code `137` | In-memory Map/cache without LRU/TTL eviction, closure retaining a large object reference, event listener without `removeEventListener`, stream without backpressure | Diff 3 V8 heap snapshots/Python `tracemalloc`, inspect `dmesg -T \| grep -i oom`, compare object `Retained Size` |
| **3. Connection & Resource Exhaustion** | `pool timeout` errors, `EMFILE / too many open files`, thousands of sockets hanging in `TIME_WAIT` | Database connection not released in a `finally` block, HTTP client response stream not closed, or a new outbound connection created per request without keep-alive | `lsof -p <pid> \| wc -l` (count file descriptors), `netstat -ant \| grep TIME_WAIT \| wc -l`, query active connection count vs `max_connections` |
| **4. Disruption & Unclean Shutdown** | `502 Bad Gateway` or `ECONNRESET` drops during deploy/restart, truncated mutation data | Container wrapped in a shell so `SIGTERM` never reaches the application process (PID 1), shutdown handler does not refuse new requests while draining in-flight jobs, grace period too short | Verify `PID 1` in the container (`ps aux`), audit the `SIGTERM`/`SIGINT` signal handlers, and run a `kill -15 <pid>` simulation in staging |

### 4.1 5-Step Fast Triage Protocol
1. **Check the exit code**: Did the process die with `137` (OOM), `143` (SIGTERM timeout), or `1` (uncaught exception)?
2. **Identify I/O vs CPU signals**: Is CPU saturated at 100% (intensive computation/loop) or at 0–5% (deadlock/I/O wait)?
3. **Check file descriptors & sockets**: Is the FD count near the system `ulimit -n`?
4. **Check hanging transactions**: Is any transaction open for more than 5 seconds in the database?
5. **Formulate a measured recommendation**: Apply the minimal fix (for example: set `statement_timeout = '3s'`, wrap the stream with `pipeline()`, or add graceful draining).
