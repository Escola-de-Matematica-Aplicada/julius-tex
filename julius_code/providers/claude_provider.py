"""Anthropic Claude provider."""

from __future__ import annotations

from typing import Iterator

from .base import BaseProvider, Message

_DEFAULT_MODEL = "claude-3-5-sonnet-20241022"
_MAX_TOKENS = 8192
_MAX_CONTEXT_TOKENS = 200_000


class ClaudeProvider(BaseProvider):
    """Streams responses from Anthropic Claude."""

    name = "Claude"
    max_context_tokens = _MAX_CONTEXT_TOKENS

    def __init__(self, api_key: str, model: str = _DEFAULT_MODEL) -> None:
        try:
            import anthropic  # noqa: PLC0415
        except ImportError as exc:
            raise ImportError(
                "The 'anthropic' package is required for the Claude provider. "
                "Install it with:  pip install anthropic"
            ) from exc
        self._client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def list_models(self) -> list[str]:
        """Return all model IDs available from the Anthropic API.

        Uses limit=1000 (the API maximum) to retrieve all models in a single
        request, avoiding pagination.
        """
        response = self._client.models.list(limit=1000)
        return sorted(m.id for m in response.data)

    def stream_chat(
        self,
        messages: list[Message],
        system: str = "",
    ) -> Iterator[str]:
        api_messages = [
            {"role": m.role, "content": m.content}
            for m in messages
            if m.role in ("user", "assistant")
        ]
        kwargs: dict = dict(
            model=self.model,
            max_tokens=_MAX_TOKENS,
            messages=api_messages,
        )
        if system:
            kwargs["system"] = system

        with self._client.messages.stream(**kwargs) as stream:
            for text in stream.text_stream:
                yield text
