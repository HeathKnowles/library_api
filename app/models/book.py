from datetime import date, datetime
from sqlalchemy import String, Integer, Boolean, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    publication_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    author: Mapped["Author"] = relationship("Author", back_populates="books")
    borrows: Mapped[list["BorrowRecord"]] = relationship("BorrowRecord", back_populates="book")

    def __repr__(self):
        return f"<Book(title='{self.title}', author_id={self.author_id})>"
