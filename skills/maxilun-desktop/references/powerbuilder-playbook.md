# PowerBuilder & Enterprise Desktop Engineering Playbook

Engineering guide for maintaining, refactoring, and modernizing PowerBuilder applications (Appeon / Sybase PB 9 through 2022+), the DataWindow engine, PowerScript, and enterprise integration.

## 1. PowerBuilder Object Architecture & Transactions

### 1.1 Transaction Lifecycle & `SQLCA`
- **Initialization**: Connect `SQLCA` only once per work session, or use an isolated connection for background batch processes.
- **`SetTransObject` vs `SetTrans`**:
  - Use `dw_1.SetTransObject(SQLCA)`: it lets the application control the transaction (`CONNECT`, `COMMIT`, `ROLLBACK`) and keeps the connection open.
  - Do not use `dw_1.SetTrans(SQLCA)` for consecutive transactions, because it disconnects and reconnects on every `Retrieve()`.
- **Safe transaction pattern**:
  ```powerscript
  // Run the transaction and validate each status code
  dw_order.AcceptText()
  IF dw_order.Update(True, False) = 1 THEN
      IF dw_details.Update(True, False) = 1 THEN
          COMMIT USING SQLCA;
          dw_order.ResetUpdate()
          dw_details.ResetUpdate()
      ELSE
          ROLLBACK USING SQLCA;
          MessageBox("Error", "Failed to update details: " + SQLCA.SQLErrText, StopSign!)
      END IF
  ELSE
      ROLLBACK USING SQLCA;
      MessageBox("Error", "Failed to update header: " + SQLCA.SQLErrText, StopSign!)
  END IF
  ```

### 1.2 PB Object Hierarchy
- **Application (`.sra`)**: Entry point. Handle `open`, `close`, and `systemerror`. Catch fatal errors in `systemerror` and log them to a file before the crash.
- **Window (`.srw`)**: Window types (`Main!`, `Response!`, `Child!`, `Popup!`). Keep every response window modal and make it free its memory on close.
- **User Object (`.sru`)**: Move business logic into a Custom Non-Visual Object (NVO). Never place a complex query directly in a window button event.
- **Menu (`.srm`)**: Synchronize menu access rights with the user's role at login.

---

## 2. DataWindow Engine Standards

### 2.1 DataWindow Buffer Management
A DataWindow manages 4 internal buffers. Do not manipulate a buffer speculatively:
1. **`Primary!`**: Active data rows that the user can see and edit.
2. **`Filter!`**: Rows filtered out by the `dw_1.SetFilter()` filter expression.
3. **`Delete!`**: Rows deleted through `dw_1.DeleteRow()`. These rows become SQL `DELETE` statements on `dw_1.Update()`.
4. **`Original!`**: Column values before modification, used for concurrency conflict checks in the `WHERE` clause.

### 2.2 Critical Event Handling
- **`ItemChanged`**:
  - Use the `data` argument instead of `GetItem...`, because the buffer has not been updated yet.
  - Return values:
    - `0`: Accept the value and change the data.
    - `1`: Reject the value and do not let focus move.
    - `2`: Reject the value but let focus move (revert to the old value).
- **`ItemError`**: Suppress the confusing built-in system dialog by returning `1` or `3` after showing a structured error message.
- **`RetrieveStart` / `RetrieveEnd`**: Call `dw_1.SetRedraw(False)` before visually manipulating many rows and `dw_1.SetRedraw(True)` at the end.

### 2.3 DataWindow Definition Syntax (`.srd`)
The `.srd` file format is an internal declarative specification. When auditing or fixing an `.srd`:
- Check that column data types in the `table(...)` block match the database types.
- Do not hardcode a database connection inside DataWindow properties.
- Validate the DropDownDataWindow (`DDDW`) edit style so the display and data columns match the reference table.

---

## 3. Modern Integration & Interoperability

1. **REST API & JSON**:
   Use the native Appeon PB components `HTTPClient`, `JSONParser`, and `JSONGenerator` to connect a legacy application to modern microservices.
2. **Native DLL calls (C/C++)**:
   Declare external libraries with the correct calling convention (`alias for ...` and exact parameter types: 32-bit `long` vs 64-bit `longlong` on 64-bit PB).
3. **PFC (PowerBuilder Foundation Class)**:
   On a PFC-based system, respect the service-oriented architecture (`pfc_u_dw`, `pfc_n_cst_dwsrv`). Enable only the services you need (`of_SetUpdateChecks`, `of_SetSort`).
