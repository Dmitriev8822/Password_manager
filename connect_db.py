import sqlite3 as sq


symbols_frbt = r'&=+<>,-. '


class Сonnect_DB_users():
    def __init__(self):
        with sq.connect('data/db/users.db') as self.con:
            self.cur = self.con.cursor()

            # self.cur.execute("DROP TABLE IF EXISTS users")
            self.cur.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER NOT NULL PRIMARY KEY,
                    login TEXT NOT NULL,
                    password TEXT NOT NULL
                    )   
                """)

            self.con.commit()

    def db_close(self):
        self.con.close() # break connection wist database
        return 0

    def new_user(self, login, password):
        if not 5 < len(password) < 31:
            return 6 # length password must be between 6 <= x <= 30

        for el in login:
            if el in symbols_frbt:
                return 3  # forbidden character in the login

        for el in password:
            if el in symbols_frbt:
                return 4  # forbidden character in the password

        result = self.cur.execute(f"SELECT login FROM users")
        result = result.fetchall()

        for log in result:
            if login == log[0]:
                return 1  # user already exists

        self.cur.execute(f" INSERT INTO users (login, password)  VALUES (?, ?)", (login, password))
        self.con.commit()

        return 0  # all ok

    def check_user(self, login, password):
        result = self.cur.execute(f"SELECT * FROM users")
        result = result.fetchall()

        for user_data in result:
            if login == user_data[1]:
                if password == user_data[2]:
                    return 0
                else:
                    return 2 # incorrect password

        return 1


class Сonnect_DB_data():
    def __init__(self):
        with sq.connect('data/db/users.db') as self.con:
            self.cur = self.con.cursor()

            self.cur.execute("DROP TABLE IF EXISTS data")
            self.cur.execute("""CREATE TABLE IF NOT EXISTS data (
                    id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    login TEXT NOT NULL,
                    password TEXT NOT NULL
                    )   
                """)

            self.con.commit()

    def new_entry(self, id, title, login, password):
        result = self.cur.execute(f"SELECT login FROM users")
        result = result.fetchall()

        for log in result:
            if login == log[0]:
                return 1  # user already exists

        self.cur.execute(f" INSERT INTO users (login, password)  VALUES (?, ?)", (login, password))
        self.con.commit()

        return 0  # all ok