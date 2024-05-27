import sys
import os

# 파이썬 시스템 실행경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from flask import Flask, jsonify, request
import sqlite3

from src.model.sw_major.sw_major_model import create_sw_major_notice, read_sw_major_notice_metadata, read_sw_major_notice_detail
from src.model.sw_7up.sw_7up_model import create_sw_7up_notice, read_sw_7up_notice, read_sw_7up_notice_detail
from src.model.user.user_model import create_user, read_user_by_username, read_user_by_email, login_user, logout_user

from src import constants

def create_app():
    app = Flask(__name__)
    # CORS(app)
    # CORS(app, resources={r"/api/*": {"origins": "*"}})

    # 데이터베이스 초기화와 데이터 추가
    init_db()

    create_sw_major_notice()
    create_sw_7up_notice()

    @app.route("/sw_major_notice")
    def get_sw_major_notice_metadata():
        sw_major_notice_metadata = read_sw_major_notice_metadata()

        # JSON 형태로 반환
        return jsonify(sw_major_notice_metadata)
    @app.route("/sw_major_notice/<noticeId>")
    def get_sw_major_notice_detail(noticeId):
        sw_major_notice_detail = read_sw_major_notice_detail(noticeId)

        # JSON 형태로 반환
        return jsonify(sw_major_notice_detail)

    @app.route("/sw_7up_notice")
    def get_sw_7up_notice():
        sw_7up_notice = read_sw_7up_notice()

        # JSON 형태로 반환
        return jsonify(sw_7up_notice)

    @app.route("/sw_7up_notice/<noticeId>")
    def get_sw_7up_detail(noticeId):
        sw_7up_notice_detail = read_sw_7up_notice_detail(noticeId)

        # JSON 형태로 반환
        return jsonify(sw_7up_notice_detail)

    @app.route("/register", methods=["POST"])
    def register(): #data.get ->
        data = request.json
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        print("정보", username, password, email)
        if read_user_by_username(username):
            return jsonify({"error": "Username already exists"}), 400
        if read_user_by_email(email):
            return jsonify({"error": "Email already exists"}), 400

        create_user(username, password, email)
        return jsonify({"message": "User created successfully"}), 201

    @app.route('/login', methods=['POST'])
    def login():
        if request.method == 'POST':
            data = request.json
            username = data.get("username")
            password = data.get("password")

            result_login = login_user(username, password)
            if result_login:
                return jsonify({"message": "login success"}), 201
            else:
                return jsonify({"error": "Invalid username or password"}), 401

    @app.route('/logout')
    def logout():
        result_logout = logout_user()
        if result_logout:
            return jsonify({"message": "logout success"}), 200


    return app

# 데이터베이스 초기화
def init_db():
    print("Connected to db")
    
    conn = sqlite3.connect(constants.database_path)
    cursor = conn.cursor()
    # 소웨 과페이지 테이블 생성
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sw_major_notice
        (notice_id INTEGER PRIMARY KEY, 
        category TEXT, 
        title TEXT, 
        created_at TEXT,
        body TEXT,
        image_urls TEXT,
        tables TEXT
        )
    """
    )
    conn.commit()
    
    # 소중사 과페이지 테이블 생성
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sw_7up_notice
        (notice_id TEXT PRIMARY KEY, 
        title TEXT, 
        body TEXT)
    """
    )
    conn.commit()

    # 북마크 테이블 생성
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS bookmark_notice
        (id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        notice_id INTEGER NOT NULL,
        notice_group TEXT NOT NULL)
    """
    )
    
    # 유저 테이블 생성
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
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
