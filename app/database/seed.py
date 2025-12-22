from app.database.core import get_connection


USERS = [
    "Alice",
    "Bob",
    "Charlie",
]

BOOKS = [
    ("The Seed Book", "John Seeder"),
    ("Docker Magic", "Tariq Hasan"),
]

REVIEWS = [
    ("Alice", "The Seed Book", 5, "Amazing tutorial seed review!"),
]

FOLLOWERS = [
    ("Alice", "Bob"),
]


def seed_data():
    conn_gen = get_connection()
    conn = next(conn_gen)

    try:
        with conn.cursor() as cur:

            # ---------------- INSERT USERS ----------------
            cur.executemany(
                """
                INSERT INTO users (name)
                SELECT %s
                WHERE NOT EXISTS (SELECT 1 FROM users WHERE name = %s);
                """,
                [(u, u) for u in USERS]
            )

            # ---------------- INSERT BOOKS ----------------
            cur.executemany(
                """
                INSERT INTO books (title, author)
                SELECT %s, %s
                WHERE NOT EXISTS (
                    SELECT 1 FROM books WHERE title = %s
                );
                """,
                [(title, author, title) for title, author in BOOKS]
            )

            # ---------------- INSERT REVIEWS ----------------
            for username, title, rating, content in REVIEWS:
                cur.execute(
                    """
                    INSERT INTO reviews (user_id, book_id, rating, content)
                    SELECT u.id, b.id, %s, %s
                    FROM users u
                    JOIN books b ON b.title = %s
                    WHERE u.name = %s
                      AND NOT EXISTS (
                        SELECT 1 FROM reviews
                        WHERE user_id = u.id AND book_id = b.id
                      )
                    ;
                    """,
                    (rating, content, title, username)
                )

            # ---------------- INSERT FOLLOWERS ----------------
            for follower, followee in FOLLOWERS:
                cur.execute(
                    """
                    INSERT INTO followers (follower_id, followee_id)
                    SELECT uf.id, ut.id
                    FROM users uf
                    JOIN users ut ON ut.name = %s
                    WHERE uf.name = %s
                      AND NOT EXISTS (
                        SELECT 1
                        FROM followers
                        WHERE follower_id = uf.id
                          AND followee_id = ut.id
                      );
                    """,
                    (followee, follower),
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
