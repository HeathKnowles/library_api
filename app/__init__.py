"""
app/__init__.py

This file initializes the FastAPI application package.
It sets up the app instance, loads configurations, registers routers,
and ensures that all database models are discovered.
"""

from fastapi import FastAPI
from app.core import settings
from app.db import Base, engine
from app.db.base import *  # ensures all models (User, Author, Book, BorrowRecord) are imported
from app.routers import (
    auth_router,
    author_router,
    book_router,
    borrow_router,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Book Library Management API built with FastAPI.",
)


app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(author_router.router, prefix="/api/v1/authors", tags=["Authors"])
app.include_router(book_router.router, prefix="/api/v1/books", tags=["Books"])
app.include_router(borrow_router.router, prefix="/api/v1/borrow", tags=["Borrowing"])


@app.on_event("startup")
def on_startup():
    print("🚀 Application has started successfully!")

@app.on_event("shutdown")
def on_shutdown():
    print("🛑 Application is shutting down.")


__all__ = ["app"]
