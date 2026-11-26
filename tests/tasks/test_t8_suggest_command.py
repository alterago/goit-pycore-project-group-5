"""T8 — guess the command (extra part). Delete the `pytestmark` line when the task is done.

ТЗ, додаткові вимоги, «Інтелектуальний аналіз»: «Помічник повинен вгадувати, що хоче від нього
користувач, на основі введеного тексту та пропонувати найближчу команду для виконання».
"""

import pytest

from personal_assistant.cli import app
from personal_assistant.cli.registry import command_names
from personal_assistant.cli.suggest import suggest_command

pytestmark = pytest.mark.xfail(reason="T8 is not done yet", strict=True)


@pytest.mark.parametrize("typed, expected", [
    ("ad-note", "add-note"),
    ("birthday", "birthdays"),
    ("serch", "search"),
    ("NOTES", "notes"),
])
def test_closest_command_is_suggested(typed, expected):
    assert suggest_command(typed, command_names()) == expected


def test_nothing_close_gives_none():
    assert suggest_command("zzzz", command_names()) is None


def test_unknown_command_message_has_the_guess():
    assert "Did you mean 'add-note'?" in str(app.unknown_command("ad-note"))


def test_loop_prints_the_guess(state, capsys):
    app.handle("serch John", state)
    assert "Did you mean 'search'?" in capsys.readouterr().out
