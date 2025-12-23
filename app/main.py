import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException

from app.bizlogic import books as books_bl
from app.bizlogic import follows as follows_bl
from app.bizlogic import reviews as reviews_bl
from app.bizlogic import users as users_bl
from app.database.core import get_connection
from app.database.seed import seed_data
from app.models.books import BookCreate
from app.models.reviews import ReviewCreate
from app.models.users import UserCreate


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run the synchronous seeding in a threadpool and wait for it to finish
    print("seeding data from fastapi hook")
    await asyncio.to_thread(seed_data)
    yield  # after this, FastAPI starts handling requests


app = FastAPI(title="Goodreads Clone Backend", lifespan=lifespan)


# ------------------------------
# User Routes
# ------------------------------
@app.get("/users")
def api_list_users(conn=Depends(get_connection)):
    return users_bl.list_users(conn)


@app.get("/users/{user_id}")
def api_get_user(user_id: int, conn=Depends(get_connection)):
    user = users_bl.get_user(conn, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users")
def api_create_user(user: UserCreate, conn=Depends(get_connection)):
    return users_bl.insert_user(conn, name=user.name)


# ------------------------------
# Book Routes
# ------------------------------
@app.get("/books")
def api_list_books(conn=Depends(get_connection)):
    return books_bl.list_books(conn)


@app.get("/books/{book_id}")
def api_get_book(book_id: int, conn=Depends(get_connection)):
    book = books_bl.get_book(conn, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books")
def api_create_book(book: BookCreate, conn=Depends(get_connection)):
    return books_bl.insert_book(conn, title=book.title, author=book.author)


# ------------------------------
# Review Routes
# ------------------------------
@app.post("/reviews")
def api_add_review(review: ReviewCreate, conn=Depends(get_connection)):
    return reviews_bl.add_review(
        conn,
        user_id=review.user_id,
        book_id=review.book_id,
        rating=review.rating,
        content=review.content,
    )


@app.get("/users/{user_id}/reviews")
def api_list_reviews_by_user(user_id: int, conn=Depends(get_connection)):
    return reviews_bl.list_reviews_by_user(conn, user_id)


@app.get("/books/{book_id}/reviews")
def api_list_reviews_by_book(book_id: int, conn=Depends(get_connection)):
    return reviews_bl.list_reviews_by_book(conn, book_id)


# ------------------------------
# Follow / Newsfeed Routes
# ------------------------------
@app.post("/follow/{followee_id}")
def api_follow_user(followee_id: int, follower_id: int, conn=Depends(get_connection)):
    return follows_bl.follow_user(conn, follower_id=follower_id, followee_id=followee_id)


@app.post("/unfollow/{followee_id}")
def api_unfollow_user(followee_id: int, follower_id: int, conn=Depends(get_connection)):
    follows_bl.unfollow_user(conn, follower_id=follower_id, followee_id=followee_id)
    return {"status": "ok"}


@app.get("/users/{user_id}/newsfeed")
def api_get_newsfeed(user_id: int, conn=Depends(get_connection)):
    return follows_bl.get_newsfeed(conn, user_id)
