from db import connect_db
from decimal import Decimal



class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def register(username, password):
        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users WHERE username=%s", (username,))
                if cur.fetchone():
                    return None
                cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                conn.commit()
                return User(username, password)

    @staticmethod
    def login(username, password):
        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
                user = cur.fetchone()
                return User(username, password) if user else None

    def get_id(self):
        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM users WHERE username=%s", (self.username,))
                return cur.fetchone()[0]

class Loan:
    def __init__(self, user_id):
        self.user_id = user_id

    def apply(self, amount):
        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO loans (user_id, amount, balance) VALUES (%s, %s, %s)",
                            (self.user_id, amount, amount))
                conn.commit()

    def pay(self, payment):
        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, balance, payments FROM loans WHERE user_id=%s ORDER BY id DESC LIMIT 1",
                            (self.user_id,))
                loan = cur.fetchone()
                if loan:
                    loan_id, balance, payments = loan
                    new_balance = max(balance - Decimal(str(payment)), Decimal('0'))
                    updated_payments = payments + f"{payment},"
                    cur.execute("UPDATE loans SET balance=%s, payments=%s WHERE id=%s",
                                (new_balance, updated_payments, loan_id))
                    conn.commit()

    def check_balance(self):
        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT balance FROM loans WHERE user_id=%s ORDER BY id DESC LIMIT 1",
                            (self.user_id,))
                result = cur.fetchone()
                return result[0] if result else None

    def view_payments(self):
        with connect_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT payments FROM loans WHERE user_id=%s ORDER BY id DESC LIMIT 1",
                            (self.user_id,))
                result = cur.fetchone()
                return result[0].strip(',').split(',') if result and result[0] else []
