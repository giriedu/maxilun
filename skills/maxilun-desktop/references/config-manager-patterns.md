# Desktop Config Manager Patterns: Safe Third-Party Config Editing, Secrets & Tauri Boundaries

<!-- metadata:
  version: "1.3.0"
  sync_target: "skills/maxilun-desktop/SKILL.md"
  origin: "Maxilun Desktop Engine"
-->

Rules for desktop tools that edit configuration files owned by other programs (CLI tools, IDEs, agents), store credentials on the user's machine, and expose that power through a webview IPC boundary. Covers key ownership, format-preserving patches, crash-safe atomic writes, concurrent-edit detection, per-OS path resolution, secret tiers, Tauri capability scoping, import/restore hardening, tray/autostart lifecycle, and the self-update channel. Complements `cross-platform-qt-tauri.md` (command shape, packaging), which this file does not repeat.

---

## 1. Ownership Model Before Any Write

A config manager is a guest in another program's file. Decide, per file, what it owns before writing a line of code.

| Ownership class | Example | Write rule | Removal rule |
|---|---|---|---|
| **Whole file owned** | A credentials file the manager generates per profile | Replace entire content | Delete allowed |
| **Owned keys** (connection: endpoint, auth, model id, protocol switch) | `base_url`, `api_key`, `model` | Clear all owned keys, then write the target profile's values | Always cleared on switch |
| **Profile-exclusive extras** (compat flags, window sizes a profile injected) | `max_output_tokens` set by profile A | Write on switch-in | Remove on switch-out only if the current value still equals what the manager wrote |
| **User keys** (everything else) | Theme, telemetry opt-out, custom hooks | Never written, never deleted | Never |

Rules:
1. Match owned keys by exact name, or by prefix only when the entire prefix namespace is connection/auth (an `AUTH_*` family). A prefix that also hosts feature toggles must be enumerated key by key.
2. An unclassified key is treated as a user key. This fails safe: the worst case is a stale value left behind, never a deleted user setting.
3. Keep the owned-key list in one module with a test that pins it. If the frontend mirrors the list (preset validation), add a parity test that loads both and diffs them.
4. Values the manager itself injected in older versions (defaults written by a legacy whole-file writer) form a frozen residue list of exact `(key, value)` pairs. Remove a residue entry only on an exact match; never widen the list by pattern.

---

## 2. Format-Preserving Patches

Parse, patch only the named key paths, serialize from the same syntax tree. Never round-trip through a plain data model that drops comments, ordering, or formatting.

| Format | Preserving approach (Rust) | Fallback when no preserving parser exists |
|---|---|---|
| TOML | `toml_edit::DocumentMut` | none needed |
| JSON | `serde_json` with `preserve_order`; re-indent with the file's detected indent | none needed |
| JSONC / JSON5 | Round-trip token tree that keeps comments and trailing commas; validate semantics with a separate strict parse | Refuse the edit and show the file path |
| YAML | Comment-preserving editors are rare and immature | Line-scoped edit of a single top-level scalar, or refuse; never `serde_yaml` round-trip on user files |
| `.env` | Line-oriented: replace `KEY=` lines in place, append new keys at end, keep comments and blank lines | none needed |

Invariants:
- **Parse failure is a hard stop.** Never fall back to an empty document. Writing a fresh document over an unparseable file erases the user's whole configuration; it is the single most damaging bug class in this domain.
- **Key paths are segment arrays**, not dotted strings. TOML and JSON keys may contain dots (`models."v4.5"`).
- **Duplicate keys** (legal in JSON5 parsers, last-wins) are detected and refused, not silently collapsed.
- **No-op detection**: if the serialized bytes hash equal to the original, skip the write entirely; this keeps mtimes stable and avoids waking file watchers in the host tool.
- A patch is a pure function `(path, Option<&[u8]>) -> Result<Option<Vec<u8>>>` where `None` output means delete. Pure patches make plan/preview/test trivial.

```rust
pub trait FilePatch {
    /// `before` is None when the file does not exist. Returning Ok(None) deletes the file.
    fn apply(&self, before: Option<&[u8]>) -> Result<Option<Vec<u8>>, PatchError>;
}

fn patch_toml(before: Option<&[u8]>, set: &[(Vec<&str>, toml_edit::Item)]) -> Result<Vec<u8>, PatchError> {
    let text = std::str::from_utf8(before.unwrap_or_default()).map_err(PatchError::Encoding)?;
    let mut doc: toml_edit::DocumentMut = text.parse().map_err(PatchError::Parse)?; // never default()
    for (path, item) in set {
        let (leaf, parents) = path.split_last().ok_or(PatchError::EmptyPath)?;
        let mut table = doc.as_table_mut();
        for seg in parents {
            table = table.entry(seg).or_insert(toml_edit::table())
                .as_table_mut().ok_or(PatchError::NotATable)?;
        }
        table.insert(leaf, item.clone());
    }
    Ok(doc.to_string().into_bytes())
}
```

---

## 3. Crash-Safe Write Pipeline

Order for every file write:

1. Read current bytes; record `sha256(before)` (`None` if absent).
2. Parse and patch in memory (Section 2). Abort here on any error; nothing is touched yet.
3. **Stage**: create a temp file in the *same directory* as the target (a cross-volume rename is not atomic), open with `create_new` to avoid clobbering a collision, set restrictive mode at creation for secret-bearing files, write, flush, `sync_all`.
4. **First-write backup**: the first time the manager ever touches a given path, copy the original bytes to a device-local backup directory keyed by a hash of the absolute path, plus a sidecar recording the original path. Once per path, never overwritten.
5. **Re-read and compare**: hash the target again. Unchanged means publish. Changed means an external writer raced you: re-plan from the new bytes (bounded, e.g. 3 attempts), or refuse for guarded writes (Section 5).
6. **Publish**: replace atomically.

Platform replace semantics:

| Platform | Primitive | Notes |
|---|---|---|
| Linux / macOS | `rename(tmp, target)` | Atomic within one filesystem. `fsync` the parent directory if durability across power loss matters. |
| Windows | `ReplaceFileW`, falling back to `MoveFileExW(MOVEFILE_REPLACE_EXISTING)` (what `std::fs::rename` uses) | `ReplaceFileW` keeps the target's ACL and identity. It fails on WSL UNC shares (`\\wsl$\`, `\\wsl.localhost\`); detect the prefix and go straight to the rename path. Retry a small fixed count on sharing violations (antivirus, indexers hold handles briefly). |

Symlinks: users often symlink dotfiles into a dotfiles repo. Resolve the link chain (bounded hop count, mirror the OS limit of about 40) and replace the *final target*, so the link survives. Renaming over the link itself turns it into a regular file on Unix and errors on Windows. Do not `canonicalize` on Windows just to resolve links: it rewrites the path to the `\\?\` verbatim form, which then leaks into logs, UI, and comparisons.

Permissions: on Unix, a staged file inherits the existing target's mode unless the file is secret-bearing (then force `0600`). On Windows, mode bits are meaningless; files under the user profile inherit a user-only ACL, which is the equivalent protection. Do not claim `0600` protection on Windows in UI text.

On failure after staging, delete the temp file unless a journal entry (Section 4) still references it for roll-forward.

---

## 4. Multi-File Operations: Intent Journal and Roll-Forward

Switching a profile often touches several files plus the manager's own database pointer ("active profile = B"). Reordering writes does not make this atomic: file written, pointer update fails, state is split.

Protocol:
1. Plan and stage every file first. Any failure in this phase aborts with zero changes.
2. Write a device-local journal entry: for each file, `{path, before_hash, after_hash, temp_path}`, plus the state commit to apply afterwards. Mark "publishing started" before the first replace.
3. Publish files in order, then apply the state commit. The state commit must be idempotent because recovery may run it twice.
4. Delete the journal entry.

Recovery on next start (or before the next operation on the same target), per file:

| Journal says | File hash equals | Action |
|---|---|---|
| publishing not started | before | Discard journal, delete temp files |
| publishing not started | neither | External edit happened; discard, touch nothing |
| publishing started | before | Commit the staged temp file (roll forward) |
| publishing started | after | Already published; continue |
| publishing started | neither | External writer wins; leave the file, still apply the state commit so pointers match published files, and report the path to the user |

Keep the journal and first-write backups in a **device-local** directory, never in a folder the user may point at a cloud-synced drive: intents and backups describe this machine's files.

---

## 5. Concurrent Edit Detection

Two kinds of writers exist and need different defenses.

- **In-process writers** (main window, tray menu, background sync, deep-link import): serialize with one lock per target application, held across plan, stage, and publish. Make it non-reentrant and acquire it in exactly one layer to avoid self-deadlock.
- **External writers** (the host CLI refreshing its own login token, the user in an editor): they do not participate in your lock. Use optimistic hash comparison (Section 3, step 5).

Rules:
- **Patch writes** re-plan on conflict: the patch applies to the new bytes, so user edits are preserved.
- **Guarded whole-file writes** (credential files the host tool also rewrites) record the expected pre-hash and **refuse** on mismatch instead of re-planning. Overwriting a token the host just refreshed logs the user out.
- State the residual race honestly in code comments: between the final hash check and the replace there is a small window no user-space protocol closes. Advisory file locks (`flock`, `LockFileEx`) only help if the host tool also takes them; most do not, so do not rely on them.
- File watchers (`notify`, `FSEvents`, `ReadDirectoryChangesW`) are for refreshing UI, not for correctness. Debounce them and ignore events caused by your own publish (compare post-write hash).

---

## 6. Per-OS Config Path Resolution

| Concern | Rule |
|---|---|
| Home directory | Use the platform API (`dirs::home_dir`, `SHGetKnownFolderPath`), not `HOME`/`USERPROFILE` alone. If unresolvable, fail loudly; a silent fallback to the working directory scatters files. |
| Host-tool locations | Mirror each tool's own documented resolution, including its env var override (for example a `<TOOL>_CONFIG_DIR` variable), then user-configured override, then the default. Show the resolved path in the UI. |
| Manager's own data | Per-OS app data dir (`%APPDATA%`, `~/Library/Application Support`, `$XDG_CONFIG_HOME` falling back to `~/.config`), or one dotfolder if the product already ships one. Do not migrate silently. |
| User override dirs | Expand `~` and `~\` yourself; normalize separators for comparison only, never for the path actually written. |
| Test isolation | One explicit env var overrides home for tests and short-circuits every heuristic. Tests must never fall through to the real profile. Read it with `var_os` so a non-UTF-8 value still counts as set. |
| WSL from Windows | Detect UNC prefixes `wsl$` and `wsl.localhost`; SQLite file locking and `ReplaceFileW` both misbehave there. Mapped drive letters cannot be detected; document it. |
| Device-local vs syncable | Split state: syncable (profiles, prompts) vs device-local (journals, backups, tokens index, window state). The override "store my data in this folder" applies to syncable state only. |

---

## 7. Secret Storage Tiers

| Tier | Mechanism | Use when | Caveats |
|---|---|---|---|
| 1. OS credential store | macOS Keychain, Windows Credential Manager (`CredWriteW`), Linux Secret Service (libsecret) | Secrets only the manager reads (sync passwords, repo tokens, OAuth refresh tokens) | Windows generic credential blob limit is 2560 bytes: check length before writing and fail with a specific message. Secret Service is absent on many headless and minimal Linux desktops: probe at runtime. |
| 2. Owner-only file | `0600` on Unix, profile ACL on Windows, written via the atomic path | Tier 1 unavailable | Surface a `secure_storage: false` flag so the UI states where the secret lives. |
| 3. Plaintext in host config | The host tool reads its key from its own file | Unavoidable when the host tool requires it | Mark those files private (Section 3); never copy them into logs or diagnostics bundles. |

Rules:
1. **Redact at the IPC boundary.** The settings object sent to the webview has every secret field emptied; the UI shows "set / not set". A write command accepts a new secret, but an empty field means "unchanged", never "clear". Clearing is an explicit command.
2. **Bind tokens to a host.** Store tokens keyed by hostname and look them up by the hostname of the actual request URL. A synced or imported record that changes a repo's host can then never redirect the token elsewhere.
3. **Keep secrets out of sync payloads.** If the database that holds profiles is uploaded to WebDAV or S3, either exclude secret columns, or encrypt client-side with a user passphrase-derived key (Argon2id plus an AEAD such as XChaCha20-Poly1305). A plaintext dump on a third-party server is a credential leak with extra steps.
4. Error strings from HTTP clients include the URL; strip query strings and userinfo before logging.
5. Test secret backends through a trait with an in-memory implementation; tests must never touch the real keychain.

---

## 8. Tauri Command Boundary and Capabilities

Capabilities in Tauri 2 scope plugin and core permissions per window. **Application commands registered with `generate_handler!` are callable from every window unless the app manifest declares them**, which makes them subject to capabilities. A narrow capability on a secondary window (tray panel, overlay) does not by itself restrict your own commands.

```rust
// build.rs: opt app commands into the permission system
fn main() {
    let attrs = tauri_build::Attributes::new().app_manifest(
        tauri_build::AppManifest::new().commands(&[
            "list_profiles", "switch_profile", "export_backup", "restore_backup",
        ]),
    );
    tauri_build::try_build(attrs).expect("tauri build");
}
```

Then grant `allow-list-profiles` alone to the tray window's capability and the full set to `main`.

Command rules:
1. **Paths from the webview are untrusted.** Prefer commands that open the native dialog in Rust and use the returned path directly. If the frontend must pass a path, verify it against a short-lived allowlist of dialog-issued paths.
2. **Filename arguments** (backup names, rename targets) reject separators, `..`, absolute paths, drive prefixes, and reserved Windows names (`CON`, `NUL`, `COM1`); then join to a fixed directory and assert the result's parent equals that directory.
3. **CSP**: `script-src 'self'` plus hashes only; restrict `connect-src` to the hosts the UI actually calls. Wide `http:`/`https:` sources in `img-src` and `connect-src` turn any injected markup into an exfiltration channel. Keep `assetProtocol.scope` empty unless a feature needs it.
4. Return typed errors with a stable code plus a message; a bare `String` error loses the code the UI needs for localization and recovery.
5. Long operations run in `spawn_blocking` or a tokio task (see `cross-platform-qt-tauri.md`) and report progress through events, not polling.

---

## 9. Import, Export, Restore and Deep Links

**SQL restore into a scratch database.** Load the dump into a temp file database, validate there, then swap.
- Install a SQLite authorizer (`rusqlite` `hooks` feature) that denies `ATTACH`/`DETACH` (also triggered by `VACUUM INTO`), virtual table creation (file-backed modules read and write arbitrary paths), any `PRAGMA` outside a small allowlist, and unknown action codes (deny by default so future SQLite statements fail closed). An authorizer works on the parsed statement; keyword scanning is bypassed by comments and casing.
- Run `PRAGMA integrity_check` and compare the schema against the expected tables and columns before the swap.
- Take an automatic backup of the live database before replacing it, and hold a restore lock that excludes every other writer during the swap.
- The same hardening applies to dumps arriving from sync: remote input is untrusted input.

**Archives** (skill bundles, exports): cap entry count, total uncompressed size, and per-entry ratio; use `ZipFile::enclosed_name` (or equivalent) and reject anything that resolves outside the extraction root; never follow symlink entries.

**Deep links** (`myapp://import?...`):
1. Register through the deep-link plugin; with single-instance enabled, a second launch forwards argv to the running instance, which must parse the link there.
2. Parse and validate in Rust, then queue the result in backend state and emit an event. The frontend may not be mounted yet (cold start, recreated window), so it also pulls the queue on mount.
3. **Never auto-apply.** Show what will change (endpoint host, which keys) and require a click. A link that silently installs a provider pointed at an attacker's endpoint routes the user's prompts and keys to that host.
4. Remote icon or metadata fetches triggered by a link: https only, size cap, timeout, no redirects to private address ranges.

---

## 10. Tray, Close-to-Tray, Autostart, Single Instance

- **Close-to-tray** is a setting, not a default surprise. Intercept `WindowEvent::CloseRequested`, call `prevent_close()`, hide. On Windows hide also requires `set_skip_taskbar(true)`; reset it when the window is shown again, including when a second-instance launch re-shows it.
- **Lightweight mode**: for tray-resident apps, destroying the webview window (not hiding it) frees the browser process memory. Requires the backend to own all authoritative state (downloaded updates, pending deep links, progress) so a recreated window can rehydrate. Persist window geometry before destroying.
- **Tray menu** is rebuilt from backend state after every state change; never cache labels in the menu itself.
- **macOS activation policy**: switch to `Accessory` when no window is visible so the Dock icon disappears, back to `Regular` when a window opens.
- **Autostart**: Windows `HKCU\...\Run` (per-user, no elevation), macOS login item pointing at the `.app` bundle path (pointing at the inner `Contents/MacOS` binary opens a terminal), Linux XDG autostart `.desktop` file. Read the actual OS state to render the toggle; do not trust a stored flag.
- **Single instance** plugin must be registered first in the builder so the second process exits before creating windows.

---

## 11. Self-Update Channel

| Rule | Reason |
|---|---|
| Updater artifacts are signed (Tauri updater uses minisign); the public key ships in config, the private key lives only in CI secrets | Integrity independent of hosting and TLS |
| Multiple endpoints are fine when every one serves the same signed manifest | Availability; signature still gates install |
| Detect install types that must not self-update: portable builds (marker file beside the executable), Linux `deb`/`rpm` (only AppImage is self-replaceable), store builds | Self-replacing a package-managed binary corrupts the package database |
| Download in the background, install only after explicit user confirmation; warn when installing will interrupt work in progress (an active local proxy, a running sync) | No surprise restarts |
| Keep the downloaded payload in backend memory, verified, rather than on disk | Avoids re-verification and stale-file cleanup on next launch; acceptable for payloads of tens of MB |
| One global "installing" guard shared by every entry point (dialog, settings page, tray) | Two concurrent installs race the binary replace |
| First check delayed after startup, then a fixed interval (hours) for long-running tray apps | Startup stays fast; resident apps still learn about fixes |
| A revoked release clears the cached payload and tells the UI to withdraw the prompt | Do not install a pulled build |

Do not hand-roll an updater that downloads and executes a script; never pipe a remote script into a shell during install or update.

---

## 12. Anti-Patterns and Verification

| Anti-pattern | Replace with |
|---|---|
| Rewrite the whole host config from the manager's model | Patch owned keys only (Sections 1, 2) |
| Default to an empty document when parsing fails | Refuse, surface path and parse error |
| Temp file in the system temp dir, then rename | Temp file beside the target |
| Blind overwrite of a credential file the host also writes | Guarded write with expected pre-hash |
| Secrets returned to the webview for display | Redacted settings plus set/not-set flags |
| Narrow window capability assumed to restrict app commands | App manifest command list plus per-window grants |
| Deep link applied without confirmation | Queue, preview, confirm |

Evidence to collect before claiming a config feature works:
- Round-trip test per format: a fixture with comments, odd indentation, unknown keys, and unicode keys survives patch then no-op patch byte-for-byte.
- Broken-file test: unparseable input leaves the file unchanged (bytes and mtime) and leaves no temp files.
- Race test: mutate the file between plan and publish; patch writes re-plan, guarded writes refuse.
- Crash test: kill the process after the journal is written at each publish step; next start converges per Section 4.
- Windows: symlinked target, read-only target, file held open by another process, WSL UNC path.
- IPC: invoke a privileged command from the restricted window and confirm it is denied.
