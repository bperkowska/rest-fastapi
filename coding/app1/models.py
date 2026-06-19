"""SQLAlchemy ORM models."""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Task(Base):
    """Task model."""
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    def __repr__(self):
        return f"<Task(id={self.id}, name='{self.name}')>"
