"""T1 — e-mail and address fields. Delete the `pytestmark` line when the task is done."""

import pytest

from personal_assistant.contacts import Record
from personal_assistant.fields import Address, Email

pytestmark = pytest.mark.xfail(reason="T1 is not done yet", strict=True)


def test_email_is_stored_stripped():
    assert Email(" john.doe+work@mail.example.com ").value == "john.doe+work@mail.example.com"


@pytest.mark.parametrize("bad", ["", "john", "john@", "@example.com", "john@example",
                                 "jo hn@example.com", "john@@example.com"])
def test_bad_email_is_rejected(bad):
    with pytest.raises(ValueError):
        Email(bad)


def test_address_is_stored_stripped():
    assert Address("  Kyiv, Khreshchatyk St 1 ").value == "Kyiv, Khreshchatyk St 1"


@pytest.mark.parametrize("bad", ["", "   ", "x" * 201])
def test_bad_address_is_rejected(bad):
    with pytest.raises(ValueError):
        Address(bad)


def test_record_shows_email_and_address():
    record = Record("John")
    record.set_email("john@example.com")
    record.set_address("Kyiv")
    assert str(record) == "John: no phones, email: john@example.com, address: Kyiv"
