# app/models.py

from flask_login import UserMixin
from . import login_manager, get_db
import sqlite3

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    @staticmethod
    def get(user_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            return None
        return User(id=user[0], username=user[1], password_hash=user[2])

    @staticmethod
    def get_by_username(username):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if not user:
            return None
        return User(id=user[0], username=user[1], password_hash=user[2])

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
