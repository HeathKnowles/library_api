from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.models.author import Author
from app.schemas.author_schema import AuthorCreate, AuthorOut, AuthorWithBooks
from app.core.security import get_current_user  # assumes you implemented this in core/security.py

router = APIRouter()

# ---------- Create Author ----------
@router.post("/", response_model=AuthorOut, status_code=status.HTTP_201_CREATED)
def create_author(
    payload: AuthorCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    author = Author(name=payload.name, bio=payload.bio)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author

# ---------- List Authors ----------
@router.get("/", response_model=list[AuthorOut])
def list_authors(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    authors = db.scalars(select(Author).order_by(Author.id).limit(limit).offset(offset)).all()
    return authors

# ---------- Get Author (with Books) ----------
@router.get("/{author_id}", response_model=AuthorWithBooks)
def get_author(
    author_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    author = db.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    # Load related books
    _ = author.books
    return author
