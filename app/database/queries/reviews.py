from psycopg.rows import dict_row

def insert_review(conn, *, user_id: int, book_id: int, rating: int, content: str) -> dict:
    sql = """
    INSERT INTO reviews (user_id, book_id, rating, content)
    VALUES (%(user_id)s, %(book_id)s, %(rating)s, %(content)s)
    RETURNING id, user_id, book_id, rating, content, created_at;
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql, {
            "user_id": user_id,
            "book_id": book_id,
            "rating": rating,
            "content": content
        })
        conn.commit()
        return cur.fetchone()


def get_review(conn, *, review_id: int) -> dict | None:
    sql = """
    SELECT id, user_id, book_id, rating, content, created_at
    FROM reviews
    WHERE id = %(review_id)s;
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql, {"review_id": review_id})
        return cur.fetchone()


def list_reviews_by_user(conn, *, user_id: int) -> list[dict]:
    sql = """
    SELECT id, user_id, book_id, rating, content, created_at
    FROM reviews
    WHERE user_id = %(user_id)s
    ORDER BY created_at DESC;
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql, {"user_id": user_id})
        return cur.fetchall()


def list_reviews_by_book(conn, *, book_id: int) -> list[dict]:
    sql = """
    SELECT id, user_id, book_id, rating, content, created_at
    FROM reviews
    WHERE book_id = %(book_id)s
    ORDER BY created_at DESC;
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql, {"book_id": book_id})
        return cur.fetchall()
