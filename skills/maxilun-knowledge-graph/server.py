import http.server
import json
import os
import threading
from pathlib import Path
from urllib.parse import urlparse
from typing import Dict, Any, Optional

from graph_builder import GraphBuilder


class MaxilunServer:
    MAX_BODY_BYTES = 1048576  # 1MB limit

    def __init__(self, port: int = 8765, host: str = '127.0.0.1'):
        self.port = port
        self.host = host
        self.builder = GraphBuilder()
        self.current_graph: Optional[Dict[str, Any]] = None
        self.viewer_path = Path(__file__).parent / 'graph-viewer' / 'lens.html'
        self._server = None
        self._thread = None

    def scan(self, paths: list, names: list = None):
        for i, path in enumerate(paths):
            name = names[i] if names and i < len(names) else None
            print(f"  Scanning: {path} (as '{name or Path(path).name}')...")
            self.builder.scan_project(path, name)

        self.current_graph = self.builder.merge_projects()
        stats = self.builder.get_stats()
        print(f"\n  Indexed {stats['total_projects']} project(s):")
        for pname, pstats in stats['projects'].items():
            print(f"    - {pname}: {pstats['nodes']} nodes, {pstats['edges']} edges, {pstats['clusters']} clusters")

        return self.current_graph

    def start(self, open_browser: bool = False):
        server_ref = self

        class Handler(http.server.SimpleHTTPRequestHandler):
            def _validate_host_and_origin(self) -> bool:
                # DNS rebinding protection: validate Host header
                host_header = self.headers.get('Host', '')
                allowed_hosts = {
                    f'{server_ref.host}:{server_ref.port}',
                    server_ref.host,
                    f'localhost:{server_ref.port}',
                    'localhost',
                    f'127.0.0.1:{server_ref.port}',
                    '127.0.0.1'
                }
                if host_header and host_header not in allowed_hosts:
                    self.send_error(403, "Forbidden: Invalid Host header")
                    return False
                return True

            def _get_safe_cors_origin(self) -> Optional[str]:
                origin = self.headers.get('Origin')
                if not origin or origin == 'null':
                    return None
                parsed = urlparse(origin)
                try:
                    origin_port = parsed.port
                except ValueError:
                    return None
                if (parsed.scheme == 'http'
                        and origin_port == server_ref.port
                        and parsed.hostname in ('127.0.0.1', 'localhost', server_ref.host)):
                    return origin
                return None

            def do_OPTIONS(self):
                if not self._validate_host_and_origin():
                    return
                safe_origin = self._get_safe_cors_origin()
                self.send_response(204)
                if safe_origin:
                    self.send_header('Access-Control-Allow-Origin', safe_origin)
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.send_header('Access-Control-Max-Age', '86400')
                self.end_headers()

            def do_GET(self):
                if not self._validate_host_and_origin():
                    return

                parsed = urlparse(self.path)

                if parsed.path == '/':
                    self._serve_file(server_ref.viewer_path, 'text/html')
                elif parsed.path == '/api/graph':
                    self._serve_json(server_ref.current_graph or {})
                elif parsed.path == '/api/projects':
                    self._serve_json(server_ref.builder.get_stats())
                elif parsed.path == '/api/health':
                    self._serve_json({'status': 'ok', 'version': '1.0.0'})
                else:
                    requested = server_ref.viewer_path.parent / parsed.path.lstrip('/')
                    # Prevent path traversal
                    try:
                        safe_root = server_ref.viewer_path.parent.resolve()
                        file_path = requested.resolve()
                        file_path.relative_to(safe_root)
                    except (ValueError, OSError):
                        self.send_error(403)
                        return
                    if file_path.exists() and file_path.is_file():
                        content_type = 'text/html' if file_path.suffix == '.html' else \
                                       'application/javascript' if file_path.suffix == '.js' else \
                                       'text/css' if file_path.suffix == '.css' else \
                                       'application/json' if file_path.suffix == '.json' else 'text/plain'
                        self._serve_file(file_path, content_type)
                    else:
                        self.send_error(404)

            def do_POST(self):
                if not self._validate_host_and_origin():
                    return

                # Prevent untrusted external sites from triggering scan
                origin = self.headers.get('Origin')
                if origin == 'null':
                    self.send_error(403, "Forbidden: Opaque origins are not allowed")
                    return
                if origin and self._get_safe_cors_origin() != origin:
                    self.send_error(403, "Forbidden: Untrusted origin")
                    return

                parsed = urlparse(self.path)

                if parsed.path == '/api/scan':
                    try:
                        content_length = int(self.headers.get('Content-Length', 0))
                    except ValueError:
                        self.send_error(400, "Bad Content-Length")
                        return

                    if content_length > server_ref.MAX_BODY_BYTES:
                        self.send_error(413, "Payload Too Large: maximum 1MB")
                        return

                    body = self.rfile.read(content_length)
                    try:
                        data = json.loads(body)
                        paths = data.get('paths', [])
                        names = data.get('names', [])
                        # Validate all paths are within the server's working directory
                        safe_cwd = Path(os.getcwd()).resolve()
                        for p in paths:
                            try:
                                Path(p).resolve().relative_to(safe_cwd)
                            except ValueError:
                                self._serve_json(
                                    {'status': 'error', 'message': f'Path not allowed: {p}'},
                                    status=403
                                )
                                return
                        server_ref.scan(paths, names)
                        self._serve_json({'status': 'ok', 'graph': server_ref.current_graph})
                    except Exception as e:
                        self._serve_json({'status': 'error', 'message': str(e)}, status=500)
                else:
                    self.send_error(404)

            def _serve_file(self, file_path: Path, content_type: str):
                try:
                    content = file_path.read_bytes()
                    self.send_response(200)
                    self.send_header('Content-Type', f'{content_type}; charset=utf-8')
                    self.send_header('Content-Length', str(len(content)))
                    self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                    safe_origin = self._get_safe_cors_origin()
                    if safe_origin:
                        self.send_header('Access-Control-Allow-Origin', safe_origin)
                    self.end_headers()
                    self.wfile.write(content)
                except Exception:
                    self.send_error(500)

            def _serve_json(self, data: Any, status: int = 200):
                content = json.dumps(data, ensure_ascii=False).encode('utf-8')
                self.send_response(status)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Content-Length', str(len(content)))
                self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                safe_origin = self._get_safe_cors_origin()
                if safe_origin:
                    self.send_header('Access-Control-Allow-Origin', safe_origin)
                self.end_headers()
                self.wfile.write(content)

            def log_message(self, format, *args):
                pass

        self._server = http.server.HTTPServer((self.host, self.port), Handler)
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()

        url = f"http://{self.host}:{self.port}"
        print(f"\n  Maxilun Knowledge Graph Server running at {url}")

        if open_browser:
            import webbrowser
            webbrowser.open(url)

        return url

    def stop(self):
        if self._server:
            self._server.shutdown()
            self._server = None
            print("  Server stopped.")
