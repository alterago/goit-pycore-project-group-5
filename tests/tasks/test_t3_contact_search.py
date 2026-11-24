"""T3 — contact search. Delete the `pytestmark` line when the task is done."""

import pytest

pytestmark = pytest.mark.xfail(reason="T3 is not done yet", strict=True)


def names(records):
    return [r.name.value for r in records]


def test_search_by_part_of_name_ignores_case(book):
    assert names(book.search("JO")) == ["John"]
    assert names(book.search("j")) == ["John", "Jane"]


def test_search_by_part_of_phone(book):
    assert names(book.search("0679")) == ["Jane"]


def test_nothing_found_gives_empty_list(book):
    assert book.search("zzz") == []
