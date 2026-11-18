"""Maxilun Zero-Dependency Output & Context Compressor.

Compresses CLI output and in-process message/log streams. Strips passing-test
noise and repeated log lines while preserving exit codes, file:line citations,
errors, and failing assertions.
"""

import re
from typing import List


class OutputCompressor:
    """Compresses noisy shell, log, and JSON outputs before they enter LLM context."""

    ERROR_LINE_RE = re.compile(
        r'(?i)(error|fail|failed|exception|traceback|panic|fatal|assert|warning|exit code|:\d+:\d+)'
    )

    @classmethod
    def compress_bash_output(cls, text: str, max_lines: int = 120) -> str:
        """Deduplicate consecutive/repeated lines and collapse verbose passing noise."""
        if not text:
            return text
        lines = text.splitlines()
        if len(lines) <= max_lines:
            return text

        kept: List[str] = []
        suppressed = 0
        seen_counts = {}

        # Always keep head (15 lines) and tail (40 lines), plus any error/warning lines in the middle
        head_end = 15
        tail_start = max(head_end, len(lines) - 40)

        for idx, line in enumerate(lines):
            if idx < head_end or idx >= tail_start:
                kept.append(line)
                continue

            if cls.ERROR_LINE_RE.search(line):
                if suppressed > 0:
                    kept.append(f"... [{suppressed} passing/verbose lines compressed] ...")
                    suppressed = 0
                kept.append(line)
                continue

            norm = re.sub(r'\d+', '#', line.strip())
            seen_counts[norm] = seen_counts.get(norm, 0) + 1
            if seen_counts[norm] <= 2 and len(kept) < max_lines - 45:
                kept.append(line)
            else:
                suppressed += 1

        if suppressed > 0:
            # Insert summary right before tail
            insert_at = max(0, len(kept) - (len(lines) - tail_start))
            kept.insert(insert_at, f"... [{suppressed} repetitive/passing lines compressed by Maxilun] ...")

        return "\n".join(kept)

