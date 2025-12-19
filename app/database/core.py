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


# Read the DB URL from environment, fallback to default
# Construct the DATABASE_URL dynamically
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

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
