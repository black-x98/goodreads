import os
from psycopg import connect
from psycopg.rows import dict_row

# ------------------------------
# Configuration from environment
# ------------------------------
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "goodreads")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

# ------------------------------
# DB Connection Factory
# ------------------------------
def get_connection():
    """
    Provides a fresh connection. Use it with FastAPI Depends.
    """
    conn = connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        row_factory=dict_row
    )
    try:
        yield conn
    finally:
        conn.close()
