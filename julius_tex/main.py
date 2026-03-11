"""Julius Tex — main entry point and chat loop."""

from __future__ import annotations

import sys
from pathlib import Path

from .config import (
    build_context_block,
    estimate_tokens,
    load_text_files,
    load_system_prompt,
    load_tokens,
)
from .history import list_session_files, save_conversation_turn
from .providers import (
    BaseProvider,
    get_available_providers,
    select_default_provider,
)
from .providers.base import Message
from . import ui

# ---------------------------------------------------------------------------
# System-prompt helper
# ---------------------------------------------------------------------------

_DEFAULT_SYSTEM = (
    "You are Julius, an expert AI research assistant and LaTeX editor. "
    "You have been given the project's text files (LaTeX, BibTeX, and Markdown) as context. "
    "Use it to give accurate, actionable answers."
)


def _build_system_prompt(user_prompt: str, context: str) -> str:
    base = user_prompt or _DEFAULT_SYSTEM
    if context:
        return (
            f"{base}\n\n"
            "---\n\n"
            "## Project Context (text files)\n\n"
            f"{context}"
        )
    return base


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

def _cmd_help() -> None:
    ui.show_help()


def _cmd_provider(provider: BaseProvider) -> None:
    ui.print_info(f"Active provider: [bold]{provider.display_name}[/bold]")


def _cmd_providers(providers: list[BaseProvider], current: BaseProvider) -> BaseProvider:
    if not providers:
        ui.print_warning("No providers are configured.")
        return current
    lines = []
    for i, p in enumerate(providers, start=1):
        marker = "[green]●[/green]" if p is current else "[dim]○[/dim]"
        lines.append(f"  {marker}  [bold]{i}[/bold].  {p.display_name}")
    ui.console.print("\n".join(lines))
    ui.console.print()

    choice = ui.prompt_provider_selection(len(providers))
    if choice is None:
        return current

    selected = providers[choice - 1]
    if selected is current:
        ui.print_info(f"Already using {selected.display_name}.")
    else:
        ui.print_success(f"Switched to {selected.display_name}")
    return selected


def _cmd_models(provider: BaseProvider) -> None:
    models = []
    try:
        models = provider.list_models()
    except Exception as exc:  # noqa: BLE001
        ui.print_error(f"Could not retrieve models: {exc}")
        return

    if not models:
        ui.print_warning(
            f"No models returned by {provider.display_name}. "
            "The provider may not support dynamic model listing."
        )
        return

    lines = []
    for i, m in enumerate(models, start=1):
        marker = "[green]●[/green]" if m == provider.model else "[dim]○[/dim]"
        lines.append(f"  {marker}  [bold]{i}[/bold].  {m}")
    ui.console.print("\n".join(lines))
    ui.console.print()

    choice = ui.prompt_model_selection(len(models))
    if choice is None:
        return

    selected = models[choice - 1]
    provider.model = selected
    ui.print_success(f"Model switched to [bold]{selected}[/bold]")


def _cmd_context(text_files: list[tuple[str, str]]) -> None:
    if not text_files:
        ui.print_info("No context files loaded.")
        return
    ui.print_info(f"{len(text_files)} context file(s) loaded:")
    for name, _ in text_files:
        ui.console.print(f"   [dim]·  {name}[/dim]")
    ui.console.print()


def _cmd_clear(history: list[Message]) -> list[Message]:
    history.clear()
    ui.print_success("Conversation history cleared for this session.")
    return history


# ---------------------------------------------------------------------------
# Main chat loop
# ---------------------------------------------------------------------------

def _run(working_dir: Path) -> None:
    # ── Load configuration ────────────────────────────────────────────────
    tokens = load_tokens(working_dir)
    system_prompt_text = load_system_prompt(working_dir)
    text_files = load_text_files(working_dir)
    session_files = list_session_files(working_dir)
    context = build_context_block(text_files)
    system = _build_system_prompt(system_prompt_text, context)

    # ── Discover providers ────────────────────────────────────────────────
    providers = get_available_providers(tokens)
    if not providers:
        ui.print_error(
            "No AI provider is configured. "
            "Copy [bold]TOKENS.example[/bold] to [bold]TOKENS[/bold] and fill in at least one API key."
        )
        sys.exit(1)

    preferred = tokens.get("DEFAULT_PROVIDER", "")
    provider = select_default_provider(providers, preferred)
    assert provider is not None  # guaranteed by the check above

    # ── Welcome screen ────────────────────────────────────────────────────
    context_names = [name for name, _ in text_files]
    context_token_estimate = sum(estimate_tokens(content) for _, content in text_files)
    ui.show_welcome(
        provider_display=provider.display_name,
        context_files=context_names,
        session_count=len(session_files),
        has_system_prompt=bool(system_prompt_text),
        max_context_tokens=provider.max_context_tokens,
        context_token_estimate=context_token_estimate,
    )

    # Warn when the system prompt alone would already exceed the provider limit.
    system_token_estimate = estimate_tokens(system)
    if (
        provider.max_context_tokens is not None
        and system_token_estimate > provider.max_context_tokens
    ):
        ui.print_warning(
            f"⚠️  The system prompt and context files are estimated at "
            f"{system_token_estimate:,} tokens, which exceeds the "
            f"{provider.display_name} input limit of "
            f"{provider.max_context_tokens:,} tokens. "
            "Remove some context files from this directory or switch to a "
            "provider with a larger context window."
        )

    # ── In-session state ──────────────────────────────────────────────────
    history: list[Message] = []
    last_user: str = ""
    last_assistant: str = ""

    # ── Chat loop ─────────────────────────────────────────────────────────
    while True:
        user_input = ui.get_input()

        if not user_input:
            continue

        # ── Slash commands ────────────────────────────────────────────────
        if user_input.startswith("/"):
            parts = user_input.split(maxsplit=1)
            cmd = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else ""

            if cmd in ("/quit", "/exit"):
                ui.print_info("Goodbye! 👋")
                break
            elif cmd == "/help":
                _cmd_help()
            elif cmd == "/provider":
                _cmd_provider(provider)
            elif cmd == "/providers":
                provider = _cmd_providers(providers, provider)
            elif cmd == "/models":
                _cmd_models(provider)
            elif cmd == "/context":
                _cmd_context(text_files)
            elif cmd == "/clear":
                history = _cmd_clear(history)
            elif cmd == "/save":
                if last_user and last_assistant:
                    path = save_conversation_turn(
                        working_dir,
                        last_user,
                        last_assistant,
                        provider.name,
                        provider.model,
                    )
                    ui.print_success(f"Saved to [bold]{path.name}[/bold]")
                else:
                    ui.print_warning("Nothing to save yet.")
            else:
                ui.print_warning(
                    f"Unknown command [bold]{cmd}[/bold]. "
                    "Type [bold]/help[/bold] to see available commands."
                )
            continue

        # ── Regular chat ──────────────────────────────────────────────────
        ui.print_user_message(user_input)
        history.append(Message(role="user", content=user_input))

        response_text = ""
        try:
            with ui.StreamingPanel(provider.name) as panel:
                for chunk in provider.stream_chat(history, system):
                    panel.write(chunk)
            response_text = panel.content
        except KeyboardInterrupt:
            ui.print_warning("Response interrupted.")
            response_text = panel.content if panel.content else ""  # type: ignore[union-attr]
            if not response_text:
                history.pop()
                continue
        except Exception as exc:  # noqa: BLE001
            ui.print_error(f"Provider error: {exc}")
            history.pop()
            continue

        if not response_text:
            ui.print_warning("The provider returned an empty response.")
            history.pop()
            continue

        history.append(Message(role="assistant", content=response_text))
        last_user = user_input
        last_assistant = response_text

        # Auto-save every exchange.
        try:
            save_conversation_turn(
                working_dir,
                user_input,
                response_text,
                provider.name,
                provider.model,
            )
        except OSError as exc:
            ui.print_warning(f"Could not save conversation: {exc}")

        # Show updated token estimate so the user can track context size.
        total_tokens = estimate_tokens(system) + sum(
            estimate_tokens(msg.role + ": " + msg.content) for msg in history
        )
        ui.print_token_count(total_tokens, provider.max_context_tokens)


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """CLI entry point registered in pyproject.toml."""
    working_dir = Path.cwd()
    try:
        _run(working_dir)
    except KeyboardInterrupt:
        ui.console.print()
        ui.print_info("Session terminated.")
