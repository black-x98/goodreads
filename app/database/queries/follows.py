from psycopg.rows import dict_row

from app.database.queries.validations import ensure_user_exists


def follow_user(conn, *, follower_id: int, followee_id: int) -> dict | None:
    # Validate users first
    ensure_user_exists(conn, follower_id)
    ensure_user_exists(conn, followee_id)

    sql = """
    INSERT INTO followers (follower_id, followee_id)
    VALUES (%(follower_id)s, %(followee_id)s)
    ON CONFLICT DO NOTHING
    RETURNING follower_id, followee_id, created_at;
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql, {"follower_id": follower_id, "followee_id": followee_id})
        conn.commit()
        return cur.fetchone()


def unfollow_user(conn, *, follower_id: int, followee_id: int) -> None:
    sql = """
    DELETE FROM followers
    WHERE follower_id = %(follower_id)s
      AND followee_id = %(followee_id)s;
    """
    with conn.cursor() as cur:
        cur.execute(sql, {"follower_id": follower_id, "followee_id": followee_id})
        conn.commit()


def get_newsfeed(conn, *, user_id: int) -> list[dict]:
    sql = """
    SELECT r.id, r.user_id, r.book_id, r.rating, r.content, r.created_at
    FROM reviews r
    JOIN followers f ON r.user_id = f.followee_id
    WHERE f.follower_id = %(user_id)s
    UNION
    SELECT r.id, r.user_id, r.book_id, r.rating, r.content, r.created_at
    FROM reviews r
    WHERE r.user_id = %(user_id)s
    ORDER BY created_at DESC;
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql, {"user_id": user_id})
        return cur.fetchall()
