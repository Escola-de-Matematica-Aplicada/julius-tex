"""Provider registry: discover and select an AI provider from the token config."""

from __future__ import annotations

from .base import BaseProvider, Message


def get_available_providers(tokens: dict[str, str]) -> list[BaseProvider]:
    """Inspect *tokens* and return a list of instantiated, ready-to-use providers.

    Providers whose SDK is not installed or whose key is missing / placeholder
    are silently skipped.
    """
    providers: list[BaseProvider] = []

    # ── Claude ─────────────────────────────────────────────────────────────
    key = tokens.get("ANTHROPIC_API_KEY", "")
    if key and not key.startswith("your_"):
        try:
            from .claude_provider import ClaudeProvider  # noqa: PLC0415

            model = tokens.get("CLAUDE_MODEL", "")
            base_url = tokens.get("CLAUDE_BASE_URL", "")
            providers.append(ClaudeProvider(key, model, base_url))
        except ImportError:
            pass

    # ── Mistral ────────────────────────────────────────────────────────────
    key = tokens.get("MISTRAL_API_KEY", "")
    if key and not key.startswith("your_"):
        try:
            from .mistral_provider import MistralProvider  # noqa: PLC0415

            model = tokens.get("MISTRAL_MODEL", "")
            providers.append(
                MistralProvider(key, model) if model else MistralProvider(key)
            )
        except ImportError:
            pass

    # ── Perplexity ─────────────────────────────────────────────────────────
    key = tokens.get("PERPLEXITY_API_KEY", "")
    if key and not key.startswith("your_"):
        try:
            from .openai_compat import PerplexityProvider  # noqa: PLC0415

            model = tokens.get("PERPLEXITY_MODEL", "")
            providers.append(
                PerplexityProvider(key, model)
                if model
                else PerplexityProvider(key)
            )
        except ImportError:
            pass

    # ── Grok ───────────────────────────────────────────────────────────────
    key = tokens.get("GROK_API_KEY", "")
    if key and not key.startswith("your_"):
        try:
            from .openai_compat import GrokProvider  # noqa: PLC0415

            model = tokens.get("GROK_MODEL", "")
            providers.append(
                GrokProvider(key, model) if model else GrokProvider(key)
            )
        except ImportError:
            pass

    # ── LM Studio ──────────────────────────────────────────────────────────
    lmstudio_url = tokens.get("LMSTUDIO_URL", "")
    if lmstudio_url:
        try:
            from .openai_compat import LMStudioProvider  # noqa: PLC0415

            model = tokens.get("LMSTUDIO_MODEL", "")
            providers.append(
                LMStudioProvider(lmstudio_url, model)
                if model
                else LMStudioProvider(lmstudio_url)
            )
        except ImportError:
            pass

    # ── Ollama ─────────────────────────────────────────────────────────────
    ollama_url = tokens.get("OLLAMA_URL", "")
    if ollama_url:
        try:
            from .ollama_provider import OllamaProvider  # noqa: PLC0415

            model = tokens.get("OLLAMA_MODEL", "")
            providers.append(
                OllamaProvider(ollama_url, model)
                if model
                else OllamaProvider(ollama_url)
            )
        except ImportError:
            pass

    # ── GitHub Models ──────────────────────────────────────────────────────
    key = tokens.get("GITHUB_TOKEN", "")
    if key and not key.startswith("your_"):
        try:
            from .openai_compat import GitHubModelsProvider  # noqa: PLC0415

            model = tokens.get("GITHUB_MODEL", "")
            providers.append(
                GitHubModelsProvider(key, model)
                if model
                else GitHubModelsProvider(key)
            )
        except ImportError:
            pass

    # ── Azure AI Foundry ───────────────────────────────────────────────────────
    key = tokens.get("AZURE_AI_FOUNDRY_API_KEY", "")
    endpoint = tokens.get("AZURE_AI_FOUNDRY_ENDPOINT", "")
    if key and not key.startswith("your_") and endpoint:
        try:
            from .openai_compat import AzureAIFoundryProvider  # noqa: PLC0415

            model = tokens.get("AZURE_AI_FOUNDRY_MODEL", "")
            api_version = tokens.get("AZURE_AI_FOUNDRY_API_VERSION", "")
            providers.append(AzureAIFoundryProvider(key, endpoint, model, api_version))
        except ImportError:
            pass

    # ── Alibaba Cloud ──────────────────────────────────────────────────────────
    key = tokens.get("DASHSCOPE_API_KEY", "")
    if key and not key.startswith("your_"):
        try:
            from .openai_compat import AlibabaCloudProvider  # noqa: PLC0415

            model = tokens.get("ALIBABA_CLOUD_MODEL", "")
            providers.append(
                AlibabaCloudProvider(key, model)
                if model
                else AlibabaCloudProvider(key)
            )
        except ImportError:
            pass

    # ── Zhipu AI ───────────────────────────────────────────────────────────────
    key = tokens.get("ZHIPU_API_KEY", "")
    if key and not key.startswith("your_"):
        try:
            from .openai_compat import ZhipuAIProvider  # noqa: PLC0415

            model = tokens.get("ZHIPU_MODEL", "")
            providers.append(
                ZhipuAIProvider(key, model) if model else ZhipuAIProvider(key)
            )
        except ImportError:
            pass

    return providers


def select_default_provider(
    providers: list[BaseProvider],
    preferred: str = "",
) -> BaseProvider | None:
    """Return the preferred provider, or the first in the list."""
    if not providers:
        return None
    if preferred:
        pref = preferred.lower()
        for p in providers:
            if p.name.lower() == pref:
                return p
    return providers[0]


__all__ = [
    "BaseProvider",
    "Message",
    "get_available_providers",
    "select_default_provider",
]
