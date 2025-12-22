from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReviewCreate(BaseModel):
    user_id: int
    book_id: int
    rating: int
    content: str


class ReviewOut(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    book_id: int
    rating: int
    content: str
    created_at: datetime

