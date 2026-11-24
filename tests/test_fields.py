from datetime import date

import pytest

from personal_assistant.fields import Birthday, Name, Phone


def test_name_is_stripped_and_required():
    assert Name("  John ").value == "John"
    for bad in ["", "   ", None]:
        with pytest.raises(ValueError):
            Name(bad)


def test_phone_needs_exactly_ten_digits():
    assert Phone("0501234567").value == "0501234567"
    for bad in ["123", "05012345678", "05012abcde", ""]:
        with pytest.raises(ValueError):
            Phone(bad)


def test_birthday_is_parsed_and_printed():
    birthday = Birthday("30.10.1990")
    assert birthday.value == date(1990, 10, 30)
    assert str(birthday) == "30.10.1990"


def test_birthday_rejects_bad_format_and_future():
    for bad in ["1990-10-30", "31.02.1990", "30/10/1990", "", "01.01.2999"]:
        with pytest.raises(ValueError):
            Birthday(bad)


def test_fields_compare_by_type_and_value():
    assert Phone("0501234567") == Phone("0501234567")
    assert Phone("0501234567") != Phone("0679876543")
    assert Name("0501234567") != Phone("0501234567")
