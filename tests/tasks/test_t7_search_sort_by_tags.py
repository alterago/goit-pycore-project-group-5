"""T7 — search and sort notes by tags (extra part). Delete the `pytestmark` line when done.

ТЗ, додаткові вимоги: «Здійснювати пошук та сортування нотаток за ключовими словами (тегами)»;
«Пошук та сортування нотаток за "тегами"».
Tags are set directly here, so this task does not wait for T6.
"""

import pytest

from personal_assistant.notes import Note, NoteBook

pytestmark = pytest.mark.xfail(reason="T7 is not done yet", strict=True)


def tagged_notes():
    notes = NoteBook()
    for text, tags in [("a", ["work"]), ("b", []), ("c", ["python", "work"]), ("d", ["home"])]:
        note = Note(text)
        note.tags = list(tags)
        notes.add(note)
    return notes


def test_find_by_tag_ignores_hash_and_case():
    notes = tagged_notes()
    assert [note_id for note_id, _ in notes.find_by_tag("#Work")] == [1, 3]
    assert notes.find_by_tag("missing") == []


def test_sorted_by_tags_puts_untagged_last():
    # Sorted by the note's tags in alphabetical order; notes without tags go last.
    assert [note.text for _, note in tagged_notes().sorted_by_tags()] == ["d", "c", "a", "b"]


# Command level: what the user sees.

@pytest.fixture
def with_tags(cli, state):
    state.notes = tagged_notes()
    return cli


def test_cmd_find_tag(with_tags):
    output = with_tags("find-tag #python")
    assert "│ c " in output and "│ a " not in output
    assert with_tags("find-tag nothing") == "Nothing found."


def test_cmd_notes_by_tags(with_tags):
    output = with_tags("notes-by-tags")
    order = [line.split("│")[2].strip() for line in output.splitlines() if line.startswith("│")]
    assert order == ["d", "c", "a", "b"]
