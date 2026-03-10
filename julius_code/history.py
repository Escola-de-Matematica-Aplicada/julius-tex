"""Conversation history: save Q&A turns as timestamped Markdown files."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

# Prefix used for auto-generated session files so they can be identified.
SESSION_PREFIX = "julius_"
SESSION_SUFFIX = ".md"


def session_filename(dt: datetime | None = None) -> str:
    """Return a filename like ``julius_YYYYMMDD_HHMMSS.md``."""
    if dt is None:
        dt = datetime.now()
    return f"{SESSION_PREFIX}{dt.strftime('%Y%m%d_%H%M%S')}{SESSION_SUFFIX}"


def save_conversation_turn(
    directory: Path,
    user_message: str,
    assistant_message: str,
    provider_name: str,
    model_name: str,
    dt: datetime | None = None,
) -> Path:
    """Persist one Q&A exchange as a Markdown file and return its path.

    The file is written to *directory* with a timestamped filename.
    """
    if dt is None:
        dt = datetime.now()

    filename = session_filename(dt)
    filepath = directory / filename

    content = (
        f"# Julius Code — Chat Session\n\n"
        f"**Date**: {dt.strftime('%Y-%m-%d %H:%M:%S')}  \n"
        f"**Provider**: {provider_name}  \n"
        f"**Model**: {model_name}\n\n"
        f"---\n\n"
        f"## User\n\n{user_message}\n\n"
        f"---\n\n"
        f"## Assistant\n\n{assistant_message}\n"
    )

    filepath.write_text(content, encoding="utf-8")
    return filepath


def list_session_files(directory: Path) -> list[Path]:
    """Return all session files in *directory* sorted chronologically."""
    return sorted(
        p for p in directory.glob(f"{SESSION_PREFIX}*{SESSION_SUFFIX}")
    )
