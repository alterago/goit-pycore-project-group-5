"""The command loop: read a line, run the command, save the data, until exit."""

import sys
from collections.abc import Callable

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from rich.console import Console, RenderableType
from rich.text import Text

from personal_assistant.cli.base import AppState
from personal_assistant.cli.output import commands_table
from personal_assistant.cli.registry import COMMANDS, EXIT_COMMANDS, command_names, parse_input
from personal_assistant.cli.suggest import suggest_command
from personal_assistant.storage import StorageError, load_all, save_all

PROMPT = "> "

console = Console()


def make_reader() -> Callable[[str], str]:
    """Return a line reader: prompt_toolkit with completion in a terminal, input() otherwise."""
    if not sys.stdin.isatty():
        return input
    completer = WordCompleter(command_names(), ignore_case=True, sentence=True)
    session = PromptSession(completer=completer, complete_while_typing=True)
    return session.prompt


def unknown_command(name: str) -> Text:
    try:
        guess = suggest_command(name, command_names())
    except NotImplementedError:  # T9 is not done yet
        guess = None
    hint = f" Did you mean '{guess}'?" if guess else " Type 'help' to see the commands."
    return Text(f"Unknown command '{name}'.{hint}", style="yellow")


def show(result: RenderableType) -> None:
    # Plain strings carry user data, so square brackets in them are not markup.
    console.print(result, markup=not isinstance(result, str))


def save(state: AppState) -> None:
    try:
        save_all(state.book, state.notes)
    except StorageError as error:
        console.print(Text(str(error), style="red"))


def handle(line: str, state: AppState) -> bool:
    """Run one line; return False when the user wants to leave."""
    name, args = parse_input(line)
    if not name:
        return True
    if name in EXIT_COMMANDS:
        return False
    command = COMMANDS.get(name)
    if command is None:
        show(unknown_command(name))
        return True
    show(command.run(args, state))
    if command.changes_data:
        save(state)
    return True


def run(state: AppState) -> None:
    read = make_reader()
    while True:
        try:
            line = read(PROMPT)
        except (KeyboardInterrupt, EOFError):  # Ctrl+C and Ctrl+D leave like 'exit'
            break
        if not handle(line, state):
            break
    console.print("Good bye!")


def main() -> None:
    try:
        book, notes = load_all()
    except StorageError as error:
        console.print(Text(str(error), style="red"))
        console.print("The assistant was not started, so the saved data is not overwritten.")
        return
    state = AppState(book, notes)
    console.print("[bold]Personal assistant[/bold]: contacts and notes.")
    console.print(commands_table(COMMANDS.values()))
    console.print("Type 'exit' or 'close' to leave.")
    try:
        run(state)
    finally:
        save(state)
