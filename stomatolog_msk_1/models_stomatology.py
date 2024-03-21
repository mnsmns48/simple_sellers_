from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import stomat_settings


class StomatBase(DeclarativeBase):
    __abstract__ = True


class Stomat(StomatBase):
    __tablename__ = stomat_settings.tablename
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    company: Mapped[str]
    address: Mapped[str]
    site: Mapped[str]
    category: Mapped[Optional[str]]
    med_service: Mapped[Optional[str]]
    price: Mapped[Optional[str]]
    price_promo: Mapped[Optional[str]]
