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


# Command level: what the user sees.

@pytest.fixture
def with_note(cli):
    cli("add-note Buy milk")
    return cli


def test_cmd_edit_note(with_note):
    assert with_note("edit-note 1 Buy oat milk") == "Note changed."
    assert "Buy oat milk" in with_note("notes")


def test_cmd_edit_unknown_note(with_note):
    assert with_note("edit-note 7 text").startswith("Not found")


def test_cmd_delete_note(with_note):
    assert with_note("delete-note 1") == "Note deleted."
    assert with_note("notes") == "No notes saved."


def test_edit_and_delete_survive_restart(with_note, reload):
    with_note("add-note Second")
    with_note("edit-note 1 Changed")
    with_note("delete-note 2")
    notes = reload().notes
    assert [(i, n.text) for i, n in notes.items()] == [(1, "Changed")]
