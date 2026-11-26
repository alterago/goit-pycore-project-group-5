"""T7 — note search. Delete the `pytestmark` line when the task is done."""

import pytest

from personal_assistant.notes import Note, NoteBook

pytestmark = pytest.mark.xfail(reason="T7 is not done yet", strict=True)


@pytest.fixture
def notes():
    notes = NoteBook()
    for text in ["Buy milk", "Call the mentor", "buy a book about Python"]:
        notes.add(Note(text))
    return notes


def test_search_ignores_case_and_keeps_id_order(notes):
    assert [note_id for note_id, _ in notes.search("BUY")] == [1, 3]


def test_search_returns_the_notes(notes):
    [(note_id, note)] = notes.search("mentor")
    assert (note_id, note.text) == (2, "Call the mentor")


def test_nothing_found_gives_empty_list(notes):
    assert notes.search("zzz") == []


# Command level: what the user sees.

def test_cmd_search_notes(cli):
    cli("add-note Buy milk")
    cli("add-note Call the mentor")
    output = cli("search-notes MILK")
    assert "Buy milk" in output and "mentor" not in output


def test_cmd_search_notes_nothing_found(cli):
    cli("add-note Buy milk")
    assert cli("search-notes zzz") == "Nothing found."
