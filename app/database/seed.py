from app.database.core import get_connection

def seed_data():
    """
    Seeds initial demo data idempotently.
    Each record checks by name/title before inserting,
    so seeds never duplicate across restarts.
    """

    conn_gen = get_connection()
    conn = next(conn_gen)

    try:
        with conn.cursor() as cur:

            # ---------------- USERS ----------------
            users = ["Alice", "Bob", "Charlie"]

            for username in users:
                cur.execute(
                    """
                    INSERT INTO users (name)
                    SELECT %s
                    WHERE NOT EXISTS (
                        SELECT 1 FROM users WHERE name = %s
                    );
                    """,
                    (username, username),
                )

            # ---------------- BOOKS ----------------
            books = [
                ("The Seed Book", "John Seeder"),
                ("Docker Magic", "Tariq Hasan"),
            ]

            for (title, author) in books:
                cur.execute(
                    """
                    INSERT INTO books (title, author)
                    SELECT %s, %s
                    WHERE NOT EXISTS (
                        SELECT 1 FROM books WHERE title = %s
                    );
                    """,
                    (title, author, title),
                )

            # ---------------- REVIEWS ----------------
            # Only insert if the specific user-book combination doesn't have a review
            cur.execute(
                """
                INSERT INTO reviews (user_id, book_id, rating, content)
                SELECT
                    u.id,
                    b.id,
                    5,
                    'Amazing tutorial seed review!'
                FROM users u, books b
                WHERE u.name = %s
                  AND b.title = %s
                  AND NOT EXISTS (
                      SELECT 1 FROM reviews r
                      WHERE r.user_id = u.id
                        AND r.book_id = b.id
                  );
                """,
                ("Alice", "The Seed Book"),
            )

            # ---------------- FOLLOWERS ----------------
            # Only insert if the specific follower-followee relationship doesn't exist
            cur.execute(
                """
                INSERT INTO followers (follower_id, followee_id)
                SELECT uf.id, ut.id
                FROM users uf, users ut
                WHERE uf.name = %s
                  AND ut.name = %s
                  AND NOT EXISTS (
                      SELECT 1 FROM followers f
                      WHERE f.follower_id = uf.id
                        AND f.followee_id = ut.id
                  );
                """,
                ("Alice", "Bob"),
            )

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