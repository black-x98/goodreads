from psycopg.pool import ConnectionPool
from psycopg.rows import dict_row
import os

# ------------------------------
# Configuration from environment
# ------------------------------
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "goodreads")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_MINCONN = int(os.getenv("DB_MINCONN", 1))
DB_MAXCONN = int(os.getenv("DB_MAXCONN", 10))

# ------------------------------
# Initialize connection pool
# ------------------------------
pool = ConnectionPool(
    conninfo=f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}",
    min_size=DB_MINCONN,
    max_size=DB_MAXCONN
)


# ------------------------------
# FastAPI dependency
# ------------------------------
def get_connection():
    """
    Yield a connection from the pool for FastAPI routes.

    Usage:

        @app.get("/users")
        def list_users(conn = Depends(get_connection)):
            ...
    """
    conn = pool.getconn()
    try:
        yield conn
    finally:
        pool.putconn(conn)
