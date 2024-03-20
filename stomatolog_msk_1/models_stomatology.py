from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import stomat_settings


class StomatBase(DeclarativeBase):
    __abstract__ = True


class Stomat(StomatBase):
    __tablename__ = stomat_settings.tablename
    company: Mapped[str] = mapped_column(primary_key=True)
    address: Mapped[str]
    site: Mapped[str]
    category: Mapped[Optional[str]]
    med_service: Mapped[str]
    price: Mapped[float]