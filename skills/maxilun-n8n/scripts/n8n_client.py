#!/usr/bin/env python3
"""Zero-dependency n8n REST API Client & Webhook Tester.

Allows agents to deploy, activate, and test workflows against live n8n instances.
Zero external dependencies (uses standard urllib.request).
"""

import sys
import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional


class N8nClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/api/v1/{endpoint.lstrip('/')}"
        headers = {
            "X-N8N-API-KEY": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        body = json.dumps(data).encode("utf-8") if data else None
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            raise RuntimeError(f"n8n API Error [{e.code}]: {error_body}")
        except Exception as e:
            raise RuntimeError(f"Connection failed to {url}: {e}")

    def list_workflows(self) -> Dict[str, Any]:
        return self._request("GET", "workflows")

    def create_workflow(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", "workflows", data=workflow_data)

    def activate_workflow(self, workflow_id: str) -> Dict[str, Any]:
        return self._request("POST", f"workflows/{workflow_id}/activate")

    def test_webhook(self, webhook_url: str, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        req_headers = {"Content-Type": "application/json"}
        if headers:
            req_headers.update(headers)
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(webhook_url, data=body, headers=req_headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return {"status": resp.status, "body": resp.read().decode("utf-8")}
        except urllib.error.HTTPError as e:
            return {"status": e.code, "error": e.read().decode("utf-8")}
