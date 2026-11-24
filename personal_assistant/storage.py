"""Saving the address book and the notebook in the user's folder and loading them back.

The files live in ~/.personal_assistant/ (or in $PERSONAL_ASSISTANT_HOME).
Only load files this program saved itself: unpickling untrusted data can run
arbitrary code.
"""

import os
import pickle
from pathlib import Path

from personal_assistant.contacts import AddressBook
from personal_assistant.notes import NoteBook

HOME_VARIABLE = "PERSONAL_ASSISTANT_HOME"
CONTACTS_FILE = "contacts.pkl"
NOTES_FILE = "notes.pkl"


class StorageError(Exception):
    """A data file cannot be read or written."""


def data_dir() -> Path:
    return Path(os.environ.get(HOME_VARIABLE) or Path.home() / ".personal_assistant")


def save(obj, filename: str) -> None:
    """Save ``obj`` with pickle; a half-written file never replaces the old one."""
    folder = data_dir()
    path = folder / filename
    temp = path.with_name(path.name + ".tmp")
    try:
        folder.mkdir(parents=True, exist_ok=True)
        with open(temp, "wb") as file:
            pickle.dump(obj, file)
        os.replace(temp, path)
    except OSError as error:
        temp.unlink(missing_ok=True)
        raise StorageError(f"Cannot save {path}: {error.strerror}.") from error


def load(filename: str, kind: type):
    """Return the saved object of ``kind``, or a new empty one when there is no file.

    A damaged file is moved to '<file>.corrupted' so it is not overwritten,
    and an empty object is returned.
    """
    path = data_dir() / filename
    try:
        with open(path, "rb") as file:
            obj = pickle.load(file)
    except FileNotFoundError:
        return kind()
    except OSError as error:
        raise StorageError(f"Cannot read {path}: {error.strerror}.") from error
    except (pickle.UnpicklingError, EOFError, AttributeError, ImportError, IndexError):
        return _set_aside(path, kind)
    if not isinstance(obj, kind):
        return _set_aside(path, kind)
    return obj


def _set_aside(path: Path, kind: type):
    os.replace(path, path.with_name(path.name + ".corrupted"))
    print(f"{path} is damaged; it was moved to {path.name}.corrupted.")
    return kind()


def load_all() -> tuple[AddressBook, NoteBook]:
    return load(CONTACTS_FILE, AddressBook), load(NOTES_FILE, NoteBook)


def save_all(book: AddressBook, notes: NoteBook) -> None:
    save(book, CONTACTS_FILE)
    save(notes, NOTES_FILE)
