# React Server Components, Flight Serialization & Server Actions

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-frontend/SKILL.md"
  origin: "Maxilun Frontend Engine"
-->

Architecture guide for React Server Components (RSC) execution boundaries and the React Flight serialization protocol on Next.js 15 and React 19.

---

## 1. RSC vs Client Island Execution Boundaries

1. **Server Component by default**:
   - Every component inside the `app/` directory is a Server Component by default.
   - Add `import 'server-only'` to modules that read internal secrets or access the database directly, so compilation fails if one is accidentally imported into a Client Component.
2. **Client Leaf Component (`'use client'`)**:
   - Push the `'use client'` directive as deep as possible, to the leaves of the component tree (*leaf component*).
   - Never wrap `app/layout.tsx` or a whole page in `'use client'`.
3. **Donut Composition (Donut Pattern)**:
   - When an interactive component (such as a modal, dropdown, or tab) needs server-rendered content, pass the server content as `children: ReactNode` into the Client Component wrapper:

```tsx
// ClientWrapper.tsx ('use client')
export function ModalShell({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);
  return isOpen ? <div className="modal-backdrop">{children}</div> : null;
}

// Page.tsx (Server Component)
export default async function Page() {
  const data = await fetchSensitiveData();
  return (
    <ModalShell>
      <ServerRenderedContent data={data} />
    </ModalShell>
  );
}
```

---

## 2. React Flight Serialization Contract

The Flight protocol turns the RSC tree into a structured byte stream. Only certain data types are safe to send across the Server $\rightarrow$ Client boundary:

### Supported Types
- Primitive types: `string`, `number`, `boolean`, `null`, `undefined`, `bigint`.
- Standard data structures: `Array`, *plain object* (`{}`), `Map`, `Set`, `TypedArray`.
- Async contract: `Promise` (unwrapped in a Client Component with the React 19 `use()` hook).
- Components & elements: JSX nodes (`ReactNode`), and Server Action references marked `'use server'`.

### Types That Fail Serialization (Forbidden)
- Plain functions or callbacks (for example: an `onClick` defined in a Server Component).
- Custom class instances with a prototype or internal methods (for example: ORM model objects, `Decimal.js`). Map them to flat data objects (*Plain Old JavaScript Object* / POJO) before sending them to the Client.
- Real DOM nodes, `Symbol`, and `WeakMap`/`WeakSet`.

---

## 3. Server Actions Are Public HTTP Endpoints

Every function marked `'use server'` is an HTTP POST endpoint that can be called directly from outside the UI:

1. **Authorize inside the action**:
   - Always check the active user session on the first line of every Server Action.
2. **Validate the input schema**:
   - Validate the whole input payload (`FormData` or object) with Zod or a similar validation library before executing the mutation.
3. **Discriminated result pattern**:
   - Return a structured status object, `{ ok: true, data }` or `{ ok: false, fieldErrors }`, so form input stays intact and is not lost on failure.
