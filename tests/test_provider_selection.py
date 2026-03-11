"""Tests for provider selection logic and related fixes."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch


# ─── Helpers ──────────────────────────────────────────────────────────────────


def _build_claude_provider(mock_anthropic: Any, api_key: str = "fake-key", **kwargs):
    """Instantiate ClaudeProvider with a patched ``anthropic`` module."""
    import julius_tex.providers.claude_provider as mod

    with patch.dict(sys.modules, {"anthropic": mock_anthropic}):
        provider = mod.ClaudeProvider(api_key, **kwargs)
    return provider


# ─── ClaudeProvider base URL tests ────────────────────────────────────────────


class TestClaudeProviderBaseUrl:
    """ClaudeProvider should use the official Anthropic URL, not env-var overrides."""

    def test_default_base_url_is_anthropic(self) -> None:
        """Without explicit base_url the provider uses the official Anthropic endpoint."""
        import julius_tex.providers.claude_provider as mod

        mock_anthropic = MagicMock()
        _build_claude_provider(mock_anthropic)

        call_kwargs = mock_anthropic.Anthropic.call_args[1]
        assert call_kwargs.get("base_url") == mod._ANTHROPIC_BASE_URL

    def test_explicit_base_url_is_passed_through(self) -> None:
        """Passing base_url in TOKENS overrides the default Anthropic endpoint."""
        mock_anthropic = MagicMock()
        custom_url = "https://my-custom-proxy.example.com"
        _build_claude_provider(mock_anthropic, base_url=custom_url)

        call_kwargs = mock_anthropic.Anthropic.call_args[1]
        assert call_kwargs.get("base_url") == custom_url

    def test_empty_base_url_falls_back_to_anthropic(self) -> None:
        """An empty base_url string falls back to the official Anthropic endpoint."""
        import julius_tex.providers.claude_provider as mod

        mock_anthropic = MagicMock()
        _build_claude_provider(mock_anthropic, base_url="")

        call_kwargs = mock_anthropic.Anthropic.call_args[1]
        assert call_kwargs.get("base_url") == mod._ANTHROPIC_BASE_URL

    def test_env_var_does_not_override_default(self, monkeypatch) -> None:
        """ANTHROPIC_BASE_URL environment variable is ignored in favour of the explicit URL."""
        import julius_tex.providers.claude_provider as mod

        monkeypatch.setenv("ANTHROPIC_BASE_URL", "http://localhost:1234")
        mock_anthropic = MagicMock()
        _build_claude_provider(mock_anthropic)

        call_kwargs = mock_anthropic.Anthropic.call_args[1]
        # The Anthropic SDK receives the explicit URL, not the env-var value.
        assert call_kwargs.get("base_url") == mod._ANTHROPIC_BASE_URL

    def test_default_model_still_works(self) -> None:
        """Default model is unchanged after the base_url refactor."""
        mock_anthropic = MagicMock()
        provider = _build_claude_provider(mock_anthropic)
        assert provider.model == "claude-sonnet-4-6"


# ─── _parse_models_from_md tests ──────────────────────────────────────────────


class TestParseModelsFromMd:
    """_parse_models_from_md should handle backticks and the require_slash flag."""

    def _md_file(self, tmp_path: Path, content: str) -> Path:
        p = tmp_path / "models.md"
        p.write_text(content, encoding="utf-8")
        return p

    def test_strips_backticks_from_model_ids(self, tmp_path: Path) -> None:
        """Backtick-wrapped model names are returned without the backticks."""
        from julius_tex.providers.openai_compat import _parse_models_from_md

        content = (
            "| Model | Tokens |\n"
            "|-------|--------|\n"
            "| `org/model-a` | 131072 |\n"
            "| `org/model-b` | 65536 |\n"
        )
        md = self._md_file(tmp_path, content)
        models = _parse_models_from_md(md)
        assert "org/model-a" in models
        assert "org/model-b" in models
        assert "`org/model-a`" not in models

    def test_require_slash_true_excludes_slash_free_ids(self, tmp_path: Path) -> None:
        """With require_slash=True (default), model IDs without '/' are excluded."""
        from julius_tex.providers.openai_compat import _parse_models_from_md

        content = (
            "| Model | Tokens |\n"
            "|-------|--------|\n"
            "| org/model-a | 131072 |\n"
            "| noslash-model | 65536 |\n"
        )
        md = self._md_file(tmp_path, content)
        models = _parse_models_from_md(md, require_slash=True)
        assert "org/model-a" in models
        assert "noslash-model" not in models

    def test_require_slash_false_includes_slash_free_ids(self, tmp_path: Path) -> None:
        """With require_slash=False, model IDs without '/' are included."""
        from julius_tex.providers.openai_compat import _parse_models_from_md

        content = (
            "| Model | Tokens |\n"
            "|-------|--------|\n"
            "| org/model-a | 131072 |\n"
            "| noslash-model | 65536 |\n"
        )
        md = self._md_file(tmp_path, content)
        models = _parse_models_from_md(md, require_slash=False)
        assert "org/model-a" in models
        assert "noslash-model" in models

    def test_header_rows_excluded_even_without_slash_requirement(
        self, tmp_path: Path
    ) -> None:
        """Header cells containing spaces are never treated as model IDs."""
        from julius_tex.providers.openai_compat import _parse_models_from_md

        content = (
            "| ID do Modelo | Max Tokens |\n"
            "|:-------------|:-----------|\n"
            "| `real-model` | 131072 |\n"
        )
        md = self._md_file(tmp_path, content)
        models = _parse_models_from_md(md, require_slash=False)
        assert "real-model" in models
        assert "ID do Modelo" not in models

    def test_separator_rows_excluded(self, tmp_path: Path) -> None:
        """Separator rows (|---|---|) are skipped."""
        from julius_tex.providers.openai_compat import _parse_models_from_md

        content = (
            "| Model | Tokens |\n"
            "|-------|--------|\n"
            "| org/model | 131072 |\n"
        )
        md = self._md_file(tmp_path, content)
        models = _parse_models_from_md(md)
        assert models == ["org/model"]

    def test_returns_sorted_list(self, tmp_path: Path) -> None:
        """Returned model list is sorted alphabetically."""
        from julius_tex.providers.openai_compat import _parse_models_from_md

        content = (
            "| Model | Tokens |\n"
            "|-------|--------|\n"
            "| org/zebra | 131072 |\n"
            "| org/alpha | 65536 |\n"
        )
        md = self._md_file(tmp_path, content)
        models = _parse_models_from_md(md)
        assert models == sorted(models)


# ─── LMStudioProvider.list_models tests ───────────────────────────────────────


class TestLMStudioProviderListModels:
    """LMStudioProvider.list_models() should use the bundled lmstudio_julio.md."""

    def _build_lmstudio_provider(self):
        mock_openai = MagicMock()
        from julius_tex.providers.openai_compat import LMStudioProvider

        with patch.dict(sys.modules, {"openai": mock_openai}):
            provider = LMStudioProvider()
        return provider

    def test_returns_models_from_md_file(self) -> None:
        """list_models() returns the curated list from lmstudio_julio.md."""
        mock_openai = MagicMock()
        with patch.dict(sys.modules, {"openai": mock_openai}):
            from julius_tex.providers.openai_compat import LMStudioProvider

            provider = LMStudioProvider()

        models = provider.list_models()
        assert isinstance(models, list)
        assert len(models) > 0

    def test_does_not_call_live_api(self) -> None:
        """list_models() must not make any HTTP request to the LM Studio server."""
        mock_openai = MagicMock()
        with patch.dict(sys.modules, {"openai": mock_openai}):
            from julius_tex.providers.openai_compat import LMStudioProvider

            provider = LMStudioProvider()

        provider.list_models()

        # The OpenAI client's models.list() must NOT be called.
        provider._client.models.list.assert_not_called()

    def test_models_are_sorted(self) -> None:
        """list_models() returns models in sorted order."""
        mock_openai = MagicMock()
        with patch.dict(sys.modules, {"openai": mock_openai}):
            from julius_tex.providers.openai_compat import LMStudioProvider

            provider = LMStudioProvider()

        models = provider.list_models()
        assert models == sorted(models)

    def test_bundled_md_file_exists(self) -> None:
        """The lmstudio_julio.md file shipped with the package actually exists."""
        import julius_tex.providers.openai_compat as oc_mod

        pkg_dir = Path(oc_mod.__file__).parent
        assert (pkg_dir / "lmstudio_julio.md").exists()


# ─── get_available_providers: CLAUDE_BASE_URL support ─────────────────────────


class TestGetAvailableProvidersClaudeBaseUrl:
    """get_available_providers() should forward CLAUDE_BASE_URL to ClaudeProvider."""

    def test_claude_base_url_forwarded_from_tokens(self) -> None:
        """CLAUDE_BASE_URL in TOKENS is forwarded to ClaudeProvider as base_url."""
        mock_anthropic = MagicMock()
        custom_url = "https://my-proxy.example.com"

        tokens = {
            "ANTHROPIC_API_KEY": "real-key",
            "CLAUDE_BASE_URL": custom_url,
        }

        with patch.dict(sys.modules, {"anthropic": mock_anthropic}):
            from julius_tex.providers import get_available_providers

            providers = get_available_providers(tokens)

        assert providers, "Expected at least one provider"
        claude = next((p for p in providers if p.name == "Claude"), None)
        assert claude is not None

        call_kwargs = mock_anthropic.Anthropic.call_args[1]
        assert call_kwargs.get("base_url") == custom_url

    def test_no_claude_base_url_uses_default(self) -> None:
        """When CLAUDE_BASE_URL is absent, the official Anthropic URL is used."""
        import julius_tex.providers.claude_provider as mod

        mock_anthropic = MagicMock()
        tokens = {"ANTHROPIC_API_KEY": "real-key"}

        with patch.dict(sys.modules, {"anthropic": mock_anthropic}):
            from julius_tex.providers import get_available_providers

            providers = get_available_providers(tokens)

        assert providers
        call_kwargs = mock_anthropic.Anthropic.call_args[1]
        assert call_kwargs.get("base_url") == mod._ANTHROPIC_BASE_URL
