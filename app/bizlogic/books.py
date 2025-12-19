from app.database.queries import books as books_queries

def get_book(conn, book_id: int):
    return books_queries.get_book(conn, book_id=book_id)

def list_books(conn):
    return books_queries.list_books(conn)

def insert_book(conn, *, title: str, author: str):
    """
    Insert a new book and return it.
    """
    return books_queries.insert_book(conn, title=title, author=author)
