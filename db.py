import sqlite3
import time

db = sqlite3.connect('database.db')


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()


    def add_user(self, user_id, referrer_id=None):
        with self.connection:
            if referrer_id != None:
                pass
            else:
                return self.cursor.execute("INSERT INTO users (user_id, referrer_id) VALUES (?, ?)", (user_id, referrer_id,))

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchall()
            return bool(len(result))

    def set_nickname(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute("UPDATE users SET nickname=? WHERE user_id=?", (nickname, user_id,))

    def get_signup(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT signup FROM users WHERE user_id=?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def set_signup(self, user_id, signup):
        with self.connection:
            return self.cursor.execute("UPDATE users SET signup=? WHERE user_id=?", (signup, user_id,))


    def get_nickname(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT nickname FROM users WHERE user_id=?", (user_id,)).fetchall()
            for row in result:
                nickname = str(row[0])
            return nickname

    def set_time_sub(self, user_id, time_sub):
        with self.connection:
            current_time_sub = self.get_time_sub(user_id)
            if current_time_sub is None:
                current_time_sub = int(time.time())
            new_time_sub = int(current_time_sub) + time_sub
            return self.cursor.execute("UPDATE users SET time_sub=? WHERE user_id=?", (new_time_sub, user_id,))

    def get_time_sub(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT time_sub FROM users WHERE user_id=?", (user_id,)).fetchall()
            for row in result:
                time_sub = int(row[0])
            return time_sub

    def get_sub_status(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT time_sub FROM users WHERE user_id=?", (user_id,)).fetchall()
            for row in result:
                time_sub = int(row[0])
            if time_sub > int(time.time()):
                return True
            else:
                return False

    def get_count_refers(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT referal_count FROM users WHERE user_id=?", (user_id,)).fetchall()
            for row in result:
                count_refers = int(row[0])
            return count_refers



    def set_count_refers(self, user_id):
        with self.connection:
            current_count = self.get_count_refers(user_id)
            new_count = int(current_count) + 1
            return self.cursor.execute("UPDATE users SET referal_count=? WHERE user_id=?", (new_count, user_id,))



    def get_user_wallet(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT user_wallet FROM users WHERE user_id=?", (user_id,)).fetchall()
            for row in result:
                wallet = str(row[0])
            return wallet

    def set_user_wallet_make(self, user_id, county):
        with self.connection:
            current_wallet = self.get_user_wallet(user_id)
            new_current_wallet = float(current_wallet) + county
            return self.cursor.execute("UPDATE users SET user_wallet=? WHERE user_id=?", (new_current_wallet, user_id,))

    def set_user_wallet_take(self, user_id, county):
        with self.connection:
            current_wallet = self.get_user_wallet(user_id)
            new_current_wallet = float(current_wallet) - county
            return self.cursor.execute("UPDATE users SET user_wallet=? WHERE user_id=?", (new_current_wallet, user_id,))