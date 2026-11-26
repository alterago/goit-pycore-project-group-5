"""Commands for contacts."""

from personal_assistant.cli.base import AppState, Command, get_record, require_args
from personal_assistant.cli.output import contacts_table
from personal_assistant.contacts import Record

DEFAULT_BIRTHDAY_DAYS = 7


def add_contact(args: list[str], state: AppState):
    require_args(args, 2, "add <name> <phone>")
    name, phone = args[0], args[1]
    record = state.book.find(name)
    if record is None:
        record = Record(name)
        record.add_phone(phone)  # an invalid phone stops before the record is stored
        state.book.add_record(record)
        return "Contact added."
    record.add_phone(phone)
    return "Phone added."


def change_phone(args: list[str], state: AppState):
    require_args(args, 3, "change <name> <old phone> <new phone>")
    get_record(state.book, args[0]).edit_phone(args[1], args[2])
    return "Phone changed."


def remove_phone(args: list[str], state: AppState):
    require_args(args, 2, "remove-phone <name> <phone>")
    get_record(state.book, args[0]).remove_phone(args[1])
    return "Phone removed."


def show_contact(args: list[str], state: AppState):
    require_args(args, 1, "show <name>")
    return contacts_table([get_record(state.book, args[0])], title="Contact")


def show_all(args: list[str], state: AppState):
    if not state.book:
        return "No contacts saved."
    return contacts_table(state.book.values())


def set_birthday(args: list[str], state: AppState):
    require_args(args, 2, "add-birthday <name> <DD.MM.YYYY>")
    get_record(state.book, args[0]).set_birthday(args[1])
    return "Birthday saved."


def set_email(args: list[str], state: AppState):
    require_args(args, 2, "add-email <name> <email>")
    get_record(state.book, args[0]).set_email(args[1])
    return "E-mail saved."


def set_address(args: list[str], state: AppState):
    require_args(args, 2, "add-address <name> <address>")
    get_record(state.book, args[0]).set_address(" ".join(args[1:]))
    return "Address saved."


def search_contacts(args: list[str], state: AppState):
    require_args(args, 1, "search <text>")
    found = state.book.search(" ".join(args))
    return contacts_table(found, title="Found") if found else "Nothing found."


def delete_contact(args: list[str], state: AppState):
    require_args(args, 1, "delete <name>")
    state.book.delete(args[0])
    return "Contact deleted."


def birthdays(args: list[str], state: AppState):
    days = int(args[0]) if args and args[0].isdigit() else DEFAULT_BIRTHDAY_DAYS
    upcoming = state.book.upcoming_birthdays(days)
    if not upcoming:
        return f"No birthdays in the next {days} days."
    lines = [f"{day:%d.%m.%Y} ({day:%A}): {record.name}" for day, record in upcoming]
    return "\n".join(lines)


COMMANDS = [
    Command("add", add_contact, "add <name> <phone>", "add a contact or a phone to it"),
    Command("change", change_phone, "change <name> <old> <new>", "change a phone"),
    Command("remove-phone", remove_phone, "remove-phone <name> <phone>", "remove a phone"),
    Command("show", show_contact, "show <name>", "show one contact", changes_data=False),
    Command("all", show_all, "all", "show all contacts", changes_data=False),
    Command("add-birthday", set_birthday, "add-birthday <name> <DD.MM.YYYY>", "set a birthday"),
    Command("add-email", set_email, "add-email <name> <email>", "set an e-mail"),
    Command("add-address", set_address, "add-address <name> <address>", "set an address"),
    Command("search", search_contacts, "search <text>", "find contacts by any field",
            changes_data=False),
    Command("delete", delete_contact, "delete <name>", "delete a contact"),
    Command("birthdays", birthdays, "birthdays [days]",
            f"birthdays in the next days (default {DEFAULT_BIRTHDAY_DAYS})", changes_data=False),
]
