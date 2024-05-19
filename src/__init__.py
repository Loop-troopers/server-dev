from flask import Flask, jsonify, make_response
from flask_cors import CORS
import sqlite3
from src.model.sw_major.sw_major_model import create_sw_major_notice, read_sw_major_notice_metadata, read_sw_major_notice_detail
from src.model.sw_7up.sw_7up_model import create_sw_7up_notice, read_sw_7up_notice
import asyncio


def create_app():
    app = Flask(__name__)
    # CORS(app)
    # CORS(app, resources={r"/api/*": {"origins": "*"}})

    # 데이터베이스 초기화와 데이터 추가
    init_db()

    return app

# 데이터베이스 초기화
def init_db():
    print("Connected to db")
    conn = sqlite3.connect("../db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sw_major_notice
        (notice_id INTEGER PRIMARY KEY, 
        category TEXT, 
        title TEXT, 
        created_at TEXT,
        body TEXT,
        other_elements TEXT)
    """
    )
    conn.commit()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sw_7up_notice
        (notice_id TEXT PRIMARY KEY, 
        title TEXT, 
        body TEXT)
    """
    )
    conn.commit()

    conn.close()


def main():
    app = create_app()

    # Flask 앱 실행
    app.run("0.0.0.0")


if __name__ == "__main__":
    main()
