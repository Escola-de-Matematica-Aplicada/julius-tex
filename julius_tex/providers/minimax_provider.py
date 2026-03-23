"""Minimax provider using Anthropic-compatible API.

This provider implements Minimax's Anthropic-compatible API using the 'anthropic' SDK,
supporting features like thinking blocks and streaming responses.
"""
from __future__ import annotations

from typing import Iterator

import anthropic

from .base import BaseProvider, Message

_DEFAULT_BASE_URL = "https://api.minimax.io/anthropic"
_DEFAULT_MODEL = "MiniMax-M2.7"
# Max tokens varies by model; M2-her has a strict 2048 limit
_MAX_TOKENS_MAP = {
    "M2-her": 2048,
    "MiniMax-M2.5": 8192,
    "MiniMax-M2.5-highspeed": 8192,
    "MiniMax-M2.7": 8192,
    "MiniMax-M2.7-highspeed": 8192,
    "MiniMax-M2": 8192,
}


class MinimaxProvider(BaseProvider):
    """Provider for Minimax using the Anthropic-compatible API.

    Uses the 'anthropic' SDK with Minimax's custom base URL.
    Supports both streaming text and thinking blocks.
    """

    name = "Minimax"
    max_context_tokens = None

    def __init__(self, api_key: str, model: str = "", base_url: str = "") -> None:
        # Store configuration and initialize the Anthropic client with Minimax base URL.
        self.api_key = api_key
        self.model = model or _DEFAULT_MODEL
        self.base_url = (base_url.rstrip("/") if base_url else _DEFAULT_BASE_URL).rstrip("/")
        self._client = anthropic.Anthropic(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    _MINIMAX_MODELS = [
        "M2-her",
        "MiniMax-M2.5",
        "MiniMax-M2.5-highspeed",
        "MiniMax-M2.7",
        "MiniMax-M2.7-highspeed",
        "MiniMax-M2",
    ]

    def list_models(self) -> list[str]:
        """Return a list of available models from the Minimax API.

        Attempts to fetch the model list via the Anthropic-style models endpoint,
        falling back to the standard Minimax models API or a static list.
        """
        try:
            # Try dynamic model discovery via the Anthropic SDK
            response = self._client.models.list()
            models = [m.id for m in response.data]
            if models:
                return sorted(set(models))
        except Exception as exc:  # noqa: BLE001
            # Anthropic-compatible /v1/models might return 404 on Minimax.
            # Avoid printing huge HTML error bodies from Minimax.
            err_msg = str(exc)
            if "404" not in err_msg and "<html>" not in err_msg.lower():
                print(f"Error listing Minimax models via Anthropic SDK: {exc}")

        # Fallback: try the standard Minimax models endpoint
        try:
            import httpx  # noqa: PLC0415
            # Minimax root URL for standard API; normally https://api.minimax.io
            root_url = self.base_url.replace("/anthropic", "").rstrip("/")
            resp = httpx.get(
                f"{root_url}/v1/models",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=5.0,
            )
            if resp.status_code == 200:
                data = resp.json()
                models = []
                if isinstance(data, dict):
                    # Check for "data" (OpenAI-style) or "models"
                    for key in ("data", "models"):
                        items = data.get(key)
                        if isinstance(items, list):
                            for item in items:
                                if isinstance(item, dict):
                                    name = (
                                        item.get("id")
                                        or item.get("model")
                                        or item.get("name")
                                    )
                                    if name:
                                        models.append(name)
                                elif isinstance(item, str):
                                    models.append(item)
                if models:
                    return sorted(set(models))
        except Exception:  # noqa: BLE001
            pass

        return list(self._MINIMAX_MODELS)

    def stream_chat(self, messages: list[Message], system: str = "") -> Iterator[str]:
        """Stream assistant text from Minimax using the Anthropic SDK.

        Supports thinking blocks and text content from the Anthropic response format.
        """
        # Convert project Message objects to Anthropic's expected dict format
        api_messages = [
            {"role": m.role, "content": m.content}
            for m in messages
            if m.role in ("user", "assistant")
        ]

        # Use model-specific max_tokens; default to 8192 for unknown models
        max_tokens = _MAX_TOKENS_MAP.get(self.model, 8192)

        kwargs: dict = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": api_messages,
        }
        if system:
            kwargs["system"] = system

        try:
            # Use streaming if supported by the compatible endpoint
            with self._client.messages.stream(**kwargs) as stream:
                for event in stream:
                    # Handle text deltas
                    if event.type == "content_block_delta" and event.delta.type == "text_delta":
                        yield event.delta.text
                    # Handle thinking block deltas (if the SDK/Minimax supports it in streaming)
                    elif event.type == "content_block_delta" and event.delta.type == "thinking_delta":
                        # Optionally format thinking blocks if desired; here we just yield the content
                        yield f"\n[Thinking: {event.delta.thinking}]\n"

        except Exception as exc:
            # Fallback to non-streaming if stream fails or is not supported
            try:
                message = self._client.messages.create(**kwargs)
                for block in message.content:
                    if block.type == "thinking":
                        yield f"\n[Thinking: {block.thinking}]\n"
                    elif block.type == "text":
                        yield block.text
            except Exception as nested_exc:
                err_msg = str(nested_exc)
                if "<html>" in err_msg.lower():
                    err_msg = "Received an unexpected HTML error response from Minimax API."
                raise RuntimeError(f"Failed to communicate with Minimax API: {err_msg}") from exc
