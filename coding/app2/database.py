"""Database configuration and session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from typing import Generator


DATABASE_URL = "postgresql://fastapi_user:fastapi_pass@localhost:5433/fastapi_db"

engine = create_engine(DATABASE_URL, echo=True)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass


def get_db() -> Generator[Session, None, None]:
    """Dependency that provides database session."""
    with Session(engine) as session:
        yield session