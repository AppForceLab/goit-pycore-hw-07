import re
from datetime import datetime, timedelta
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not Phone.validate_phone(value):
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)

    @staticmethod
    def validate_phone(phone):
        pattern = re.compile(r"^\d{10}$")
        return pattern.match(phone) is not None

class Birthday(Field):
    def __init__(self, value):
        if not self.validate_date(value):
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(datetime.strptime(value, "%d.%m.%Y"))

    @staticmethod
    def validate_date(date_text):
        try:
            datetime.strptime(date_text, "%d.%m.%Y")
            return True
        except ValueError:
            return False

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        return next((p for p in self.phones if p.value == phone), None)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = '; '.join(str(p) for p in self.phones)
        birthday_str = f", Birthday: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, days=7):
        today = datetime.today()
        upcoming = today + timedelta(days=days)
        birthdays_next_week = []
        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)
                if today <= birthday_this_year < upcoming:
                    birthdays_next_week.append(record.name.value)
        return birthdays_next_week

# Usage example:
book = AddressBook()
rec1 = Record("Alice")
rec1.add_phone("1234567890")
rec1.add_birthday("01.08.1990")
book.add_record(rec1)

rec2 = Record("Bob")
rec2.add_phone("0987654321")
rec2.add_birthday("05.08.1990")
book.add_record(rec2)

print(book.get_upcoming_birthdays()) 
