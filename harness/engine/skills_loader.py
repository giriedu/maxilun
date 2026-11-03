"""Maxilun Native Skills Loader & Indexer.

Discovers, parses, and indexes the 18 Maxilun specialist skills from disk.
Zero external dependencies.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any


@dataclass
class SkillDefinition:
    name: str
    version: str
    ecosystem: str
    path: Path
    description: str
    triggers: List[str] = field(default_factory=list)
    contract: Dict[str, str] = field(default_factory=dict)
    references: List[Path] = field(default_factory=list)
    line_count: int = 0
    full_content: str = ""

    def summary(self) -> str:
        ref_count = len(self.references)
        triggers_preview = ", ".join(self.triggers[:4]) if self.triggers else "none"
        return f"{self.name} (v{self.version}, {self.line_count} lines, {ref_count} references) — Triggers: [{triggers_preview}]"


class SkillsLoader:
    """Discovers, parses, and provides runtime system prompts for the 18 Maxilun skills."""

    def __init__(self, root_dir: Optional[Path] = None):
        self.root = root_dir or Path.cwd()
        self.skills_dir = self._find_skills_dir()
        self.skills: Dict[str, SkillDefinition] = {}
        self.load_all()

    def _find_skills_dir(self) -> Path:
        candidates = [
            self.root / "skills",
            self.root / ".agents" / "skills",
            self.root / ".claude" / "skills",
        ]
        for c in candidates:
            if c.exists() and (c / "maxilun" / "SKILL.md").exists():
                return c
        return self.root / "skills"

    def load_all(self) -> Dict[str, SkillDefinition]:
        if not self.skills_dir.exists():
            return {}

        for skill_folder in self.skills_dir.iterdir():
            if not skill_folder.is_dir():
                continue
            skill_md = skill_folder / "SKILL.md"
            if skill_md.exists():
                skill_def = self._parse_skill(skill_md)
                self.skills[skill_def.name] = skill_def

        return self.skills

    def _parse_skill(self, skill_md: Path) -> SkillDefinition:
        text = skill_md.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()

        # Frontmatter
        frontmatter = {}
        fm_match = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
        if fm_match:
            for line in fm_match.group(1).splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k in ("name", "version", "ecosystem", "author"):
                        frontmatter[k] = v

        name = frontmatter.get("name", skill_md.parent.name)
        version = frontmatter.get("version", "1.0.0")
        ecosystem = frontmatter.get("ecosystem", "maxilun")

        # Triggers
        triggers = []
        desc_match = re.search(r'Triggers:\s*([^\n\r]+)', text)
        if desc_match:
            raw_triggers = desc_match.group(1)
            triggers = [t.strip().strip('"').strip("'") for t in raw_triggers.split(",") if t.strip()]

        # Contract parsing
        contract = {}
        contract_patterns = {
            "Owns": r'\*\*Owns\*\*:\s*([^\n\r]+)',
            "Does not own": r'\*\*Does not own\*\*:\s*([^\n\r]+)',
            "Inputs": r'\*\*Inputs\*\*:\s*([^\n\r]+)',
            "Outputs": r'\*\*Outputs\*\*:\s*([^\n\r]+)',
            "Handoff": r'\*\*Handoff\*\*:\s*([^\n\r]+)',
        }
        for k, pat in contract_patterns.items():
            m = re.search(pat, text)
            if m:
                contract[k] = m.group(1).strip()

        # References
        ref_dir = skill_md.parent / "references"
        references = []
        if ref_dir.exists() and ref_dir.is_dir():
            references = [f for f in ref_dir.rglob("*.md") if f.is_file()]

        return SkillDefinition(
            name=name,
            version=version,
            ecosystem=ecosystem,
            path=skill_md,
            description=frontmatter.get("description", ""),
            triggers=triggers,
            contract=contract,
            references=references,
            line_count=len(lines),
            full_content=text
        )

    def get_skill(self, name: str) -> Optional[SkillDefinition]:
        return self.skills.get(name)

    def list_skills(self) -> List[SkillDefinition]:
        return sorted(self.skills.values(), key=lambda s: s.name)

    def match_skill(self, prompt: str) -> SkillDefinition:
        """Finds the most specific specialist matching the prompt; defaults to maxilun."""
        p = prompt.lower()
        scored_skills = []

        for skill in self.skills.values():
            if skill.name == "maxilun":
                continue  # Evaluate specialists first
            score = 0
            for trig in skill.triggers:
                trig_clean = trig.lower().lstrip("/").strip()
                if trig_clean in p:
                    score += len(trig_clean) * 2  # Longer specific trigger matches win

            if score > 0:
                scored_skills.append((score, skill))

        if scored_skills:
            scored_skills.sort(key=lambda x: x[0], reverse=True)
            return scored_skills[0][1]

        return self.skills.get("maxilun-engineer") or self.skills.get("maxilun")

    def build_system_prompt(self, skill_name: str) -> str:
        """Constructs an active system prompt for an agent executing as this specialist."""
        skill = self.get_skill(skill_name)
        if not skill:
            skill = self.get_skill("maxilun") or list(self.skills.values())[0]

        parts = [
            f"# Role: {skill.name} (Maxilun Ecosystem v{skill.version})",
            "",
            skill.full_content,
        ]

        # Summarize available on-demand references
        if skill.references:
            parts.extend([
                "",
                "## Bundled On-Demand Reference Files Available on Disk:",
            ])
            for ref in skill.references[:10]:
                try:
                    rel = ref.relative_to(self.root)
                    parts.append(f"- `{rel}`")
                except ValueError:
                    parts.append(f"- `{ref.name}`")

        return "\n".join(parts)
