"""What every command shares: the app state, the command type and the error handling."""

from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps

from rich.console import RenderableType
from rich.text import Text

from personal_assistant.contacts import AddressBook, Record
from personal_assistant.notes import NoteBook


@dataclass
class AppState:
    """The data the commands work on."""

    book: AddressBook
    notes: NoteBook


Handler = Callable[[list[str], AppState], RenderableType]


def input_error(func: Handler) -> Handler:
    """Turn errors raised by a handler into a message for the user."""

    @wraps(func)
    def inner(args: list[str], state: AppState) -> RenderableType:
        try:
            return func(args, state)
        except NotImplementedError as error:
            return Text(f"Not implemented yet ({error}).", style="yellow")
        except ValueError as error:
            return Text(str(error), style="red")
        except KeyError as error:
            return Text(f"Not found: {error.args[0]}.", style="red")

    return inner


@dataclass(frozen=True)
class Command:
    """A command the user types: its name, handler, usage line and help text."""

    name: str
    handler: Handler
    usage: str
    help: str
    changes_data: bool = True

    def run(self, args: list[str], state: AppState) -> RenderableType:
        return input_error(self.handler)(args, state)


def require_args(args: list[str], count: int, usage: str) -> None:
    """Raise ValueError with a usage hint when there are too few arguments."""
    if len(args) < count:
        raise ValueError(f"Usage: {usage}")


def get_record(book: AddressBook, name: str) -> Record:
    """Return the record or raise KeyError when there is no such contact."""
    record = book.find(name)
    if record is None:
        raise KeyError(f"contact {name}")
    return record


def parse_id(value: str) -> int:
    """Return a note id from the user's text."""
    if not value.isdigit():
        raise ValueError(f"Note id must be a number, got '{value}'.")
    return int(value)
