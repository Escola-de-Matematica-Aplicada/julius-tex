"""Anthropic Claude provider."""

from __future__ import annotations

from typing import Iterator

from .base import BaseProvider, Message

_DEFAULT_MODEL = "claude-sonnet-4-6"
_MAX_TOKENS = 16_000
_MAX_CONTEXT_TOKENS = 200_000
# Use the official Anthropic API URL explicitly so that environment variables
# such as ANTHROPIC_BASE_URL (which LM Studio's CLI may set to a local server)
# do not accidentally redirect Claude traffic to a local endpoint.
_ANTHROPIC_BASE_URL = "https://api.anthropic.com"


class ClaudeProvider(BaseProvider):
    """Streams responses from Anthropic Claude."""

    name = "Claude"
    max_context_tokens = _MAX_CONTEXT_TOKENS

    def __init__(
        self,
        api_key: str,
        model: str = _DEFAULT_MODEL,
        base_url: str = "",
    ) -> None:
        try:
            import anthropic  # noqa: PLC0415
        except ImportError as exc:
            raise ImportError(
                "The 'anthropic' package is required for the Claude provider. "
                "Install it with:  pip install anthropic"
            ) from exc
        self._client = anthropic.Anthropic(
            api_key=api_key,
            base_url=base_url or _ANTHROPIC_BASE_URL,
        )
        # Use `or` fallback so that passing an empty string (which happens when
        # CLAUDE_MODEL is absent from TOKENS and get_available_providers passes
        # "" explicitly) is handled the same as omitting the argument.
        self.model = model or _DEFAULT_MODEL

    def list_models(self) -> list[str]:
        """Return the list of available Claude models."""
        return [
            "claude-haiku-4-5-20251001",
            "claude-sonnet-4-6",
            "claude-opus-4-6",
        ]

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
