"""Contact fields. Each field checks its value when it is created."""

from datetime import date, datetime

PHONE_LENGTH = 10
DATE_FORMAT = "%d.%m.%Y"


class Field:
    """Base class: a value with equality and a text form."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return type(self) is type(other) and self.value == other.value

    def __hash__(self):
        return hash((type(self), self.value))


class Name(Field):
    """Contact name, a required field."""

    def __init__(self, value: str):
        value = (value or "").strip()
        if not value:
            raise ValueError("Name is required.")
        super().__init__(value)


def normalize_phone(value: str) -> str:
    """Bring a phone written as '+38 (050) 123-45-67' to '0501234567'.

    TASK T2 — see TASKS.md.
    """
    raise NotImplementedError("T2: phone normalization")


class Phone(Field):
    """Phone number of exactly 10 digits."""

    def __init__(self, value: str):
        # T2: normalize the value with normalize_phone() before the check.
        if not (len(value) == PHONE_LENGTH and value.isdigit()):
            raise ValueError(f"Phone must contain exactly {PHONE_LENGTH} digits.")
        super().__init__(value)


class Birthday(Field):
    """Birthday given as DD.MM.YYYY and stored as a date."""

    def __init__(self, value: str):
        try:
            birthday = datetime.strptime(value, DATE_FORMAT).date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") from None
        if birthday > date.today():
            raise ValueError("Birthday cannot be in the future.")
        super().__init__(birthday)

    def __str__(self):
        return self.value.strftime(DATE_FORMAT)


class Email(Field):
    """E-mail address such as 'name@example.com'.

    TASK T1 — see TASKS.md.
    """

    def __init__(self, value: str):
        raise NotImplementedError("T1: e-mail validation")


class Address(Field):
    """Postal address: free text, not empty, at most 200 characters.

    TASK T1 — see TASKS.md.
    """

    def __init__(self, value: str):
        raise NotImplementedError("T1: address validation")
