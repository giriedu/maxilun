# Server Actions, Flight Boundaries & State Hierarchy Playbook

Architecture standards for Next.js 15 App Router and React 19 applications: secure Server Actions, React Flight serialization boundaries, and hierarchical state management.

---

## 1. Server Actions Are Public HTTP POST Endpoints

Server Actions are compiled into accessible HTTP POST endpoints with synthetic action IDs. Treat every Server Action with the same security rigor as a public REST/GraphQL endpoint:

1. **Authentication & Authorization**:
   - Check user session and tenant authorization inside the action body. Never rely on client-side state or route middleware alone for mutation security.
2. **Input Validation at the Boundary**:
   - Parse every action argument through a strict schema validator (Zod, Valibot):

```typescript
'use server';

import { auth } from '@/lib/auth';
import { db } from '@/lib/db';
import { z } from 'zod';
import { revalidatePath } from 'next/cache';

const CreateCommentSchema = z.object({
  postId: z.string().uuid(),
  body: z.string().min(1).max(2000),
});

export async function createCommentAction(formData: FormData) {
  const session = await auth();
  if (!session?.user?.id) {
    throw new Error('Unauthorized');
  }

  const parsed = CreateCommentSchema.safeParse({
    postId: formData.get('postId'),
    body: formData.get('body'),
  });

  if (!parsed.success) {
    return { error: 'Validation failed', issues: parsed.error.issues };
  }

  await db.comments.create({
    data: {
      postId: parsed.data.postId,
      userId: session.user.id,
      body: parsed.data.body,
    },
  });

  revalidatePath(`/posts/${parsed.data.postId}`);
  return { success: true };
}
```

3. **Return Type Invariant**:
   - Return plain serializable JSON objects (e.g. `{ success: true, data }` or `{ error: string }`). Never leak database exceptions or internal stack traces to the client.

---

## 2. React Flight Boundary Serialization Invariants

React Server Components serialize data across the server-to-client boundary via the Flight protocol:

1. **Serializable Data Only**:
   - Only JSON-compatible primitives, plain objects, arrays, Maps, Sets, and Promises can cross the boundary.
   - Passing class instances with methods, closures, or non-serializable symbols results in a serialization runtime error.
2. **Data Minimization across Boundaries**:
   - Do not pass an entire database record containing 50 columns (including password hashes or internal tenant secrets) to a Client Component.
   - Project and pick only the fields needed by the visual component before passing them across the `'use client'` boundary.

---

## 3. Hierarchical State Architecture

Organize state into 4 distinct layers:

```text
[Layer 1: URL State (Search Params)]
  ├── Filter, sorting, active tab, page number
  └── Single source of truth for shareable, bookmarkable UI state
       │
[Layer 2: Server State (RSC Cache)]
  ├── Fetched database records, user profiles, permissions
  └── Revalidated on mutation via revalidateTag / revalidatePath
       │
[Layer 3: Client Island State (useState / useReducer)]
  ├── Transient UI: dropdown open/closed, modal visibility, active hover
  └── Scoped to the smallest possible leaf component
       │
[Layer 4: Optimistic State (useOptimistic)]
  ├── Immediate UI feedback during pending Server Action mutation
  └── Automatically rolls back on server rejection
```

### URL as Single Source of Truth
Never duplicate URL search parameters in local component `useState`. Read directly from `searchParams` in Server Components, or via `useSearchParams()` in Client Components with `Suspense` wrapping.
