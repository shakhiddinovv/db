import sqlite3

class DbConnect:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print("Ma'lumotlar bazasiga ulanildi!")
            return self.cursor
        except sqlite3.Error as error:
            print("Ulanishda xatolik yuz berdi:", error)

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.commit()
            self.connection.close()
            print("Ma'lumotlar bazasidan chiqildi!")

class Person:
    def __init__(self, full_name, age, email):
        self.full_name = full_name
        self.age = age
        self.email = email

    def save(self, cursor):
        try:
            cursor.execute("INSERT INTO person (full_name, age, email) VALUES (?, ?, ?)",
                           (self.full_name, self.age, self.email))
            print("Shaxs ma'lumotlari saqlandi!")
        except sqlite3.Error as error:
            print("Ma'lumotlarni saqlashda xatolik yuz berdi:", error)

    @staticmethod
    def get_person(cursor, person_id):
        try:
            cursor.execute("SELECT * FROM person WHERE id = ?", (person_id,))
            row = cursor.fetchone()
            if row:
                person = Person(row[1], row[2], row[3])
                person.id = row[0]
                return person
            else:
                print("Shaxs topilmadi!")
        except sqlite3.Error as error:
            print("Shaxs ma'lumotlarini olishda xatolik yuz berdi:", error)

with DbConnect('my_database.db') as cursor:
    cursor.execute('''CREATE TABLE IF NOT EXISTS person (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        full_name TEXT,
                        age INTEGER,
                        email TEXT)''')
    print("Jadval yaratildi!")

    person = Person("John Doe", 25, "john.doe@example.com")
    person.save(cursor)
    print("Shaxs ma'lumotlari saqlandi!")

    retrieved_person = Person.get_person(cursor, 1)
    if retrieved_person:
        print("Shaxs ma'lumotlari:")
        print("ID:", retrieved_person.id)
        print("Full Name:", retrieved_person.full_name)
        print("Age:", retrieved_person.age)
        print("Email:", retrieved_person.email)