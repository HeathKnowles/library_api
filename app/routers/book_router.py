from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_, join

from app.db.session import get_db
from app.models.book import Book
from app.models.author import Author
from app.schemas.book_schema import BookCreate, BookUpdate, BookOut
from app.core.security import get_current_user

router = APIRouter()

# ---------- Create Book ----------
@router.post("/", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(
    payload: BookCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    author = db.get(Author, payload.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    book = Book(
        title=payload.title,
        author_id=payload.author_id,
        publication_date=payload.publication_date,
        is_available=True,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

# ---------- List Books (Search & Filter) ----------
@router.get("/", response_model=list[BookOut])
def list_books(
    q: str | None = Query(None, description="Search title or author"),
    author_id: int | None = Query(None, ge=1),
    available: bool | None = Query(None),
    pub_from: date | None = Query(None),
    pub_to: date | None = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    stmt = select(Book).where(Book.deleted_at.is_(None))
    if available is not None:
        stmt = stmt.where(Book.is_available == available)
    if author_id:
        stmt = stmt.where(Book.author_id == author_id)
    if pub_from:
        stmt = stmt.where(Book.publication_date >= pub_from)
    if pub_to:
        stmt = stmt.where(Book.publication_date <= pub_to)

    if q:
        j = join(Book, Author, Book.author_id == Author.id)
        stmt = (
            select(Book)
            .select_from(j)
            .where(
                and_(
                    Book.deleted_at.is_(None),
                    or_(
                        Book.title.ilike(f"%{q}%"),
                        Author.name.ilike(f"%{q}%"),
                    ),
                )
            )
        )

    stmt = stmt.order_by(Book.id).limit(limit).offset(offset)
    return db.scalars(stmt).all()

# ---------- Get Book ----------
@router.get("/{book_id}", response_model=BookOut)
def get_book(
    book_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    book = db.get(Book, book_id)
    if not book or book.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# ---------- Update Book ----------
@router.patch("/{book_id}", response_model=BookOut)
def update_book(
    book_id: int,
    payload: BookUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    book = db.get(Book, book_id)
    if not book or book.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Book not found")

    if payload.author_id:
        if not db.get(Author, payload.author_id):
            raise HTTPException(status_code=404, detail="Author not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(book, field, value)

    db.add(book)
    db.commit()
    db.refresh(book)
    return book

# ---------- Delete Book ----------
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_user),
):
    book = db.get(Book, book_id)
    if not book or book.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Book not found")

    if not book.is_available:
        raise HTTPException(status_code=409, detail="Cannot delete a borrowed book")

    book.deleted_at = date.today()
    db.add(book)
    db.commit()
    return
