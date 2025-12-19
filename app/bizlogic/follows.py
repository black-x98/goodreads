from app.database.queries import follows as follows_queries
from psycopg import Connection

def follow_user(conn: Connection, *, follower_id: int, followee_id: int) -> dict:
    """
    Follow a user.
    """
    return follows_queries.follow_user(
        conn,
        follower_id=follower_id,
        followee_id=followee_id,
    )


def unfollow_user(conn: Connection, *, follower_id: int, followee_id: int) -> None:
    """
    Unfollow a user.
    """
    follows_queries.unfollow_user(
        conn,
        follower_id=follower_id,
        followee_id=followee_id,
    )


def get_newsfeed(conn: Connection, user_id: int) -> list[dict]:
    """
    Fetch the newsfeed for a user (reviews from followed users).
    """
    return follows_queries.get_newsfeed(conn, user_id=user_id)
