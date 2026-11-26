"""T5 — birthdays in the next N days. Delete the `pytestmark` line when the task is done."""

from datetime import date

import pytest

from personal_assistant.contacts import AddressBook, Record

pytestmark = pytest.mark.xfail(reason="T5 is not done yet", strict=True)


def make_book(*items):
    book = AddressBook()
    for name, birthday in items:
        record = Record(name)
        record.set_birthday(birthday)
        book.add_record(record)
    return book


def result(upcoming):
    return [(day, record.name.value) for day, record in upcoming]


def test_range_includes_today_and_the_last_day():
    book = make_book(("Ann", "08.03.1990"), ("Bob", "15.03.1985"), ("Cid", "16.03.2000"))
    assert result(book.upcoming_birthdays(7, today=date(2026, 3, 8))) == [
        (date(2026, 3, 8), "Ann"), (date(2026, 3, 15), "Bob")]


def test_sorted_by_date_across_new_year():
    book = make_book(("Late", "02.01.1990"), ("Early", "30.12.1990"))
    assert result(book.upcoming_birthdays(7, today=date(2026, 12, 28))) == [
        (date(2026, 12, 30), "Early"), (date(2027, 1, 2), "Late")]


def test_contacts_without_birthday_are_skipped(book):
    assert result(book.upcoming_birthdays(30, today=date(2026, 3, 1))) == [
        (date(2026, 3, 15), "John")]


def test_negative_days_are_rejected(book):
    with pytest.raises(ValueError):
        book.upcoming_birthdays(-1)


# Command level: what the user sees. The dates are counted from the real today.

def in_days(days):
    from datetime import timedelta
    day = date.today() + timedelta(days=days)
    return day.replace(year=day.year - 28).strftime("%d.%m.%Y")  # 28 years: leap stays leap


def test_cmd_birthdays_lists_within_days(cli, state):
    state.book["Jane"].set_birthday(in_days(3))
    state.book["John"].set_birthday(in_days(20))
    output = cli("birthdays 7")
    assert "Jane" in output and "John" not in output


def test_cmd_birthdays_default_is_seven_days(cli, state):
    state.book["Jane"].set_birthday(in_days(7))
    assert "Jane" in cli("birthdays")


def test_cmd_birthdays_none_in_range(cli, state):
    state.book["John"].set_birthday(in_days(20))
    assert cli("birthdays 2") == "No birthdays in the next 2 days."
