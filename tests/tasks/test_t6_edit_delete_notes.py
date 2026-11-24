"""T6 — edit and delete notes. Delete the `pytestmark` line when the task is done."""

import pytest

from personal_assistant.notes import Note, NoteBook

pytestmark = pytest.mark.xfail(reason="T6 is not done yet", strict=True)


@pytest.fixture
def notes():
    notes = NoteBook()
    notes.add(Note("first"))
    notes.add(Note("second"))
    return notes


def test_edit_replaces_the_text(notes):
    assert notes.edit(1, " changed ").text == "changed"
    assert notes.get_note(1).text == "changed"


def test_edit_with_empty_text_keeps_the_old_one(notes):
    with pytest.raises(ValueError):
        notes.edit(1, "  ")
    assert notes.get_note(1).text == "first"


def test_edit_unknown_note_raises_key_error(notes):
    with pytest.raises(KeyError):
        notes.edit(99, "text")


def test_delete_removes_the_note_and_ids_are_not_reused(notes):
    notes.delete(2)
    assert list(notes) == [1]
    assert notes.add(Note("third")) == 3


def test_delete_unknown_note_raises_key_error(notes):
    with pytest.raises(KeyError):
        notes.delete(99)
