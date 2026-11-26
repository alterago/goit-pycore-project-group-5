"""T3 — delete a contact. Delete the `pytestmark` line when the task is done.

ТЗ: «Редагувати та видаляти записи з книги контактів»; «Редагування та видалення контактів».
Editing is already there: change, add-birthday, add-email, add-address.
"""

import pytest

pytestmark = pytest.mark.xfail(reason="T3 is not done yet", strict=True)


def test_delete_ignores_letter_case(book):
    book.delete("john")
    assert book.find("John") is None
    assert len(book) == 1


def test_delete_unknown_contact_raises_key_error(book):
    with pytest.raises(KeyError):
        book.delete("Nobody")


# Command level: what the user sees.

def test_cmd_delete(cli):
    assert cli("delete john") == "Contact deleted."
    assert "John" not in cli("all")


def test_cmd_delete_unknown(cli):
    assert cli("delete Nobody") == "Not found: contact Nobody."


def test_delete_survives_restart(cli, reload):
    cli("delete Jane")
    assert list(reload().book) == ["John"]
