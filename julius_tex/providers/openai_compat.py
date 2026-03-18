"""OpenAI-compatible providers: Perplexity, Grok (xAI), LM Studio, GitHub Models, Azure AI Foundry, Alibaba Cloud, Zhipu AI, and Moonshot AI."""

from __future__ import annotations

from pathlib import Path
from typing import Iterator

import httpx

from .base import BaseProvider, Message


def _parse_models_from_md(md_path: Path, *, require_slash: bool = True) -> list[str]:
    """Extract model names from the first column of markdown tables in *md_path*.

    Reads every pipe-delimited table row in the file and returns the value
    from the first column, skipping header and separator rows.  Backtick
    characters are stripped from cell values so that both plain and
    backtick-quoted model IDs are handled correctly.

    When *require_slash* is ``True`` (the default) a cell is only accepted as
    a valid model ID when it contains a ``/`` character, matching the
    ``organization/model-name`` convention used by GitHub Models.  Set
    *require_slash* to ``False`` for providers (such as LM Studio) whose model
    IDs do not follow that convention.
    """
    try:
        text = md_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise OSError(
            f"Could not read provider parameter file '{md_path}': {exc}. "
            "Ensure the file exists inside the julius_tex/providers/ package directory."
        ) from exc

    models: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        # Skip separator rows like |---|---|---|
        if "|---" in stripped or "| ---" in stripped:
            continue
        cols = [c.strip() for c in stripped.split("|")]
        # After splitting "| a | b | c |", cols is ['', 'a', 'b', 'c', '']
        if len(cols) < 3:
            continue
        # Strip backtick characters that some markdown files use to quote model IDs.
        cell = cols[1].strip().strip("`")
        if not cell:
            continue
        # When require_slash is True, only accept cells that look like a model
        # ID in "organization/model-name" format (used by GitHub Models).
        if require_slash and "/" not in cell:
            continue
        # Skip header-style cells that contain spaces (e.g. "ID do Modelo").
        if " " in cell:
            continue
        models.append(cell)
    return sorted(models)


# ─── Perplexity ───────────────────────────────────────────────────────────────
_PERPLEXITY_BASE_URL = "https://api.perplexity.ai"
_PERPLEXITY_DEFAULT_MODEL = "llama-3.1-sonar-large-128k-online"
_PERPLEXITY_MAX_CONTEXT_TOKENS = 127_072
# Perplexity does not expose a GET /models endpoint, so we maintain a static
# list.  Update this list as Perplexity releases or retires models.
_PERPLEXITY_MODELS = [
    "sonar-deep-research",
    "sonar-reasoning-pro",
    "sonar-reasoning",
    "sonar-pro",
    "sonar",
    "llama-3.1-sonar-huge-128k-online",
    "llama-3.1-sonar-large-128k-online",
    "llama-3.1-sonar-small-128k-online",
]

# ─── Grok (xAI) ───────────────────────────────────────────────────────────────
_GROK_BASE_URL = "https://api.x.ai/v1"
_GROK_DEFAULT_MODEL = "grok-beta"
_GROK_MAX_CONTEXT_TOKENS = 131_072

# ─── LM Studio ────────────────────────────────────────────────────────────────
_LMSTUDIO_DEFAULT_URL = "http://localhost:1234"
_LMSTUDIO_DEFAULT_MODEL = "local-model"

# ─── GitHub Models ────────────────────────────────────────────────────────────
_GITHUB_MODELS_BASE_URL = "https://models.github.ai/inference"
_GITHUB_MODELS_DEFAULT_MODEL = "openai/gpt-4o-mini"
_GITHUB_MODELS_MAX_CONTEXT_TOKENS = 128_000

# ─── Azure AI Foundry ─────────────────────────────────────────────────────────
_AZURE_AI_FOUNDRY_DEFAULT_MODEL = "gpt-4o"
_AZURE_AI_FOUNDRY_MAX_CONTEXT_TOKENS = 128_000
_AZURE_AI_FOUNDRY_DEFAULT_API_VERSION = "2024-12-01-preview"

# ─── Alibaba Cloud (DashScope) ────────────────────────────────────────────────
_ALIBABA_CLOUD_BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
_ALIBABA_CLOUD_DEFAULT_MODEL = "qwen-max"
# The DashScope OpenAI-compatible endpoint enforces a strict input limit of
# 30,720 tokens (total context window is 32,768, with 2,048 reserved for output).
_ALIBABA_CLOUD_MAX_CONTEXT_TOKENS = 1_000_000

# ─── Zhipu AI (z.ai / BigModel) ───────────────────────────────────────────────
_ZHIPU_AI_BASE_URL = "https://open.bigmodel.cn/api/paas/v4/"
_ZHIPU_AI_DEFAULT_MODEL = "glm-4"
_ZHIPU_AI_MAX_CONTEXT_TOKENS = 128_000

# ─── Moonshot AI ──────────────────────────────────────────────────────────────
_MOONSHOT_BASE_URL = "https://api.moonshot.ai/v1"
_MOONSHOT_DEFAULT_MODEL = "kimi-k2.5"
_MOONSHOT_MAX_OUTPUT_TOKENS = 1024 * 32
_MOONSHOT_MAX_CONTEXT_TOKENS = 256_000
# Moonshot does not require explicit reasoning parameters — thinking is enabled
# by default for kimi-k2.5 models.
_MOONSHOT_MODELS = [
    "kimi-k2.5",
    "moonshot-v1-8k",
    "moonshot-v1-32k",
    "moonshot-v1-128k",
]


class _OpenAICompatProvider(BaseProvider):
    """Shared implementation for providers that expose an OpenAI-compatible API."""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
        default_query: dict | None = None,
    ) -> None:
        try:
            from openai import OpenAI  # noqa: PLC0415
        except ImportError as exc:
            raise ImportError(
                "The 'openai' package is required. "
                "Install it with:  pip install openai"
            ) from exc
        self._client = OpenAI(api_key=api_key, base_url=base_url, default_query=default_query)
        self.model = model

    def list_models(self) -> list[str]:
        """Return all model IDs available from this OpenAI-compatible API."""
        response = self._client.models.list()
        return sorted(m.id for m in response.data)

    def stream_chat(
        self,
        messages: list[Message],
        system: str = "",
    ) -> Iterator[str]:
        from ..config import estimate_tokens  # noqa: PLC0415

        system_tokens = estimate_tokens(system) if system else 0
        limit = self.max_context_tokens

        # When the provider exposes a context limit, guard against sending
        # more tokens than the API accepts.
        if limit is not None:
            if system_tokens > limit:
                raise ValueError(
                    f"The system prompt and context files are too large for "
                    f"{self.name} ({system_tokens:,} estimated tokens; limit "
                    f"is {limit:,}). Remove some *.md files from this "
                    "directory or switch to a provider with a larger context "
                    "window."
                )

            # Build conversation list (oldest-first), keeping only user/assistant turns.
            conv_msgs: list[dict] = [
                {"role": m.role, "content": m.content}
                for m in messages
                if m.role in ("user", "assistant")
            ]

            # Drop the oldest messages until the total fits within the limit.
            # The last message (current user request) is always preserved.
            while len(conv_msgs) > 1:
                total = system_tokens + sum(
                    estimate_tokens(msg["content"]) for msg in conv_msgs
                )
                if total <= limit:
                    break
                conv_msgs.pop(0)

            api_messages: list[dict] = []
            if system:
                api_messages.append({"role": "system", "content": system})
            api_messages.extend(conv_msgs)
        else:
            api_messages = []
            if system:
                api_messages.append({"role": "system", "content": system})
            for m in messages:
                if m.role in ("user", "assistant"):
                    api_messages.append({"role": m.role, "content": m.content})

        stream = self._client.chat.completions.create(
            model=self.model,
            messages=api_messages,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content if chunk.choices else None
            if delta:
                yield delta


class PerplexityProvider(_OpenAICompatProvider):
    """Streams responses from Perplexity AI."""

    name = "Perplexity"
    max_context_tokens = _PERPLEXITY_MAX_CONTEXT_TOKENS

    def __init__(
        self,
        api_key: str,
        model: str = _PERPLEXITY_DEFAULT_MODEL,
    ) -> None:
        super().__init__(api_key, _PERPLEXITY_BASE_URL, model)

    def list_models(self) -> list[str]:
        """Return the known Perplexity models.

        Perplexity does not support the standard OpenAI ``GET /models``
        endpoint, so we return a curated static list instead.
        """
        return list(_PERPLEXITY_MODELS)


class GrokProvider(_OpenAICompatProvider):
    """Streams responses from Grok (xAI)."""

    name = "Grok"
    max_context_tokens = _GROK_MAX_CONTEXT_TOKENS

    def __init__(
        self,
        api_key: str,
        model: str = _GROK_DEFAULT_MODEL,
    ) -> None:
        super().__init__(api_key, _GROK_BASE_URL, model)


class LMStudioProvider(_OpenAICompatProvider):
    """Streams responses from a locally running LM Studio server."""

    name = "LMStudio"

    def __init__(
            self,
            base_url: str = _LMSTUDIO_DEFAULT_URL,
            model: str = _LMSTUDIO_DEFAULT_MODEL,
    ) -> None:
        # LM Studio does not require a real API key.
        # Create httpx client with custom timeout for local server
        httpx_client = httpx.Client(timeout=30000)
        try:
            from openai import OpenAI  # noqa: PLC0415
            # Pass httpx_client via http_client to OpenAI client
            self._client = OpenAI(
                api_key="lm-studio",
                base_url=base_url.rstrip("/") + "/v1",
                http_client=httpx_client,
            )
        except ImportError as exc:
            raise ImportError(
                "The 'openai' package is required. "
                "Install it with:  pip install openai"
            ) from exc
        self.model = model

    def list_models(self) -> list[str]:
        """Return the list of available models for LM Studio.

        Prefer reading the bundled "lmstudio_julio.md" parameter file shipped with
        the package to avoid making network calls during tests or when the local
        LM Studio server is not running. If the bundled file is missing or
        cannot be parsed, fall back to calling the LM Studio API.
        """
        _md = Path(__file__).parent / "lmstudio_julio.md"
        try:
            return _parse_models_from_md(_md, require_slash=False)
        except Exception:
            # Fall back to live API if bundled file is unavailable
            try:
                response = self._client.models.list()
                return sorted(m.id for m in response.data)
            except Exception as e:
                print(f"Erro ao listar modelos: {e}")
                return []


class GitHubModelsProvider(_OpenAICompatProvider):
    """Streams responses from GitHub Models (https://models.github.ai/catalog/models)."""

    name = "GitHub"
    max_context_tokens = _GITHUB_MODELS_MAX_CONTEXT_TOKENS

    def __init__(
        self,
        api_key: str,
        model: str = _GITHUB_MODELS_DEFAULT_MODEL,
    ) -> None:
        super().__init__(api_key, _GITHUB_MODELS_BASE_URL, model)

    def list_models(self) -> list[str]:
        """Return the valid GitHub Models model IDs from the bundled parameter file.

        The GitHub Models inference endpoint returns model IDs in the internal
        ``azureml://`` URI format, which cannot be used with the chat API.
        Instead we read the curated list of valid model names from the
        ``github_max_tokens.md`` file that ships with this package, mirroring
        the same pattern used for other providers (e.g. Perplexity) that
        maintain a static list of supported models.
        """
        _md = Path(__file__).parent / "github_max_tokens.md"
        return _parse_models_from_md(_md)


class AzureAIFoundryProvider(_OpenAICompatProvider):
    """Streams responses from Azure AI Foundry serverless inference endpoints."""

    name = "AzureAIFoundry"
    max_context_tokens = _AZURE_AI_FOUNDRY_MAX_CONTEXT_TOKENS

    def __init__(
        self,
        api_key: str,
        endpoint: str,
        model: str = _AZURE_AI_FOUNDRY_DEFAULT_MODEL,
        api_version: str = _AZURE_AI_FOUNDRY_DEFAULT_API_VERSION,
    ) -> None:
        # Ensure the base_url always ends with a trailing slash so that URL
        # joining behaves correctly regardless of whether the user included
        # one in the configured endpoint.
        # Azure AI Foundry requires the api-version query parameter on every
        # request, so we pass it as a default query param.
        super().__init__(
            api_key,
            endpoint.rstrip("/") + "/",
            model or _AZURE_AI_FOUNDRY_DEFAULT_MODEL,
            default_query={"api-version": api_version or _AZURE_AI_FOUNDRY_DEFAULT_API_VERSION},
        )


class AlibabaCloudProvider(_OpenAICompatProvider):
    """Streams responses from Alibaba Cloud Model Studio (DashScope) via the OpenAI-compatible API.

    Singapore endpoint: https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    Get your API key at: https://bailian.console.alibabacloud.com/
    """

    name = "AlibabaCloud"
    max_context_tokens = _ALIBABA_CLOUD_MAX_CONTEXT_TOKENS

    def __init__(
        self,
        api_key: str,
        model: str = _ALIBABA_CLOUD_DEFAULT_MODEL,
    ) -> None:
        super().__init__(api_key, _ALIBABA_CLOUD_BASE_URL, model)


class ZhipuAIProvider(_OpenAICompatProvider):
    """Streams responses from Zhipu AI (z.ai / BigModel) via the OpenAI-compatible API.

    Endpoint: https://open.bigmodel.cn/api/paas/v4/
    Get your API key at: https://open.bigmodel.cn/
    """

    name = "ZhipuAI"
    max_context_tokens = _ZHIPU_AI_MAX_CONTEXT_TOKENS

    def __init__(
        self,
        api_key: str,
        model: str = _ZHIPU_AI_DEFAULT_MODEL,
    ) -> None:
        super().__init__(api_key, _ZHIPU_AI_BASE_URL, model)


class MoonshotProvider(_OpenAICompatProvider):
    """Streams responses from Moonshot AI with reasoning (thinking) enabled.

    Endpoint: https://api.moonshot.ai/v1
    Get your API key at: https://platform.moonshot.ai/
    Thinking is enabled by default for kimi-k2.5 models — no extra parameters
    needed.  The provider exposes ``reasoning_content`` chunks in the stream
    which are rendered as a collapsible thinking block before the final answer.
    """

    name = "Moonshot"
    max_context_tokens = _MOONSHOT_MAX_CONTEXT_TOKENS

    def __init__(
        self,
        api_key: str,
        model: str = _MOONSHOT_DEFAULT_MODEL,
    ) -> None:
        super().__init__(api_key, _MOONSHOT_BASE_URL, model)

    def list_models(self) -> list[str]:
        """Return the list of available models from the Moonshot AI API."""
        try:
            response = self._client.models.list()
            return sorted(m.id for m in response.data)
        except Exception as e:
            print(f"Erro ao listar modelos: {e}")
            return []

    def stream_chat(
        self,
        messages: list[Message],
        system: str = "",
    ) -> Iterator[str]:
        from ..config import estimate_tokens  # noqa: PLC0415

        system_tokens = estimate_tokens(system) if system else 0
        limit = self.max_context_tokens

        if limit is not None:
            if system_tokens > limit:
                raise ValueError(
                    f"The system prompt and context files are too large for "
                    f"{self.name} ({system_tokens:,} estimated tokens; limit "
                    f"is {limit:,}). Remove some *.md files from this "
                    "directory or switch to a provider with a larger context "
                    "window."
                )

            conv_msgs: list[dict] = [
                {"role": m.role, "content": m.content}
                for m in messages
                if m.role in ("user", "assistant")
            ]

            while len(conv_msgs) > 1:
                total = system_tokens + sum(
                    estimate_tokens(msg["content"]) for msg in conv_msgs
                )
                if total <= limit:
                    break
                conv_msgs.pop(0)

            api_messages: list[dict] = []
            if system:
                api_messages.append({"role": "system", "content": system})
            api_messages.extend(conv_msgs)
        else:
            api_messages = []
            if system:
                api_messages.append({"role": "system", "content": system})
            for m in messages:
                if m.role in ("user", "assistant"):
                    api_messages.append({"role": m.role, "content": m.content})

        stream = self._client.chat.completions.create(
            model=self.model,
            messages=api_messages,
            max_tokens=_MOONSHOT_MAX_OUTPUT_TOKENS,
            stream=True,
        )

        thinking = False
        for chunk in stream:
            if not chunk.choices:
                continue
            choice = chunk.choices[0]
            if not choice.delta:
                continue
            reasoning = getattr(choice.delta, "reasoning_content", None)
            if reasoning:
                if not thinking:
                    thinking = True
                    yield "\n💭 *Thinking...*\n\n"
                yield reasoning
            content = choice.delta.content
            if content:
                if thinking:
                    thinking = False
                    yield "\n\n---\n\n"
                yield content
