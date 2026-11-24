"""Notes: a text note with tags and the notebook that keeps notes by id."""

from collections import UserDict
from datetime import datetime

MAX_NOTE_LENGTH = 2000


def check_text(text: str) -> str:
    """Return the stripped text or raise ValueError when it is empty or too long."""
    text = (text or "").strip()
    if not text:
        raise ValueError("Note text cannot be empty.")
    if len(text) > MAX_NOTE_LENGTH:
        raise ValueError(f"Note text is longer than {MAX_NOTE_LENGTH} characters.")
    return text


class Note:
    """A text note. Tags are lowercase words without spaces."""

    def __init__(self, text: str):
        self.text = check_text(text)
        self.tags: list[str] = []
        self.created = datetime.now()

    def add_tag(self, tag: str) -> None:
        """TASK T8 — see TASKS.md."""
        raise NotImplementedError("T8: add a tag")

    def remove_tag(self, tag: str) -> None:
        """TASK T8 — see TASKS.md."""
        raise NotImplementedError("T8: remove a tag")

    def __str__(self):
        tags = f" [{', '.join('#' + t for t in self.tags)}]" if self.tags else ""
        return f"{self.text}{tags}"


class NoteBook(UserDict):
    """Notes by their id: 1, 2, 3... An id is never reused."""

    last_id = 0

    def add(self, note: Note) -> int:
        self.last_id += 1
        self.data[self.last_id] = note
        return self.last_id

    def get_note(self, note_id: int) -> Note:
        """Return the note or raise KeyError when there is no such id."""
        if note_id not in self.data:
            raise KeyError(f"note {note_id}")
        return self.data[note_id]

    def edit(self, note_id: int, text: str) -> Note:
        """Replace the note's text and return the note.

        TASK T6 — see TASKS.md.
        """
        raise NotImplementedError("T6: edit a note")

    def delete(self, note_id: int) -> None:
        """TASK T6 — see TASKS.md."""
        raise NotImplementedError("T6: delete a note")

    def search(self, query: str) -> list[tuple[int, Note]]:
        """Return (id, note) for notes whose text contains ``query``.

        TASK T7 — see TASKS.md.
        """
        raise NotImplementedError("T7: note search")

    def find_by_tag(self, tag: str) -> list[tuple[int, Note]]:
        """TASK T8 — see TASKS.md."""
        raise NotImplementedError("T8: notes by tag")

    def sorted_by_tags(self) -> list[tuple[int, Note]]:
        """TASK T8 — see TASKS.md."""
        raise NotImplementedError("T8: notes sorted by tags")
