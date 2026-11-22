"""Terminal CLI entry point for the stateless Gemini chatbot."""

from __future__ import annotations

import sys

from rich.console import Console
from rich.panel import Panel

from chatbot.client import GeminiChatClient
from chatbot.config import MissingAPIKeyError, load_config

HELP_TEXT = """사용 가능한 명령어:
  /help   도움말 표시
  /exit   챗봇 종료 (또는 /quit, Ctrl+C)

안내: 이 챗봇은 메모리 기능이 없으며, 매 질문이 독립적으로 처리됩니다."""


def _print_banner(console: Console, model: str) -> None:
    console.print(
        Panel.fit(
            f"[bold cyan]Gemini Terminal Chatbot[/bold cyan]\n"
            f"Model: [green]{model}[/green] (메모리 없음 · 단발성 응답)\n"
            f"명령어: [yellow]/help[/yellow], [yellow]/exit[/yellow]",
            border_style="cyan",
        )
    )


def run_chat_loop(chat_client: GeminiChatClient, console: Console | None = None) -> None:
    """Run the interactive terminal prompt loop."""
    active_console = console or Console()
    _print_banner(active_console, chat_client.model)

    while True:
        try:
            user_input = active_console.input("\n[bold blue]You>[/bold blue] ").strip()
        except (KeyboardInterrupt, EOFError):
            active_console.print("\n[dim]챗봇을 종료합니다.[/dim]")
            break

        if not user_input:
            continue

        command = user_input.lower()
        if command in ("/exit", "/quit"):
            active_console.print("[dim]챗봇을 종료합니다.[/dim]")
            break
        if command == "/help":
            active_console.print(Panel(HELP_TEXT, title="도움말", border_style="yellow"))
            continue

        active_console.print("[bold green]Gemini>[/bold green] ", end="")
        try:
            has_output = False
            for chunk in chat_client.send_message_stream(user_input):
                active_console.print(chunk, end="", markup=False, highlight=False)
                has_output = True
            if not has_output:
                active_console.print("[dim](응답 텍스트가 비어 있습니다)[/dim]", end="")
            active_console.print()
        except Exception as exc:  # noqa: BLE001
            active_console.print(f"\n[bold red]오류:[/bold red] {exc}")


def main() -> None:
    """Application entry point."""
    console = Console()
    try:
        config = load_config()
    except MissingAPIKeyError as exc:
        console.print(f"[bold red]설정 오류:[/bold red] {exc}")
        sys.exit(1)

    chat_client = GeminiChatClient(config)
    run_chat_loop(chat_client, console=console)


if __name__ == "__main__":
    main()
