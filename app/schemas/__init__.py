"""
Schemas package:
Contains all Pydantic models for data validation and serialization.
"""

from app.schemas.user_schema import UserCreate, UserOut, TokenOut
from app.schemas.author_schema import AuthorCreate, AuthorOut, AuthorWithBooks
from app.schemas.book_schema import BookCreate, BookUpdate, BookOut
from app.schemas.borrow_schema import BorrowCreate, BorrowOut

__all__ = [
    "UserCreate", "UserOut", "TokenOut",
    "AuthorCreate", "AuthorOut", "AuthorWithBooks",
    "BookCreate", "BookUpdate", "BookOut",
    "BorrowCreate", "BorrowOut",
]
