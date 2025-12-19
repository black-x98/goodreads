from fastapi import FastAPI, Depends, HTTPException
from psycopg import connect
from app.database.core import get_connection
from app.bizlogic import users as users_bl, books as books_bl, reviews as reviews_bl, follows as follows_bl
from pydantic import BaseModel

app = FastAPI(title="Goodreads Clone Backend")

# ------------------------------
# Pydantic Schemas
# ------------------------------
class ReviewCreate(BaseModel):
    user_id: int
    book_id: int
    rating: int
    content: str

# ------------------------------
# Dependency to get DB connection
# ------------------------------
def get_conn():
    with get_connection() as conn:
        yield conn

# ------------------------------
# User Routes
# ------------------------------

@app.get("/users")
def get_users(conn=Depends(get_connection)):
    rows = conn.execute("SELECT id, name, created_at FROM users ORDER BY id").fetchall()
    return rows

@app.get("/users/{user_id}")
def api_get_user(user_id: int, conn = Depends(get_conn)):
    user = users_bl.get_user(conn, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ------------------------------
# Book Routes
# ------------------------------
@app.get("/books")
def api_list_books(conn = Depends(get_conn)):
    return books_bl.list_books(conn)

@app.get("/books/{book_id}")
def api_get_book(book_id: int, conn = Depends(get_conn)):
    book = books_bl.get_book(conn, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# ------------------------------
# Review Routes
# ------------------------------
@app.post("/reviews")
def api_add_review(review: ReviewCreate, conn = Depends(get_conn)):
    return reviews_bl.add_review(
        conn,
        user_id=review.user_id,
        book_id=review.book_id,
        rating=review.rating,
        content=review.content
    )

@app.get("/users/{user_id}/reviews")
def api_list_reviews_by_user(user_id: int, conn = Depends(get_conn)):
    return reviews_bl.list_reviews_by_user(conn, user_id)

@app.get("/books/{book_id}/reviews")
def api_list_reviews_by_book(book_id: int, conn = Depends(get_conn)):
    return reviews_bl.list_reviews_by_book(conn, book_id)

# ------------------------------
# Follow / Newsfeed Routes
# ------------------------------
@app.post("/follow/{followee_id}")
def api_follow_user(followee_id: int, follower_id: int, conn = Depends(get_conn)):
    return follows_bl.follow_user(conn, follower_id=follower_id, followee_id=followee_id)

@app.post("/unfollow/{followee_id}")
def api_unfollow_user(followee_id: int, follower_id: int, conn = Depends(get_conn)):
    follows_bl.unfollow_user(conn, follower_id=follower_id, followee_id=followee_id)
    return {"status": "ok"}

@app.get("/users/{user_id}/newsfeed")
def api_get_newsfeed(user_id: int, conn = Depends(get_conn)):
    return follows_bl.get_newsfeed(conn, user_id)
