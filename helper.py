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