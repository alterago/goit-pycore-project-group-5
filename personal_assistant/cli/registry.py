"""All commands by name, and parsing of the user's line."""

import shlex

from personal_assistant.cli import contact_commands, note_commands
from personal_assistant.cli.base import AppState, Command
from personal_assistant.cli.output import commands_table

EXIT_COMMANDS = ("exit", "close")


def hello(args: list[str], state: AppState):
    return "How can I help you?"


def show_help(args: list[str], state: AppState):
    return commands_table(COMMANDS.values())


GENERAL = [
    Command("hello", hello, "hello", "greeting", changes_data=False),
    Command("help", show_help, "help", "show this list", changes_data=False),
]

COMMANDS: dict[str, Command] = {
    command.name: command
    for command in GENERAL + contact_commands.COMMANDS + note_commands.COMMANDS
}


def command_names() -> list[str]:
    return [*COMMANDS, *EXIT_COMMANDS]


def parse_input(line: str) -> tuple[str, list[str]]:
    """Split the line into a lowercase command and its arguments.

    Quotes group words: add-address John "Kyiv, Main St 1". A line with an
    unpaired quote (an apostrophe in a word) is split on spaces.
    """
    try:
        parts = shlex.split(line)
    except ValueError:
        parts = line.split()
    if not parts:
        return "", []
    return parts[0].lower(), parts[1:]
