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
