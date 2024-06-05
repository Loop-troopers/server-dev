import sqlite3
import asyncio
from src import constants
from flask import session, jsonify
# 로그인 확인 데코레이터 함수 추가
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Login required"}), 401
        return f(*args, **kwargs)
    return decorated_function

def create_user(username, password, email):
    conn = sqlite3.connect(constants.database_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user (username, password, email) VALUES (?, ?, ?)",
        (username, password, email)
    )
    conn.commit()
    conn.close()

def read_user_by_username(username):
    conn = sqlite3.connect(constants.database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def read_user_by_email(email):
    conn = sqlite3.connect(constants.database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def login_user(username, password):
    conn = sqlite3.connect(constants.database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    if user is None:
        return False
    else:
        session['user_id'] = user[0]
        session['username'] = user[1]
        print('session', session)
        return True

def logout_user():
    session.pop('user_id', None)
    session.pop('username', None)
    return True

def check_password(username, password):
    conn = sqlite3.connect(constants.database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def update_user_password(username, new_password):
    conn = sqlite3.connect(constants.database_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE user SET password = ? WHERE username = ?", (new_password, username))
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated

