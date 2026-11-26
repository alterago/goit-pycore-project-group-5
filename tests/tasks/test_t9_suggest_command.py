"""T9 — guess the command the user meant. Delete the `pytestmark` line when the task is done."""

import pytest

from personal_assistant.cli.app import unknown_command
from personal_assistant.cli.registry import command_names
from personal_assistant.cli.suggest import suggest_command

pytestmark = pytest.mark.xfail(reason="T9 is not done yet", strict=True)


@pytest.mark.parametrize("typed, expected", [
    ("ad-note", "add-note"),
    ("birthday", "birthdays"),
    ("serch", "search"),
    ("ext", "exit"),
])
def test_closest_command_is_suggested(typed, expected):
    assert suggest_command(typed, command_names()) == expected


def test_nothing_close_gives_none():
    assert suggest_command("zzzz", command_names()) is None


def test_unknown_command_message_has_the_guess():
    assert "Did you mean 'add-note'?" in str(unknown_command("ad-note"))


def test_suggestion_ignores_letter_case():
    assert suggest_command("NOTES", command_names()) == "notes"


def test_loop_prints_the_guess(state, capsys):
    from personal_assistant.cli import app
    app.handle("serch John", state)
    assert "Did you mean 'search'?" in capsys.readouterr().out
