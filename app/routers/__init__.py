"""
Routers package:
Holds all route definitions for FastAPI endpoints.
"""

from app.routers import (
    auth_router,
    author_router,
    book_router,
    borrow_router,
)

__all__ = ["auth_router", "author_router", "book_router", "borrow_router"]
