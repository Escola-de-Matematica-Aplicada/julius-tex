"""Mistral AI provider."""

from __future__ import annotations

from typing import Iterator

from .base import BaseProvider, Message

_DEFAULT_MODEL = "mistral-large-latest"
_MAX_CONTEXT_TOKENS = 128_000


class MistralProvider(BaseProvider):
    """Streams responses from Mistral AI."""

    name = "Mistral"
    max_context_tokens = _MAX_CONTEXT_TOKENS

    def __init__(self, api_key: str, model: str = _DEFAULT_MODEL) -> None:
        try:
            from mistralai import Mistral  # noqa: PLC0415
        except ImportError as exc:
            raise ImportError(
                "The 'mistralai' package is required for the Mistral provider. "
                "Install it with:  pip install mistralai"
            ) from exc
        self._client = Mistral(api_key=api_key)
        self.model = model

    def list_models(self) -> list[str]:
        """Return all model IDs available from the Mistral API."""
        response = self._client.models.list()
        return sorted(m.id for m in response.data)

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

        with self._client.chat.stream(
            model=self.model,
            messages=api_messages,
        ) as stream:
            for event in stream:
                delta = event.data.choices[0].delta.content if event.data.choices else None
                if not delta:
                    continue
                if isinstance(delta, list):
                    for chunk in delta:
                        if hasattr(chunk, "text") and chunk.text:
                            yield chunk.text
                else:
                    yield delta
