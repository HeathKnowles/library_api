from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.schemas.book_schema import BookOut  # for nested relationship

# ---------- Input Schema ----------

class AuthorCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    bio: Optional[str] = None

# ---------- Output Schema ----------

class AuthorOut(BaseModel):
    id: int
    name: str
    bio: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class AuthorWithBooks(AuthorOut):
    books: List[BookOut] = []
