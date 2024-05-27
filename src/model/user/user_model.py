import sqlite3
import asyncio
from src import constants

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
