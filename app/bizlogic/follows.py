from app.database.queries import follows as follows_queries

def follow_user(conn, *, follower_id, followee_id):
    return follows_queries.follow_user(
        conn,
        follower_id=follower_id,
        followee_id=followee_id
    )

def unfollow_user(conn, *, follower_id, followee_id):
    return follows_queries.unfollow_user(
        conn,
        follower_id=follower_id,
        followee_id=followee_id
    )

def get_newsfeed(conn, user_id):
    return follows_queries.get_newsfeed(conn, user_id=user_id)
