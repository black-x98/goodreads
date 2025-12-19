from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str
