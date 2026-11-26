"""T6 — add tags to notes (extra part). Delete the `pytestmark` line when the task is done.

ТЗ, додаткові вимоги: «Додавати в нотатки "теги", ключові слова, що описують тему
та предмет запису»;
«Додавання "тегів" до нотаток».
"""

import pytest

from personal_assistant.notes import Note

pytestmark = pytest.mark.xfail(reason="T6 is not done yet", strict=True)


def test_tags_are_lowercase_without_hash_and_unique():
    note = Note("text")
    note.add_tag("#Python")
    note.add_tag("python")
    note.add_tag("study")
    assert note.tags == ["python", "study"]


@pytest.mark.parametrize("bad", ["", "#", "two words"])
def test_bad_tag_is_rejected(bad):
    note = Note("text")
    with pytest.raises(ValueError):
        note.add_tag(bad)
    assert note.tags == []


# Command level: what the user sees.

def test_cmd_tags_show_in_notes(cli):
    cli("add-note Learn decorators")
    assert cli("tag 1 python Study") == "Tags added."
    assert "#python, #study" in cli("notes")


def test_tags_survive_restart(cli, reload):
    cli("add-note Learn decorators")
    cli("tag 1 python")
    assert reload().notes.get_note(1).tags == ["python"]
