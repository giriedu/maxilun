"""Maxilun Native Skills & Agents Loader & Indexer.
Discovers, parses, and indexes the 27 Maxilun skills (1 orchestrator + 26 specialists)
and 21 autonomous agents from disk.
Zero external dependencies.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any, Set


AGENT_TOOL_MAP = {
    "Read": "read_file",
    "Write": "write_file",
    "Edit": "edit_file",
    "Glob": "glob_files",
    "Grep": "grep_files",
    "Bash": "execute_bash",
}

# The repo this harness ships in; used when the working directory has no installed skills.
HARNESS_REPO = Path(__file__).resolve().parents[2]


def _layout_roots(root: Path) -> List[Path]:
    return [root, root / ".agents", root / ".claude", HARNESS_REPO]


@dataclass
class AgentDefinition:
    name: str
    path: Path
    tools: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    allowed_harness_tools: Set[str] = field(default_factory=set)
    full_content: str = ""


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
    """Discovers, parses, and provides runtime system prompts for the 27 Maxilun skills and 21 agents."""
    def __init__(self, root_dir: Optional[Path] = None):
        self.root = root_dir or Path.cwd()
        self.skills_dir = self._find_skills_dir()
        self.agents_dir = self._find_agents_dir()
        self.skills: Dict[str, SkillDefinition] = {}
        self.agents: Dict[str, AgentDefinition] = {}
        self.load_all()
        self.load_agents()

    def _find_agents_dir(self) -> Path:
        for base in _layout_roots(self.root):
            if (base / "agents" / "maxilun-orchestrator.md").exists():
                return base / "agents"
        return self.root / "agents"

    def load_agents(self) -> Dict[str, AgentDefinition]:
        if not self.agents_dir.exists():
            return {}
        for agent_md in self.agents_dir.glob("*.md"):
            text = agent_md.read_text(encoding="utf-8", errors="replace")
            fm_match = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
            name = agent_md.stem
            tools: List[str] = []
            skills: List[str] = []
            if fm_match:
                fm = fm_match.group(1)
                n_match = re.search(r"^name:\s*([^\s]+)", fm, re.MULTILINE)
                if n_match:
                    name = n_match.group(1).strip()
                section = ""
                for line in fm.splitlines():
                    if re.match(r"^tools:\s*$", line):
                        section = "tools"
                        continue
                    if re.match(r"^skills:\s*$", line):
                        section = "skills"
                        continue
                    if section:
                        m_item = re.match(r"^\s*-\s*([A-Za-z0-9_-]+)", line)
                        if m_item:
                            if section == "tools":
                                tools.append(m_item.group(1))
                            else:
                                skills.append(m_item.group(1))
                        elif line.strip() and not line.startswith(" "):
                            section = ""
            allowed = {AGENT_TOOL_MAP[t] for t in tools if t in AGENT_TOOL_MAP}
            allowed.update({"kg_query", "kg_scan", "kg_locate", "send_handoff", "read_handoffs"})
            self.agents[name] = AgentDefinition(
                name=name,
                path=agent_md,
                tools=tools,
                skills=skills,
                allowed_harness_tools=allowed,
                full_content=text,
            )
        return self.agents

    def get_agent(self, name: str) -> Optional[AgentDefinition]:
        return self.agents.get(name)

    def _find_skills_dir(self) -> Path:
        for base in _layout_roots(self.root):
            if (base / "skills" / "maxilun" / "SKILL.md").exists():
                return base / "skills"
        raise FileNotFoundError(
            f"No Maxilun skills found under {self.root} (skills/, .agents/skills/, .claude/skills/) "
            f"or the harness repo {HARNESS_REPO}. Run from a repo with Maxilun installed."
        )

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

        # Frontmatter (supports inline scalars & folded/block multiline description)
        frontmatter: Dict[str, str] = {}
        fm_match = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
        if fm_match:
            fm_lines = fm_match.group(1).splitlines()
            idx = 0
            while idx < len(fm_lines):
                line = fm_lines[idx]
                if ":" in line and not line.startswith(" "):
                    k, v = line.split(":", 1)
                    k = k.strip()
                    v = v.strip()
                    if v in (">", "|", ">-", "|-"):
                        block = []
                        idx += 1
                        while idx < len(fm_lines) and (fm_lines[idx].startswith((" ", "\t")) or not fm_lines[idx].strip()):
                            if fm_lines[idx].strip():
                                block.append(fm_lines[idx].strip())
                            idx += 1
                        if k == "description":
                            frontmatter[k] = " ".join(block)
                        continue
                    v = v.strip('"').strip("'")
                    if k in ("name", "version", "ecosystem", "author", "description"):
                        frontmatter[k] = v
                idx += 1

        name = frontmatter.get("name", skill_md.parent.name)
        version = frontmatter.get("version", "1.3.0")
        ecosystem = frontmatter.get("ecosystem", "maxilun")

        # Triggers (from full description, including multi-line YAML folded descriptions)
        triggers = []
        desc_source = frontmatter.get("description") or text
        desc_match = re.search(r'Triggers:\s*(.+?)(?:$|\n[a-zA-Z0-9_-]+:)', desc_source, re.DOTALL)
        if desc_match:
            raw_triggers = re.sub(r'\s+', ' ', desc_match.group(1)).strip()
            raw_triggers = re.sub(r'\.\s*$', '', raw_triggers)
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
        """Finds the most specific skill matching the prompt (including maxilun); defaults to maxilun."""
        p = prompt.lower()
        scored_skills = []

        for skill in self.skills.values():
            score = 0
            for trig in skill.triggers:
                trig_clean = trig.lower().lstrip("/").strip()
                if not trig_clean:
                    continue
                if re.search(rf"(?<![a-z0-9_-]){re.escape(trig_clean)}(?![a-z0-9_-])", p):
                    score += len(trig_clean) * 2
                elif len(trig_clean) > 4 and trig_clean in p:
                    score += len(trig_clean)
            if score > 0:
                # Slight tie-break in favor of specialists when explicit slash/council isn't longer.
                priority = 0 if skill.name == "maxilun" else 1
                scored_skills.append((score, priority, skill))

        if scored_skills:
            scored_skills.sort(key=lambda x: (x[0], x[1]), reverse=True)
            return scored_skills[0][2]

        return self.skills.get("maxilun") or self.skills.get("maxilun-engineer")

    def build_system_prompt(self, skill_name: str, agent_name: Optional[str] = None) -> str:
        """Constructs an active system prompt for an agent executing with its declared skills."""
        skill = self.get_skill(skill_name)
        if not skill:
            skill = self.get_skill("maxilun") or list(self.skills.values())[0]

        parts = [
            f"# Role: {agent_name or skill.name} (Maxilun Ecosystem v{skill.version})",
        ]

        agent_def = self.get_agent(agent_name) if agent_name else None
        if agent_def:
            parts.extend([
                "",
                "## Autonomous Agent Contract",
                agent_def.full_content,
                "",
                "## Primary Skill Reference",
            ])

        parts.extend([
            "",
            skill.full_content,
        ])

        # Include secondary declared agent skills so multi-skill agents never drop capabilities.
        if agent_def and agent_def.skills:
            extra_skills = [self.get_skill(s) for s in agent_def.skills if s != skill.name and self.get_skill(s)]
            if extra_skills:
                parts.extend(["", "## Bundled Specialist Skills (Declared in Agent Frontmatter)"])
                for es in extra_skills:
                    summary = es.description or es.contract.get("Owns", "")
                    parts.append(f"- `{es.name}` ({es.path.name}, {es.line_count} lines): {summary[:220]}")
                    if es.contract.get("Owns"):
                        parts.append(f"  Owns: {es.contract['Owns']}")

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
