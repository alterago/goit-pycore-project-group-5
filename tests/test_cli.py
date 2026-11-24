from personal_assistant.cli import app
from personal_assistant.cli.base import Command
from personal_assistant.cli.registry import COMMANDS, parse_input
from personal_assistant.storage import load_all


def run(line, state):
    name, args = parse_input(line)
    return COMMANDS[name].run(args, state)


def test_parse_input_lowercases_command_and_keeps_quoted_words():
    assert parse_input('ADD-Address John "Kyiv, Main St 1"') == (
        "add-address", ["John", "Kyiv, Main St 1"])
    assert parse_input("add-note п'ять хвилин") == ("add-note", ["п'ять", "хвилин"])
    assert parse_input("   ") == ("", [])


def test_add_creates_a_contact_then_adds_phones(state):
    assert run("add Bob 0501112233", state) == "Contact added."
    assert run("add bob 0504445566", state) == "Phone added."
    assert [p.value for p in state.book["Bob"].phones] == ["0501112233", "0504445566"]


def test_invalid_phone_does_not_create_a_contact(state):
    result = run("add Bob 123", state)
    assert "10 digits" in str(result)
    assert state.book.find("Bob") is None


def test_errors_become_messages(state):
    assert str(run("add", state)) == "Usage: add <name> <phone>"
    assert str(run("change Nobody 0501234567 0501234568", state)) == "Not found: contact Nobody."
    assert "Note id must be a number" in str(run("delete-note abc", state))


def test_unfinished_task_is_reported_not_crashed(state):
    def unfinished(args, state):
        raise NotImplementedError("T0: example")

    command = Command("demo", unfinished, "demo", "demo")
    assert str(command.run([], state)) == "Not implemented yet (T0: example)."


def test_handle_saves_changes_and_stops_on_exit(state):
    assert app.handle("add-note call the mentor", state) is True
    _, notes = load_all()
    assert notes.get_note(1).text == "call the mentor"
    assert app.handle("exit", state) is False
    assert app.handle("close", state) is False


def test_unknown_command_gives_a_hint():
    assert "Type 'help'" in str(app.unknown_command("zzzz"))
