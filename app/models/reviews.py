from pydantic import BaseModel, Field, conint

from datetime import datetime


class ReviewCreate(BaseModel):
    user_id: int
    book_id: int
    rating: conint(ge=1, le=5)  # ensures rating is 1-5
    content: str = Field(..., min_length=1, max_length=2000)


class ReviewOut(BaseModel):
    id: int
    user_id: int
    book_id: int
    rating: int
    content: str
    created_at: datetime

    class Config:
        orm_mode = True
