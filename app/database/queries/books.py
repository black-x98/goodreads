from fastapi import HTTPException
from psycopg.rows import dict_row


def get_book(conn, *, book_id: int) -> dict | None:
    sql = """
    SELECT id, title, author, created_at
    FROM books
    WHERE id = %(book_id)s;
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql, {"book_id": book_id})
        return cur.fetchone()


def list_books(conn) -> list[dict]:
    sql = """
    SELECT id, title, author, created_at
    FROM books
    ORDER BY id;
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql)
        return cur.fetchall()


def insert_book(conn, *, title: str, author: str) -> dict:
    sql = """
    INSERT INTO books (title, author)
    VALUES (%(title)s, %(author)s)
    RETURNING id, title, author, created_at;
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql, {"title": title, "author": author})
        conn.commit()
        return cur.fetchone()
