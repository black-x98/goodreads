from app.database.queries import reviews as reviews_queries
from psycopg import Connection

from app.database.queries.validations import ensure_user_exists, ensure_book_exists


def add_review(
        conn: Connection, *,
        user_id: int,
        book_id: int,
        rating: int,
        content: str
) -> dict:
    """
    Insert a new review and return the created review as a dict.
    """
    ensure_user_exists(conn, user_id)
    ensure_book_exists(conn, book_id)

    return reviews_queries.insert_review(
        conn,
        user_id=user_id,
        book_id=book_id,
        rating=rating,
        content=content,
    )


def get_review(conn: Connection, review_id: int) -> dict | None:
    """
    Fetch a single review by its ID.
    """
    return reviews_queries.get_review(conn, review_id=review_id)


def list_reviews_by_user(conn: Connection, user_id: int) -> list[dict]:
    """
    Fetch all reviews made by a specific user.
    """
    return reviews_queries.list_reviews_by_user(conn, user_id=user_id)


def list_reviews_by_book(conn: Connection, book_id: int) -> list[dict]:
    """
    Fetch all reviews for a specific book.
    """
    return reviews_queries.list_reviews_by_book(conn, book_id=book_id)
