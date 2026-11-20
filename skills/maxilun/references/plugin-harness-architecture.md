# Plugin Harness Architecture: Design Rules for Agent Runtimes

<!-- metadata:
  version: "1.3.0"
  sync_target: "skills/maxilun/SKILL.md"
  origin: "Maxilun Harness Engine"
-->

Design and review rules for the runtime underneath an autonomous coding agent: how plugins compose and tear down, how capabilities are injected, how tools are registered and gated, how model providers sit behind one contract, how context is compacted without losing replayability, how events are dispatched, and how process confinement is expressed. `harness-engineering.md` governs how an agent behaves inside a task and `harness-hooks-memory.md` governs how an operator configures hooks and context budget; this file governs how the harness runtime itself is built. Use it when building a harness, adding a capability to one, or auditing a third-party harness before adoption.

---

## 1. Composition: No Privileged Core

1. **Everything mountable is a plugin.** The model adapter, tool registry, session log, approval policy, and the agent loop itself are units mounted into a shared context. If a behavior can only be changed by editing the loop, the architecture has a privileged core and every extension becomes a fork.
2. **Composition is data, layered by precedence.** The running tree is built from ordered layers: a shared base layer, a product layer (web, headless, SDK), the user profile patch, then per-invocation overlays. Each row has a stable id; a later layer replaces a row by id or inserts a new one. Never merge config fields across layers; replace the whole row so the effective value has one author.
3. **The effective tree is inspectable.** The harness must print the fully resolved plugin tree it will boot. A composition you cannot dump is a composition you cannot debug or audit.
4. **One launcher.** Every supported entry (CLI, desktop, SDK subprocess) boots through the same composition path with a named profile. Side doors (direct in-process mounting, demo binaries, ad hoc argv escapes) bypass the patch layers and the security defaults, so reject them.

| Smell in a harness under review | Consequence | Required shape |
|---|---|---|
| Loop calls tools, compaction, retries by direct import | Cannot swap or disable any of them | Loop dispatches through events and service keys |
| Config merged field-by-field across layers | Nobody owns the effective value | Whole-row replacement by id |
| Several executables each building their own tree | Security defaults diverge per entry | One launcher, profiles select composition |

---

## 2. Lifecycle and Scoped Disposal

Every registration is an effect with an owner and an undo. This is the single rule that makes hot reload, per-agent capability sets, and clean shutdown possible.

1. **Register through the owning scope, receive a disposer.** Tool definitions, prompt sections, listeners, provider routes, and timers are all installed through the plugin's own context so unloading the plugin unwinds them. A registration with no disposer is a leak by construction.
2. **Ordered teardown lives in one effect.** If B must be released before A, create both in one effect whose disposer releases them in reverse order. Two independent effects give no ordering guarantee.
3. **Dispose reaches quiescence, not intent.** After aborting a child process or a stream, await its actual exit before reporting the scope disposed. Resources needed for final persistence (log writer, storage handle) outlive every consumer that may still write.
4. **Racing disposers share one completion.** Two callers disposing the same scope must await the same promise; the second call must not return early while the first is still unwinding.
5. **Per-agent scopes overlay a global layer.** A registry holds a global layer plus lazily created per-agent layers keyed by object identity. Lookup merges global entries with the agent's shadows; disposing an agent drops its layer without touching siblings. This is how one session gets a different tool set without a second registry.
6. **No module-level shared state.** Caches, "current session" pointers, and global maps outlive every teardown and leak between tests. Shared state hangs on a service instance with a lifecycle; each view carries its own key instead of reading a global "active" field.
7. **Plugins never reach the root context.** Reading services or adding listeners on the root bypasses dependency checks and scope filtering, and the registration survives plugin disposal. A listener that truly must observe every scope declares that explicitly.

```ts
// Ordered teardown: the watcher stops before the index it feeds is closed.
scope.effect(async () => {
  const index = await openIndex(root)
  const watcher = watchTree(root, (path) => index.refresh(path))
  return async () => {
    await watcher.close()   // quiescent: no more refresh calls in flight
    await index.close()
  }
})
```

---

## 3. Capability Injection and Seams

1. **Services are found by key, not by import.** A consumer declares the service keys it needs; the framework activates the consumer only after those services exist and deactivates it when one disappears. Load order is derived from declared requirements, never hand-sequenced at boot.
2. **A seam has three roles.** A *definition* (the interface and its key), one or more *providers* (implementations), and *consumers* (often a model-facing tool). Code that fills only one of those roles is a plugin, not a seam; a new capability is incomplete until all three roles are designed.
3. **Providers that share an execution world move together.** Filesystem, subprocess, terminal, and language-server providers must resolve to the same machine. Pointing the filesystem provider at a remote host while shell commands still run locally produces an agent that reads one world and edits another. Bind them as one switchable world.
4. **Misconfiguration fails at load, not at first call.** A provider that requires a confining shell executor, or a reserved name in a config table, throws while mounting. Silent degradation discovered mid-task is the expensive failure mode.
5. **Seams own the narrowest operation.** A storage seam saves bytes and returns an opaque locator plus a retrieval hint; retention, replacement, and search are separate policies layered on top. Fat seams force every provider to reimplement policy.

---

## 4. Event Bus

### 4.1 Three event domains

| Domain | Purpose | Persistence | Use it when |
|---|---|---|---|
| Durable session facts | What happened (message, tool call, tool result, turn boundaries) | Appended to the log | The fact must survive reload, fork, or replay |
| Live agent control | Work in flight (inbox, step admission, request shaping, stop checks) | Process-local | You must observe or intercept a running agent |
| Capability policy | Attach policy to a seam (fs intents, tool execution, telemetry) | Process-local | You need policy without importing the loop |

### 4.2 Dispatch mode is part of the contract

Declare the mode with the event and verify dispatch sites against it.

| Mode | Shape | Listener obligation |
|---|---|---|
| Notify | Fire-and-forget, no return | Must not throw into the producer |
| Fan-out | All listeners run concurrently, awaited | Must be order-independent |
| Ordered | Listeners run in sequence, awaited | Each may veto or annotate a checkpoint |
| First-answer | Stop at the first listener that returns a value | Return only when you own the answer |
| Around (middleware) | Listener receives the request and `next` | Call `next` unless you own the decision |

1. **Around-listeners that only observe or annotate must delegate.** Short-circuiting is reserved for the listener that owns the decision (a deny policy, a cached answer). A wrapper that forgets `next()` silently disables every listener registered after it.
2. **Wrapping preserves downstream fields.** When rewriting a decision object, spread the original and replace only the field you own; dropping flags you did not set changes behavior you do not own.
3. **The dispatcher contains listener exceptions.** One faulty plugin must not abort the turn; the dispatcher converts a listener throw into a reported error and continues per the mode's rules.
4. **Async status is not a per-request result.** A shared "running/idle" status covers many queued inputs, steering, and injected work. A caller that needs per-request completion must define its own interval explicitly; never infer it from status flips.
5. **Ordering comes from named call points, never from timing.** A microtask or zero-delay timer that "usually runs first" is a race that only shows under load.

---

## 5. Tool Registration and the Permission Pipeline

### 5.1 What a tool definition carries

- Model-facing fields: name, description, parameter schema. The registry builds the request schema by **allowlist**; host-only fields (timeouts, concurrency classifier, presenters, renderers) must never leak into a provider request.
- A declared output schema the body's return value is validated against, plus a pure renderer from value to model content.
- An `execute` body that honors the cancellation signal and settles only after its own work is quiescent.
- Concurrency is opt-in: a pure classifier returns `true` for calls that may overlap siblings. Absence, exceptions, or non-boolean returns mean exclusive.

### 5.2 Pipeline order

```text
model emits call -> log tool/call (before any execution)
  -> pre-execute policies (hooks, permission, sandbox selection)
       deny -> skip body | ask -> approval service | allow
  -> monotonic guards (may only deny or abstain)
  -> around-execute wrappers (timeout, retry, metrics) -> tool body
  -> content projection -> post-execute policies (accept, block, replace, add context)
  -> final content-only transform -> frozen outcome -> log tool/result
```

1. **Log the call before executing it.** A crash mid-tool must leave a call with no result, which recovery fills with an explicit error result; never a silent gap the model misreads.
2. **Exactly one model-facing result per call**, including denials, timeouts, and pipeline failures. Any throw inside the pipeline is normalized into an error result, not propagated past it.
3. **Guards are monotonic.** A guard can tighten (deny) but never loosen. Policies that must not be reordered by later registrations live as guards, not as around-listeners that a prepended listener could bypass.
4. **Approval fails closed.** The outcome set is closed: allowed-once, rejected, cancelled, unavailable. Missing, throwing, or non-owning answerers resolve to unavailable, and callers deny on everything except allowed-once. Grants are one-shot; a reusable grant is a policy change and is recorded as one.
5. **A strict non-interactive policy is enforced inside the service**, before any answerer runs, so a late-registered answerer cannot bypass it. Unattended runs (CI) use it.
6. **Approval requests reference the streamed call by id**; they do not re-render arguments, so the prompt cannot drift from what will execute.
7. **Approval and audit are logged, but stay out of the transcript.** The model sees the derived tool result and the current permission snapshot, not the audit pair.
8. **Oversized output is spilled, not truncated blindly.** Persist the full text privately (owner-only permissions, exclusive create so a planted symlink cannot redirect the write), return an opaque locator with a retrieval hint, and show the model a bounded excerpt.

---

## 6. Model-Provider Abstraction

One adapter contract; every consumer relies on it, every adapter must satisfy it.

| Rule | Why |
|---|---|
| One adapter call is one provider attempt; library-level retries disabled | Retries become visible, logged, and policy-driven at the agent level |
| Usage is emitted before finish; nothing after finish | Consumers can close accounting at the terminal chunk |
| The adapter passes tool-call arguments through as the provider's original JSON string, never parsed and re-encoded | Re-serialization differences cannot alter what was logged |
| Failures surface through one public path (a terminal error chunk with a typed failure) | Consumers can tell provider failure from their own defects |
| Context overflow maps to one canonical code; route on the code, never on provider message text | Compaction triggers reliably across providers |
| Empty completion is an error with a canonical code, retryable by default | A blank answer never masquerades as success |
| Idle-stream watchdog bounded at the transport; its expiry is a timeout, an earlier caller abort stays an abort | Stalled providers cannot hang a turn; causes stay distinguishable |
| Provider replay state is opaque and handed back only to the same adapter instance | Cross-provider history never receives foreign reasoning metadata |
| Model catalogs are advisory; the adapter decides whether a model id is valid | New models work without a registry release |
| Attribution headers carry only static public product facts | No session ids, paths, or user identifiers leak to providers |

Model selection is snapshotted per turn and retained across retries, so a retry never silently switches model or reasoning effort.

```ts
// Boundary normalization: whatever the vendor SDK does, consumers see one shape.
async function* streamNormalized(adapter: Adapter, req: Request) {
  try {
    for await (const chunk of adapter.stream(req)) yield chunk
  } catch (err) {
    yield { kind: 'finish', status: 'error', failure: classify(err) } // canonical code
  }
}
```

---

## 7. Context: Logged, Derived, Compacted

1. **Model-visible means logged.** Every request sent to a model must be reconstructable from the append-only session log. A plugin that adds model-visible input without a session event breaks resume, fork, and audit. Content rewrites are pure projections over logged events, registered so detached readers apply the same definitions.
2. **History is derived, then frozen.** The loop derives the message list from the log, freezes it, and sends an immutable request. Live streaming frames are transient; the durable settlement (successful message or failed attempt record) is the replay source.
3. **Compaction is an optional capability, not loop spine.** It plugs into two triggers: pre-step *pressure* (estimated tokens near the window) and request-error *overflow* (the canonical overflow code). Overflow may be handled more aggressively than pressure.
4. **Cheapest reduction first.** Prune or offload bulky tool results and images before summarizing; summarize only when pruning does not suffice.
5. **Retry only on progress.** After an overflow, retry the request only if the reduction actually changed the visible surface; otherwise the original error stays authoritative. This prevents a summarize-retry loop that burns tokens without shrinking anything.
6. **Bracket compaction with a logged lock.** Append a start marker, then the summary record and the replacement message, then the end marker last. A crash leaves an orphaned start, which is detectable; writing the end marker early would falsely claim success.
7. **Summaries shadow, never delete.** The replacement records which events it shadows; raw events remain in the log for audit and alternative projections.
8. **Runtime context is a snapshot, not an edit.** When permission mode or other runtime state changes, append a fresh full snapshot after retained history instead of rewriting the system prompt; earlier prompt bytes stay stable for provider caching.

---

## 8. Sandboxing and Process Confinement

1. **Policy is resolved per call and carried with the call.** Mode, workspace root, and extra writable roots are computed once per capability call from the session; providers stay stateless with respect to policy, so concurrent sessions and one-shot escalations do not mutate each other.
2. **Modes are few and named.** Read-only, workspace-write, full-access. Full-access never reaches the sandbox provider; the consumer spawns the original command. Network and process visibility are separate concerns; do not let a file-effect mode imply network isolation.
3. **Enforcement completeness is a reported fact.** A backend reports `full` or `partial` (older kernel features, platform ACL gaps). Callers that need an absolute boundary must refuse `partial` rather than treat it as `full`.
4. **Sandbox and approval are independent knobs.** Presets may bundle them for the UI, but each is set through its own single write path and recorded in the log, so replay reconstructs both.
5. **Escalation is one-shot.** An approved retry outside the sandbox applies to that call only; it never flips the session mode.
6. **Roots are validated where the files live.** Reject missing, non-directory, and symlinked writable roots on every call; canonicalize on the enforcing host, including remote hosts.
7. **The sandbox is not the only control.** State plainly that confinement reduces risk but does not guarantee isolation; recommend least privilege and disposable environments for untrusted workloads.

---

## 9. Harness Evaluation Checklist

Answer each with evidence (file, test, or command output), per the Maxilun proof standard.

| # | Question | Fail signal |
|---|---|---|
| 1 | Can the agent loop be replaced from configuration? | Loop imported directly by tools or UI |
| 2 | Does every registration return a disposer? | Listeners added in constructors with no undo |
| 3 | Does shutdown await child process exit? | Kill sent, completion reported immediately |
| 4 | Is the request schema built by allowlist? | Host-only fields visible in a captured request |
| 5 | Does an absent approval answerer deny? | Headless run executes a gated command |
| 6 | Is every model request reconstructable from the log? | Context injected from memory with no event |
| 7 | Is context overflow routed on a canonical code? | String matching on provider error text |
| 8 | Does the sandbox report partial enforcement? | Same success value on every platform |
| 9 | Are filesystem and shell bound to one execution world? | Remote fs with local shell is a valid config |
| 10 | Is there module-level shared state? | Global caches or "current" pointers |

---

## 10. Weaknesses to Reject When Adopting This Pattern

- **Package explosion.** A plugin per concern can grow to hundreds of packages and thousands of generated reference lines. Maxilun standard: one cohesive owner per surface; split only at a real seam (three roles present), not per helper.
- **Generated catalogs as the primary documentation.** Catalogs prove drift-freedom but are unreadable as guidance. Keep a short hand-written rule set (like this file) and treat catalogs as lookup data.
- **Deprecated hooks kept alive alongside replacements.** Two ways to shape a request double the review surface. Clean cutover: migrate every caller and remove the old hook.
- **Heavy framework before need.** A DI and event framework pays off only with genuinely swappable providers. For a single-provider tool, a plain registry with disposers delivers rules 2.1 to 2.4 at a fraction of the weight (native platform before heavy dependency).
- **Safety by disclaimer.** A harness that executes model-generated commands must ship fail-closed approval and a confining default, not only a warning document. Treat any harness whose default preset is full-access with no approval as unsafe for adoption.
