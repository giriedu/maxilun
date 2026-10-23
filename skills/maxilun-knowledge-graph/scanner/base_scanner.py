import fnmatch
from pathlib import Path
from typing import Set


class BaseScanner:
    """Shared utilities for all language scanners."""

    COMMON_SKIP_DIRS = frozenset({
        '.git', '.svn', '.hg', 'node_modules', 'dist', 'build', '.next',
        '__pycache__', '.venv', 'venv', 'vendor', '.maxilun', 'coverage',
        '.turbo', '.cache', 'target', '.idea', '.vscode'
    })

    def should_skip(self, file_path: Path, root: Path) -> bool:
        """
        Check if a file should be skipped based on relative path parts and gitignore.
        Always evaluates relative to root to prevent false skips on hidden parent folders.
        """
        try:
            rel = file_path.relative_to(root)
        except ValueError:
            return True

        # Check relative parts only (e.g. .hidden_subfolder inside project)
        for part in rel.parts[:-1]:  # check parent folders of the file
            if part.startswith('.') or part in self.COMMON_SKIP_DIRS:
                return True

        if rel.name.startswith('.'):
            return True

        return self._is_gitignored(file_path, root)

    def _is_gitignored(self, file_path: Path, root: Path) -> bool:
        """
        Check if file matches any gitignore patterns from root or parent directories.
        Supports standard glob, directory trailing slash, and negative (!) patterns.
        """
        try:
            rel = str(file_path.relative_to(root)).replace('\\', '/')
        except ValueError:
            return False

        # Gather gitignore files from root down to file directory
        gitignore_files = []
        curr = file_path.parent
        while curr >= root:
            gi = curr / '.gitignore'
            if gi.is_file():
                gitignore_files.append(gi)
            if curr == root:
                break
            curr = curr.parent

        # If no local gitignore, check root
        if not gitignore_files:
            root_gi = root / '.gitignore'
            if root_gi.is_file():
                gitignore_files.append(root_gi)

        # Process patterns (earliest/root first)
        ignored = False
        for gi in reversed(gitignore_files):
            try:
                patterns = gi.read_text(encoding='utf-8', errors='replace').splitlines()
                for line in patterns:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    is_negation = line.startswith('!')
                    if is_negation:
                        line = line[1:].strip()

                    match = False
                    if line.endswith('/'):
                        dir_name = line.rstrip('/')
                        if any(part == dir_name for part in file_path.relative_to(root).parts[:-1]):
                            match = True
                    elif '/' in line:
                        clean_pat = line.lstrip('/')
                        if fnmatch.fnmatch(rel, clean_pat) or fnmatch.fnmatch(rel, f"**/{clean_pat}"):
                            match = True
                    else:
                        if fnmatch.fnmatch(file_path.name, line) or any(part == line for part in file_path.relative_to(root).parts[:-1]):
                            match = True

                    if match:
                        ignored = not is_negation
            except Exception:
                pass

        return ignored
