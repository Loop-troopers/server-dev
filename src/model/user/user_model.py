import sqlite3
import asyncio
from src import constants
from flask import session

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
    print("user: ", username, password)
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