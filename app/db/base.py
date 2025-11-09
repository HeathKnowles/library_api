"""
This module imports all SQLAlchemy models so that Alembic and Base.metadata.create_all()
can discover them automatically.

You typically won't import Base from here directly — instead, import from app.db.session.
"""

from app.db.session import Base

# Import all models (ensures they are registered with SQLAlchemy metadata)
from app.models.user import User
from app.models.author import Author
from app.models.book import Book
from app.models.borrow import BorrowRecord

__all__ = ["Base", "User", "Author", "Book", "BorrowRecord"]
