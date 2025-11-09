from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

# ---------- Input Schema ----------

class BorrowCreate(BaseModel):
    book_id: int
    days: int = Field(..., ge=1, le=60, description="Number of days to borrow the book")

# ---------- Output Schema ----------

class BorrowOut(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrowed_at: datetime
    due_date: datetime
    returned_at: Optional[datetime] = None

    class Config:
        from_attributes = True
