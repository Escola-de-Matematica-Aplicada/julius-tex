"""Base provider interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterator


@dataclass
class Message:
    """A single chat message."""

    role: str  # "user" | "assistant" | "system"
    content: str


class BaseProvider(ABC):
    """Abstract base class that every AI provider must implement."""

    #: Human-readable provider name shown in the UI.
    name: str = ""
    #: Model identifier used for API calls.
    model: str = ""
    #: Maximum context-window size in tokens (None means unknown).
    max_context_tokens: int | None = None

    # ------------------------------------------------------------------
    # Abstract interface
    # ------------------------------------------------------------------

    @abstractmethod
    def stream_chat(
        self,
        messages: list[Message],
        system: str = "",
    ) -> Iterator[str]:
        """Yield text chunks as they arrive from the provider."""

    # ------------------------------------------------------------------
    # Concrete helpers
    # ------------------------------------------------------------------

    def chat(self, messages: list[Message], system: str = "") -> str:
        """Return the full assistant response as a single string."""
        return "".join(self.stream_chat(messages, system))

    def list_models(self) -> list[str]:
        """Return a list of model identifiers available from this provider.

        Providers that support dynamic model discovery should override this
        method.  The default implementation returns an empty list, which the
        UI interprets as "not supported".
        """
        return []

    @property
    def display_name(self) -> str:
        """Return a label such as ``Claude (claude-3-5-sonnet-20241022)``."""
        return f"{self.name} ({self.model})"
