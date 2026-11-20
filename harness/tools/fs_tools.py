"""Maxilun Native Filesystem Tools.

Provides deterministic read, write, edit, glob, and grep operations confined
to one root directory. Zero external dependencies.
"""

import re
from pathlib import Path
from typing import Dict, Any, Optional

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".next", "dist", "build"}
GREP_SUFFIXES = {".ts", ".tsx", ".js", ".jsx", ".py", ".md", ".sql", ".json", ".go", ".rs"}
GREP_HIT_CAP = 50
GLOB_HIT_CAP = 100


class FSTools:
    """Reads, writes, edits, and searches files under `root` only."""

    def __init__(self, root: Optional[Path] = None):
        self.root = Path(root or Path.cwd()).resolve()

    def _resolve(self, path: str) -> Path:
        # Model-supplied paths are untrusted: `../` or absolute paths must not escape the workspace.
        p = (self.root / (path or ".")).resolve()
        if p != self.root and self.root not in p.parents:
            raise PermissionError(f"Path '{path}' is outside the workspace root.")
        return p

    def _display(self, p: Path) -> str:
        try:
            return str(p.relative_to(self.root)).replace("\\", "/")
        except ValueError:
            return str(p)

    def read_file(self, path: str, offset: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        try:
            p = self._resolve(path)
        except PermissionError as e:
            return {"error": str(e)}
        if not p.exists():
            return {"error": f"File '{path}' does not exist."}
        if not p.is_file():
            return {"error": f"Path '{path}' is a directory, not a file."}

        try:
            lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
            start = max(1, offset or 1) - 1
            count = limit if limit is not None else len(lines)
            selected_lines = lines[start:start + count]
            formatted = [f"{start + idx + 1:4d} | {line}" for idx, line in enumerate(selected_lines)]
            return {
                "path": self._display(p),
                "total_lines": len(lines),
                "offset": start + 1,
                "lines_shown": len(selected_lines),
                "content": "\n".join(formatted)
            }
        except Exception as e:
            return {"error": f"Failed to read file: {str(e)}"}

    def write_file(self, path: str, content: str) -> Dict[str, Any]:
        try:
            p = self._resolve(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
            return {
                "success": True,
                "path": self._display(p),
                "bytes_written": len(content.encode("utf-8")),
                "line_count": len(content.splitlines())
            }
        except Exception as e:
            return {"error": f"Failed to write file: {str(e)}"}

    def edit_file(self, path: str, old_snippet: str, new_snippet: str) -> Dict[str, Any]:
        try:
            p = self._resolve(path)
        except PermissionError as e:
            return {"error": str(e)}
        if not p.exists():
            return {"error": f"File '{path}' does not exist for editing."}

        try:
            content = p.read_text(encoding="utf-8", errors="replace")
            occurrences = content.count(old_snippet)
            if occurrences == 0:
                return {"error": f"Target snippet not found in '{path}'. Please ensure exact match including whitespace."}
            if occurrences > 1:
                return {"error": f"Target snippet appears {occurrences} times in '{path}'. Provide a larger unique snippet."}

            p.write_text(content.replace(old_snippet, new_snippet, 1), encoding="utf-8")
            return {
                "success": True,
                "path": self._display(p),
                "diff_summary": f"Replaced {len(old_snippet.splitlines())} lines with {len(new_snippet.splitlines())} lines."
            }
        except Exception as e:
            return {"error": f"Failed to edit file: {str(e)}"}

    def glob_files(self, pattern: str, root_dir: str = ".") -> Dict[str, Any]:
        try:
            base = self._resolve(root_dir)
        except PermissionError as e:
            return {"error": str(e)}
        normalized_pat = pattern.replace("\\", "/")
        if normalized_pat.startswith("/") or ".." in normalized_pat.split("/"):
            return {"error": f"Pattern '{pattern}' must be relative and stay inside the workspace."}
        glob_pat = normalized_pat if "/" in normalized_pat or normalized_pat.startswith("**") else f"**/{normalized_pat}"

        matches = []
        for p in base.glob(glob_pat):
            if any(part in SKIP_DIRS or part.startswith("_maxilun_backup") for part in p.parts):
                continue
            matches.append(str(p.relative_to(base)).replace("\\", "/"))
            if len(matches) >= GLOB_HIT_CAP:
                break

        return {"pattern": pattern, "root": root_dir, "matches_count": len(matches), "files": sorted(matches)}

    def grep_files(self, pattern: str, path: str = ".") -> Dict[str, Any]:
        try:
            base = self._resolve(path)
            regex = re.compile(pattern)
        except (PermissionError, re.error) as e:
            return {"error": str(e)}

        hits = []
        search_files = [base] if base.is_file() else base.rglob("*")
        for f in search_files:
            if len(hits) >= GREP_HIT_CAP:
                break
            if not f.is_file() or f.suffix not in GREP_SUFFIXES or any(part in SKIP_DIRS for part in f.parts):
                continue
            try:
                lines = f.read_text(encoding="utf-8", errors="ignore").splitlines()
            except OSError:
                continue
            rel = self._display(f)
            for idx, line in enumerate(lines, 1):
                if regex.search(line):
                    hits.append(f"{rel}:{idx}: {line.strip()[:100]}")
                    if len(hits) >= GREP_HIT_CAP:
                        break

        return {"pattern": pattern, "hits_count": len(hits), "matches": hits, "truncated": len(hits) >= GREP_HIT_CAP}
