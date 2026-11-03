"""Maxilun Universal LLM Provider Adapter.

Supports DeepSeek, OpenRouter, OpenAI, and local Ollama/vLLM endpoints.
Handles tool calling and mock offline fallback.
Zero external dependencies (uses urllib.request).
"""

import json
import os
import time
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class ProviderResponse:
    content: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None
    latency_ms: float = 0.0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    raw_response: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


class UniversalProvider:
    """Dispatches chat completions and tool calls to any OpenAI-compatible API."""

    PRESETS = {
        "deepseek": {
            "endpoint": "https://api.deepseek.com/v1",
            "model": "deepseek-chat",
            "env_key": "DEEPSEEK_API_KEY",
        },
        "openai": {
            "endpoint": "https://api.openai.com/v1",
            "model": "gpt-4o",
            "env_key": "OPENAI_API_KEY",
        },
        "openrouter": {
            "endpoint": "https://openrouter.ai/api/v1",
            "model": "anthropic/claude-3.5-sonnet",
            "env_key": "OPENROUTER_API_KEY",
        },
        "groq": {
            "endpoint": "https://api.groq.com/openai/v1",
            "model": "llama-3.3-70b-versatile",
            "env_key": "GROQ_API_KEY",
        },
        "ollama": {
            "endpoint": "http://localhost:11434/v1",
            "model": "qwen2.5-coder:7b",
            "env_key": "OLLAMA_API_KEY",
        },
        "gemini": {
            "endpoint": "https://generativelanguage.googleapis.com/v1beta/openai",
            "model": "gemini-1.5-pro",
            "env_key": "GEMINI_API_KEY",
        },
    }

    def __init__(
        self,
        provider: Optional[str] = None,
        endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        mock_mode: bool = False
    ):
        provider_name = (provider or os.environ.get("LLM_PROVIDER") or "").lower()
        preset = self.PRESETS.get(provider_name, {})

        self.endpoint = endpoint or os.environ.get("LLM_ENDPOINT") or preset.get("endpoint") or "https://api.deepseek.com/v1"
        self.model = model or os.environ.get("LLM_MODEL") or preset.get("model") or "deepseek-chat"

        env_key_name = preset.get("env_key")
        preset_key = os.environ.get(env_key_name, "") if env_key_name else ""
        self.api_key = (
            api_key
            or preset_key
            or os.environ.get("DEEPSEEK_API_KEY")
            or os.environ.get("OPENAI_API_KEY")
            or os.environ.get("OPENROUTER_API_KEY")
            or os.environ.get("GROQ_API_KEY")
            or os.environ.get("GEMINI_API_KEY")
            or ""
        )

        is_local = "localhost" in self.endpoint or "127.0.0.1" in self.endpoint
        self.mock_mode = mock_mode or (not self.api_key and not is_local)
    def complete(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.2,
        max_tokens: int = 2000
    ) -> ProviderResponse:
        """Sends chat completion request with optional tool calling schemas."""
        if self.mock_mode:
            return self._mock_completion(messages, tools)

        url = f"{self.endpoint.rstrip('/')}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )

        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                latency = (time.time() - t0) * 1000

                choice = data["choices"][0]["message"]
                usage = data.get("usage", {})
                return ProviderResponse(
                    content=choice.get("content"),
                    tool_calls=choice.get("tool_calls"),
                    latency_ms=latency,
                    prompt_tokens=usage.get("prompt_tokens", 0),
                    completion_tokens=usage.get("completion_tokens", 0),
                    raw_response=data
                )
        except urllib.error.HTTPError as e:
            latency = (time.time() - t0) * 1000
            err_body = e.read().decode("utf-8", errors="replace")
            return ProviderResponse(
                error=f"HTTP {e.code}: {err_body}",
                latency_ms=latency
            )
        except Exception as e:
            latency = (time.time() - t0) * 1000
            return ProviderResponse(
                error=f"Connection Error: {str(e)}",
                latency_ms=latency
            )

    def _mock_completion(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> ProviderResponse:
        """Provides deterministic mock responses for testing and offline demo."""
        last_msg = messages[-1] if messages else {}
        content = last_msg.get("content", "").lower()

        # If user asked to inspect or read files and tools are available, simulate tool call
        if any(k in content for k in ["baca", "read", "lihat", "inspect"]) and tools:
            tool_call = {
                "id": "call_mock_1",
                "type": "function",
                "function": {
                    "name": "read_file",
                    "arguments": json.dumps({"path": "package.json", "limit": 15})
                }
            }
            return ProviderResponse(
                content="Memeriksa berkas konfigurasi repositori...",
                tool_calls=[tool_call],
                latency_ms=45.0,
                prompt_tokens=150,
                completion_tokens=25
            )

        # Standard clean Maxilun response mock
        mock_text = """
Eksekusi selesai dengan kepatuhan Core Rules Maxilun.
1. Status Perubahan: Terverifikasi [CONFIRMED].
2. Invarian: Bebas dari buzzword, mengimplementasikan 4 UI states, dan parameter query aman.
"""
        return ProviderResponse(
            content=mock_text.strip(),
            latency_ms=60.0,
            prompt_tokens=200,
            completion_tokens=40
        )
