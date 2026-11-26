# Personal Assistant

A console assistant that keeps an address book and notes. Team project of
group 5, Python Programming (GoIT Neoversity).

## What it does

- Contacts: name, phones, birthday, e-mail, address; add, change, search, delete.
- Birthdays coming in the next N days.
- Validation of phones, e-mails and birthdays when a contact is added or changed.
- Notes: add, show, edit, delete, search; tags, search and sorting by tags.
- Command completion (Tab) and a guess of the command when it is mistyped.
- The data is kept in `~/.personal_assistant/` and survives a restart.

## Install

Python 3.10 or newer.

```bash
git clone <repository URL>
cd <repository folder>
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e .
```

## Run

```bash
assistant
# or
python -m personal_assistant
```

The list of commands is shown once at start; type `help` to see it again,
`exit` or `close` (or Ctrl+D) to leave. Words with spaces go in quotes:

```text
> add John 0501234567
Contact added.
> add-birthday John 15.03.1990
Birthday saved.
> add-address John "Kyiv, Khreshchatyk St 1"
Address saved.
> add-note Call the mentor about the review
Note 1 added.
> birthdays 30
15.03.2026 (Sunday): John
```

| Command | What it does |
|---|---|
| `add <name> <phone>` | add a contact, or one more phone to it |
| `change <name> <old> <new>` | change a phone |
| `remove-phone <name> <phone>` | remove a phone |
| `show <name>` / `all` | show one contact / all contacts |
| `add-birthday <name> <DD.MM.YYYY>` | set a birthday |
| `add-email <name> <email>` | set an e-mail |
| `add-address <name> <address>` | set an address |
| `search <text>` | find contacts by any field |
| `delete <name>` | delete a contact |
| `birthdays [days]` | birthdays in the next days (7 by default) |
| `add-note <text>` / `notes` | add a note / show all notes |
| `edit-note <id> <text>` / `delete-note <id>` | change / delete a note |
| `search-notes <text>` | find notes by text |
| `tag <id> <tag> [tag...]` | add tags to a note |
| `find-tag <tag>` / `notes-by-tags` | notes with a tag / notes sorted by tags |

## Development

```bash
pip install -e '.[dev]'
pre-commit install        # flake8 and whitespace checks before each commit
pytest                    # tests
flake8                    # PEP 8
```

Set `PERSONAL_ASSISTANT_HOME` to keep the data in another folder (the tests
do this, so they never touch your real data).

### Layout

```text
personal_assistant/
  fields.py          Field and its subclasses: Name, Phone, Birthday, Email, Address
  contacts.py        Record (one contact) and AddressBook
  birthdays.py       date helpers for birthdays
  notes.py           Note and NoteBook
  storage.py         saving and loading in the user's folder
  cli/
    app.py           the command loop (prompt_toolkit), start and exit
    registry.py      all commands by name, parsing of the input line
    base.py          AppState, Command, the error-handling decorator
    contact_commands.py, note_commands.py   command handlers
    output.py        rich tables
    suggest.py       guessing a mistyped command
tests/               tests of the core
tests/tasks/         tests of the team tasks (see TASKS.md)
```

### How we work

- The tasks are in [TASKS.md](TASKS.md). Take one, make a branch
  `t<number>-<short-name>`, open a pull request to `main`.
- An unfinished part raises `NotImplementedError("T<n>: ...")`; the
  assistant answers "Not implemented yet (T<n>...)" instead of crashing.
- Each task has its tests in `tests/tasks/`. They are marked as expected to
  fail; when your code is ready, delete the `pytestmark = ...` line in your
  task's test file and make all of them pass.
- Before a pull request: `pytest` and `flake8` are clean.
