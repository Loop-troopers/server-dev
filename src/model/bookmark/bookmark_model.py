import sqlite3
from src import constants
from flask import session

# CREATE
def create_bookmark(notice_id):
    conn = sqlite3.connect(constants.database_path)
    user_id = session['user_id']
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO bookmark_notice (user_id, notice_id)
        VALUES (?, ?)
        """, (user_id, notice_id)
    )
    conn.commit()
    c.close()
    conn.close()

    return True

# READ (all)
def read_user_bookmarks():
    conn = sqlite3.connect(constants.database_path)
    conn.row_factory = sqlite3.Row
    user_id = session['user_id']

    bookmarked_notice_ids = []
    c = conn.cursor()
    c.execute("SELECT * FROM bookmark_notice WHERE user_id = ?", (user_id,))
    rows = c.fetchall()

    for row in rows:
        bookmarked_notice_ids.append(row["notice_id"])

    if not bookmarked_notice_ids:
        return []

    # 동적 쿼리 생성 (사용자가 저장한 notice_id로 notice 정보 가져오기)
    placeholders = ','.join(['?'] * len(bookmarked_notice_ids))
    query = f"SELECT notice_id, notice_group, title FROM notice WHERE notice_id IN ({placeholders})"

    c.execute(query, bookmarked_notice_ids)
    rows = c.fetchall()

    notices = []
    for row in rows:
        notice = {
            "noticeId": row["notice_id"],
            "noticeGroup": row["notice_group"],
            "title": row["title"]
        }
        notices.append(notice)

    c.close()
    conn.close()

    return notices

# DELETE
def delete_bookmarks(noticed_id):
    conn = sqlite3.connect(constants.database_path)
    user_id = session['user_id']

    c = conn.cursor()
    c.execute("DELETE FROM bookmark_notice WHERE user_id = ? AND notice_id = ?", (user_id, noticed_id))
    conn.commit()
    c.close()
    conn.close()

    return

