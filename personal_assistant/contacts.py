"""Contacts: a record of one person and the address book of records."""

from collections import UserDict
from datetime import date

from personal_assistant.fields import Address, Birthday, Email, Name, Phone


class Record:
    """One contact: a name, phones and optional birthday, e-mail and address."""

    # Class-level defaults keep books saved by older versions loadable.
    birthday = None
    email = None
    address = None

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []

    def add_phone(self, phone: str) -> None:
        new_phone = Phone(phone)
        if new_phone in self.phones:
            raise ValueError(f"Phone {new_phone} already exists for {self.name}.")
        self.phones.append(new_phone)

    def remove_phone(self, phone: str) -> None:
        self.phones.remove(self._existing_phone(phone))

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        found = self._existing_phone(old_phone)
        replacement = Phone(new_phone)  # validate before replacing
        if replacement != found and replacement in self.phones:
            raise ValueError(f"Phone {replacement} already exists for {self.name}.")
        self.phones[self.phones.index(found)] = replacement

    def find_phone(self, phone: str) -> Phone | None:
        return next((p for p in self.phones if p.value == phone), None)

    def set_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def set_email(self, email: str) -> None:
        self.email = Email(email)

    def set_address(self, address: str) -> None:
        self.address = Address(address)

    def _existing_phone(self, phone: str) -> Phone:
        found = self.find_phone(phone)
        if found is None:
            raise ValueError(f"Phone {phone} not found for {self.name}.")
        return found

    def __str__(self):
        phones = "; ".join(str(p) for p in self.phones) or "no phones"
        parts = [f"{self.name}: {phones}"]
        for label, field in (("birthday", self.birthday), ("email", self.email),
                             ("address", self.address)):
            if field is not None:
                parts.append(f"{label}: {field}")
        return ", ".join(parts)


class AddressBook(UserDict):
    """Records by name. Names are unique regardless of letter case."""

    def add_record(self, record: Record) -> None:
        existing = self.find(record.name.value)
        if existing is not None and existing is not record:
            raise ValueError(f"Contact {record.name} already exists.")
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        """Return the record by name; the letter case does not matter."""
        if name in self.data:
            return self.data[name]
        lowered = name.lower()
        return next((r for n, r in self.data.items() if n.lower() == lowered), None)

    def delete(self, name: str) -> None:
        """Delete the contact; raise KeyError when there is no such contact.

        TASK T4 — see TASKS.md.
        """
        raise NotImplementedError("T4: delete a contact")

    def rename(self, old_name: str, new_name: str) -> Record:
        """Give the contact a new name and return its record.

        TASK T4 — see TASKS.md.
        """
        raise NotImplementedError("T4: rename a contact")

    def search(self, query: str) -> list[Record]:
        """Return contacts whose name, phone, e-mail or address contains ``query``.

        TASK T3 — see TASKS.md.
        """
        raise NotImplementedError("T3: contact search")

    def upcoming_birthdays(self, days: int, today: date | None = None) -> list[tuple[date, Record]]:
        """Return (birthday date, record) for birthdays from today to today + ``days``.

        TASK T5 — see TASKS.md. Use birthdays.next_birthday().
        """
        raise NotImplementedError("T5: upcoming birthdays")
