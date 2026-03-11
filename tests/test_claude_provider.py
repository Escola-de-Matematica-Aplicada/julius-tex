"""Tests for ClaudeProvider.list_models()."""

from __future__ import annotations

import sys
from typing import Any
from unittest.mock import MagicMock, patch


def _build_provider(mock_anthropic: Any, api_key: str = "fake-key"):
    """Instantiate ClaudeProvider with a patched ``anthropic`` module.

    The patch must be active both at class-definition time (for the lazy
    import) and at instantiation time.
    """
    import julius_tex.providers.claude_provider as mod

    with patch.dict(sys.modules, {"anthropic": mock_anthropic}):
        provider = mod.ClaudeProvider(api_key)
    return provider


class TestClaudeProviderListModels:
    """list_models() should return the hardcoded list of available Claude models."""

    def test_returns_hardcoded_models(self) -> None:
        """list_models() returns the fixed list of supported Claude models."""
        mock_anthropic = MagicMock()
        provider = _build_provider(mock_anthropic)

        models = provider.list_models()

        assert models == [
            "claude-haiku-4-5-20251001",
            "claude-sonnet-4-6",
            "claude-opus-4-6",
        ]

    def test_contains_expected_models(self) -> None:
        """All three supported Claude models are present in the list."""
        mock_anthropic = MagicMock()
        provider = _build_provider(mock_anthropic)

        models = provider.list_models()

        assert "claude-haiku-4-5-20251001" in models
        assert "claude-sonnet-4-6" in models
        assert "claude-opus-4-6" in models

    def test_no_api_call_made(self) -> None:
        """list_models() does not make any API calls."""
        mock_anthropic = MagicMock()
        mock_client = MagicMock()
        mock_anthropic.Anthropic.return_value = mock_client

        provider = _build_provider(mock_anthropic)
        provider.list_models()

        mock_client.models.list.assert_not_called()

    def test_default_model_is_sonnet_4_6(self) -> None:
        """The default model is claude-sonnet-4-6."""
        mock_anthropic = MagicMock()
        provider = _build_provider(mock_anthropic)

        assert provider.model == "claude-sonnet-4-6"

