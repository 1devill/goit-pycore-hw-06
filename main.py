
from collections import UserDict


class Field:
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    pass


class PhoneLengthException(ValueError):
    pass


class Phone(Field):
    def __init__(self, phone_num: str) -> None:
        if not isinstance(phone_num, str) or not phone_num.isdigit():
            raise ValueError("Phone number must contain only digits")

        if len(phone_num) != 10:
            raise PhoneLengthException(
                "Phone number must be exactly 10 digits long"
            )

        super().__init__(phone_num)


class Record:
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones: list[Phone] = []

    def __str__(self) -> str:
        phones = "; ".join(str(phone) for phone in self.phones)
        return f"Contact name: {self.name}, phones: {phones}"

    def add_phone(self, phone_num: str) -> None:
        phone = Phone(phone_num)

        if self.find_phone(phone_num) is not None:
            raise ValueError(f"Phone number {phone_num} already exists")

        self.phones.append(phone)

    def find_phone(self, phone_num: str) -> Phone | None:
        return next(
            (phone for phone in self.phones if phone.value == phone_num),
            None
        )

    def edit_phone(self, prev_phone_num: str, new_phone_num: str) -> None:
        if prev_phone_num == new_phone_num:
            raise ValueError(f"Phone numbers {prev_phone_num} and {new_phone_num} are identical")
        
        phone = self.find_phone(prev_phone_num)

        if phone is None:
            raise ValueError(f"Phone number {prev_phone_num} not found")

        if self.find_phone(new_phone_num) is not None:
            raise ValueError(f"Phone number {new_phone_num} already exists")

        new_phone = Phone(new_phone_num)
        self.phones[self.phones.index(phone)] = new_phone

    def remove_phone(self, phone_num: str) -> None:
        phone = self.find_phone(phone_num)

        if phone is None:
            raise ValueError(f"Phone number {phone_num} not found")

        self.phones.remove(phone)


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        name = record.name.value

        if name in self.data:
            raise ValueError(f"Contact {name} already exists")

        self.data[name] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name not in self.data:
            raise KeyError(f"Contact {name} not found")

        del self.data[name]


# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону в записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")
