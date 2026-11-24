import pytest

from personal_assistant.cli.base import AppState
from personal_assistant.contacts import AddressBook, Record
from personal_assistant.notes import NoteBook
from personal_assistant.storage import HOME_VARIABLE


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
