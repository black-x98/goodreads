from psycopg.rows import dict_row
from psycopg import Connection


def insert_book(conn, *, title: str, author: str) -> dict:
    """
    Insert a new book and return the created row.
    """
    sql = """
    INSERT INTO books (title, author)
    VALUES (%(title)s, %(author)s)
    RETURNING id, title, author, created_at;
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql, {"title": title, "author": author})
        return cur.fetchone()


def get_book(conn: Connection, *, book_id: int) -> dict | None:
    """
    Fetch a single book by ID.
    """
    sql = """
    SELECT id, title, author, created_at
    FROM books
    WHERE id = %(book_id)s;
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql, {"book_id": book_id})
        return cur.fetchone()


def list_books(conn: Connection) -> list[dict]:
    """
    Fetch all books.
    """
    sql = """
    SELECT id, title, author, created_at
    FROM books
    ORDER BY id;
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql)
        return cur.fetchall()
