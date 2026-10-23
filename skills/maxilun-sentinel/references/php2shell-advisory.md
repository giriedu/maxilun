

---

## 8. Active Threat Advisory: php2shell (CVE-2026-109618, CVE-2026-109619)

**Status**: CRITICAL — Unauthenticated Remote Code Execution
**Published**: 21 October 2026
**Source**: [NCSC-NL/php2shell](https://github.com/NCSC-NL/php2shell), [CERT-EU 2026-018](https://cert.europa.eu/publications/security-advisories/2026-018/)
**Fixed versions**: PHP 8.5.12, 8.4.27, 8.3.36, 8.2.35

### What It Is

Two critical vulnerabilities in PHP that allow **unauthenticated remote code execution**:

- **CVE-2026-109618**: RCE via out-of-memory corruption during request cleanup
- **CVE-2026-109619**: RCE via stale request-owned global state reused by a later request on the same worker

**All PHP installations serving web requests are at risk**, including PHP-FPM, Apache mod_php, php-cgi, FrankenPHP, and LiteSpeed. Risk is highest for mod_php where exploitation can occur before application code runs.

PHP 8.1 and older are no longer supported. Backports exist for 7.4, 8.0, 8.1 but are minimal.

### Impact Scope

Not limited to websites. PHP is embedded in:
- Network appliances and management interfaces
- IoT devices and embedded systems
- Vendor products where admins cannot update PHP directly
- Docker images and container base images

### Immediate Actions

#### 1. Inventory (Priority: Internet-Facing First)

```bash
# Find all PHP installations
php -v                          # CLI version
php-fpm -v                      # FPM version
apachectl -M | grep php         # mod_php loaded?
docker ps --format '{{.Image}}' | xargs -I{} docker run --rm {} php -v 2>/dev/null

# Check package manager
apt list --installed 2>/dev/null | grep php
yum list installed 2>/dev/null | grep php
brew list | grep php            # macOS/Homebrew
```

Also check: cPanel EasyApache, Plesk, DirectAdmin, Bitnami stacks, XAMPP, Laragon.

#### 2. Patch

Update to fixed version immediately:
- PHP 8.5.12
- PHP 8.4.27
- PHP 8.3.36
- PHP 8.2.35

For vendor-bundled PHP (appliances, SaaS, managed hosting): check vendor advisory and apply their update.

#### 3. Temporary Mitigations (If Patching Not Possible)

These are **NOT complete fixes**. They reduce attack surface only.

```ini
; php.ini temporary mitigations
session.upload_progress.enabled = Off
memory_limit = 128M              ; Review: lower limits reduce OOM corruption window
post_max_size = 8M               ; Review: limit large payload attack surface

; PHP 8.5 only
fatal_error_backtraces = Off     ; Reduces memory pressure during error handling
```

Restart PHP workers after any ini change:
```bash
systemctl restart php*-fpm       # FPM
apachectl graceful               # mod_php
```

#### 4. Detection

Monitor for exploitation indicators:
- Unexpected outbound connections from PHP processes
- Anomalous `exec()`, `system()`, `passthru()`, `eval()` calls in logs
- Worker crashes/restarts without corresponding application errors
- Memory corruption errors in PHP error logs preceding suspicious activity

Community detection tool: [php2shell-guard](https://github.com/hezhidong/php2shell-guard) — cross-platform Python CLI that detects local PHP installations, classifies exposure, applies mitigations, and verifies.

#### 5. Verification After Patch

```bash
php -v   # Confirm version >= fixed version
# Re-run inventory to ensure ALL installations updated
```

### Integration dengan Maxilun Workflow

| Trigger | Action |
|---|---|
| User asks about PHP security / php2shell | Run §8 inventory + patch check |
| PR touches PHP dependencies | Block if PHP version < fixed version |
| Deploy pipeline with PHP | Add version gate: fail if vulnerable |
| Security audit requested | Include php2shell in scope until confirmed patched |
| New project with PHP stack | Set minimum PHP version to latest stable in composer.json / Dockerfile |

### References

- [NCSC-NL/php2shell](https://github.com/NCSC-NL/php2shell) — operational info, software list, detection tools
- [PHP Security Advisory](https://www.php.net/archive/2026.php#2026-10-21-5)
- [CERT-EU 2026-018](https://cert.europa.eu/publications/security-advisories/2026-018/)
- [EU CSIRT advisories collection](https://github.com/enisaeu/CNW/blob/main/advisories/2026/CNW-2026-04_php.md)
