from psycopg.rows import dict_row

def get_book(conn, *, book_id: int) -> dict | None:
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


def list_books(conn) -> list[dict]:
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
