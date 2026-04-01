"""Configuration loading: TOKENS file, PROMPT.sys, and plain-text context files."""

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
# Plain-text context files
# ---------------------------------------------------------------------------

# Supported plain-text file extensions for context loading.
TEXT_FILE_EXTENSIONS: frozenset[str] = frozenset(
    {
        ".md", ".tex", ".bst", ".cls", ".bib", ".txt",
        ".html", ".htm", ".xml", ".json", ".yaml", ".yml", ".csv",
        ".py", ".js", ".ts", ".c", ".cpp", ".h", ".java", ".sh", ".sql"
    }
)

# Pattern that matches the header we write when saving sessions so we can
# distinguish session files from plain docs if needed.
_SESSION_HEADER_RE = re.compile(
    r"^# Julius Tex — Chat Session\b", re.MULTILINE
)


def load_text_files(directory: Path) -> list[tuple[str, str]]:
    """Return ``[(relative_path, content), ...]`` for every supported
    plain-text file found in *directory* and its sub-directories, sorted by
    relative path.

    Supported extensions: ``.md``, ``.tex``, ``.bst``, ``.cls``, ``.bib``, ``.txt``, ``.html``, etc.
    Files inside hidden directories (names starting with ``.``) are skipped.
    """
    results: list[tuple[str, str]] = []
    for text_file in sorted(directory.rglob("*")):
        if not text_file.is_file():
            continue
        if text_file.suffix not in TEXT_FILE_EXTENSIONS:
            continue
        rel = text_file.relative_to(directory)
        # Skip files inside hidden directories (e.g. .git, .venv).
        # rel.parts[:-1] contains only the parent directory components,
        # excluding the filename itself.
        if any(part.startswith(".") for part in rel.parts[:-1]):
            continue
        content = text_file.read_text(encoding="utf-8").strip()
        if content:
            results.append((str(rel), content))
    return results


def build_context_block(text_files: list[tuple[str, str]]) -> str:
    """Concatenate all text file contents into a single context string."""
    if not text_files:
        return ""
    parts = [f"### [{name}]\n\n{content}" for name, content in text_files]
    return "\n\n---\n\n".join(parts)


def estimate_tokens(text: str) -> int:
    """Return a rough token estimate for *text*.

    Uses the common approximation of 1 token ≈ 4 characters, which is
    accurate enough for display purposes across different model families.
    """
    return max(0, len(text) // 4)
