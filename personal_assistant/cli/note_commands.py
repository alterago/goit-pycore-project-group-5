"""Commands for notes."""

from personal_assistant.cli.base import AppState, Command, parse_id, require_args
from personal_assistant.cli.output import notes_table
from personal_assistant.notes import Note


def add_note(args: list[str], state: AppState):
    require_args(args, 1, "add-note <text>")
    note_id = state.notes.add(Note(" ".join(args)))
    return f"Note {note_id} added."


def show_notes(args: list[str], state: AppState):
    if not state.notes:
        return "No notes saved."
    return notes_table(state.notes.items())


def edit_note(args: list[str], state: AppState):
    require_args(args, 2, "edit-note <id> <text>")
    state.notes.edit(parse_id(args[0]), " ".join(args[1:]))
    return "Note changed."


def delete_note(args: list[str], state: AppState):
    require_args(args, 1, "delete-note <id>")
    state.notes.delete(parse_id(args[0]))
    return "Note deleted."


def search_notes(args: list[str], state: AppState):
    require_args(args, 1, "search-notes <text>")
    found = state.notes.search(" ".join(args))
    return notes_table(found, title="Found") if found else "Nothing found."


def tag_note(args: list[str], state: AppState):
    require_args(args, 2, "tag <id> <tag> [tag...]")
    note = state.notes.get_note(parse_id(args[0]))
    for tag in args[1:]:
        note.add_tag(tag)
    return "Tags added."


def untag_note(args: list[str], state: AppState):
    require_args(args, 2, "untag <id> <tag>")
    state.notes.get_note(parse_id(args[0])).remove_tag(args[1])
    return "Tag removed."


def find_tag(args: list[str], state: AppState):
    require_args(args, 1, "find-tag <tag>")
    found = state.notes.find_by_tag(args[0])
    return notes_table(found, title=f"#{args[0].lstrip('#')}") if found else "Nothing found."


def notes_by_tags(args: list[str], state: AppState):
    if not state.notes:
        return "No notes saved."
    return notes_table(state.notes.sorted_by_tags(), title="Notes by tags")


COMMANDS = [
    Command("add-note", add_note, "add-note <text>", "add a note"),
    Command("notes", show_notes, "notes", "show all notes", changes_data=False),
    Command("edit-note", edit_note, "edit-note <id> <text>", "change a note's text"),
    Command("delete-note", delete_note, "delete-note <id>", "delete a note"),
    Command("search-notes", search_notes, "search-notes <text>", "find notes by text",
            changes_data=False),
    Command("tag", tag_note, "tag <id> <tag> [tag...]", "add tags to a note"),
    Command("untag", untag_note, "untag <id> <tag>", "remove a tag from a note"),
    Command("find-tag", find_tag, "find-tag <tag>", "notes with a tag", changes_data=False),
    Command("notes-by-tags", notes_by_tags, "notes-by-tags", "notes sorted by tags",
            changes_data=False),
]
