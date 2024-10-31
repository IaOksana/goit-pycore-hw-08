import re, pickle
from address_book import *

'''decorator'''
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            return (f"Error {e}.")

        except IndexError as e:
            return (f"Error {e}.")

        except ValueError as e:
            return (f"Error {e}.")

    return inner


def save_data(book, filename : str = "addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename : str = "addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

'''
розбиратиме введений користувачем рядок на команду та її аргументи. 
Команди та аргументи мають бути розпізнані незалежно від регістру введення.
'''
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args : list[str], book : AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Please enter name and phone")
    
    name, phone = args
    record = book.find(name)

    if isinstance(record, Record):
        record.add_phone(phone)
        return "Contact updated."
    else:
        new_record = Record(name)
        new_record.add_phone(phone)
        book.add_record(new_record)
    
    return "Contact added."


@input_error
def add_phone(args : list[str], book : AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Please enter name and phone (10 digits). ")
    
    name, phone = args
    record = book.find(name)

    if isinstance(record, Record):
        record.add_phone(phone)
        return "Phone added."
    
    return "Name or phone is incorrect."    


@input_error
def add_birthday(args : list[str], book : AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Please enter name and birthday (DD.MM.YYYY). ")
    
    name, birthday = args
    record = book.find(name)

    if isinstance(record, Record):
        record.add_birthday(birthday)
        return "Birthday added."
    
    return "Name or date is incorrect."


@input_error
def change_contact(args : list[str], book : AddressBook) -> str:
    if len(args) < 2:
        raise ValueError("Please give name and phone")
    
    name, phone = args
    record = book.find(name)
    
    if isinstance(record, Record):
        # Change the first phone if available
        if record.phones:
            record.edit_phone(record.phones[0].value, phone)
            return "Contact updated"
        else:
            record.add_phone(phone)
            return "Phone added"
    else:
        add_contact(args, book)
        raise KeyError("contact was not existed")


@input_error    
def show_phone(args : list[str], book : AddressBook) -> str:
    if len(args) < 1:
        raise IndexError("Please give name")
    
    record = book.find(args[0])
    
    if isinstance(record, Record):
        return f"{record.name.value} phones:{'; '.join(p.value for p in record.phones)}"
    else:
        raise KeyError("Please give existing name")


@input_error    
def show_birthday(args : list[str], book : AddressBook) -> str:
    if len(args) < 1:
        raise IndexError("Please give name")
    
    record = book.find(args[0])
    
    if isinstance(record, Record):
        birthday = datetime.strftime(record.birthday.birthday, "%d.%m.%Y") if record.birthday != None else "No info"
        return f"{record.name.value} birthday:{birthday}"
    else:
        raise KeyError("Please give existing name")


@input_error
def get_upcoming_birthdays(book : AddressBook) -> AddressBook:
    congrat_book = book.get_upcoming_birthdays()
    if congrat_book:
        return congrat_book
    else:
        return ("Nobody to congrat")
    

def main() :

    # словник Python для зберігання імен і номерів телефонів. Ім'я буде ключем, а номер телефону – значенням.
    #book = AddressBook()

    book = load_data()
    
    print("Welcome to the assistant bot!")

    while True:
        user_input  = input("Enter a command: ").strip().lower()
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        #  За цією командою бот зберігає у пам'яті, наприклад у словнику, новий контакт. 
        elif command == "add":
            print(add_contact(args, book))
 
        #За цією командою бот виводить всі збереженні контакти з номерами телефонів у консоль
        elif command == "all":
            if book:
                for record in book.data:
                    print(f"{book.data[record]}") 
            else: 
                print("No contacts")

        # За цією командою бот виводить у консоль номер телефону для зазначеного контакту username
        elif command == "phone":
            print(show_phone(args, book))

        # За цією командою бот зберігає в пам'яті новий номер телефону phone для контакту username, що вже існує в записнику.
        elif command == "change":
            print(change_contact(args, book))

        elif command == "add-phone":
            print(add_phone(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))
        
        elif command == "birthdays":
            congrat_list = (get_upcoming_birthdays(book))
            for record in congrat_list.data:
                user = congrat_list.data[record]
                print(user) 

        else:
            print("Invalid command.")
    
    save_data(book)

if __name__ == "__main__":
    main()