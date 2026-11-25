"""Maxilun Tool Registry & Function Dispatcher.

Formats native tools into OpenAI/DeepSeek function calling schemas
and executes tool calls deterministically. Zero external dependencies.
"""

from pathlib import Path
from typing import Dict, Any, List, Callable, Optional, Set

from .fs_tools import FSTools
from .bash_tool import BashTool
from .kg_tool import KnowledgeGraphTool


class ToolRegistry:
    """Central registry and dispatcher for all agent-callable tools."""

    def __init__(self, repo_root: Path):
        self.root = repo_root
        self.fs = FSTools(repo_root)
        self.bash = BashTool(repo_root)
        self.kg = KnowledgeGraphTool(repo_root)
        self._custom_schemas: Dict[str, Dict[str, Any]] = {}

        self._tools: Dict[str, Callable] = {
            "read_file": self.fs.read_file,
            "write_file": self.fs.write_file,
            "edit_file": self.fs.edit_file,
            "glob_files": self.fs.glob_files,
            "grep_files": self.fs.grep_files,
            "execute_bash": self.bash.execute,
            "kg_query": self.kg.query,
            "kg_scan": self.kg.scan,
            "kg_locate": self.kg.locate,
        }

    def get_tool_schemas(self, allowed_tools: Optional[Set[str]] = None) -> List[Dict[str, Any]]:
        """Returns standard OpenAI/DeepSeek function schemas for tool calling."""
        schemas = [
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Read file contents with line numbering, optional offset, and limit.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Relative path to file"},
                            "offset": {"type": "integer", "description": "1-based starting line number"},
                            "limit": {"type": "integer", "description": "Maximum lines to read"}
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "write_file",
                    "description": "Create a new file or completely overwrite an existing file.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Relative path to file"},
                            "content": {"type": "string", "description": "Full file content"}
                        },
                        "required": ["path", "content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "edit_file",
                    "description": "Surgically replace an exact code snippet inside a file.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Relative path to file"},
                            "old_snippet": {"type": "string", "description": "Exact text to find and replace"},
                            "new_snippet": {"type": "string", "description": "Replacement text"}
                        },
                        "required": ["path", "old_snippet", "new_snippet"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "glob_files",
                    "description": "Find files matching a glob pattern.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pattern": {"type": "string", "description": "File glob pattern (e.g. '*.ts', 'SKILL.md')"},
                            "root_dir": {"type": "string", "description": "Root directory to search", "default": "."}
                        },
                        "required": ["pattern"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "grep_files",
                    "description": "Search code using regular expressions.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pattern": {"type": "string", "description": "Regular expression pattern"},
                            "path": {"type": "string", "description": "File or folder path", "default": "."}
                        },
                        "required": ["pattern"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "execute_bash",
                    "description": "Execute a terminal shell command.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "command": {"type": "string", "description": "Shell command to run"},
                            "timeout": {"type": "integer", "description": "Timeout in seconds", "default": 30}
                        },
                        "required": ["command"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "kg_query",
                    "description": "Query the Knowledge Graph AST index (defOf, callsIn, callsOut, importersOf, implementsOf, extendsOf, routesOf).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "operator": {
                                "type": "string",
                                "enum": ["defOf", "callsIn", "callsOut", "importersOf", "implementsOf", "extendsOf", "routesOf"],
                                "description": "Query operator",
                            },
                            "symbol": {"type": "string", "description": "Symbol or file name to inspect"},
                            "target_path": {"type": "string", "description": "Project root path", "default": "."}
                        },
                        "required": ["operator", "symbol"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "kg_locate",
                    "description": "Find where behaviour lives. Takes a plain-language question, a stack trace, or a symbol name; returns ranked file:line ranges with verbatim excerpts and caller leads. Call this before read_file or grep_files when the target location is unknown.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string", "description": "Question, stack trace, or symbol name"},
                            "also": {"type": "string", "description": "Comma-separated identifiers or synonyms the code may use"},
                            "target_path": {"type": "string", "description": "Project root path", "default": "."},
                            "top": {"type": "integer", "description": "Maximum files to return", "default": 5},
                            "lines": {"type": "integer", "description": "Maximum excerpt lines per range", "default": 14},
                            "budget": {"type": "integer", "description": "Total excerpt characters", "default": 6000},
                            "include_hits": {"type": "boolean", "description": "Return structured hit metadata", "default": False},
                            "refresh": {"type": "boolean", "description": "Refresh index before locating", "default": False}
                        },
                        "required": ["question"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "kg_scan",
                    "description": "Scan project to build or update Knowledge Graph AST index.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "target_path": {"type": "string", "description": "Path to scan", "default": "."}
                        }
                    }
                }
            }
        ] + list(self._custom_schemas.values())
        if allowed_tools is None:
            return schemas
        return [s for s in schemas if s.get("function", {}).get("name") in allowed_tools]

    def execute(self, tool_name: str, arguments: Dict[str, Any], allowed_tools: Optional[Set[str]] = None) -> Dict[str, Any]:
        """Dispatches tool execution safely with error handling."""
        if allowed_tools is not None and tool_name not in allowed_tools:
            return {"error": f"Permission denied: tool '{tool_name}' is not allowed for this agent."}
        fn = self._tools.get(tool_name)
        if not fn:
            return {"error": f"Tool '{tool_name}' not found in registry."}

        try:
            return fn(**arguments)
        except TypeError as e:
            return {"error": f"Invalid arguments for tool '{tool_name}': {str(e)}"}
        except Exception as e:
            return {"error": f"Execution error in tool '{tool_name}': {str(e)}"}

    def register_tool(self, name: str, fn: Callable, schema: Dict[str, Any]) -> None:
        """Registers an active runtime tool with its schema."""
        self._tools[name] = fn
        self._custom_schemas[name] = schema

    def unregister_tool(self, name: str) -> None:
        """Removes a runtime tool."""
        self._tools.pop(name, None)
        self._custom_schemas.pop(name, None)
