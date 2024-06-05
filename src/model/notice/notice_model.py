from api.sw_major.scrape import scrape_sw_major_notice
from api.sw_7up.scrape import scrape_sw7up_notice
import asyncio
from src import constants
import sqlite3
from flask import session

# 소프트웨어학과 홈페이지 공지사항
# CREATE
def create_sw_major_notice():
    all_notice = scrape_sw_major_notice()
    
    # 스크래핑한 결과가 빈 배열일 경우(최신 게시물 존재하지 않는 경우)
    if not all_notice:
        return

    conn = sqlite3.connect(constants.database_path)
    c = conn.cursor()

    for notice_item in all_notice:
        notice_id = notice_item["noticeId"]
        notice_group = notice_item["noticeGroup"]
        category = notice_item.get('category', None)
        title = notice_item.get("title", None)
        created_at = notice_item.get('createdAt', None)
        body = notice_item.get('body', None)
        image_urls = notice_item.get('imageUrls', None)
        tables = notice_item.get('tables', None)
        
        # DB 반영
        c.execute(
            """
        INSERT INTO notice
        (notice_id, notice_group, category, title, created_at, body, image_urls, tables)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (notice_id, notice_group, category, title, created_at, body, image_urls, tables),
        )

    c.close()
    conn.commit()
    conn.close()

    return

# 소중사 홈페이지 공지사항 메타데이터
# CREATE
def create_sw_7up_notice():
    all_notice = asyncio.run(scrape_sw7up_notice())
    # 크롤링한 결과가 빈 배열일 경우(최신 게시물 존재하지 않는 경우)
    if not all_notice:
        return

    conn = sqlite3.connect(constants.database_path)
    c = conn.cursor()
    c.execute("SELECT title FROM notice")
    existing_titles = set(row[0] for row in c.fetchall())

    for notice_item in all_notice:
        title = notice_item["title"]
        if title in existing_titles:
            continue
        notice_id = notice_item["noticeId"]
        notice_group = notice_item["noticeGroup"]
        category = notice_item.get('category', None)
        body = notice_item.get('body', None)
        # 게시 날짜 크롤링 로직 필요
        created_at = notice_item.get('createdAt', None)
        image_urls = notice_item.get('imageUrls', None)
        tables = notice_item.get('tables', None)

        c.execute(
            """
            INSERT INTO notice
            (notice_id, notice_group, category, title, created_at, body, image_urls, tables)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (notice_id, notice_group, category, title, created_at, body, image_urls, tables),
        )

    c.close()
    conn.commit()
    conn.close()

# READ(all)
def read_notice_metadata():
    conn = sqlite3.connect(constants.database_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM notice")

    notice_metadata = []
    for row in c.fetchall():
        metadata = {
            "noticeId": row["notice_id"],
            "noticeGroup": row["notice_group"],
            "title": row["title"],
            "createdAt": row["created_at"],
        }
        notice_metadata.append(metadata)
    c.close()
    conn.close()

    return notice_metadata

# READ(detail)
def read_notice_detail(notice_id):
    conn = sqlite3.connect(constants.database_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM notice WHERE notice_id = ?",  (notice_id,))
    row = c.fetchone()
    user_id = session['user_id']

    c.execute("SELECT * FROM bookmark_notice WHERE notice_id = ? and user_id = ?",  (notice_id, user_id))

    notice_detail = {
        "noticeId": row["notice_id"],
        "noticeGroup": row["notice_group"],
        "category": row["category"],
        "title": row["title"],
        "createdAt": row["created_at"],
        "body": row["body"],
        "imageUrls": [",".join(row["image_urls"].split())] if row["image_urls"] else [],
        "tables": row["tables"]
    }
    c.close()
    conn.close()

    return notice_detail