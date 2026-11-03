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

    def __init__(
        self,
        endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        mock_mode: bool = False
    ):
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("OPENAI_API_KEY") or ""
        self.endpoint = endpoint or os.environ.get("LLM_ENDPOINT") or "https://api.deepseek.com/v1"
        self.model = model or os.environ.get("LLM_MODEL") or "deepseek-chat"
        self.mock_mode = mock_mode or (not self.api_key and "localhost" not in self.endpoint and "127.0.0.1" not in self.endpoint)

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
