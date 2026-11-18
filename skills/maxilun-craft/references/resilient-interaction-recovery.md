# Resilient Interaction Recovery: Fault-Tolerant UX Patterns

<!-- metadata:
  version: "1.0.0"
  sync_target: "skills/maxilun-craft/SKILL.md"
  origin: "Maxilun Craft Engine"
-->

Engineering guide for error handling and fault-tolerant interaction recovery (*resilient interaction recovery*). A production interface treats network, validation, and transaction failures as a normal part of the application lifecycle. They are not anomalies to cover with an empty alert dialog.

---

## 1. Inline Proximity Principle (Error Next to Its Source)

1. **No Global Alert Modals for Local Errors**:
   - Show form-entry errors, single-file upload failures, and field validation errors directly below or beside the affected control.
   - Use a modal dialog only for fatal system-level failures that end the whole work session (for example: a permanently expired authentication token).
2. **Anatomy of a Complete Error Message**:
   A valid error message follows a three-part formula:
   - **What happened**: The objective fact (for example: *"The phone number is 2 digits short"*).
   - **Why it failed**: The system constraint that was not met (*"The standard format requires at least 10 digits"*).
   - **Direct fix path**: A concrete corrective action that needs no page reload (*"Add the area code"* or a *"Try sending again"* button).

---

## 2. Undo Transaction Pattern vs Confirmation Modal Fatigue

A pop-up dialog asking *"Are you sure you want to delete this data?"* causes cognitive fatigue (*confirmation modal fatigue*). Users often click through it without reading.

Replace it with the **Reversible Mutation (Undo Toast)** pattern:

```text
[Data removed from the list immediately]
        │
        ▼ (Show a floating status row for 6 seconds)
┌────────────────────────────────────────────────────────┐
│  1 contact moved to trash.                 [ Undo ]    │
└────────────────────────────────────────────────────────┘
```

### Undo Toast Invariants:
1. **Measured Duration**: Show the notification row for 5 to 8 seconds before the transaction is finalized on the server.
2. **Instant Undo Action**: Clicking the *"Undo"* button returns the element to its original position in the list immediately, without a full network refetch.
3. **Permanent Mutation Exception**: Use an explicit confirmation dialog only when the action is permanently destructive and cannot be undone (for example: deleting a production repository or permanently deleting an account).

---

## 3. Input Data Protection Invariants (Data Preservation)

1. **Never Clear the Form When Submission Fails**:
   - If `submit` fails because of a non-200 status response or a dropped network, keep everything the user typed intact in its field.
   - Mark invalid fields with a semantic red border and an icon indicator, but keep the user's input text so they do not retype from scratch.
2. **Automatic Local Draft Saving**:
   - For long forms (> 4 fields), save interim changes to local storage (`sessionStorage` or IndexedDB) so input survives an accidental tab close or a browser crash.
3. **Optimistic Mutation Rollback**:
   - If the interface updates state optimistically (for example: ticking a done checkbox) and the server then rejects the request, return the visual state to its original condition smoothly. Add a short inline notification stating why the request was rejected.

---

## 4. Degraded Mode & Network Partition Handling

1. **Active Connectivity Detection**:
   - Use the `navigator.onLine` event and `fetch` timeout monitoring to show a passive connection indicator in the status bar (*offline badge*). Do not block reading of content that is already cached.
2. **Pending Action Queue (Offline Queue)**:
   - Store user actions taken while the connection is down in a local queue, and synchronize them automatically when the connection returns (*automatic replay*).
