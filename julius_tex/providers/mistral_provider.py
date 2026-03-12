"""Mistral AI provider."""

from __future__ import annotations

from typing import Iterator

from .base import BaseProvider, Message

_DEFAULT_MODEL = "mistral-large-latest"
_MAX_CONTEXT_TOKENS = 128_000


class MistralProvider(BaseProvider):
    """Streams responses from Mistral AI."""

    name = "MistralProvider"
    max_context_tokens = _MAX_CONTEXT_TOKENS

    def __init__(self, api_key: str, model: str = _DEFAULT_MODEL) -> None:
        try:
            from mistralai.client import MistralClient
        except ImportError as exc:
            raise ImportError(
                "The 'mistralai' package is required for the Mistral provider. "
                "Install it with:  pip install mistralai"
            ) from exc
        self._mistral_cls = MistralClient  # guarda a classe para reuso
        self.api_key = api_key
        self.model = model

    def list_models(self) -> list[str]:
        """Return all model IDs available from the Mistral API."""
        try:
            with self._mistral_cls(api_key=self.api_key) as client:
                result = client.models.list()
                return sorted(m.id for m in result.data)
        except Exception as e:
            print(f"Erro ao listar modelos: {e}")
            return []

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

        try:
            with self._mistral_cls(api_key=self.api_key) as client:
                with client.chat.stream(
                    model=self.model,
                    messages=api_messages,
                ) as stream:
                    for chunk in stream:
                        content = chunk.data.choices[0].delta.content
                        if content:
                            yield content
        except Exception as e:
            print(f"Erro ao transmitir chat: {e}")
            yield ""
