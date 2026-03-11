"""Anthropic Claude provider."""

from __future__ import annotations

from typing import Iterator

from .base import BaseProvider, Message

_DEFAULT_MODEL = "claude-sonnet-4-5"
_MAX_TOKENS = 16_000
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

        Only model objects whose ``type`` field equals ``"model"`` are
        included.  The Anthropic SDK uses lenient (non-strict) response
        parsing, so if the underlying HTTP call accidentally reaches a
        different OpenAI-compatible endpoint (e.g. LM Studio), those
        responses are parsed without validation and their model objects will
        have ``type=None`` — filtering on ``type == "model"`` ensures only
        genuine Anthropic models are returned.
        """
        return sorted(
            m.id
            for m in self._client.models.list(limit=1000)
            if m.type == "model"
        )

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
