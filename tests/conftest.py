import io

import pytest
from rich.console import Console

from personal_assistant.cli.base import AppState
from personal_assistant.cli.registry import COMMANDS, parse_input
from personal_assistant.contacts import AddressBook, Record
from personal_assistant.notes import NoteBook
from personal_assistant.storage import HOME_VARIABLE, load_all, save_all


@pytest.fixture(autouse=True)
def data_home(tmp_path, monkeypatch):
    """Every test saves into its own temporary folder, never into the real one."""
    monkeypatch.setenv(HOME_VARIABLE, str(tmp_path))
    return tmp_path


@pytest.fixture
def book() -> AddressBook:
    book = AddressBook()
    john = Record("John")
    john.add_phone("0501234567")
    john.set_birthday("15.03.1990")
    book.add_record(john)
    jane = Record("Jane")
    jane.add_phone("0679876543")
    book.add_record(jane)
    return book


@pytest.fixture
def state(book) -> AppState:
    return AppState(book, NoteBook())


def render(result) -> str:
    """The text a user would see for a command result (tables included)."""
    console = Console(width=200, record=True, file=io.StringIO(), color_system=None)
    console.print(result, markup=not isinstance(result, str))
    return console.export_text().strip()


@pytest.fixture
def cli(state):
    """Run a command line against ``state`` and return what the user sees."""

    def run(line: str) -> str:
        name, args = parse_input(line)
        return render(COMMANDS[name].run(args, state))

    return run


@pytest.fixture
def reload(state):
    """Save ``state`` and load it back, as after a restart of the assistant."""

    def run() -> AppState:
        save_all(state.book, state.notes)
        return AppState(*load_all())

    return run
