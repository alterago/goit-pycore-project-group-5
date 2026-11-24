from personal_assistant.notes import Note, NoteBook
from personal_assistant.storage import CONTACTS_FILE, load_all, save_all


def test_data_survives_a_restart(book):
    notes = NoteBook()
    notes.add(Note("call John"))
    save_all(book, notes)

    loaded_book, loaded_notes = load_all()
    assert str(loaded_book["John"]) == str(book["John"])
    assert loaded_notes.get_note(1).text == "call John"
    assert loaded_notes.add(Note("next")) == 2  # ids go on after a restart


def test_no_files_give_empty_books():
    book, notes = load_all()
    assert len(book) == 0 and len(notes) == 0


def test_damaged_file_is_set_aside(data_home):
    (data_home / CONTACTS_FILE).write_bytes(b"not a pickle")
    book, _ = load_all()
    assert len(book) == 0
    assert (data_home / f"{CONTACTS_FILE}.corrupted").exists()
