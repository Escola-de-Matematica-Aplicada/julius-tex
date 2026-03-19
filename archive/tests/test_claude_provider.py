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
    """list_models() should return available Claude models from the API or fallback."""

    def test_returns_dynamic_models(self) -> None:
        """list_models() returns models fetched from the API."""
        mock_anthropic = MagicMock()
        mock_client = MagicMock()
        mock_anthropic.Anthropic.return_value = mock_client

        # Mock Model objects
        m1 = MagicMock()
        m1.id = "claude-4-sonnet"
        m2 = MagicMock()
        m2.id = "claude-4-opus"
        
        # Mock the response object with .data attribute
        mock_response = MagicMock()
        mock_response.data = [m1, m2]
        mock_client.models.list.return_value = mock_response

        provider = _build_provider(mock_anthropic)
        models = provider.list_models()

        assert models == ["claude-4-opus", "claude-4-sonnet"]
        mock_client.models.list.assert_called_once()

    def test_returns_fallback_on_error(self) -> None:
        """list_models() returns the hardcoded list if the API call fails."""
        mock_anthropic = MagicMock()
        mock_client = MagicMock()
        mock_anthropic.Anthropic.return_value = mock_client
        mock_client.models.list.side_effect = Exception("API Error")

        provider = _build_provider(mock_anthropic)
        models = provider.list_models()

        assert models == [
            "claude-haiku-4-5-20251001",
            "claude-sonnet-4-6",
            "claude-opus-4-6",
        ]

    def test_contains_expected_models_in_fallback(self) -> None:
        """Fallback list contains expected legacy models."""
        mock_anthropic = MagicMock()
        mock_client = MagicMock()
        mock_anthropic.Anthropic.return_value = mock_client
        mock_client.models.list.side_effect = Exception("API Error")

        provider = _build_provider(mock_anthropic)
        models = provider.list_models()

        assert "claude-haiku-4-5-20251001" in models
        assert "claude-sonnet-4-6" in models
        assert "claude-opus-4-6" in models

    def test_default_model_is_sonnet_4_6(self) -> None:
        """The default model is claude-sonnet-4-6."""
        mock_anthropic = MagicMock()
        provider = _build_provider(mock_anthropic)

        assert provider.model == "claude-sonnet-4-6"

