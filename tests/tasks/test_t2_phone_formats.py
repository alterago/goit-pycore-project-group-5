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
