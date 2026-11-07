import os
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple


CACHE_VERSION = "v1.2.0-s1"


class CacheManager:
    """
    Manages multi-tier file fingerprinting and granular per-file AST caching.

    Tier 1: O(1) stat check (st_size, st_mtime_ns) via stat-index.
    Tier 2: Content SHA-256 fingerprinting.
    Tier 3: Granular per-file AST cache (.maxilun/cache/ast/<version>/<sha256>.json).
    """

    def __init__(self, project_root: str, cache_dir: Optional[str] = None):
        self.project_root = Path(project_root).resolve()
        self.cache_dir = Path(cache_dir).resolve() if cache_dir else self.project_root / ".maxilun" / "cache"
        self.ast_dir = self.cache_dir / "ast" / CACHE_VERSION
        self.stat_index_file = self.cache_dir / "stat-index.json"
        self.manifest_file = self.project_root / ".maxilun" / "manifest.json"

        self.stat_index: Dict[str, Dict[str, Any]] = {}
        self.manifest: Dict[str, Dict[str, Any]] = {}
        self._load_state()

    def _load_state(self):
        self.ast_dir.mkdir(parents=True, exist_ok=True)
        if self.stat_index_file.is_file():
            try:
                with open(self.stat_index_file, "r", encoding="utf-8") as f:
                    self.stat_index = json.load(f)
            except Exception:
                self.stat_index = {}

        if self.manifest_file.is_file():
            try:
                with open(self.manifest_file, "r", encoding="utf-8") as f:
                    self.manifest = json.load(f)
            except Exception:
                self.manifest = {}

    def get_file_ast(self, rel_path: str, abs_path: Path) -> Tuple[Optional[Dict[str, Any]], str]:
        """
        Retrieves cached AST nodes/edges if file has not changed.
        Returns: (cached_ast_dict or None, current_sha256)
        """
        try:
            stat = abs_path.stat()
            size = stat.st_size
            mtime_ns = stat.st_mtime_ns
        except OSError:
            return None, ""

        entry = self.stat_index.get(rel_path)
        sha256_hash = ""

        # Tier 1: Check stat equality
        if entry and entry.get("size") == size and entry.get("mtime_ns") == mtime_ns:
            sha256_hash = entry.get("sha256", "")
            if sha256_hash:
                ast_file = self.ast_dir / f"{sha256_hash}.json"
                if ast_file.is_file():
                    try:
                        with open(ast_file, "r", encoding="utf-8") as f:
                            cached_data = json.load(f)
                            return cached_data, sha256_hash
                    except Exception:
                        pass

        # Tier 2: Compute SHA-256 content hash
        try:
            content = abs_path.read_bytes()
            sha256_hash = hashlib.sha256(content).hexdigest()
        except OSError:
            return None, ""

        # Check if AST exists for this content hash (e.g. reverted file or touched mtime)
        ast_file = self.ast_dir / f"{sha256_hash}.json"
        if ast_file.is_file():
            try:
                with open(ast_file, "r", encoding="utf-8") as f:
                    cached_data = json.load(f)
                    self._update_stat_entry(rel_path, size, mtime_ns, sha256_hash)
                    return cached_data, sha256_hash
            except Exception:
                pass

        return None, sha256_hash

    def save_file_ast(self, rel_path: str, abs_path: Path, sha256_hash: str, ast_data: Dict[str, Any]):
        """
        Caches the AST extraction result for a file by its SHA-256 content hash.
        """
        try:
            stat = abs_path.stat()
            size = stat.st_size
            mtime_ns = stat.st_mtime_ns
        except OSError:
            size = 0
            mtime_ns = 0

        if not sha256_hash:
            try:
                sha256_hash = hashlib.sha256(abs_path.read_bytes()).hexdigest()
            except OSError:
                return

        ast_file = self.ast_dir / f"{sha256_hash}.json"
        try:
            with open(ast_file, "w", encoding="utf-8") as f:
                json.dump(ast_data, f, ensure_ascii=False)
        except Exception:
            pass

        self._update_stat_entry(rel_path, size, mtime_ns, sha256_hash)

    def _update_stat_entry(self, rel_path: str, size: int, mtime_ns: int, sha256_hash: str):
        self.stat_index[rel_path] = {
            "size": size,
            "mtime_ns": mtime_ns,
            "sha256": sha256_hash
        }
        self.manifest[rel_path] = {
            "mtime": mtime_ns / 1_000_000_000.0,
            "ast_hash": sha256_hash
        }

    def prune_stale_entries(self, active_rel_paths: Set[str]):
        """
        Removes metadata for deleted files.
        """
        current_tracked = set(self.stat_index.keys())
        deleted = current_tracked - active_rel_paths
        for d in deleted:
            self.stat_index.pop(d, None)
            self.manifest.pop(d, None)

    def persist(self):
        """
        Flushes stat-index.json and manifest.json to disk.
        """
        try:
            self.stat_index_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.stat_index_file, "w", encoding="utf-8") as f:
                json.dump(self.stat_index, f, indent=2, ensure_ascii=False)

            self.manifest_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.manifest_file, "w", encoding="utf-8") as f:
                json.dump(self.manifest, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
