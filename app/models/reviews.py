from pydantic import BaseModel, Field, conint

from datetime import datetime


class ReviewCreate(BaseModel):
    user_id: int
    book_id: int
    rating: int
    content: str


class ReviewOut(BaseModel):
    id: int
    user_id: int
    book_id: int
    rating: int
    content: str
    created_at: datetime

    class Config:
        orm_mode = True
