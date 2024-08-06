import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('bot_users.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                full_name TEXT,
                phone_number TEXT
            )
        ''')
        self.conn.commit()

    def add_user(self, user_id, full_name, phone_number):
        self.cursor.execute('''
            INSERT INTO users (user_id, full_name, phone_number)
            VALUES (?, ?, ?)
        ''', (user_id, full_name, phone_number))
        self.conn.commit()

    def get_user(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return self.cursor.fetchone()
    

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()



    def get_all_chat_ids(self):


    # SQL query to get all chat_ids from the users table
        self.cursor.execute("SELECT user_id FROM users")

    # Fetch all results and extract chat_ids
        chat_ids = [row[0] for row in self.cursor.fetchall()]


        return chat_ids


    def close(self):
        self.connection.close()
