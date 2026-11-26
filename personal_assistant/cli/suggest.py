"""Guessing the command the user meant."""

from collections.abc import Iterable


def suggest_command(text: str, commands: Iterable[str]) -> str | None:
    """Return the command closest to ``text`` (for 'ad' or 'contcts' and so on), or None.

    TASK T8 — see TASKS.md. difflib.get_close_matches is a good start.
    """
    raise NotImplementedError("T8: guess the command")
