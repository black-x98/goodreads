from app.database.queries import users as users_queries
from psycopg import Connection

def list_users(conn: Connection) -> list[dict]:
    """
    Fetch all users.
    """
    return users_queries.list_users(conn)


def get_user(conn: Connection, user_id: int) -> dict | None:
    """
    Fetch a single user by ID.
    """
    return users_queries.get_user(conn, user_id=user_id)
