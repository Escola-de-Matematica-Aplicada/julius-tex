"""Minimax provider using native API.

This provider implements Minimax's /v1/text/chatcompletion_v2 API with proper
message formatting including the 'name' field for each role.
"""
from __future__ import annotations

from typing import Iterator

import httpx

from .base import BaseProvider, Message

_DEFAULT_BASE_URL = "https://api.minimax.io"


class MinimaxProvider(BaseProvider):
    """Provider for Minimax using native /v1/text/chatcompletion_v2 API.

    Implements non-streaming chat completion with proper message formatting.
    """

    name = "Minimax"
    max_context_tokens = None

    def __init__(self, api_key: str, model: str = "", base_url: str = "") -> None:
        # Store configuration and create a simple HTTP client for requests.
        self.api_key = api_key
        self.model = model or ""
        self.base_url = (base_url.rstrip("/") if base_url else _DEFAULT_BASE_URL).rstrip("/")
        self._client = httpx.Client()

    _MINIMAX_MODELS = [
        "M2-her",
        "MiniMax-M2.5",
        "MiniMax-M2.5-highspeed",
        "MiniMax-M2.1",
        "MiniMax-M2.1-highspeed",
        "MiniMax-M2",
    ]

    def list_models(self) -> list[str]:
        """Return a list of available models from the Minimax API.

        Minimax's hosted endpoint may not support the OpenAI/Anthropic-style
        /v1/models endpoint; therefore attempt a request but fall back to a
        curated static list for reliable user experience.
        """
        try:
            url = f"{self.base_url}/v1/models"
            headers = {"Authorization": f"Bearer {self.api_key}"}
            resp = self._client.get(url, headers=headers, timeout=10.0)
            if resp.status_code != 200:
                # Known case: some Minimax deployments return 404 for /v1/models.
                # Fall back to static model list.
                return list(self._MINIMAX_MODELS)
            data = resp.json()

            models: list[str] = []
            # Parse common shapes if present
            if isinstance(data, dict):
                if "data" in data and isinstance(data["data"], list):
                    for m in data["data"]:
                        if isinstance(m, dict):
                            name = m.get("id") or m.get("model") or m.get("name")
                            if name:
                                models.append(name)
                elif "models" in data and isinstance(data["models"], list):
                    for m in data["models"]:
                        if isinstance(m, dict):
                            name = m.get("id") or m.get("model") or m.get("name")
                            if name:
                                models.append(name)
                        elif isinstance(m, str):
                            models.append(m)
            elif isinstance(data, list):
                for m in data:
                    if isinstance(m, dict):
                        name = m.get("id") or m.get("model") or m.get("name")
                        if name:
                            models.append(name)
                    elif isinstance(m, str):
                        models.append(m)

            if models:
                return sorted({m for m in models if m})
            # No usable models discovered; return fallback list.
            return list(self._MINIMAX_MODELS)
        except Exception as exc:  # noqa: BLE001
            print(f"Error listing Minimax models: {exc}")
            return list(self._MINIMAX_MODELS)

    def stream_chat(self, messages: list[Message], system: str = "") -> Iterator[str]:
        """Stream assistant text from Minimax using the /v1/text/chatcompletion_v2 API.

        The implementation uses Minimax's native API format with proper message structure
        including the 'name' field for each message role.
        """
        import json

        # Build conversation with Minimax's expected format
        api_messages = []

        # Add system message if present
        if system:
            api_messages.append({"role": "system", "content": system, "name": "MiniMax AI"})

        # Add user/assistant turns with name field
        for m in messages:
            if m.role == "user":
                api_messages.append({"role": "user", "content": m.content, "name": "User"})
            elif m.role == "assistant":
                api_messages.append({"role": "assistant", "content": m.content, "name": "MiniMax AI"})

        # Choose a model: prefer configured, otherwise pick first fallback
        model = self.model or (self._MINIMAX_MODELS[0] if self._MINIMAX_MODELS else "M2-her")

        payload = {"model": model, "messages": api_messages}
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        # Use Minimax's native API endpoint
        endpoint = f"{self.base_url}/v1/text/chatcompletion_v2"

        try:
            # Make non-streaming request to Minimax API
            resp = self._client.post(endpoint, headers=headers, json=payload, timeout=60.0)

            if resp.status_code >= 400:
                error_text = resp.text
                raise RuntimeError(f"Minimax API error (status {resp.status_code}): {error_text}")

            # Parse response
            data = resp.json()

            # Extract text from Minimax response format
            text_content = None
            if isinstance(data, dict):
                # Try common response shapes
                choices = data.get("choices")
                if isinstance(choices, list) and choices:
                    for choice in choices:
                        if isinstance(choice, dict):
                            message = choice.get("message")
                            if isinstance(message, dict):
                                text_content = message.get("content")
                                if text_content:
                                    break
                            # Alternative shapes
                            text_content = text_content or choice.get("text") or choice.get("content")
                            if text_content:
                                break

                # Direct content field
                text_content = text_content or data.get("content") or data.get("text")

            if text_content:
                yield text_content
            else:
                raise RuntimeError(f"Could not extract text from Minimax response: {data}")

        except Exception as exc:
            raise RuntimeError(f"Failed to communicate with Minimax API: {exc}") from exc
