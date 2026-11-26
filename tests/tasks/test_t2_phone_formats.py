"""T2 — phone written in common formats. Delete the `pytestmark` line when the task is done."""

import pytest

from personal_assistant.fields import Phone, normalize_phone

pytestmark = pytest.mark.xfail(reason="T2 is not done yet", strict=True)


@pytest.mark.parametrize("raw", ["+38 (050) 123-45-67", "+380501234567", "380501234567",
                                 "050-123-45-67", "(050) 123 45 67", "0501234567"])
def test_formats_become_ten_digits(raw):
    assert normalize_phone(raw) == "0501234567"


def test_phone_keeps_the_normalized_value():
    assert Phone("+38 (050) 123-45-67").value == "0501234567"


# Command level: what the user sees.

def test_cmd_add_formatted_phone(cli, state):
    assert cli('add Bob "+38 (050) 111-22-33"') == "Contact added."
    assert [p.value for p in state.book["Bob"].phones] == ["0501112233"]


def test_cmd_change_to_formatted_phone(cli, state):
    assert cli('change John 0501234567 "067 999 88 77"') == "Phone changed."
    assert [p.value for p in state.book["John"].phones] == ["0679998877"]


def test_cmd_same_phone_in_another_format_is_a_duplicate(cli, state):
    assert "already exists" in cli('add John "+38 050 123 45 67"')
    assert [p.value for p in state.book["John"].phones] == ["0501234567"]
