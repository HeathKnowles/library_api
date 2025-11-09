from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

# ---------- Input Schemas ----------

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)

# ---------- Output Schemas ----------

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True  # allows ORM model → Pydantic model conversion

# ---------- Auth Token Schema ----------

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
