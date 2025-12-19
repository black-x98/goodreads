import psycopg
from psycopg.rows import dict_row
import os
from contextlib import contextmanager

# ------------------------------
# Configuration from environment
# ------------------------------
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "goodreads")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

# ------------------------------
# Context manager for manual use
# ------------------------------
@contextmanager
def connect():
    conn = psycopg.connect(
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


# ------------------------------
# FastAPI dependency
# ------------------------------
def get_connection():
    """
    For FastAPI routes: use as Depends(get_connection)
    Do NOT wrap in 'with'.
    """
    conn = psycopg.connect(
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
