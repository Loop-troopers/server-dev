import sqlite3
from src.api.sw_major.scrape import scrape_sw_major_notice


## 소프트웨어학과 홈페이지 공지사항
# CREATE
def create_sw_major_notice():
    all_notice = scrape_sw_major_notice()
    # 스크래핑한 결과가 빈 배열일 경우(최신 게시물 존재하지 않는 경우)
    if not all_notice:
        return

    conn = sqlite3.connect("../db")
    c = conn.cursor()

    for notice_item in all_notice:
        notice_id = notice_item["noticeId"]
        category = notice_item["category"]
        title = notice_item["title"]
        created_at = notice_item["createdAt"]
        body = notice_item["body"]
        other_elements = notice_item["otherElements"]

        # DB 반영
        c.execute(
            """
        INSERT INTO sw_major_notice
        (notice_id, category, title, created_at, body, other_elements)
        VALUES (?, ?, ?, ?, ?, ?)""",
            (notice_id, category, title, created_at, body, other_elements),
        )

    c.close()
    conn.commit()
    conn.close()

    return

# READ(all)
def read_sw_major_notice_metadata():
    conn = sqlite3.connect("../db")
    sw_major_metadata = []
    c = conn.cursor()
    c.execute("SELECT * FROM sw_major_notice")
    while True:
        row = c.fetchone()

        if row == None:
            break
        metadata = {
            "notice_id": row[0],
            "category": row[1],
            "title": row[2],
            "created_at": row[3],
        }
        sw_major_metadata.append(metadata)
    c.close()
    conn.close()

    return sw_major_metadata

# READ(detail)
def read_sw_major_notice_detail(notice_id):
    conn = sqlite3.connect("../db")

    c = conn.cursor()
    c.execute("SELECT * FROM sw_major_notice WHERE notice_id = ?",  (notice_id,))
    row = c.fetchone()

    notice_detail = {
        "notice_id": row[0],
        "body": row[4],
        "other_elements": row[5],
    }
    c.close()
    conn.close()

    return notice_detail