from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.models.book import Book
from app.models.borrow import BorrowRecord
from app.schemas.borrow_schema import BorrowCreate, BorrowOut
from app.core.security import get_current_user

router = APIRouter()

# ---------- Borrow a Book ----------
@router.post("/", response_model=BorrowOut, status_code=status.HTTP_201_CREATED)
def borrow_book(
    payload: BorrowCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    book = db.get(Book, payload.book_id)
    if not book or book.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book.is_available:
        raise HTTPException(status_code=409, detail="Book already borrowed")

    borrow = BorrowRecord(
        user_id=current_user.id,
        book_id=book.id,
        borrowed_at=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=payload.days),
    )
    book.is_available = False
    db.add_all([borrow, book])
    db.commit()
    db.refresh(borrow)
    return borrow

# ---------- Return a Book ----------
@router.post("/return/{record_id}", response_model=BorrowOut)
def return_book(
    record_id: int = Path(..., ge=1),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = db.get(BorrowRecord, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    if record.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your record")
    if record.returned_at:
        raise HTTPException(status_code=409, detail="Book already returned")

    record.returned_at = datetime.utcnow()
    book = db.get(Book, record.book_id)
    if book:
        book.is_available = True

    db.add_all([record, book])
    db.commit()
    db.refresh(record)
    return record

# ---------- Borrowing History ----------
@router.get("/history", response_model=list[BorrowOut])
def borrow_history(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    stmt = (
        select(BorrowRecord)
        .where(BorrowRecord.user_id == current_user.id)
        .order_by(BorrowRecord.borrowed_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return db.scalars(stmt).all()
