from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field

# ---------- Input Schemas ----------

class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author_id: int
    publication_date: Optional[date] = None

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author_id: Optional[int] = None
    publication_date: Optional[date] = None
    is_available: Optional[bool] = None

class BookOut(BaseModel):
    id: int
    title: str
    author_id: int
    publication_date: Optional[date]
    is_available: bool
    created_at: datetime

    class Config:
        from_attributes = True
