from fastapi import HTTPException
from psycopg.rows import dict_row


def get_user(conn, *, user_id: int) -> dict | None:
    sql = """
    SELECT id, name, created_at
    FROM users
    WHERE id = %(user_id)s;
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql, {"user_id": user_id})
        return cur.fetchone()


def list_users(conn) -> list[dict]:
    sql = """
    SELECT id, name, created_at
    FROM users
    ORDER BY id;
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql)
        return cur.fetchall()


def insert_user(conn, *, name: str) -> dict:
    sql = """
    INSERT INTO users (name)
    VALUES (%(name)s)
    RETURNING id, name, created_at;
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql, {"name": name})
        conn.commit()
        return cur.fetchone()
