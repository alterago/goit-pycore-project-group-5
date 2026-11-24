from datetime import date

import pytest

from personal_assistant.birthdays import next_birthday
from personal_assistant.contacts import Record


def test_find_ignores_letter_case(book):
    assert book.find("john") is book["John"]
    assert book.find("nobody") is None


def test_same_name_in_another_case_is_rejected(book):
    with pytest.raises(ValueError):
        book.add_record(Record("JOHN"))


def test_phones_are_added_edited_and_removed():
    record = Record("Ann")
    record.add_phone("0501234567")
    record.add_phone("0679876543")
    with pytest.raises(ValueError):
        record.add_phone("0501234567")  # duplicate

    record.edit_phone("0501234567", "0931112233")
    assert [p.value for p in record.phones] == ["0931112233", "0679876543"]

    record.remove_phone("0679876543")
    assert [p.value for p in record.phones] == ["0931112233"]
    with pytest.raises(ValueError):
        record.remove_phone("0000000000")


def test_invalid_new_phone_keeps_the_old_one():
    record = Record("Ann")
    record.add_phone("0501234567")
    with pytest.raises(ValueError):
        record.edit_phone("0501234567", "123")
    assert [p.value for p in record.phones] == ["0501234567"]


def test_record_text_lists_the_fields_it_has(book):
    assert str(book["John"]) == "John: 0501234567, birthday: 15.03.1990"
    assert str(Record("Empty")) == "Empty: no phones"


@pytest.mark.parametrize(
    "birthday, today, expected",
    [
        (date(1990, 3, 15), date(2026, 3, 10), date(2026, 3, 15)),
        (date(1990, 3, 15), date(2026, 3, 15), date(2026, 3, 15)),
        (date(1990, 3, 15), date(2026, 3, 16), date(2027, 3, 15)),
        (date(2000, 2, 29), date(2027, 1, 1), date(2027, 2, 28)),
    ],
)
def test_next_birthday(birthday, today, expected):
    assert next_birthday(birthday, today) == expected
