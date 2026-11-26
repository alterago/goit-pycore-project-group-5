"""T5 — search, edit and delete notes. Delete the `pytestmark` line when the task is done.

ТЗ: «Проводити пошук за нотатками»; «Редагувати та видаляти нотатки»;
«Пошук, редагування та видалення нотаток».
"""

import pytest

from personal_assistant.notes import Note, NoteBook

pytestmark = pytest.mark.xfail(reason="T5 is not done yet", strict=True)


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


def test_search_nothing_found_gives_empty_list(notes):
    assert notes.search("zzz") == []


def test_edit_replaces_the_text(notes):
    assert notes.edit(1, " changed ").text == "changed"
    assert notes.get_note(1).text == "changed"


def test_edit_with_empty_text_keeps_the_old_one(notes):
    with pytest.raises(ValueError):
        notes.edit(1, "  ")
    assert notes.get_note(1).text == "Buy milk"


def test_edit_unknown_note_raises_key_error(notes):
    with pytest.raises(KeyError):
        notes.edit(99, "text")


def test_delete_removes_the_note(notes):
    notes.delete(2)
    assert list(notes) == [1, 3]


def test_delete_unknown_note_raises_key_error(notes):
    with pytest.raises(KeyError):
        notes.delete(99)


# Command level: what the user sees.

@pytest.fixture
def with_notes(cli):
    cli("add-note Buy milk")
    cli("add-note Call the mentor")
    return cli


def test_cmd_search_notes(with_notes):
    output = with_notes("search-notes MILK")
    assert "Buy milk" in output and "mentor" not in output
    assert with_notes("search-notes zzz") == "Nothing found."


def test_cmd_edit_note(with_notes):
    assert with_notes("edit-note 1 Buy oat milk") == "Note changed."
    assert "Buy oat milk" in with_notes("notes")
    assert with_notes("edit-note 7 text") == "Not found: note 7."


def test_cmd_delete_note(with_notes):
    assert with_notes("delete-note 1") == "Note deleted."
    output = with_notes("notes")
    assert "Buy milk" not in output and "Call the mentor" in output


def test_edit_and_delete_survive_restart(with_notes, reload):
    with_notes("edit-note 1 Changed")
    with_notes("delete-note 2")
    assert [(i, n.text) for i, n in reload().notes.items()] == [(1, "Changed")]
