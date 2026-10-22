# Maxilun Lens — WebGL & 2D Knowledge Graph Visualizer

Visualizer arsitektur dengan local server. Load file ini hanya saat user meminta visualisasi graf (`/msal-graph`, `/msal-graph view`, "visualisasi", "tampilkan graf").

## Trigger Commands
- `/msal-graph` atau `/msal-knowledge-graph` → Scan project saat ini + buka visualizer
- `/msal-graph view` → Buka visualizer tanpa re-scan (gunakan cache)
- `/msal-graph scan <path>` → Scan path spesifik + buka visualizer
- `/msal-graph multi <path1> <path2>` → Multi-project scan + buka visualizer

## Eksekusi oleh AI Agent

Saat user trigger command di atas, AI agent HARUS menjalankan:

```bash
# Tentukan lokasi cli.py relatif terhadap folder skill:
# - Di workspace repo: python skills/maxilun-knowledge-graph/cli.py
# - Di instalasi agen (~/.agents/skills atau ~/.claude/skills): python <skills_dir>/maxilun-knowledge-graph/cli.py

# Single project (paling umum):
python path/to/maxilun-knowledge-graph/cli.py scan . --view

# Multi-project:
python path/to/maxilun-knowledge-graph/cli.py scan ./proj1 ./proj2 --name "Combined" --view

# Custom port:
python path/to/maxilun-knowledge-graph/cli.py scan . --view --port 9000
```

> **Resolusi Path**: Gunakan path relatif terhadap lokasi folder skill (`cli.py` berada di dalam folder `maxilun-knowledge-graph/`), atau set `MAXILUN_KG_CLI` secara mandiri jika ingin memanggilnya berulang kali dalam sesi terminal.
> Jika `cli.py` tidak ditemukan, pastikan Python 3.8+ terpasang dan Maxilun terinstall dengan benar.

Browser akan otomatis terbuka di `http://127.0.0.1:8765`. Server berjalan hingga Ctrl+C.

## API Endpoints (untuk integrasi programatik)
| Endpoint | Method | Deskripsi |
|---|---|---|
| `/api/graph` | GET | Return graph JSON saat ini |
| `/api/projects` | GET | Return stats per-project |
| `/api/health` | GET | Health check |
| `/api/scan` | POST | Trigger scan via HTTP body `{paths: [...], names: [...]}` |

## Fitur Utama

| Fitur | Deskripsi |
|---|---|
| **3D Galaxy & Streamer Particles** | Sphere impostor Phong shader dengan partikel foton berdenyut mengalir sepanjang edge dari caller ke callee |
| **Walk & Flight Camera (`W/A/S/D`)** | Jelajahi graf secara 6-DOF (first-person flythrough) langsung di antara kumpulan fungsi dan modul |
| **Autopilot Tour** | Kamera otomatis melayang dari satu simpul ke simpul berikutnya mengikuti rantai eksekusi panggilan |
| **2D Holographic Matrix** | Simulasi fisika force-directed berkecepatan tinggi, lengkungan Bezier anti-aliased, dan halo kluster modul |
| **`Tab` Switch Mode** | Beralih instan antara mode 3D Galaxy ↔ 2D Matrix |
| **Architectural Inspector** | Klik node → pratinjau signature kode, metrik inbound/outbound, file sumber, dan kluster |
| **`Ctrl+K` Fuzzy Search** | Pencarian instan untuk fungsi, kelas, rute, dan berkas kode |
| **Path Trace (BFS)** | Menemukan dan menyorot rantai panggilan terpendek antara dua simbol arbitrer. *Catatan: akurasi bergantung pada kualitas CALLS edges — bahasa non-Python/TS menggunakan deteksi best-effort.* |
| **3 Preset Arsitektur Bawaan** | Maxilun Core Engine, Microservices E-Commerce API, dan Autonomous Agent Memory |
