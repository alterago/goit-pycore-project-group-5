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


# Command level: what the user sees.

def test_cmd_add_email_shows_in_contact(cli):
    assert cli("add-email John john@example.com") == "E-mail saved."
    assert "john@example.com" in cli("show John")


def test_cmd_bad_email_is_reported_and_not_saved(cli, state):
    assert cli("add-email John john@").startswith("Invalid e-mail")
    assert state.book["John"].email is None


def test_cmd_add_address_with_and_without_quotes(cli, state):
    assert cli('add-address John "Kyiv, Main St 1"') == "Address saved."
    assert state.book["John"].address.value == "Kyiv, Main St 1"
    cli("add-address Jane Lviv Market Sq 5")
    assert state.book["Jane"].address.value == "Lviv Market Sq 5"


def test_email_and_address_survive_restart(cli, reload):
    cli("add-email John john@example.com")
    cli("add-address John Kyiv")
    john = reload().book["John"]
    assert (john.email.value, john.address.value) == ("john@example.com", "Kyiv")
