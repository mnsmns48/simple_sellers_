from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class StomatBase(DeclarativeBase):
    __abstract__ = True


class Stomat(StomatBase):
    __tablename__ = 'stomatology'
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    company: Mapped[str] = mapped_column(primary_key=True, unique=True)
    site: Mapped[str]
    med_service: Mapped[str]
    price: Mapped[int]
    date: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.now())