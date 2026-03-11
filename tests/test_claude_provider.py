"""Tests for ClaudeProvider.list_models()."""

from __future__ import annotations

import sys
from typing import Any
from unittest.mock import MagicMock, patch


def _make_model_info(id_: str, type_: str | None = "model") -> Any:
    """Return a mock Anthropic ModelInfo-like object."""
    m = MagicMock()
    m.id = id_
    m.type = type_
    return m


def _make_anthropic_page(*models: Any) -> Any:
    """Return a mock SyncPage whose iteration yields *models*."""
    page = MagicMock()
    page.__iter__ = MagicMock(return_value=iter(list(models)))
    return page


def _build_provider(mock_anthropic: Any, api_key: str = "fake-key"):
    """Instantiate ClaudeProvider with a patched ``anthropic`` module.

    The patch must be active both at class-definition time (for the lazy
    import) and at instantiation time.
    """
    import julius_tex.providers.claude_provider as mod

    with patch.dict(sys.modules, {"anthropic": mock_anthropic}):
        provider = mod.ClaudeProvider(api_key)
    return provider, mock_anthropic.Anthropic.return_value


class TestClaudeProviderListModels:
    """list_models() should return genuine Anthropic model IDs."""

    def test_returns_claude_models_sorted(self) -> None:
        """Models with type='model' are returned in sorted order."""
        page = _make_anthropic_page(
            _make_model_info("claude-3-5-sonnet-20241022"),
            _make_model_info("claude-3-opus-20240229"),
            _make_model_info("claude-3-5-haiku-20241022"),
        )
        mock_anthropic = MagicMock()
        mock_client = MagicMock()
        mock_anthropic.Anthropic.return_value = mock_client
        mock_client.models.list.return_value = page

        provider, _ = _build_provider(mock_anthropic)

        with patch.dict(sys.modules, {"anthropic": mock_anthropic}):
            models = provider.list_models()

        assert models == sorted([
            "claude-3-5-sonnet-20241022",
            "claude-3-opus-20240229",
            "claude-3-5-haiku-20241022",
        ])

    def test_excludes_non_anthropic_models(self) -> None:
        """Models with type=None (e.g. LM Studio responses) are excluded.

        The Anthropic SDK uses lenient response parsing: when the underlying
        HTTP call accidentally reaches an OpenAI-compatible endpoint (such as
        LM Studio), the response is still parsed into ModelInfo objects, but
        the ``type`` field will be ``None`` because OpenAI-compatible payloads
        use ``object`` instead of ``type``.  Filtering by ``type == "model"``
        ensures those spurious entries are dropped.
        """
        page = _make_anthropic_page(
            # Legitimate Anthropic model
            _make_model_info("claude-3-5-sonnet-20241022", type_="model"),
            # LM Studio models (type is None because the field is absent in
            # the OpenAI-compatible /v1/models response)
            _make_model_info("allenai/olmocr-2-7b", type_=None),
            _make_model_info("deepseek/deepseek-r1-0528-qwen3-8b", type_=None),
            _make_model_info("zai-org/glm-4.7-flash", type_=None),
        )
        mock_anthropic = MagicMock()
        mock_client = MagicMock()
        mock_anthropic.Anthropic.return_value = mock_client
        mock_client.models.list.return_value = page

        provider, _ = _build_provider(mock_anthropic)

        with patch.dict(sys.modules, {"anthropic": mock_anthropic}):
            models = provider.list_models()

        assert models == ["claude-3-5-sonnet-20241022"]
        assert "allenai/olmocr-2-7b" not in models
        assert "zai-org/glm-4.7-flash" not in models

    def test_calls_models_list_with_limit_1000(self) -> None:
        """list_models() passes limit=1000 to the Anthropic API."""
        page = _make_anthropic_page()
        mock_anthropic = MagicMock()
        mock_client = MagicMock()
        mock_anthropic.Anthropic.return_value = mock_client
        mock_client.models.list.return_value = page

        provider, mock_client_instance = _build_provider(mock_anthropic)

        with patch.dict(sys.modules, {"anthropic": mock_anthropic}):
            provider.list_models()

        mock_client_instance.models.list.assert_called_once_with(limit=1000)

    def test_empty_response(self) -> None:
        """An empty response from the API returns an empty list."""
        page = _make_anthropic_page()
        mock_anthropic = MagicMock()
        mock_client = MagicMock()
        mock_anthropic.Anthropic.return_value = mock_client
        mock_client.models.list.return_value = page

        provider, _ = _build_provider(mock_anthropic)

        with patch.dict(sys.modules, {"anthropic": mock_anthropic}):
            models = provider.list_models()

        assert models == []

