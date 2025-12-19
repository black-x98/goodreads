from app.database.queries.users import list_users as list_users_query

def list_users():
    return list_users_query()
