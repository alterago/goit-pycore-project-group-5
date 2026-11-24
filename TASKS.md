# Tasks

The core already works: contacts with phones and birthdays, notes (add and
show), saving, the command loop with completion. The parts below are left as
`NotImplementedError("T<n>: ...")`. The commands for them are already wired,
so a task is only the model code and its tests.

How to take a task:

1. Write in the team chat which task you take (and in Trello).
2. Branch `t<number>-<short-name>` from `main`.
3. Write the code where the task says; delete the `pytestmark = ...` line in
   the task's test file in `tests/tasks/`; make `pytest` and `flake8` clean.
   You may add tests; do not weaken the given ones.
4. Try the commands by hand in `python -m personal_assistant`.
5. Pull request to `main`, one reviewer from the team.

| # | Task | Where | Size |
|---|------|-------|------|
| T1 | E-mail and address fields | `fields.py`: `Email`, `Address` | S |
| T2 | Phone in common formats | `fields.py`: `normalize_phone`, `Phone` | S |
| T3 | Contact search | `contacts.py`: `AddressBook.search` | S |
| T4 | Delete and rename contacts | `contacts.py`: `AddressBook.delete`, `rename` | S |
| T5 | Birthdays in the next N days | `contacts.py`: `AddressBook.upcoming_birthdays` | M |
| T6 | Edit and delete notes | `notes.py`: `NoteBook.edit`, `delete` | S |
| T7 | Note search | `notes.py`: `NoteBook.search` | S |
| T8 | Tags (extra part) | `notes.py`: `Note.add_tag`, `remove_tag`, `NoteBook.find_by_tag`, `sorted_by_tags` | M |
| T9 | Guess the command (extra part) | `cli/suggest.py`: `suggest_command` | S |

## T1 — E-mail and address fields

`Email(value)`: strip spaces; one `@`; a non-empty part before it; a domain
with a dot after it; no spaces. Otherwise `ValueError` with a clear message.
`Address(value)`: strip spaces; not empty; at most 200 characters.

Done when: `tests/tasks/test_t1_email_address.py` passes; `add-email` and
`add-address` work and the values show in `all`.

## T2 — Phone in common formats

`normalize_phone(raw)` turns `+38 (050) 123-45-67`, `+380501234567`,
`380501234567`, `050-123-45-67`, `(050) 123 45 67` into `0501234567`: drop
spaces, dashes and brackets, then the leading `+38`/`38`. `Phone` calls it
before its 10-digit check, so the stored value is always 10 digits.

Done when: `tests/tasks/test_t2_phone_formats.py` passes; `add John "+38 (050) 123-45-67"` stores `0501234567`.

## T3 — Contact search

`AddressBook.search(query)` returns the records whose name, any phone,
e-mail or address contains `query`, ignoring the letter case, in the order
they were added; `[]` when none.

Done when: `tests/tasks/test_t3_contact_search.py` passes; `search` shows a table.

## T4 — Delete and rename contacts

`AddressBook.delete(name)`: find the record ignoring the case and remove it;
`KeyError` when there is none. `AddressBook.rename(old, new)`: the record
keeps its phones and other fields and is stored under the new name;
`KeyError` for an unknown contact; `ValueError` when another contact already
has the new name (any case). Return the record.

Done when: `tests/tasks/test_t4_delete_rename.py` passes; `delete` and `rename` work.

## T5 — Birthdays in the next N days

`AddressBook.upcoming_birthdays(days, today=None)` returns
`(birthday date, record)` for every contact whose next birthday falls between
`today` and `today + days`, both included, sorted by date. `today` defaults
to `date.today()`. Contacts without a birthday are skipped; negative `days`
raise `ValueError`. Use `birthdays.next_birthday()`; it already handles 29
February and the new year.

Done when: `tests/tasks/test_t5_birthdays.py` passes; `birthdays 30` lists them.

## T6 — Edit and delete notes

`NoteBook.edit(note_id, text)`: replace the text (checked by
`notes.check_text`, the old text stays on error) and return the note.
`NoteBook.delete(note_id)`. Both raise `KeyError` for an unknown id. Ids are
never reused.

Done when: `tests/tasks/test_t6_edit_delete_notes.py` passes; `edit-note` and `delete-note` work.

## T7 — Note search

`NoteBook.search(query)` returns `(id, note)` for notes whose text contains
`query`, ignoring the case, in id order; `[]` when none.

Done when: `tests/tasks/test_t7_note_search.py` passes; `search-notes` shows a table.

## T8 — Tags (extra part, +10 points with T9)

`Note.add_tag(tag)`: a tag is stored lowercase without a leading `#`; no
spaces, not empty (`ValueError`); adding the same tag twice keeps one.
`Note.remove_tag(tag)`: same normalization; `ValueError` when the note has no
such tag. `NoteBook.find_by_tag(tag)`: `(id, note)` with that tag, in id
order. `NoteBook.sorted_by_tags()`: all notes sorted by their sorted tag
list; notes without tags last.

Done when: `tests/tasks/test_t8_tags.py` passes; `tag`, `untag`, `find-tag`,
`notes-by-tags` work.

## T9 — Guess the command (extra part)

`suggest_command(text, commands)` returns the command closest to what the
user typed, or `None` when nothing is close (`difflib.get_close_matches` with
`n=1`). The loop already shows "Did you mean '...'?" when it returns one.

Done when: `tests/tasks/test_t9_suggest_command.py` passes; typing `ad-note`
suggests `add-note`.
