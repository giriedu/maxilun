"""Maxilun Agent Persona & Alias Management Engine.

Provides bidirectional mapping between canonical agent IDs (e.g. 'maxilun-architect')
and user-defined custom callnames/personas (e.g. 'Bram', 'Maya', 'Alex').
Zero external dependencies.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, Optional, Any, List, Tuple

CANONICAL_AGENTS = [
    "maxilun-orchestrator",
    "maxilun-scout",
    "maxilun-architect",
    "maxilun-maker",
    "maxilun-studio",
    "maxilun-verifier",
    "maxilun-coder-frontend",
    "maxilun-coder-backend",
    "maxilun-coder-mobile",
    "maxilun-coder-systems",
    "maxilun-ui-designer",
    "maxilun-ui-motion",
    "maxilun-ui-reviewer",
    "maxilun-planner",
    "maxilun-security-auditor",
    "maxilun-coder-ai",
    "maxilun-data-engineer",
    "maxilun-devops",
    "maxilun-docsmith",
]

PRESETS: Dict[str, Dict[str, Dict[str, str]]] = {
    "default": {
        "maxilun-orchestrator": {"alias": "Orchestrator", "callsign": "Chief Orchestrator"},
        "maxilun-scout": {"alias": "Scout", "callsign": "Codebase Intelligence"},
        "maxilun-architect": {"alias": "Architect", "callsign": "Lead Architect"},
        "maxilun-maker": {"alias": "Maker", "callsign": "Polyglot Maker"},
        "maxilun-studio": {"alias": "Studio", "callsign": "Creative Studio"},
        "maxilun-verifier": {"alias": "Verifier", "callsign": "Verification QA"},
        "maxilun-coder-frontend": {"alias": "Frontend", "callsign": "Frontend Lead"},
        "maxilun-coder-backend": {"alias": "Backend", "callsign": "Backend Lead"},
        "maxilun-coder-mobile": {"alias": "Mobile", "callsign": "Mobile Engineer"},
        "maxilun-coder-systems": {"alias": "Systems", "callsign": "Systems & IoT"},
        "maxilun-ui-designer": {"alias": "Designer", "callsign": "UI/UX Principal"},
        "maxilun-ui-motion": {"alias": "Motion", "callsign": "Motion Specialist"},
        "maxilun-ui-reviewer": {"alias": "Reviewer", "callsign": "UI Purity Gatekeeper"},
        "maxilun-planner": {"alias": "Planner", "callsign": "Workstream Planner"},
        "maxilun-security-auditor": {"alias": "Auditor", "callsign": "Security Auditor"},
        "maxilun-coder-ai": {"alias": "AICoder", "callsign": "AI & RAG Engineer"},
        "maxilun-data-engineer": {"alias": "DataEng", "callsign": "Data Architect"},
        "maxilun-devops": {"alias": "DevOps", "callsign": "DevOps & SRE"},
        "maxilun-docsmith": {"alias": "DocSmith", "callsign": "DocSmith & Specs"},
    },
    "nusantara-squad": {
        "maxilun-orchestrator": {"alias": "Pandu", "callsign": "Chief Orchestrator"},
        "maxilun-scout": {"alias": "Sinta", "callsign": "Codebase Intelligence"},
        "maxilun-architect": {"alias": "Bram", "callsign": "Lead Architect"},
        "maxilun-maker": {"alias": "Bima", "callsign": "Polyglot Maker"},
        "maxilun-studio": {"alias": "Tara", "callsign": "Creative Studio"},
        "maxilun-verifier": {"alias": "Bagas", "callsign": "Verification QA"},
        "maxilun-coder-frontend": {"alias": "Fajar", "callsign": "Frontend Lead"},
        "maxilun-coder-backend": {"alias": "Dian", "callsign": "Backend Lead"},
        "maxilun-coder-mobile": {"alias": "Dimas", "callsign": "Mobile Engineer"},
        "maxilun-coder-systems": {"alias": "Gilang", "callsign": "Systems & IoT"},
        "maxilun-ui-designer": {"alias": "Maya", "callsign": "UI/UX Principal"},
        "maxilun-ui-motion": {"alias": "Aris", "callsign": "Motion Specialist"},
        "maxilun-ui-reviewer": {"alias": "Surya", "callsign": "UI Purity Gatekeeper"},
        "maxilun-planner": {"alias": "Arga", "callsign": "Workstream Planner"},
        "maxilun-security-auditor": {"alias": "Indra", "callsign": "Security Auditor"},
        "maxilun-coder-ai": {"alias": "Rama", "callsign": "AI & RAG Engineer"},
        "maxilun-data-engineer": {"alias": "Rian", "callsign": "Data Architect"},
        "maxilun-devops": {"alias": "Reza", "callsign": "DevOps & SRE"},
        "maxilun-docsmith": {"alias": "Citra", "callsign": "DocSmith & Specs"},
    },
    "global-forge": {
        "maxilun-orchestrator": {"alias": "Apex", "callsign": "Chief Orchestrator"},
        "maxilun-scout": {"alias": "Chloe", "callsign": "Codebase Intelligence"},
        "maxilun-architect": {"alias": "Alex", "callsign": "Lead Architect"},
        "maxilun-maker": {"alias": "Max", "callsign": "Polyglot Maker"},
        "maxilun-studio": {"alias": "Oliver", "callsign": "Creative Studio"},
        "maxilun-verifier": {"alias": "Lucas", "callsign": "Verification QA"},
        "maxilun-coder-frontend": {"alias": "Liam", "callsign": "Frontend Lead"},
        "maxilun-coder-backend": {"alias": "Viktor", "callsign": "Backend Lead"},
        "maxilun-coder-mobile": {"alias": "Leo", "callsign": "Mobile Engineer"},
        "maxilun-coder-systems": {"alias": "David", "callsign": "Systems & IoT"},
        "maxilun-ui-designer": {"alias": "Elena", "callsign": "UI/UX Principal"},
        "maxilun-ui-motion": {"alias": "Sophia", "callsign": "Motion Specialist"},
        "maxilun-ui-reviewer": {"alias": "Julian", "callsign": "UI Purity Gatekeeper"},
        "maxilun-planner": {"alias": "Arthur", "callsign": "Workstream Planner"},
        "maxilun-security-auditor": {"alias": "Ethan", "callsign": "Security Auditor"},
        "maxilun-coder-ai": {"alias": "Kai", "callsign": "AI & RAG Engineer"},
        "maxilun-data-engineer": {"alias": "Noah", "callsign": "Data Architect"},
        "maxilun-devops": {"alias": "Marcus", "callsign": "DevOps & SRE"},
        "maxilun-docsmith": {"alias": "Grace", "callsign": "DocSmith & Specs"},
    },
}


class AliasManager:
    """Manages active persona aliases, persistence, and bidirectional resolution."""

    def __init__(self, repo_root: Optional[Path] = None):
        if repo_root is None:
            # Walk up from current dir to find repository root (with .git or skills/)
            p = Path.cwd().resolve()
            while p.parent != p:
                if (p / ".git").exists() or (p / "skills" / "maxilun").exists():
                    repo_root = p
                    break
                p = p.parent
            if repo_root is None:
                repo_root = Path.cwd().resolve()

        self.repo_root = repo_root
        self.project_config_path = self.repo_root / ".maxilun" / "aliases.json"
        self.user_config_path = Path.home() / ".maxilun" / "aliases.json"
        self._cache: Optional[Dict[str, Any]] = None

    def get_config_path(self) -> Path:
        """Returns project config if it exists or parent exists, otherwise user config."""
        if self.project_config_path.exists() or (self.repo_root / ".maxilun").exists():
            return self.project_config_path
        return self.user_config_path

    def load_config(self) -> Dict[str, Any]:
        """Loads configuration from project, falling back to user global, then default preset."""
        if self._cache is not None:
            return self._cache

        for path in (self.project_config_path, self.user_config_path):
            if path.exists():
                try:
                    data = json.loads(path.read_text(encoding="utf-8"))
                    if isinstance(data, dict) and "agents" in data:
                        self._cache = data
                        return data
                except Exception:
                    pass

        # Default fallback config
        default_cfg = {
            "version": "1.0",
            "active_preset": "default",
            "agents": PRESETS["default"],
        }
        self._cache = default_cfg
        return default_cfg

    def save_config(self, config: Dict[str, Any], target: str = "project") -> Path:
        """Saves configuration to project or user global storage."""
        path = self.project_config_path if target == "project" else self.user_config_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        self._cache = config
        return path

    def apply_preset(self, preset_name: str, target: str = "project") -> Dict[str, Any]:
        """Applies a named preset and saves it."""
        if preset_name not in PRESETS:
            raise ValueError(f"Unknown preset '{preset_name}'. Available: {', '.join(PRESETS.keys())}")

        cfg = {
            "version": "1.0",
            "active_preset": preset_name,
            "agents": PRESETS[preset_name],
        }
        self.save_config(cfg, target=target)
        return cfg

    def set_alias(self, agent_id: str, alias: str, callsign: str = "", target: str = "project") -> Dict[str, Any]:
        """Updates or sets an alias for a specific canonical agent ID."""
        canonical = self.resolve_agent(agent_id) or agent_id
        if canonical not in CANONICAL_AGENTS:
            raise ValueError(f"Unknown agent '{agent_id}'. Must be one of: {', '.join(CANONICAL_AGENTS)}")

        cfg = dict(self.load_config())
        agents = dict(cfg.get("agents", {}))
        existing = agents.get(canonical, {})
        new_callsign = callsign if callsign else existing.get("callsign", canonical.replace("maxilun-", "").title())

        agents[canonical] = {
            "alias": alias.strip(),
            "callsign": new_callsign,
        }
        cfg["agents"] = agents
        cfg["active_preset"] = "custom"
        self.save_config(cfg, target=target)
        return cfg

    def resolve_agent(self, name_or_alias: str) -> Optional[str]:
        """Resolves an alias, mention (@Bram), or shortcut to canonical agent ID.
        
        Examples:
          - '@Bram' -> 'maxilun-architect' (if nusantara-squad)
          - 'maya' -> 'maxilun-ui-designer'
          - 'architect' -> 'maxilun-architect'
          - 'maxilun-architect' -> 'maxilun-architect'
        """
        if not name_or_alias:
            return None

        clean = name_or_alias.strip().lstrip("@")
        clean_lower = clean.lower()

        # 1. Direct canonical match
        if clean_lower in CANONICAL_AGENTS:
            return clean_lower

        # 2. Canonical without prefix (e.g. 'architect' -> 'maxilun-architect')
        prefixed = f"maxilun-{clean_lower}"
        if prefixed in CANONICAL_AGENTS:
            return prefixed

        # 3. Check active alias mappings
        cfg = self.load_config()
        agents = cfg.get("agents", {})
        for canonical, info in agents.items():
            if isinstance(info, dict):
                alias = info.get("alias", "")
                if alias and alias.lower() == clean_lower:
                    return canonical

        # 4. Fallback search across all known presets (case-insensitive)
        for preset_name, preset_agents in PRESETS.items():
            for canonical, info in preset_agents.items():
                alias = info.get("alias", "")
                if alias and alias.lower() == clean_lower:
                    return canonical

        return None

    def get_agent_info(self, agent_id: str) -> Dict[str, str]:
        """Returns {"alias": ..., "callsign": ...} for a canonical agent ID."""
        canonical = self.resolve_agent(agent_id) or agent_id
        cfg = self.load_config()
        agents = cfg.get("agents", {})
        if canonical in agents and isinstance(agents[canonical], dict):
            return agents[canonical]
        # Fallback
        short = canonical.replace("maxilun-", "").title()
        return {"alias": short, "callsign": short}

    def format_agent_tag(self, agent_id: str, style: str = "chat") -> str:
        """Formats agent identity tag for chat/roundtable display.
        
        Styles:
          - 'chat': '[Maya · UI/UX Principal]' or '[maxilun-ui-designer]'
          - 'verbose': '[Maya · UI/UX Principal (maxilun-ui-designer)]'
          - 'short': 'Maya'
        """
        canonical = self.resolve_agent(agent_id) or agent_id
        info = self.get_agent_info(canonical)
        alias = info.get("alias", "")
        callsign = info.get("callsign", "")

        cfg = self.load_config()
        active_preset = cfg.get("active_preset", "default")

        if active_preset == "default" and alias == canonical.replace("maxilun-", "").title():
            return f"[{canonical}]"

        if style == "short":
            return alias or canonical
        elif style == "verbose":
            return f"[{alias} · {callsign} ({canonical})]"
        else:  # default 'chat'
            if callsign and callsign.lower() != alias.lower():
                return f"[{alias} · {callsign}]"
            return f"[{alias} · {canonical}]"

    def list_presets(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        """Returns all built-in presets."""
        return PRESETS

    def get_summary(self) -> str:
        """Returns a formatted tabular summary of current alias configuration."""
        cfg = self.load_config()
        preset = cfg.get("active_preset", "default")
        agents = cfg.get("agents", {})

        lines = [
            f"Active Persona Profile: {preset.upper()}",
            f"Storage Location: {self.get_config_path()}",
            "-" * 65,
            f"{'Canonical Agent ID':<26} | {'Alias (Callname)':<15} | {'Callsign':<20}",
            "-" * 65,
        ]
        for canonical in CANONICAL_AGENTS:
            info = agents.get(canonical, {})
            alias = info.get("alias", "-")
            callsign = info.get("callsign", "-")
            lines.append(f"{canonical:<26} | {alias:<15} | {callsign:<20}")
        lines.append("-" * 65)
        return "\n".join(lines)


# Singleton instance
_GLOBAL_MANAGER: Optional[AliasManager] = None


def get_alias_manager(repo_root: Optional[Path] = None) -> AliasManager:
    """Returns the shared AliasManager instance."""
    global _GLOBAL_MANAGER
    if _GLOBAL_MANAGER is None or (repo_root and _GLOBAL_MANAGER.repo_root != repo_root):
        _GLOBAL_MANAGER = AliasManager(repo_root)
    return _GLOBAL_MANAGER
