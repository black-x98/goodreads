from app.database.queries import reviews as reviews_queries

def add_review(conn, *, user_id, book_id, rating, content):
    return reviews_queries.insert_review(
        conn,
        user_id=user_id,
        book_id=book_id,
        rating=rating,
        content=content
    )

def get_review(conn, review_id):
    return reviews_queries.get_review(conn, review_id=review_id)

def list_reviews_by_user(conn, user_id):
    return reviews_queries.list_reviews_by_user(conn, user_id=user_id)

def list_reviews_by_book(conn, book_id):
    return reviews_queries.list_reviews_by_book(conn, book_id=book_id)
