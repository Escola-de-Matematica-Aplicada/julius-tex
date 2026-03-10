"""Configuration loading: TOKENS file, PROMPT.sys, and *.md context files."""

from __future__ import annotations

import re
from pathlib import Path


# ---------------------------------------------------------------------------
# Tokens
# ---------------------------------------------------------------------------

def load_tokens(directory: Path) -> dict[str, str]:
    """Parse a KEY=VALUE token file in *directory* named ``TOKENS``.

    Lines starting with ``#`` and blank lines are ignored.
    """
    tokens: dict[str, str] = {}
    tokens_file = directory / "TOKENS"
    if not tokens_file.exists():
        return tokens
    for raw in tokens_file.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, _, value = line.partition("=")
            tokens[key.strip()] = value.strip()
    return tokens


# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

def load_system_prompt(directory: Path) -> str:
    """Return the contents of ``PROMPT.sys`` in *directory*, or ``""``."""
    prompt_file = directory / "PROMPT.sys"
    if prompt_file.exists():
        return prompt_file.read_text(encoding="utf-8").strip()
    return ""


# ---------------------------------------------------------------------------
# Markdown context
# ---------------------------------------------------------------------------

# Pattern that matches the header we write when saving sessions so we can
# distinguish session files from plain docs if needed.
_SESSION_HEADER_RE = re.compile(
    r"^# Julius Code — Chat Session\b", re.MULTILINE
)


def load_markdown_files(directory: Path) -> list[tuple[str, str]]:
    """Return ``[(filename, content), ...]`` for every ``*.md`` file found in
    *directory* (non-recursive), sorted by name so session logs appear in
    chronological order.
    """
    results: list[tuple[str, str]] = []
    for md_file in sorted(directory.glob("*.md")):
        content = md_file.read_text(encoding="utf-8").strip()
        if content:
            results.append((md_file.name, content))
    return results


def build_context_block(md_files: list[tuple[str, str]]) -> str:
    """Concatenate all markdown file contents into a single context string."""
    if not md_files:
        return ""
    parts = [f"### [{name}]\n\n{content}" for name, content in md_files]
    return "\n\n---\n\n".join(parts)


def estimate_tokens(text: str) -> int:
    """Return a rough token estimate for *text*.

    Uses the common approximation of 1 token ≈ 4 characters, which is
    accurate enough for display purposes across different model families.
    """
    return max(0, len(text) // 4)
