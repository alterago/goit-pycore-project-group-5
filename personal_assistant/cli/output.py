"""Rich tables for contacts, notes and the list of commands."""

from collections.abc import Iterable

from rich.table import Table
from rich.text import Text

from personal_assistant.contacts import Record
from personal_assistant.notes import Note


def _text(field) -> Text:
    """User data as plain text: square brackets in it are not rich markup."""
    return Text("" if field is None else str(field))


def contacts_table(records: Iterable[Record], title: str = "Contacts") -> Table:
    table = Table(title=Text(title), show_lines=False)
    for column in ("Name", "Phones", "Birthday", "Email", "Address"):
        table.add_column(column)
    for record in records:
        table.add_row(
            _text(record.name),
            _text("\n".join(str(p) for p in record.phones)),
            _text(record.birthday),
            _text(record.email),
            _text(record.address),
        )
    return table


def notes_table(items: Iterable[tuple[int, Note]], title: str = "Notes") -> Table:
    table = Table(title=Text(title))
    table.add_column("Id", justify="right")
    table.add_column("Text")
    table.add_column("Tags")
    table.add_column("Created")
    for note_id, note in items:
        table.add_row(
            str(note_id),
            _text(note.text),
            _text(", ".join("#" + tag for tag in note.tags)),
            note.created.strftime("%d.%m.%Y %H:%M"),
        )
    return table


def commands_table(commands) -> Table:
    table = Table(title="Commands", show_header=False, box=None, padding=(0, 2))
    table.add_column(style="bold cyan")
    table.add_column()
    for command in commands:
        table.add_row(Text(command.usage), Text(command.help))
    return table
