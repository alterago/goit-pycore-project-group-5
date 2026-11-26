"""T8 — tags: add, remove, find and sort by tags. Delete the `pytestmark` line when done."""

import pytest

from personal_assistant.notes import Note, NoteBook

pytestmark = pytest.mark.xfail(reason="T8 is not done yet", strict=True)


def test_tags_are_lowercase_without_hash_and_unique():
    note = Note("text")
    note.add_tag("#Python")
    note.add_tag("python")
    note.add_tag("study")
    assert note.tags == ["python", "study"]


@pytest.mark.parametrize("bad", ["", "#", "two words"])
def test_bad_tag_is_rejected(bad):
    with pytest.raises(ValueError):
        Note("text").add_tag(bad)


def test_remove_tag():
    note = Note("text")
    note.add_tag("python")
    note.remove_tag("#PYTHON")
    assert note.tags == []
    with pytest.raises(ValueError):
        note.remove_tag("python")


@pytest.fixture
def notes():
    notes = NoteBook()
    for text, tags in [("a", ["work"]), ("b", []), ("c", ["python", "work"]), ("d", ["home"])]:
        note = Note(text)
        for tag in tags:
            note.add_tag(tag)
        notes.add(note)
    return notes


def test_find_by_tag(notes):
    assert [note_id for note_id, _ in notes.find_by_tag("#Work")] == [1, 3]
    assert notes.find_by_tag("missing") == []


def test_sorted_by_tags_puts_untagged_last(notes):
    # Sorted by the note's tags in alphabetical order; notes without tags go last.
    assert [note.text for _, note in notes.sorted_by_tags()] == ["d", "c", "a", "b"]


# Command level: what the user sees.

@pytest.fixture
def tagged(cli):
    cli("add-note Learn decorators")
    cli("add-note Buy milk")
    cli("tag 1 python Study")
    return cli


def test_cmd_tags_show_in_notes(tagged):
    assert "#python, #study" in tagged("notes")


def test_cmd_find_tag(tagged):
    output = tagged("find-tag #Python")
    assert "Learn decorators" in output and "Buy milk" not in output
    assert tagged("find-tag nothing") == "Nothing found."


def test_cmd_untag(tagged, state):
    assert tagged("untag 1 study") == "Tag removed."
    assert state.notes.get_note(1).tags == ["python"]


def test_cmd_notes_by_tags_puts_untagged_last(tagged):
    output = tagged("notes-by-tags")
    assert output.index("Learn decorators") < output.index("Buy milk")


def test_tags_survive_restart(tagged, reload):
    assert reload().notes.get_note(1).tags == ["python", "study"]
