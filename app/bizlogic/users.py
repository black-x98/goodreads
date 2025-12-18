from database.queries import users as users_queries

def get_user(conn, user_id: int):
    return users_queries.get_user(conn, user_id=user_id)

def list_users(conn):
    return users_queries.list_users(conn)
