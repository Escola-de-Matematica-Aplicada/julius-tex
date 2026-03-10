"""Rich-based terminal UI for Julius Tex."""

from __future__ import annotations

from prompt_toolkit import prompt as _pt_prompt
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.rule import Rule
from rich.spinner import Spinner
from rich.style import Style
from rich.text import Text
from rich.theme import Theme

# ─── Theme ────────────────────────────────────────────────────────────────────

JULIUS_THEME = Theme(
    {
        "julius.banner": "bold cyan",
        "julius.provider": "bold green",
        "julius.user": "bold yellow",
        "julius.assistant": "bold cyan",
        "julius.info": "dim white",
        "julius.success": "bold green",
        "julius.warning": "bold yellow",
        "julius.error": "bold red",
        "julius.dim": "dim",
        "julius.command": "bold magenta",
    }
)

console = Console(theme=JULIUS_THEME)

# ─── ASCII banner ─────────────────────────────────────────────────────────────

_BANNER = r"""
     ██╗██╗   ██╗██╗     ██╗██╗   ██╗███████╗
     ██║██║   ██║██║     ██║██║   ██║██╔════╝
     ██║██║   ██║██║     ██║██║   ██║███████╗
██   ██║██║   ██║██║     ██║██║   ██║╚════██║
╚█████╔╝╚██████╔╝███████╗██║╚██████╔╝███████║
 ╚════╝  ╚═════╝ ╚══════╝╚═╝ ╚═════╝ ╚══════╝
                                  [bold white]C O D E[/bold white]
"""


# ─── Welcome screen ───────────────────────────────────────────────────────────


def show_welcome(
    provider_display: str,
    context_files: list[str],
    session_count: int,
    has_system_prompt: bool,
    max_context_tokens: int | None = None,
    context_token_estimate: int = 0,
) -> None:
    """Print the full welcome banner with session information."""
    banner_text = Text.from_markup(_BANNER.strip())

    console.print()
    console.print(Panel(banner_text, border_style="cyan", expand=False))
    console.print()

    # ── Session info ──────────────────────────────────────────────────────
    console.print(
        f"  [julius.provider]🤖 Provider :[/julius.provider]  {provider_display}"
    )

    if max_context_tokens is not None:
        console.print(
            f"  [julius.info]🔢 Max tokens:[/julius.info]  [dim]{max_context_tokens:,} tokens[/dim]"
        )

    if context_files:
        file_list = ", ".join(context_files[:5])
        extra = f" (+{len(context_files) - 5} more)" if len(context_files) > 5 else ""
        console.print(
            f"  [julius.info]📄 Context  :[/julius.info]  {len(context_files)} file(s) — "
            f"[dim]{file_list}{extra}[/dim]"
        )
        if context_token_estimate > 0:
            console.print(
                f"  [julius.info]📊 Context  :[/julius.info]  [dim]~{context_token_estimate:,} tokens (estimated)[/dim]"
            )
    else:
        console.print(
            "  [julius.dim]📄 Context  :[/julius.dim]  [dim]no text files found[/dim]"
        )

    prompt_status = "[green]✓ loaded[/green]" if has_system_prompt else "[dim]none (using default)[/dim]"
    console.print(f"  [julius.info]🧠 Prompt   :[/julius.info]  {prompt_status}")

    if session_count > 0:
        console.print(
            f"  [julius.info]📜 History  :[/julius.info]  "
            f"[dim]{session_count} previous session(s) loaded[/dim]"
        )

    console.print()
    console.print(Rule(style="dim cyan"))
    console.print(
        "  Type [julius.command]/help[/julius.command] for commands  "
        "· [julius.command]/quit[/julius.command] to exit",
        style="dim",
    )
    console.print(Rule(style="dim cyan"))
    console.print()


# ─── Help ─────────────────────────────────────────────────────────────────────


def show_help() -> None:
    """Display available slash-commands."""
    commands = [
        ("/help", "Show this help message"),
        ("/quit  or  /exit", "Exit Julius Tex"),
        ("/clear", "Clear the current session's conversation history"),
        ("/provider", "Show the active provider and model"),
        ("/providers", "List all configured providers and switch by number"),
        ("/models", "List available models and switch by number"),
        ("/context", "Show how many context files are loaded"),
        ("/save", "Manually save the last exchange to a Markdown file"),
    ]
    rows = "\n".join(f"  [julius.command]{cmd:<28}[/julius.command] {desc}" for cmd, desc in commands)
    tips = (
        "\n  [dim]Tip: press [bold]Enter[/bold] to send · "
        "[bold]Alt+Enter[/bold] (or [bold]Esc Enter[/bold]) to insert a line break[/dim]"
    )
    console.print(
        Panel(
            rows + tips,
            title="[bold cyan]Available Commands[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )
    )
    console.print()


# ─── Message display ──────────────────────────────────────────────────────────


def print_user_message(content: str) -> None:
    """Render the user's message in a styled panel."""
    console.print(
        Panel(
            Text(content, style="white"),
            title="[julius.user]👤 You[/julius.user]",
            border_style="yellow",
            padding=(0, 1),
        )
    )
    console.print()


def print_assistant_message(content: str, provider_name: str) -> None:
    """Render the assistant's full response as Markdown in a styled panel."""
    console.print(
        Panel(
            Markdown(content),
            title=f"[julius.assistant]🤖 {provider_name}[/julius.assistant]",
            border_style="cyan",
            padding=(0, 1),
        )
    )
    console.print()


def print_info(message: str) -> None:
    """Print an informational message."""
    console.print(f"[julius.info]ℹ  {message}[/julius.info]")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[julius.success]✓  {message}[/julius.success]")


def print_warning(message: str) -> None:
    """Print a warning message."""
    console.print(f"[julius.warning]⚠  {message}[/julius.warning]")


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[julius.error]✗  {message}[/julius.error]")
    console.print()


# ─── Streaming live output ────────────────────────────────────────────────────


class StreamingPanel:
    """Context-manager that streams text into a Rich panel in real time."""

    def __init__(self, provider_name: str) -> None:
        self._provider_name = provider_name
        self._buffer = ""
        self._live: Live | None = None

    def _make_panel(self) -> Panel:
        return Panel(
            Markdown(self._buffer) if self._buffer else Spinner("dots"),
            title=f"[julius.assistant]🤖 {self._provider_name}[/julius.assistant]",
            border_style="cyan",
            padding=(0, 1),
        )

    def __enter__(self) -> "StreamingPanel":
        self._live = Live(
            self._make_panel(),
            console=console,
            refresh_per_second=12,
            vertical_overflow="visible",
        )
        self._live.__enter__()
        return self

    def write(self, chunk: str) -> None:
        """Append *chunk* to the buffer and refresh the panel."""
        self._buffer += chunk
        if self._live:
            self._live.update(self._make_panel())

    def __exit__(self, *args: object) -> None:
        if self._live:
            self._live.__exit__(*args)
        console.print()

    @property
    def content(self) -> str:
        """Return the full accumulated response text."""
        return self._buffer


# ─── Token usage display ─────────────────────────────────────────────────────


def print_token_count(current_tokens: int, max_tokens: int | None = None) -> None:
    """Print the estimated token count after saving an interaction.

    If *max_tokens* is provided, also shows percentage of the limit used
    and uses colour-coding (green < 70 %, yellow < 90 %, red ≥ 90 %).
    """
    if max_tokens is not None:
        percentage = (current_tokens / max_tokens) * 100
        if percentage < 70:
            color = "green"
        elif percentage < 90:
            color = "yellow"
        else:
            color = "red"
        console.print(
            f"  [julius.info]🔢 Tokens   :[/julius.info]  "
            f"[{color}]~{current_tokens:,}[/{color}] / [dim]{max_tokens:,}[/dim]"
            f"  [{color}]({percentage:.1f}%)[/{color}]"
        )
    else:
        console.print(
            f"  [julius.info]🔢 Tokens   :[/julius.info]  "
            f"[dim]~{current_tokens:,} tokens (estimated)[/dim]"
        )


# ─── Input prompt ─────────────────────────────────────────────────────────────

# Key bindings used by the multi-line prompt:
#   Enter       → submit the current buffer
#   Alt+Enter   → insert a literal newline (for manual multi-line messages)
_INPUT_KEY_BINDINGS: KeyBindings = KeyBindings()


@_INPUT_KEY_BINDINGS.add("enter")
def _submit(event: KeyPressEvent) -> None:
    event.current_buffer.validate_and_handle()


@_INPUT_KEY_BINDINGS.add("escape", "enter")
def _newline(event: KeyPressEvent) -> None:
    event.current_buffer.insert_text("\n")


_PROMPT_LABEL = FormattedText([("bold ansiyellow", "  You"), ("", ": ")])
_PROMPT_CONTINUATION = FormattedText([("", "  ... ")])


def get_input() -> str:
    """Return the next user input, stripped of surrounding whitespace.

    Uses *prompt_toolkit* so that multi-line text pasted from the clipboard
    is inserted verbatim (including newlines) rather than being submitted line
    by line.  Press **Enter** to send a message and **Alt+Enter** to insert a
    manual line break while composing.
    """
    console.print(Rule(style="dim"))
    try:
        value = _pt_prompt(
            _PROMPT_LABEL,
            multiline=True,
            key_bindings=_INPUT_KEY_BINDINGS,
            prompt_continuation=_PROMPT_CONTINUATION,
        )
    except (EOFError, KeyboardInterrupt):
        return "/quit"
    return value.strip()


def _prompt_number_selection(kind: str, total: int) -> int | None:
    """Ask the user to pick a numbered item from a listed set.

    *kind* is used in the prompt text (e.g. ``"provider"`` or ``"model"``).
    Returns the 1-based index chosen, or *None* if the user cancels /
    provides an invalid input.
    """
    try:
        raw = Prompt.ask(
            f"[julius.info]  Enter {kind} number (1–{total}), or press Enter to cancel[/julius.info]",
            default="",
        )
    except (EOFError, KeyboardInterrupt):
        return None

    raw = raw.strip()
    if not raw:
        return None

    try:
        choice = int(raw)
    except ValueError:
        print_warning(f"'{raw}' is not a valid number.")
        return None

    if not (1 <= choice <= total):
        print_warning(f"Please enter a number between 1 and {total}.")
        return None

    return choice


def prompt_provider_selection(total: int) -> int | None:
    """Ask the user to pick a provider number from the listed options.

    Returns the 1-based index chosen, or *None* if the user cancels /
    provides an invalid input.
    """
    return _prompt_number_selection("provider", total)


def prompt_model_selection(total: int) -> int | None:
    """Ask the user to pick a model number from the listed options.

    Returns the 1-based index chosen, or *None* if the user cancels /
    provides an invalid input.
    """
    return _prompt_number_selection("model", total)
