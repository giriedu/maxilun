# Maxilun Lens — WebGL & 2D Knowledge Graph Visualizer

Architecture visualizer served by a local server. Load this file only when the user asks for a graph visualization (`/maxilun-graph`, `/maxilun-graph view`, "visualisasi" / "visualize", "tampilkan graf" / "show the graph").

## Trigger Commands
- `/maxilun-graph` or `/maxilun-knowledge-graph` → Scan the current project + open the visualizer
- `/maxilun-graph view` → Open the visualizer without re-scanning (use the cache)
- `/maxilun-graph scan <path>` → Scan a specific path + open the visualizer
- `/maxilun-graph multi <path1> <path2>` → Multi-project scan + open the visualizer

## Execution by the AI Agent

When the user triggers a command above, the AI agent MUST run:

```bash
# Locate cli.py relative to the skill folder:
# - In the repo workspace: python skills/maxilun-knowledge-graph/cli.py
# - In an agent install (~/.agents/skills or ~/.claude/skills): python <skills_dir>/maxilun-knowledge-graph/cli.py

# Scan the project folder and show its graph immediately. No manual graph.json import is needed:
python path/to/maxilun-knowledge-graph/cli.py scan . --view

# Scan another folder:
python path/to/maxilun-knowledge-graph/cli.py scan "<project-folder>" --view

# With no path argument, scan the current working folder:
python path/to/maxilun-knowledge-graph/cli.py scan --view

# Multi-project:
python path/to/maxilun-knowledge-graph/cli.py scan ./proj1 ./proj2 --name "Combined" --view

# Custom port:
python path/to/maxilun-knowledge-graph/cli.py scan . --view --port 9000
```

### Official Output Directory: `maxilun-out/`
Every `scan` automatically produces the artifact directory `maxilun-out/` at the project root:
- **`maxilun-out/lens.html`**: Self-contained 3D Galaxy & 2D Force-Directed Matrix visualizer. Double-click it to open in any browser; no local server is required.
- **`maxilun-out/graph.json`**: Structured node and edge graph data for AI agents and internal tooling.
- **`maxilun-out/MAXILUN_REPORT.md`**: Architecture report covering Core Hubs (god nodes), flow coordinators, community clusters, and language statistics.

> **Path Resolution**: Use a path relative to the skill folder location (`cli.py` lives inside the `maxilun-knowledge-graph/` folder), or set `MAXILUN_KG_CLI` yourself if you want to call it repeatedly in a terminal session.
> If `cli.py` is not found, make sure Python 3.8+ is installed and Maxilun is installed correctly.

The browser opens automatically at `http://127.0.0.1:8765` and loads the scanned graph directly. The server runs until Ctrl+C. Do not open `lens.html` directly to scan: the browser must not read local folders without the CLI process. JSON import is only for a graph that already exists.

## API Endpoints (for programmatic integration)
| Endpoint | Method | Description |
|---|---|---|
| `/api/graph` | GET | Return the current graph JSON |
| `/api/projects` | GET | Return per-project stats |
| `/api/health` | GET | Health check |
| `/api/scan` | POST | Trigger a scan via HTTP body `{paths: [...], names: [...]}` |

## Main Features

| Feature | Description |
|---|---|
| **3D Galaxy & Streamer Particles** | Phong-shaded sphere impostors with pulsing photon particles flowing along each edge from caller to callee |
| **Walk & Flight Camera (`W/A/S/D`)** | Explore the graph in 6-DOF (first-person flythrough) among the functions and modules |
| **Autopilot Tour** | The camera glides automatically from one node to the next along the call execution chain |
| **2D Holographic Matrix** | High-speed force-directed physics simulation, anti-aliased Bezier curves, and module cluster halos |
| **`Tab` Switch Mode** | Switch instantly between 3D Galaxy ↔ 2D Matrix modes |
| **Architectural Inspector** | Click a node → preview of the code signature, inbound/outbound metrics, source file, and cluster |
| **`Ctrl+K` Fuzzy Search** | Instant search for functions, classes, routes, and code files |
| **Path Trace (BFS)** | Finds and highlights the shortest call chain between two arbitrary symbols. *Note: accuracy depends on the quality of CALLS edges — non-Python/TS languages use best-effort detection.* |
| **3 Built-in Architecture Presets** | Maxilun Core Engine, Microservices E-Commerce API, and Autonomous Agent Memory |
