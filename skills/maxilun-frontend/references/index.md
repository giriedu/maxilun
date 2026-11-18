# Maxilun Frontend References Index

Reference catalog for Next.js 15 App Router and React 19 architecture:

- **`references/rsc-flight-patterns.md`**: React Server Components (RSC) vs Client Component boundaries, Next.js 15 async Request APIs (`cookies()`, `headers()`, `params`), Flight payload serialization, and layout containment.
- **`references/caching-revalidation-recipes.md`**: Deterministic cache profiles (`'force-cache'`, `'no-store'`), tag-based revalidation (`revalidateTag`), Time-Based ISR (`next: { revalidate }`), and Cache-Control headers.
- **`references/server-actions-state-hierarchy.md`**: Server Actions security (public POST endpoint paradigm, Zod boundary validation), React 19 optimistic updates (`useOptimistic`), and the 4-layer state hierarchy (URL $\to$ RSC $\to$ Client Island $\to$ Optimistic).
