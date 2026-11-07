from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB

class Base(DeclarativeBase): pass

class Document(Base):
    __tablename__ = 'documents'
    owner: Mapped[str] = mapped_column(String, primary_key=True)
    kind: Mapped[str] = mapped_column(String, primary_key=True)
    id: Mapped[str] = mapped_column(String, primary_key=True)
    revision: Mapped[int] = mapped_column(Integer, default=1)
    body: Mapped[dict] = mapped_column(JSONB)
