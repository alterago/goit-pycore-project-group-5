"""T2 — contact search. Delete the `pytestmark` line when the task is done.

ТЗ: «Здійснювати пошук контактів серед контактів книги»;
«Пошук контактів за різними критеріями (наприклад, за іменем)».
"""

import pytest

from personal_assistant.fields import Field

pytestmark = pytest.mark.xfail(reason="T2 is not done yet", strict=True)


def names(records):
    return [r.name.value for r in records]


def test_search_by_part_of_name_ignores_case(book):
    assert names(book.search("JO")) == ["John"]
    assert names(book.search("j")) == ["John", "Jane"]


def test_search_by_part_of_phone(book):
    assert names(book.search("0679")) == ["Jane"]


def test_search_by_email_and_address(book):
    book["Jane"].email = Field("jane@mail.example")
    book["John"].address = Field("Kyiv, Main St 1")
    assert names(book.search("MAIL.EXAMPLE")) == ["Jane"]
    assert names(book.search("kyiv")) == ["John"]


def test_nothing_found_gives_empty_list(book):
    assert book.search("zzz") == []


# Command level: what the user sees.

def test_cmd_search_shows_only_matches(cli):
    output = cli("search jo")
    assert "John" in output and "Jane" not in output


def test_cmd_search_words_with_spaces(cli, book):
    book["John"].address = Field("Kyiv, Main St 1")
    assert "John" in cli('search "main st"')


def test_cmd_search_nothing_found(cli):
    assert cli("search zzz") == "Nothing found."
