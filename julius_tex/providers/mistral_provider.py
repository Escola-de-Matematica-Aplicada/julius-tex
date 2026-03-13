"""Mistral AI provider (compatible with mistralai >= 2.0)."""

from __future__ import annotations

import importlib.metadata
from typing import Iterator

from .base import BaseProvider, Message


_DEFAULT_MODEL = "mistral-large-latest"

# Mapeamento atualizado de modelo → limite de contexto
_MODEL_CONTEXT_WINDOWS = {
    "mistral-large-latest": 256_000,
    "mistral-large-3": 256_000,
    "mistral-large-3-25-12": 256_000,
    "mistral-medium-latest": 128_000,
    "mistral-medium-3.1": 128_000,
    "mistral-small-latest": 128_000,
    "mistral-small-3.2": 128_000,
    "ministral-8b-latest": 256_000,
    "ministral-3-8b": 256_000,
    "ministral-3-14b": 256_000,
    "ministral-3b": 256_000,
    "pixtral-12b": 128_000,
    "codestral-latest": 256_000,
}


class MistralProvider(BaseProvider):
    """Streams responses from Mistral AI."""

    name = "Mistral"
    max_context_tokens = 128_000

    def __init__(self, api_key: str, model: str = _DEFAULT_MODEL) -> None:
        try:
            from mistralai.client import Mistral
        except ImportError as exc:
            raise ImportError(
                "The 'mistralai' package is required for the Mistral provider. "
                "Install it with:  pip install 'mistralai>=2.0'"
            ) from exc

        self._client = Mistral(api_key=api_key)
        self.model = model or _DEFAULT_MODEL
        self.max_context_tokens = _MODEL_CONTEXT_WINDOWS.get(
            self.model, 128_000
        )

    @property
    def sdk_version(self) -> str:
        """Return the installed mistralai version or 'unknown'."""
        try:
            return importlib.metadata.version("mistralai")
        except Exception:  # noqa: BLE001
            return "unknown"

    def list_models(self) -> list[str]:
        """Return all model IDs available from the Mistral API."""
        try:
            result = self._client.models.list()
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
            stream = self._client.chat.stream(
                model=self.model,
                messages=api_messages,
            )
            for chunk in stream:
                if (
                    chunk.data.choices
                    and chunk.data.choices[0].delta.content is not None
                ):
                    yield chunk.data.choices[0].delta.content
        except Exception as e:
            print(f"Erro ao transmitir chat: {e}")
            yield ""