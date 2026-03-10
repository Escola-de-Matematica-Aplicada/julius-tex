"""Ollama local provider (uses the native Ollama REST API via httpx)."""

from __future__ import annotations

import json
from typing import Iterator

from .base import BaseProvider, Message

_DEFAULT_URL = "http://localhost:11434"
_DEFAULT_MODEL = "llama3.2"


class OllamaProvider(BaseProvider):
    """Streams responses from a locally running Ollama server."""

    name = "Ollama"

    def __init__(
        self,
        base_url: str = _DEFAULT_URL,
        model: str = _DEFAULT_MODEL,
    ) -> None:
        try:
            import httpx  # noqa: PLC0415
        except ImportError as exc:
            raise ImportError(
                "The 'httpx' package is required for the Ollama provider. "
                "Install it with:  pip install httpx"
            ) from exc
        self._base_url = base_url.rstrip("/")
        self._httpx = httpx
        self.model = model

    def list_models(self) -> list[str]:
        """Return all model names available from the local Ollama server."""
        try:
            response = self._httpx.get(f"{self._base_url}/api/tags", timeout=10.0)
            response.raise_for_status()
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(
                f"Could not connect to Ollama at {self._base_url}: {exc}"
            ) from exc
        data = response.json()
        return sorted(m["name"] for m in data.get("models", []))

    def stream_chat(
        self,
        messages: list[Message],
        system: str = "",
    ) -> Iterator[str]:
        api_messages: list[dict] = []
        if system:
            api_messages.append({"role": "system", "content": system})
        for m in messages:
            if m.role in ("user", "assistant"):
                api_messages.append({"role": m.role, "content": m.content})

        url = f"{self._base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": api_messages,
            "stream": True,
        }

        with self._httpx.stream(
            "POST",
            url,
            json=payload,
            timeout=120.0,
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue
                content = data.get("message", {}).get("content", "")
                if content:
                    yield content
                if data.get("done"):
                    break
