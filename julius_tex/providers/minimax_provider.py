"""Minimax provider (Anthropic-like API).

This provider implements dynamic model listing for Minimax (text-anthropic
compatible) by calling the provider's /v1/models endpoint. Streaming chat is
not implemented because Minimax's streaming contract may differ between
installations; add it later if needed.
"""
from __future__ import annotations

from typing import Iterator

import httpx

from .base import BaseProvider, Message

_DEFAULT_BASE_URL = "https://api.minimax.io/anthropic"


class MinimaxProvider(BaseProvider):
    """Provider for Minimax (Anthropic-compatible text API).

    Only model listing is implemented reliably. Streaming APIs vary; implement
    stream_chat here if a compatible streaming endpoint is available in your
    Minimax deployment.
    """

    name = "Minimax"
    max_context_tokens = None

    def __init__(self, api_key: str, model: str = "", base_url: str = "") -> None:
        # Store configuration and create a simple HTTP client for requests.
        self.api_key = api_key
        self.model = model or ""
        self.base_url = (base_url.rstrip("/") if base_url else _DEFAULT_BASE_URL).rstrip("/")
        self._client = httpx.Client()
        # Prefer using the official Anthropic client when available because
        # Minimax exposes an Anthropic-compatible API. Fall back to raw HTTP.
        self._anthropic_client = None
        try:
            import anthropic  # type: ignore

            try:
                self._anthropic_client = anthropic.Anthropic(api_key=api_key, base_url=self.base_url)
            except TypeError:
                # Some versions accept different param names
                self._anthropic_client = anthropic.Anthropic(api_key=api_key)
        except Exception:
            # anthropic package not installed or client creation failed; ok to proceed
            self._anthropic_client = None

    _MINIMAX_MODELS = [
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
        """Stream assistant text from Minimax using an Anthropic-like streaming API.

        The implementation tries a few common Anthropic/OpenAI-compatible
        streaming endpoints and accepts both SSE-style "data: ..." lines and
        raw chunked text. It attempts to extract text from common JSON shapes
        but will fall back to yielding raw chunks when the shape is unknown.
        """
        import json

        # Build conversation (only user/assistant turns) and include system when present
        api_messages = [
            {"role": m.role, "content": m.content}
            for m in messages
            if m.role in ("user", "assistant")
        ]
        if system:
            api_messages = [{"role": "system", "content": system}] + api_messages

        # Choose a model: prefer configured, otherwise pick first fallback
        model = self.model or (self._MINIMAX_MODELS[0] if self._MINIMAX_MODELS else "")

        payload = {"model": model, "messages": api_messages, "stream": True}
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        # If an Anthropic client is available, prefer it because Minimax's
        # Anthropic-compatible API is known to work with that client.
        if self._anthropic_client is not None:
            kwargs = dict(model=model, max_tokens=16_000, messages=api_messages)
            try:
                # Newer Anthropic SDKs expose a stream helper
                if hasattr(self._anthropic_client.messages, "stream"):
                    with self._anthropic_client.messages.stream(**kwargs) as stream:
                        for text in stream.text_stream:
                            yield text
                    return

                # Fallback: call create with stream=True and iterate
                stream = self._anthropic_client.messages.create(stream=True, **kwargs)
                for chunk in stream:
                    # Try to extract textual content from chunk
                    text = None
                    try:
                        # chunk may be a dict-like or object with attributes
                        if isinstance(chunk, dict):
                            # Anthropic sometimes yields {"delta": {"content": ""}}
                            delta = chunk.get("delta") or {}
                            if isinstance(delta, dict):
                                text = delta.get("content") or delta.get("text")
                            text = text or chunk.get("text") or chunk.get("content")
                        else:
                            # Some SDKs return objects with .text attribute
                            text = getattr(chunk, "text", None) or getattr(chunk, "content", None)
                    except Exception:
                        text = None
                    if text:
                        yield text
                return
            except Exception:
                # Streaming via anthropic client failed; try non-streaming create()
                try:
                    resp = self._anthropic_client.messages.create(stream=False, **kwargs)
                    # resp may be an object or dict; attempt to extract final text
                    final = None
                    try:
                        if isinstance(resp, dict):
                            # common shapes
                            final = resp.get("text") or resp.get("content") or resp.get("output")
                            if not final:
                                choices = resp.get("choices") or resp.get("data")
                                if isinstance(choices, list) and choices:
                                    c = choices[0]
                                    if isinstance(c, dict):
                                        final = c.get("text") or c.get("message") or c.get("content")
                        else:
                            final = getattr(resp, "text", None) or getattr(resp, "content", None)
                    except Exception:
                        final = None
                    if final:
                        yield final
                        return
                except Exception:
                    pass
                # Fall through to HTTP-streaming attempts

        # Last-resort: attempt generic HTTP streaming endpoints (existing logic)
        endpoints = [
            f"{self.base_url}/v1/stream",
            f"{self.base_url}/v1/streams",
            f"{self.base_url}/v1/complete",
            f"{self.base_url}/v1/chat/completions",
            f"{self.base_url}/v1/messages",
            f"{self.base_url}/v1/ai/text?stream=true",
        ]

        # Try each endpoint until one yields data
        for endpoint in endpoints:
            try:
                with self._client.stream("POST", endpoint, headers=headers, json=payload, timeout=60.0) as resp:
                    if resp.status_code >= 400:
                        # Try next endpoint
                        continue

                    got_any = False

                    # Prefer SSE-style lines
                    for raw in resp.iter_lines(decode_unicode=True):
                        if raw is None:
                            continue
                        line = raw.strip()
                        if not line:
                            continue
                        got_any = True
                        # SSE-style: lines may start with "data: "
                        if line.startswith("data: "):
                            line = line[len("data: "):]
                        if line in ("[DONE]", "[done]"):
                            return

                        # Try to parse JSON and extract text
                        text_chunk = None
                        try:
                            obj = json.loads(line)
                            # Common shapes: {"choices":[{"delta":{"content":"..."}}]}
                            if isinstance(obj, dict):
                                choices = obj.get("choices")
                                if isinstance(choices, list) and choices:
                                    for ch in choices:
                                        if isinstance(ch, dict):
                                            delta = ch.get("delta") or {}
                                            if isinstance(delta, dict):
                                                text_chunk = delta.get("content") or delta.get("text")
                                                if text_chunk:
                                                    break
                                            # older shapes
                                            text_chunk = text_chunk or ch.get("text") or ch.get("message")
                                            if text_chunk:
                                                break
                                # other shapes
                                text_chunk = text_chunk or obj.get("content") or obj.get("text") or obj.get("output")
                        except Exception:
                            # Not JSON — treat line as raw text chunk
                            text_chunk = line

                        if text_chunk:
                            yield text_chunk

                    # If the response didn't use iter_lines but used chunked text,
                    # fall back to iter_text
                    if not got_any:
                        for chunk in resp.iter_text(chunk_size=1024):
                            if not chunk:
                                continue
                            yield chunk

                    # Successful endpoint — stop trying others
                    return
            except Exception:  # noqa: BLE001
                # Try next endpoint on any error
                continue

        # If all endpoints failed, raise an informative error
        raise RuntimeError(
            "Could not stream from Minimax: no supported streaming endpoint responded. "
            "Ensure MINIMAX_BASE_URL is correct and the deployment supports streaming."
        )
