import sqlite3
import asyncio
from src.api.sw_7up.scrape import scrape_sw7up_notice
from src import constants

## 소중사 홈페이지 공지사항 메타데이터
# CREATE
def create_sw_7up_notice():
    all_notice = asyncio.run(scrape_sw7up_notice())
    # 크롤링한 결과가 빈 배열일 경우(최신 게시물 존재하지 않는 경우)
    if not all_notice:
        return

    conn = sqlite3.connect(constants.database_path)
    c = conn.cursor()
    existing_titles = set(row[1] for row in c.fetchall())

    for notice_item in all_notice:
        title = notice_item["title"]
        if title in existing_titles:
            continue
        notice_id = notice_item["noticeId"]
        body = notice_item["body"]
        # 게시날짜 크롤링 로직 필요
        # created_at = notice_item['createdAt']

        c.execute(
            """
        INSERT INTO sw_7up_notice
        (notice_id, title, body)
        VALUES (?, ?, ?)""",
            (notice_id, title, body),
        )

    c.close()
    conn.commit()
    conn.close()

# READ
def read_sw_7up_notice():
    conn = sqlite3.connect(constants.database_path)
    sw_7up_metadata = []
    c = conn.cursor()
    c.execute("SELECT * FROM sw_7up_notice")
    while True:
        row = c.fetchone()

        if row == None:
            break
        notice_item = {
            "group": "sw_7up_notice",
            "noticeId": row[0],
            "title": row[1],
        }
        sw_7up_metadata.append(notice_item)
    c.close()
    conn.close()

    return sw_7up_metadata

# READ(detail)
def read_sw_7up_notice_detail(notice_id):
    conn = sqlite3.connect(constants.database_path)

    c = conn.cursor()
    c.execute("SELECT * FROM sw_7up_notice WHERE notice_id = ?",  (notice_id,))
    row = c.fetchone()

    notice_detail = {
        "noticeId": row[0],
        "title": row[1],
        "body": row[2],
        # "createdAt": row[3]
    }
    c.close()
    conn.close()

    return notice_detail

