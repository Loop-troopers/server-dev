import sys
import os

# 파이썬 시스템 실행경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from flask import Flask, jsonify, request, session
import sqlite3

from src.model.notice.notice_model import create_sw_major_notice, create_sw_7up_notice, read_notice_metadata, read_notice_detail
from src.model.user.user_model import create_user, read_user_by_username, read_user_by_email, login_user, logout_user,check_password, update_user_password, login_required
from src.model.bookmark.bookmark_model import create_bookmark, read_user_bookmarks, delete_bookmarks

from src import constants

def create_app():
    app = Flask(__name__)
    # CORS(app)
    # CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.secret_key = 'supersecretkey'

    # 데이터베이스 초기화와 데이터 추가
    init_db()

    create_sw_major_notice()
    create_sw_7up_notice()

    # API(GET): 공지사항
    @app.route("/notice")
    def get_sw_major_notice_metadata():
        sw_major_notice_metadata = read_notice_metadata()

        return jsonify(sw_major_notice_metadata)

    # API(GET): 공지사항 상세
    @app.route("/notice/<noticeId>")
    def get_sw_major_notice_detail(noticeId):
        sw_major_notice_detail = read_notice_detail(noticeId)

        return jsonify(sw_major_notice_detail)

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

    @app.route('/edit_password', methods=['PATCH'])
    @login_required
    def update_password():
        if request.method == 'PATCH':
            data = request.json
            print(data)
            username = session.get('username')
            old_password = data.get("oldPassword")
            new_password = data.get("newPassword")

            if not check_password(username, old_password):
                return jsonify({"error": "Incorrect current password"}), 400

            success = update_user_password(username, new_password)
            if success:
                return jsonify({"message": "Password updated successfully"}), 200
            else:
                return jsonify({"error": "Failed to update password"}), 500

    return app

# 데이터베이스 초기화
def init_db():
    print("Connected to db")

    conn = sqlite3.connect(constants.database_path)
    cursor = conn.cursor()
    # 공지사항 테이블 생성
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS notice (
            notice_id TEXT PRIMARY KEY,
            notice_group TEXT,
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
