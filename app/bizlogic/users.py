# app/bizlogic/users.py
from app.database.queries.users import insert_user as insert_user_query, get_user as get_user_query, list_users as list_users_query

def insert_user(conn, *, name: str):
    user = insert_user_query(conn, name=name)
    conn.commit()  # <- COMMIT!
    return user

def get_user(conn, user_id: int):
    return get_user_query(conn, user_id=user_id)

def list_users(conn):
    return list_users_query(conn)
