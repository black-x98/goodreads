from fastapi import HTTPException


def ensure_user_exists(conn, user_id: int):
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM users WHERE id = %s", (user_id,))
        if not cur.fetchone():
            raise HTTPException(status_code=400, detail=f"User {user_id} does not exist")


def ensure_book_exists(conn, book_id: int):
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM books WHERE id = %s", (book_id,))
        if not cur.fetchone():
            raise HTTPException(status_code=400, detail=f"Book {book_id} does not exist")
