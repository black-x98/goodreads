from database.queries import books as books_queries

def get_book(conn, book_id: int):
    return books_queries.get_book(conn, book_id=book_id)

def list_books(conn):
    return books_queries.list_books(conn)
