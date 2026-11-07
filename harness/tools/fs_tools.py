"""Maxilun Native Filesystem Tools.

Provides deterministic read, write, edit, glob, and grep operations.
Zero external dependencies.
"""

import fnmatch
import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional


class FSTools:
    """Safely reads, writes, edits, and searches repository files."""

    @staticmethod
    def read_file(path: str, offset: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        p = Path(path)
        if not p.exists():
            return {"error": f"File '{path}' does not exist."}
        if not p.is_file():
            return {"error": f"Path '{path}' is a directory, not a file."}

        try:
            content = p.read_text(encoding="utf-8", errors="replace")
            lines = content.splitlines()

            start = max(1, offset or 1) - 1
            count = limit if limit is not None else len(lines)
            selected_lines = lines[start:start + count]

            formatted = [f"{start + idx + 1:4d} | {line}" for idx, line in enumerate(selected_lines)]
            return {
                "path": str(p),
                "total_lines": len(lines),
                "offset": start + 1,
                "lines_shown": len(selected_lines),
                "content": "\n".join(formatted)
            }
        except Exception as e:
            return {"error": f"Failed to read file: {str(e)}"}

    @staticmethod
    def write_file(path: str, content: str) -> Dict[str, Any]:
        p = Path(path)
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
            return {
                "success": True,
                "path": str(p),
                "bytes_written": len(content.encode("utf-8")),
                "line_count": len(content.splitlines())
            }
        except Exception as e:
            return {"error": f"Failed to write file: {str(e)}"}

    @staticmethod
    def edit_file(path: str, old_snippet: str, new_snippet: str) -> Dict[str, Any]:
        p = Path(path)
        if not p.exists():
            return {"error": f"File '{path}' does not exist for editing."}

        try:
            content = p.read_text(encoding="utf-8", errors="replace")
            if old_snippet not in content:
                return {"error": f"Target snippet not found in '{path}'. Please ensure exact match including whitespace."}

            occurrences = content.count(old_snippet)
            if occurrences > 1:
                return {"error": f"Target snippet appears {occurrences} times in '{path}'. Provide a larger unique snippet."}

            updated = content.replace(old_snippet, new_snippet, 1)
            p.write_text(updated, encoding="utf-8")
            return {
                "success": True,
                "path": str(p),
                "diff_summary": f"Replaced {len(old_snippet.splitlines())} lines with {len(new_snippet.splitlines())} lines."
            }
        except Exception as e:
            return {"error": f"Failed to edit file: {str(e)}"}

    @staticmethod
    def glob_files(pattern: str, root_dir: str = ".") -> Dict[str, Any]:
        root = Path(root_dir)
        matches = []
        skip_dirs = {".git", "node_modules", "__pycache__", ".next", "dist", "build"}
        normalized_pat = pattern.replace("\\", "/")

        if "/" not in normalized_pat and not normalized_pat.startswith("**"):
            glob_pat = f"**/{normalized_pat}"
        else:
            glob_pat = normalized_pat

        for p in root.glob(glob_pat):
            if any(part in skip_dirs or part.startswith("_maxilun_backup") for part in p.parts):
                continue
            matches.append(str(p.relative_to(root)).replace("\\", "/"))
            if len(matches) >= 100:
                break

        return {
            "pattern": pattern,
            "root": root_dir,
            "matches_count": len(matches),
            "files": sorted(matches)
        }

    @staticmethod
    def grep_files(pattern: str, path: str = ".") -> Dict[str, Any]:
        root = Path(path)
        regex = re.compile(pattern)
        hits = []
        skip_dirs = {".git", "node_modules", "__pycache__", ".next", "dist", "build"}

        search_files = [root] if root.is_file() else root.rglob("*")
        for f in search_files:
            if not f.is_file():
                continue
            if any(part in skip_dirs for part in f.parts):
                continue
            if f.suffix not in {".ts", ".tsx", ".js", ".jsx", ".py", ".md", ".sql", ".json", ".go", ".rs"}:
                continue

            try:
                for idx, line in enumerate(f.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                    if regex.search(line):
                        rel = str(f.relative_to(Path.cwd()) if f.is_absolute() else f).replace("\\", "/")
                        hits.append(f"{rel}:{idx}: {line.strip()[:100]}")
                    if len(hits) >= 50:
                        break
            except Exception:
                continue

        return {
            "pattern": pattern,
            "hits_count": len(hits),
            "matches": hits
        }
