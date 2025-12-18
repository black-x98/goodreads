from psycopg.rows import dict_row

def get_user(conn, *, user_id: int) -> dict | None:
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


def list_users(conn) -> list[dict]:
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
