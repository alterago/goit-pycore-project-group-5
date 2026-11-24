import pytest

from personal_assistant.notes import MAX_NOTE_LENGTH, Note, NoteBook


def test_note_text_is_stripped_and_checked():
    assert Note("  buy milk ").text == "buy milk"
    for bad in ["", "   ", "x" * (MAX_NOTE_LENGTH + 1)]:
        with pytest.raises(ValueError):
            Note(bad)


def test_notes_get_increasing_ids():
    notes = NoteBook()
    assert notes.add(Note("first")) == 1
    assert notes.add(Note("second")) == 2
    assert notes.get_note(2).text == "second"


def test_missing_note_raises_key_error():
    with pytest.raises(KeyError):
        NoteBook().get_note(1)
