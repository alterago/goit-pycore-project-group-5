# Tasks

Every task is a line of the project's ТЗ (the «Персональний помічник» sheet):
the ТЗ words are quoted in each task. Each task is also a GitHub issue with a
checklist (links in the table).

Already done in the core (not tasks): contacts with names, phones and
birthdays; phone and birthday validation; changing a phone; adding and showing
notes; saving to the user's folder and loading after a restart; the command
loop.

How to take a task:

1. Assign the issue to yourself and write in the team chat.
2. Branch `t<number>-<short-name>` from `main`.
3. Delete the `pytestmark = ...` line in the task's test file in `tests/tasks/`,
   write the code, make `pytest` and `flake8` clean. You may add tests; do not
   weaken the given ones.
4. Try the commands by hand in `python -m personal_assistant`.
5. Pull request to `main` with `Closes #<issue>`, one reviewer from the team.

| # | Task | Where | Issue |
|---|------|-------|-------|
| T1 | E-mail and address in a contact | `fields.py`: `Email`, `Address` | [#10](https://github.com/alterago/goit-pycore-project-group-5/issues/10) |
| T2 | Contact search | `contacts.py`: `AddressBook.search` | [#11](https://github.com/alterago/goit-pycore-project-group-5/issues/11) |
| T3 | Delete a contact | `contacts.py`: `AddressBook.delete` | [#12](https://github.com/alterago/goit-pycore-project-group-5/issues/12) |
| T4 | Birthdays in the next N days | `contacts.py`: `AddressBook.upcoming_birthdays` | [#13](https://github.com/alterago/goit-pycore-project-group-5/issues/13) |
| T5 | Search, edit and delete notes | `notes.py`: `NoteBook.search`, `edit`, `delete` | [#14](https://github.com/alterago/goit-pycore-project-group-5/issues/14) |
| T6 | Add tags to notes (extra) | `notes.py`: `Note.add_tag` | [#15](https://github.com/alterago/goit-pycore-project-group-5/issues/15) |
| T7 | Search and sort notes by tags (extra) | `notes.py`: `NoteBook.find_by_tag`, `sorted_by_tags` | [#16](https://github.com/alterago/goit-pycore-project-group-5/issues/16) |
| T8 | Guess the command (extra) | `cli/suggest.py`: `suggest_command` | [#17](https://github.com/alterago/goit-pycore-project-group-5/issues/17) |

Where the ТЗ says nothing about a detail, the rule below is the team's choice
and is marked so.

## T1 — E-mail and address in a contact

ТЗ: «Зберігати контакти з іменами, адресами, номерами телефонів, email та днями
народження»; «Валідація номера телефону та електронної пошти під час додавання
або редагування контакту».

- `Email(value)`: strip spaces; reject a value that is not like `name@domain.tld`
  with `ValueError` whose message starts with `Invalid e-mail` (team's choice of
  the message and of the check: one `@`, a dot in the domain, no spaces).
- `Address(value)`: strip spaces; an empty address is `ValueError`. The ТЗ asks
  only to store it — no other checks.

Tests: `tests/tasks/test_t1_email_address.py`.

## T2 — Contact search

ТЗ: «Здійснювати пошук контактів серед контактів книги»; «Пошук контактів за
різними критеріями (наприклад, за іменем)».

- `AddressBook.search(query)`: records whose name, any phone, e-mail or address
  contains `query`, ignoring the case, in the order they were added; `[]` when
  none.

Tests: `tests/tasks/test_t2_contact_search.py`.

## T3 — Delete a contact

ТЗ: «Редагувати та видаляти записи з книги контактів»; «Редагування та видалення
контактів». Editing is already there (`change`, `add-birthday`, `add-email`,
`add-address`); deleting is the task.

- `AddressBook.delete(name)`: find the record ignoring the case and remove it;
  `KeyError(f"contact {name}")` when there is none.

Tests: `tests/tasks/test_t3_delete_contact.py`.

## T4 — Birthdays in the next N days

ТЗ: «Виводити список контактів, у яких день народження через задану кількість
днів від поточної дати».

- `AddressBook.upcoming_birthdays(days, today=None)`: `(birthday date, record)`
  for every contact whose next birthday is from `today` to `today + days`, both
  included, sorted by date; without a birthday — skipped. Use
  `birthdays.next_birthday()`.

Tests: `tests/tasks/test_t4_birthdays.py`.

## T5 — Search, edit and delete notes

ТЗ: «Проводити пошук за нотатками»; «Редагувати та видаляти нотатки»; «Пошук,
редагування та видалення нотаток».

- `NoteBook.search(query)`: `(id, note)` whose text contains `query`, ignoring
  the case, in id order.
- `NoteBook.edit(note_id, text)`: check the text with `check_text` (the old text
  stays on error), replace it, return the note.
- `NoteBook.delete(note_id)`. Edit and delete raise `KeyError` for an unknown id.

Tests: `tests/tasks/test_t5_notes_search_edit_delete.py`.

## T6 — Add tags to notes (extra part)

ТЗ, додаткові вимоги: «Додавати в нотатки "теги", ключові слова, що описують
тему та предмет запису»; «Додавання "тегів" до нотаток».

- `Note.add_tag(tag)`: team's choice of the tag form — lowercase, without a
  leading `#`, one word; empty or with a space is `ValueError`; the same tag
  twice is kept once.

Tests: `tests/tasks/test_t6_add_tags.py`.

## T7 — Search and sort notes by tags (extra part)

ТЗ, додаткові вимоги: «Здійснювати пошук та сортування нотаток за ключовими
словами (тегами)»; «Пошук та сортування нотаток за "тегами"».

- `NoteBook.find_by_tag(tag)`: `(id, note)` with that tag (compared like T6:
  without `#`, ignoring the case), in id order.
- `NoteBook.sorted_by_tags()`: all `(id, note)` sorted by the note's sorted tag
  list; notes without tags last (team's choice of the order).

Tests: `tests/tasks/test_t7_search_sort_by_tags.py` (they set tags directly, so
T7 does not wait for T6).

## T8 — Guess the command (extra part)

ТЗ, додаткові вимоги, «Інтелектуальний аналіз»: «Помічник повинен вгадувати, що
хоче від нього користувач, на основі введеного тексту та пропонувати найближчу
команду для виконання». Not in the TECH acceptance criteria; asked the mentor
how much is expected.

- `suggest_command(text, commands)`: the command closest to `text`, ignoring
  the case, or `None` when nothing is close. The loop already prints
  "Did you mean '...'?".

Tests: `tests/tasks/test_t8_suggest_command.py`.
