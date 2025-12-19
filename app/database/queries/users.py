from psycopg.rows import dict_row
from psycopg import Connection

def get_user(conn: Connection, *, user_id: int) -> dict | None:
    """
    Fetch a single user by ID.
    """
    sql = """
    SELECT id, name, created_at
    FROM users
    WHERE id = %(user_id)s;
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql, {"user_id": user_id})
        return cur.fetchone()


def list_users(conn: Connection) -> list[dict]:
    """
    Fetch all users.
    """
    sql = """
    SELECT id, name, created_at
    FROM users
    ORDER BY id;
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql)
        return cur.fetchall()


def insert_user(conn: Connection, *, name: str) -> dict:
    """
    Insert a new user and return it.
    """
    sql = """
    INSERT INTO users (name)
    VALUES (%(name)s)
    RETURNING id, name, created_at;
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql, {"name": name})
        return cur.fetchone()
