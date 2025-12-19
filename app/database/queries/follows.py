from psycopg.rows import dict_row
from psycopg import Connection

def follow_user(conn: Connection, *, follower_id: int, followee_id: int) -> dict | None:
    """
    Follower follows followee.
    """
    sql = """
    INSERT INTO followers (follower_id, followee_id)
    VALUES (%(follower_id)s, %(followee_id)s)
    ON CONFLICT DO NOTHING
    RETURNING follower_id, followee_id, created_at;
    """
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute(sql, {"follower_id": follower_id, "followee_id": followee_id})
        return cur.fetchone()


def unfollow_user(conn: Connection, *, follower_id: int, followee_id: int) -> None:
    """
    Follower unfollows followee.
    """
    sql = """
    DELETE FROM followers
    WHERE follower_id = %(follower_id)s
      AND followee_id = %(followee_id)s;
    """
    with conn.cursor() as cur:
        cur.execute(sql, {"follower_id": follower_id, "followee_id": followee_id})


def get_newsfeed(conn: Connection, *, user_id: int) -> list[dict]:
    """
    Fetch recent reviews by the user and followed users.
    """
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
