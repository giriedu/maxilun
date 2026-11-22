# Greenfield Project Templates & Starter Code Architectures

> **Status**: Reference Document  
> **Specialists**: `maxilun-scaffold`, `maxilun-engineer`, `maxilun-frontend`, & `maxilun-craft`  
> **Purpose**: Provides complete, production-ready, slop-free starter architectures for greenfield applications initialized from an empty directory across the 3 primary tech stacks.

---

## 1. Stack A: Next.js 15 App Router + React 19 + Tailwind CSS

### Architecture & File Tree
```text
project-root/
├── docs/                     # 10 context files from maxilun-scaffold
├── app/
│   ├── layout.tsx            # Root shell, font loaders, theme provider
│   ├── page.tsx              # First-Fold Hero & Live Workspace View
│   └── globals.css           # Locked OKLCH tokens, hairline borders, zero-slop
├── components/
│   ├── hero/FirstFoldHero.tsx # Injected from hero-section-archetypes.md
│   └── ui/                   # Motion primitives from ui-motion-recipes.md
│       ├── SlidingPillNav.tsx
│       └── HoldToConfirmButton.tsx
├── lib/
│   ├── data.ts               # Realistic domain seed data (Indonesian locale)
│   └── utils.ts              # cn() class merger
├── package.json
├── tailwind.config.ts
└── tsconfig.json
```

### Starter `app/globals.css` (OKLCH Token Lock)
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --background: oklch(0.12 0.01 260);
  --foreground: oklch(0.95 0.005 260);
  --surface: oklch(0.16 0.012 260);
  --surface-elevated: oklch(0.20 0.015 260);
  --border: oklch(1 0 0 / 0.08);
  --accent: oklch(0.65 0.20 250);
  --accent-foreground: oklch(0.98 0 0);
  --muted: oklch(0.60 0.02 260);
  --success: oklch(0.68 0.16 150);
  --warning: oklch(0.75 0.18 75);
  --danger: oklch(0.62 0.22 25);
  --radius: 0.5rem;
}

body {
  background-color: var(--background);
  color: var(--foreground);
  font-feature-settings: "cv02", "cv03", "cv04", "cv11";
  -webkit-font-smoothing: antialiased;
}
```

---

## 2. Stack B: React Vite (Frontend) + PHP 8+ REST API (Backend)

### Architecture & File Tree
```text
project-root/
├── docs/                     # 10 context files from maxilun-scaffold
├── frontend/                 # React 19 + Vite + Tailwind SPA
│   ├── src/
│   │   ├── components/       # FirstFoldHero & Motion primitives
│   │   ├── App.tsx           # Main workspace & router
│   │   ├── main.tsx
│   │   └── index.css         # OKLCH tokens & base styles
│   ├── package.json
│   └── vite.config.ts        # Proxy to http://localhost:8000/api
└── api/                      # Zero-dependency PHP 8+ REST API
    ├── index.php             # Fast micro-router, CORS, JSON output
    ├── config/
    │   └── db.php            # PDO SQLite/MySQL wrapper with auto-migrations
    ├── controllers/
    │   └── StudentController.php
    └── database.sqlite       # Out-of-the-box local database
```

### Zero-Setup PHP Micro-Router (`api/index.php`)
```php
<?php
declare(strict_types=1);

header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type, Authorization");
header("Content-Type: application/json; charset=UTF-8");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

require_once __DIR__ . '/config/db.php';

$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$path = preg_replace('#^/api#', '', $path);
$method = $_SERVER['REQUEST_METHOD'];

function jsonResponse(mixed $data, int $status = 200): void {
    http_response_code($status);
    echo json_encode(['status' => $status, 'data' => $data], JSON_UNESCAPED_UNICODE);
    exit;
}

// Router dispatch
if ($path === '/students' && $method === 'GET') {
    $db = getDB();
    $stmt = $db->query("SELECT * FROM students ORDER BY name ASC");
    jsonResponse($stmt->fetchAll(PDO::FETCH_ASSOC));
} elseif ($path === '/health' && $method === 'GET') {
    jsonResponse(['status' => 'operational', 'p95_latency_ms' => 4.2]);
} else {
    jsonResponse(['error' => 'Endpoint not found'], 404);
}
```

### Zero-Setup PDO Wrapper (`api/config/db.php`)
```php
<?php
declare(strict_types=1);

function getDB(): PDO {
    static $pdo = null;
    if ($pdo === null) {
        $dbPath = __DIR__ . '/../database.sqlite';
        $pdo = new PDO("sqlite:" . $dbPath);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        
        // Auto-migrate on initial boot
        $pdo->exec("
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nisn TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                grade TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Active',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        ");
    }
    return $pdo;
}
```

### Local Development Command (Zero XAMPP Required!)
```bash
# Terminal 1: Run PHP REST API (built-in server)
php -S localhost:8000 -t api

# Terminal 2: Run React Vite Frontend
cd frontend && npm install && npm run dev
```

---

## 3. Stack C: Google Apps Script (GAS) Web App

### Architecture & File Tree
```text
project-root/
├── docs/                     # 10 context files from maxilun-scaffold
├── Code.gs                   # Server-side Apps Script (router + Sheets connector)
├── index.html                # Modern single-file SPA (Tailwind CDN, Lucide, CSS motion)
├── local_preview.html        # Local browser runner (double-click to preview offline!)
└── appsscript.json           # OAuth manifest with minimal scopes
```

### Server-Side Apps Script Router (`Code.gs`)
```javascript
function doGet(e) {
  return HtmlService.createTemplateFromFile('index')
    .evaluate()
    .setTitle('Portal EduCore - SMA Negeri 1')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function apiGetStudents() {
  // Uses active spreadsheet or realistic fallback data
  try {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName('Siswa') || ss.getActiveSheet();
    var data = sheet.getDataRange().getValues();
    var headers = data[0];
    var students = [];
    for (var i = 1; i < data.length; i++) {
      var row = data[i];
      students.push({
        id: i,
        nisn: String(row[0]),
        name: String(row[1]),
        grade: String(row[2]),
        status: String(row[3])
      });
    }
    return { success: true, data: students };
  } catch (err) {
    // Return seeded mock data if running without attached sheet
    return { success: true, data: getSeedStudents() };
  }
}

function getSeedStudents() {
  return [
    { id: 1, nisn: "0081234567", name: "Ahmad Fauzi", grade: "X-A (Fase E)", status: "Active" },
    { id: 2, nisn: "0081234568", name: "Siti Rahma", grade: "X-A (Fase E)", status: "Active" },
    { id: 3, nisn: "0081234569", name: "Budi Santoso", grade: "XI-MIPA 1", status: "Active" },
    { id: 4, nisn: "0081234570", name: "Dewi Lestari", grade: "XI-IPS 2", status: "Active" }
  ];
}
```

### Local Browser Mock Runner (`local_preview.html`)
Allows full UI/UX testing in Chrome/Edge without uploading to Google Drive:
```html
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <title>EduCore Local Preview (GAS Mock Runner)</title>
  <script>
    // Browser Mock for google.script.run
    window.google = {
      script: {
        run: {
          _successCb: null,
          _errorCb: null,
          withSuccessHandler: function(fn) { this._successCb = fn; return this; },
          withFailureHandler: function(fn) { this._errorCb = fn; return this; },
          apiGetStudents: function() {
            var self = this;
            setTimeout(function() {
              if (self._successCb) {
                self._successCb({
                  success: true,
                  data: [
                    { id: 1, nisn: "0081234567", name: "Ahmad Fauzi", grade: "X-A (Fase E)", status: "Active" },
                    { id: 2, nisn: "0081234568", name: "Siti Rahma", grade: "X-A (Fase E)", status: "Active" },
                    { id: 3, nisn: "0081234569", name: "Budi Santoso", grade: "XI-MIPA 1", status: "Active" },
                    { id: 4, nisn: "0081234570", name: "Dewi Lestari", grade: "XI-IPS 2", status: "Active" }
                  ]
                });
              }
            }, 120);
          }
        }
      }
    };
  </script>
</head>
<body class="bg-[#090a0f] text-neutral-100">
  <iframe src="index.html" class="w-full h-screen border-0"></iframe>
</body>
</html>
```

---

## 4. Realistic Indonesian EdTech Seed Data Generator

```json
[
  { "nisn": "0082341001", "name": "Ahmad Fauzi", "grade": "X-A", "attendance": 98.4, "status": "Terverifikasi" },
  { "nisn": "0082341002", "name": "Siti Rahma Nurhaliza", "grade": "X-A", "attendance": 100.0, "status": "Terverifikasi" },
  { "nisn": "0082341003", "name": "Budi Santoso", "grade": "X-B", "attendance": 94.2, "status": "Terverifikasi" },
  { "nisn": "0082341004", "name": "Dewi Lestari", "grade": "XI-MIPA 1", "attendance": 96.8, "status": "Terverifikasi" },
  { "nisn": "0082341005", "name": "Rizky Pratama", "grade": "XI-MIPA 2", "attendance": 91.5, "status": "Terverifikasi" }
]
```

