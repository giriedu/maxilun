# Surface State Topology: Deterministic UI Finite State Machines

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-craft/SKILL.md"
  origin: "Maxilun Craft Engine"
-->

Model interface states (*surface states*) as a finite state machine (FSM). Give every asynchronous component and dynamic screen surface a measured visual representation for all six discrete states, so *impossible states* cannot occur.

---

## 1. Taxonomy of the 6 Discrete Interface States

```text
       [Initial / Idle]
               │
               ▼
       [Loading / Shimmer] ◄───┐
         │           │          │
         ▼           ▼          │ (Refetch / Retry)
    [Populated]   [Empty]       │
         │           │          │
         ▼           ▼          │
      [Pending / Mutating]      │
               │                │
               ▼                │
       [Error / Degraded] ──────┘
```

1. **Idle / Initial**:
   - The state before the user interacts or before the first data load is triggered.
   - The surface shows the base structure, system navigation, and a calm content area.
2. **Loading / Shimmer (CLS = 0 Discipline)**:
   - Do not place an isolated animated spinner in the middle of an empty screen.
   - Use a geometric *skeleton* whose dimensions, aspect ratio, and spacing match the final data content exactly 1:1.
3. **Populated (Data Present)**:
   - The normal state once the data payload is received and rendered.
   - It must survive extreme variation: long names without spaces (`min-w-0` + `truncate`), numbers in the hundreds of millions (`tabular-nums`), and images with unexpected ratios (`object-fit: cover`).
4. **Empty / Zero-Data**:
   - The state when the query succeeds but the entity collection is empty ($N = 0$).
   - Include these 3 components:
     1. A factual explanation of why the data is empty (not a sad message or an oversized empty illustration).
     2. A button or link for the first action that fills the data.
     3. A documentation or help link when the empty data is caused by missing access permission.
5. **Pending / Optimistic Mutating**:
   - The state while a data mutation is being sent to the server.
   - Apply an optimistic update to the interface with a non-intrusive micro indicator (button shows a *busy* state, opacity $0.8$, action text stays readable).
6. **Error / Degraded (Fault Tolerance)**:
   - The state when network transmission fails, the API returns a non-200 code, or the connection drops.
   - Separate field-level errors (handled inline) from full-screen errors (handled with an isolated fallback).

---

## 2. State Transition Table & Impossible State Prevention

Do not design separate boolean variables that can conflict logically (for example: `isLoading = true` together with `isError = true`). Use one uniform discriminated type:

```typescript
type SurfaceState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'populated'; data: T }
  | { status: 'empty'; reason: string; actionText: string; onAction: () => void }
  | { status: 'pending'; optimisticData: T; rollbackSnapshot: T }
  | { status: 'error'; message: string; recoverable: boolean; retry: () => void };
```

*Note: The 4 standard data states (loading, empty, populated, error) form the core content subset of the 6 full surface states.*

| Current State | Trigger Event | Next State | Visual Invariant That Must Hold |
|---|---|---|---|
| `idle` | `FETCH_START` | `loading` | Show the geometric skeleton; lock scroll if full-screen. |
| `loading` | `FETCH_SUCCESS (len > 0)` | `populated` | Replace the skeleton without a layout jump (*zero shift*). |
| `loading` | `FETCH_SUCCESS (len == 0)`| `empty` | Show guidance for creating the first data. |
| `loading` | `FETCH_FAILURE` | `error` | Show a specific message near the point of failure + a retry button. |
| `populated` | `MUTATE_OPTIMISTIC` | `pending` | Update the local view immediately; record a rollback snapshot. |
| `pending` | `MUTATE_CONFIRMED` | `populated` | Commit optimistic state; dismiss pending indicator without redraw flicker. |
| `pending` | `MUTATE_REJECTED` | `error` | Restore the data to the initial snapshot (*rollback*) + undo notification. |

---

## 3. Skeleton Geometry Discipline

1. **Locked Aspect Ratio**: Set an explicit CSS `aspect-ratio` on placeholder image boxes to prevent reflow when the image file loads.
2. **Low Chroma**: Use a neutral shimmer background with the same color temperature as the active theme, with minimal contour contrast so it does not glare.
3. **Motion Damping**: Respect the `@media (prefers-reduced-motion: reduce)` query: turn off the shimmering pulse animation (*pulsing wave*) and replace it with a static transparent color.
