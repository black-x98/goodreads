from app.database.core import get_connection

def seed_data():
    """
    Idempotent DB seeding using WHERE NOT EXISTS checks.
    Adjusted to real schema: reviews table has no comment column.
    """

    conn_gen = get_connection()
    conn = next(conn_gen)

    try:
        with conn.cursor() as cur:

            # ---------------- USERS ----------------
            cur.execute("""
                INSERT INTO users (name)
                SELECT 'Alice'
                WHERE NOT EXISTS (
                    SELECT 1 FROM users WHERE name='Alice'
                );
            """)

            cur.execute("""
                INSERT INTO users (name)
                SELECT 'Bob'
                WHERE NOT EXISTS (
                    SELECT 1 FROM users WHERE name='Bob'
                );
            """)

            cur.execute("""
                INSERT INTO users (name)
                SELECT 'Charlie'
                WHERE NOT EXISTS (
                    SELECT 1 FROM users WHERE name='Charlie'
                );
            """)

            # ---------------- BOOKS ----------------
            cur.execute("""
                INSERT INTO books (title, author)
                SELECT 'The Seed Book', 'John Seeder'
                WHERE NOT EXISTS (
                    SELECT 1 FROM books WHERE title='The Seed Book'
                );
            """)

            cur.execute("""
                INSERT INTO books (title, author)
                SELECT 'Docker Magic', 'Tariq Hasan'
                WHERE NOT EXISTS (
                    SELECT 1 FROM books WHERE title='Docker Magic'
                );
            """)

            # -------------------------------------------
            # REVIEWS
            # Safely insert by using JOINs so user/book lookup returns exactly 1 row
            # -------------------------------------------
            cur.execute("""
                INSERT INTO reviews (user_id, book_id, rating, content)
                SELECT 
                    u.id,
                    b.id,
                    5,
                    'Amazing tutorial seed review!'
                FROM users u
                JOIN books b ON b.title = 'The Seed Book'
                WHERE u.name = 'Alice'
                  AND NOT EXISTS (
                    SELECT 1
                    FROM reviews r
                    WHERE r.user_id = u.id
                      AND r.book_id = b.id
                  );
            """)

            # -------------------------------------------
            # FOLLOWERS
            # -------------------------------------------
            cur.execute("""
                INSERT INTO followers (follower_id, followee_id)
                SELECT
                    uf.id,
                    ut.id
                FROM users uf
                JOIN users ut ON ut.name = 'Bob'
                WHERE uf.name = 'Alice'
                  AND NOT EXISTS (
                      SELECT 1
                      FROM followers f
                      WHERE f.follower_id = uf.id
                        AND f.followee_id = ut.id
                  );
            """)

            conn.commit()

    finally:
        try:
            conn.close()
        except:
            pass

        try:
            next(conn_gen)
        except StopIteration:
            pass
