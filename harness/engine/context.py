"""Maxilun Session Context & State Manager.

Tracks conversation history, tool calls, touched files, and token usage.
Zero external dependencies.
"""

import uuid
import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Set, Optional


@dataclass
class Message:
    role: str  # "system", "user", "assistant", "tool"
    content: Optional[str] = None
    name: Optional[str] = None
    tool_call_id: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {"role": self.role}
        if self.content is not None:
            d["content"] = self.content
        if self.name:
            d["name"] = self.name
        if self.tool_call_id:
            d["tool_call_id"] = self.tool_call_id
        if self.tool_calls:
            d["tool_calls"] = self.tool_calls
        return d


@dataclass
class SessionContext:
    session_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    active_skill: str = "maxilun"
    decision_type: int = 2  # 1 (Type 1 Irreversible) or 2 (Type 2 Reversible)
    created_at: float = field(default_factory=time.time)
    messages: List[Message] = field(default_factory=list)
    touched_files: Set[str] = field(default_factory=set)
    commands_run: List[str] = field(default_factory=list)
    purity_warnings: List[str] = field(default_factory=list)
    tokens_in: int = 0
    tokens_out: int = 0

    def add_system_message(self, content: str):
        self.messages.append(Message(role="system", content=content))

    def add_user_message(self, content: str):
        self.messages.append(Message(role="user", content=content))

    def add_assistant_message(self, content: Optional[str], tool_calls: Optional[List[Dict[str, Any]]] = None):
        self.messages.append(Message(role="assistant", content=content, tool_calls=tool_calls))

    def add_tool_result(self, tool_call_id: str, tool_name: str, content: str):
        self.messages.append(Message(
            role="tool",
            name=tool_name,
            tool_call_id=tool_call_id,
            content=content
        ))

    def to_provider_messages(self) -> List[Dict[str, Any]]:
        return [m.to_dict() for m in self.messages]

    def record_file_edit(self, file_path: str):
        self.touched_files.add(file_path)

    def record_command(self, cmd: str):
        self.commands_run.append(cmd)

    def summary(self) -> Dict[str, Any]:
        duration_s = time.time() - self.created_at
        return {
            "session_id": self.session_id,
            "active_skill": self.active_skill,
            "decision_type": f"Type {self.decision_type}",
            "messages_count": len(self.messages),
            "touched_files": sorted(list(self.touched_files)),
            "commands_run_count": len(self.commands_run),
            "purity_warnings_count": len(self.purity_warnings),
            "duration_seconds": round(duration_s, 2),
            "tokens": {"in": self.tokens_in, "out": self.tokens_out}
        }
