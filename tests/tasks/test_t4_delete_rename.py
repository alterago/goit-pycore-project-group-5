"""T4 — delete and rename contacts. Delete the `pytestmark` line when the task is done."""

import pytest

pytestmark = pytest.mark.xfail(reason="T4 is not done yet", strict=True)


def test_delete_ignores_letter_case(book):
    book.delete("john")
    assert book.find("John") is None
    assert len(book) == 1


def test_delete_unknown_contact_raises_key_error(book):
    with pytest.raises(KeyError):
        book.delete("Nobody")


def test_rename_keeps_the_data(book):
    record = book.rename("John", "Johnny")
    assert book.find("John") is None
    assert book.find("Johnny") is record
    assert [p.value for p in record.phones] == ["0501234567"]


def test_rename_to_existing_name_is_rejected(book):
    with pytest.raises(ValueError):
        book.rename("John", "jane")
    assert book.find("John") is not None


def test_rename_unknown_contact_raises_key_error(book):
    with pytest.raises(KeyError):
        book.rename("Nobody", "Somebody")


# Command level: what the user sees.

def test_cmd_delete(cli):
    assert cli("delete john") == "Contact deleted."
    assert "John" not in cli("all")


def test_cmd_delete_unknown(cli):
    assert cli("delete Nobody").startswith("Not found")


def test_cmd_rename(cli):
    assert cli("rename John Johnny") == "Contact renamed."
    assert "0501234567" in cli("show Johnny")


def test_cmd_rename_to_existing_name(cli, state):
    assert cli("rename John Jane") == "Contact Jane already exists."
    assert state.book.find("John") is not None


def test_delete_and_rename_survive_restart(cli, reload):
    cli("delete Jane")
    cli("rename John Johnny")
    assert list(reload().book) == ["Johnny"]
