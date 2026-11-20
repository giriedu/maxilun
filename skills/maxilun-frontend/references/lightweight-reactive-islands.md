# Lightweight Reactive Islands: No-Build Runtimes vs React/Next.js

<!-- metadata:
  version: "1.3.0"
  sync_target: "skills/maxilun-frontend/SKILL.md"
  origin: "Maxilun Frontend Engine"
-->

Decide when a small, platform-primitive reactive runtime (ES modules + tagged template literals + `Proxy` state + direct DOM writes, no compiler) is the right tool instead of a React/Next.js tree, and how to build one safely: fine-grained dependency tracking, escape-by-construction rendering, deterministic cleanup, and isolation for embeds and agent-generated UI. Complements `rsc-flight-patterns.md` (where the client boundary sits) by covering what can live on the far side of that boundary without React.

---

## 1. Decision Table: Primitive Runtime vs React/Next.js

Default stays Next.js App Router for routed, data-heavy products. Choose a primitive runtime only when one of the rows below is true and evidence (bundle report, host constraints) backs it.

| Situation | Pick | Why |
|---|---|---|
| Third-party embed / widget dropped into pages you do not own | Primitive runtime in Shadow DOM | No React version clash with the host, single-digit KB payload, no global CSS bleed |
| One interactive island on an otherwise static page (calculator, filter, cart badge) | Primitive runtime or plain DOM | Shipping a full React runtime for one control costs more than the feature |
| UI generated at runtime by an LLM or user (previews, playgrounds, dashboards) | Primitive runtime inside a sandbox (Section 6) | No build step to run, no JSX transform, template source is plain JS the model already writes reliably |
| Admin page or internal tool in a non-Node backend (Go, Rails, Django templates) | Primitive runtime via `<script type="module">` | No bundler pipeline to own; progressive enhancement over server HTML |
| Routed app, shared layouts, server data, auth, forms with Server Actions | Next.js / React | RSC streaming, caching, Server Actions, ecosystem (a11y libs, testing) |
| Large team, design system already in React | React | One component model beats two; mixed runtimes double review cost |
| Heavy form state, complex focus management, i18n, SSR + hydration everywhere | React | Mature primitives; reimplementing them in a micro runtime is negative value |

Gate before adopting: (1) the island has no need for React context or React-only libraries, (2) a measured payload win exists (compare gzip sizes of both builds, not marketing numbers), (3) one owner maintains the second runtime. If any gate fails, write a `'use client'` leaf instead.

## 2. Fine-Grained Reactivity Mechanics

A primitive runtime replaces "re-render the component, diff the tree" with "re-run only the binding that read the changed property". The moving parts:

1. **Read tracking**: state is a `Proxy`; its `get` trap records `(objectId, key)` into the dependency list of whichever effect is currently running (a module-level "active effect" stack).
2. **Write notification**: the `set` trap compares old and new value; on change it schedules every effect subscribed to `(objectId, key)`.
3. **Batching**: scheduled effects go into a queue flushed once per microtask (`queueMicrotask`). Ten synchronous writes produce one DOM update; an effect queued twice runs once.
4. **Dependency re-collection**: every effect run drops its old subscriptions and records fresh ones, so conditional branches (`state.open ? state.a : state.b`) subscribe only to what was actually read. Skipping the re-subscribe when the dependency list is identical is a cheap, worthwhile optimization.
5. **Lazy deep wrapping**: nested objects are wrapped on first access, and child-to-parent links let a nested write or an array mutator (`push`, `splice`, `sort`) notify bindings that read the parent key.
6. **Derived values**: a computed is an effect that writes its result into its own reactive cell; consumers subscribe to that cell, not to its inputs.

Minimal original sketch of the core (illustrative, not production):

```js
let active = null;
const subs = new WeakMap(); // target -> Map<key, Set<effect>>
const queue = new Set();

function schedule(fx) {
  if (queue.size === 0) queueMicrotask(() => { const run = [...queue]; queue.clear(); run.forEach((f) => f()); });
  queue.add(fx);
}

export function state(obj) {
  return new Proxy(obj, {
    get(t, k) {
      if (active) {
        const byKey = subs.get(t) ?? subs.set(t, new Map()).get(t);
        const set = byKey.get(k) ?? byKey.set(k, new Set()).get(k);
        set.add(active); active.deps.add(set);
      }
      return t[k];
    },
    set(t, k, v) {
      if (Object.is(t[k], v)) return true;
      t[k] = v;
      subs.get(t)?.get(k)?.forEach(schedule);
      return true;
    },
  });
}

export function effect(fn) {
  const fx = () => {
    fx.deps.forEach((s) => s.delete(fx)); fx.deps.clear();   // re-collect every run
    const prev = active; active = fx;
    try { fn(); } finally { active = prev; }
  };
  fx.deps = new Set();
  fx();
  return () => { fx.deps.forEach((s) => s.delete(fx)); fx.deps.clear(); queue.delete(fx); };
}
```

### Reactivity failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Value renders once, never updates | Read happened outside a tracked function: `${state.count}` instead of `${() => state.count}` | Interpolate a thunk for anything that changes; plain values are static by design |
| Updates stop after refactor | Destructured `const { count } = state` copies the primitive | Read through the proxy at use site |
| Some writes ignored | Code mutated the raw object, not the proxy | Keep only the proxy reachable; never export the raw seed |
| `Map`/`Set`/`Date` changes not seen | Plain `Proxy` traps do not observe internal slots | Store plain objects/arrays, or replace the whole value to trigger `set` |
| Effect runs in a loop | Effect writes a key it also reads | Move the write into an event handler or a computed |
| Identity checks fail | `proxy !== raw` | Compare by id field, not by reference to the seed |
| Memory grows per navigation | Effects never disposed | Section 4 |

## 3. Template-Literal Rendering and XSS Safety

A tagged template splits markup into a frozen `strings` array (author-controlled, identical object for every call of the same literal) and `values` (runtime data). A safe runtime exploits that split:

- Parse `strings.join(marker)` once into a `<template>` and cache it by the `strings` array identity. Values are never concatenated into markup.
- Each hole becomes a position: a text hole is written via `Text.data`/`textContent`, an attribute hole via `setAttribute`. The parser never sees runtime data, so `<script>` or `"><img onerror>` in data stays inert text. This is escape-by-construction, not escape-by-regex.
- Event holes (`@click`, `on:click`, whatever the syntax) are bound with `addEventListener`; the marker attribute is removed so no inline handler string exists.

Escape-by-construction does NOT cover these sinks; treat each as a review gate:

| Sink | Risk | Rule |
|---|---|---|
| URL attributes (`href`, `src`, `action`, `formaction`, `xlink:href`) | `javascript:` and `data:` schemes execute | Parse with `new URL(value, location.href)`; allow only `https:`, `http:`, `mailto:` |
| Property bindings to `innerHTML`, `outerHTML`, `srcdoc` | Data parsed as HTML | Ban in review; if rich text is required, sanitize with a maintained sanitizer or the Sanitizer API where supported, then enforce Trusted Types |
| Hole in attribute NAME or tag name position | Attacker picks `onload` or `script` | Never let data choose names; map data to an allowlisted set |
| `style` attribute or `<style>` with data | CSS exfiltration, overlay phishing | Bind individual properties via `el.style.setProperty` with validated values |
| Building the static part from data (`html(['<div>' + userInput + '</div>'])`, `new Function`, string concatenation before tagging) | Bypasses the whole model | The `strings` array must come from source literals only; lint against calling the tag as a plain function |
| Server-side string rendering of the same template | No DOM to do the escaping | SSR renderer must HTML-escape `& < > " '` for text and attribute holes explicitly, plus run the URL rule |

Defense in depth for any island: a strict CSP (`script-src 'self'` plus nonces, no `'unsafe-inline'`, no `'unsafe-eval'`) and `require-trusted-types-for 'script'` turn a missed sink into a blocked violation report instead of an exploit. Coordinate policy with `maxilun-sentinel`.

## 4. Lifecycle and Cleanup

Fine-grained runtimes have no render cycle to hang cleanup on, so ownership must be explicit:

1. **Owner scope**: creating a component pushes a collector; every effect, listener, and binding created during setup registers its disposer there. Unmounting the component's DOM range calls all disposers once.
2. **What must be disposed**: reactive subscriptions, `setInterval`/`setTimeout`, `ResizeObserver`/`IntersectionObserver`/`MutationObserver`, listeners on `window`/`document`, `BroadcastChannel`, WebSocket/EventSource, in-flight `fetch` (use one `AbortController` per scope and abort it on dispose).
3. **Idempotent disposers**: a disposer that runs twice must be a no-op; dispose can be triggered by both a parent unmount and an explicit close.
4. **Deferred unmount**: runtimes may batch DOM removal to a later tick. Never rely on the node being detached synchronously after a state write; await the runtime's next-tick hook in tests.
5. **Keyed lists**: give each item a stable domain key so reorders move existing DOM (preserving focus, input value, and scoped state) instead of recreating it. Index keys are only acceptable for append-only, never-reordered lists.

```js
export function Clock(root) {
  const s = state({ now: Date.now() });
  const ctrl = new AbortController();
  const id = setInterval(() => (s.now = Date.now()), 1000);
  const stop = effect(() => { root.textContent = new Date(s.now).toISOString(); });
  document.addEventListener('visibilitychange', () => { if (!document.hidden) s.now = Date.now(); }, { signal: ctrl.signal });
  let done = false;
  return () => { if (done) return; done = true; clearInterval(id); stop(); ctrl.abort(); };
}
```

Leak check: mount and unmount the island 100 times in a test, then assert subscriber counts and `getEventListeners`-style counters (or heap snapshots in DevTools) return to baseline.

## 5. Mounting an Island Inside a Next.js App

When a primitive-runtime widget must live inside a React page:

- Mount it from the deepest `'use client'` leaf in `useEffect`; return the widget's disposer as the effect cleanup. React StrictMode mounts, unmounts, and remounts in development, so a missing or non-idempotent disposer shows up as duplicate DOM or double listeners.
- The server renders only a sized placeholder (explicit width/height or aspect-ratio) to keep CLS at zero and avoid hydration mismatches; the island fills it after mount.
- React must never render children into the island's root node; give the runtime its own element and let React treat it as opaque.
- Cross-runtime state goes through one explicit bridge: the island exposes `subscribe(cb)`/`getSnapshot()` consumed with `useSyncExternalStore`, or emits DOM `CustomEvent`s. Do not let both runtimes write the same DOM.
- Prefer the bundled import over a CDN URL. If a no-build ESM import from a CDN is unavoidable, pin an exact version, add `integrity` via an import map or self-host the file, and allow only that origin in CSP.

## 6. Agent-Generated and Untrusted UI

Template-literal runtimes are attractive for model-generated UI because the source is plain JavaScript with no transform step. That same property means generated code is arbitrary code.

| Trust level | Execution venue |
|---|---|
| Code reviewed and committed by a human | Main page realm |
| Generated per request, rendered for the same user who prompted it | Sandboxed `<iframe sandbox="allow-scripts">` on a separate origin, no `allow-same-origin` |
| Generated or authored by one user, shown to other users | Separate origin iframe, or a JS VM compiled to WASM that only emits a render description the host applies via an allowlisted renderer |

Rules for the host bridge: communicate with `postMessage` and validate `event.origin` plus a schema on every message; forward events as plain data (type, key, value, checked) never as live DOM nodes; proxy network access through a host function that allowlists hosts and strips credentials; cap CPU time and memory in the VM and kill on overrun.

## 7. Verification Gates

Evidence required before shipping an island (hand to `maxilun-verify`):

- Bundle: gzip size of the island entry measured in CI with a budget assertion.
- XSS: unit tests that render `<img src=x onerror=alert(1)>` and `javascript:alert(1)` through every text, attribute, and URL hole and assert no element or handler is created.
- Lifecycle: mount/unmount loop test with listener and timer counts back to baseline.
- Accessibility: the island passes the same axe/Playwright checks as React pages; a micro runtime ships no a11y helpers, so roles, labels, and focus return are hand-written.
