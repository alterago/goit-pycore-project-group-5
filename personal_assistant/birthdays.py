"""Date helpers for birthdays."""

from datetime import date


def birthday_in_year(birthday: date, year: int) -> date:
    """Return the birthday in ``year``; 29 February becomes 28 February in a common year."""
    try:
        return birthday.replace(year=year)
    except ValueError:
        return birthday.replace(year=year, day=28)


def next_birthday(birthday: date, today: date) -> date:
    """Return the nearest birthday that is today or later."""
    this_year = birthday_in_year(birthday, today.year)
    if this_year >= today:
        return this_year
    return birthday_in_year(birthday, today.year + 1)
