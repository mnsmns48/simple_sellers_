from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from config import altera_settings


class AlteraModel(DeclarativeBase):
    __abstract__ = True


class Links(AlteraModel):
    __tablename__ = altera_settings.table_links
    id: Mapped[Optional[int]] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    category: Mapped[str] = mapped_column(unique=True)
    link: Mapped[str] = mapped_column(unique=True)


class Data(AlteraModel):
    __tablename__ = altera_settings.table_data
    id: Mapped[Optional[int]] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    category: Mapped[str]
    title: Mapped[Optional[str]]
    city: Mapped[Optional[str]]
    date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=False))
    price: Mapped[Optional[str]]
    profit: Mapped[Optional[str]]
    payback: Mapped[Optional[str]]
    confirm: Mapped[Optional[str]]
    link: Mapped[str]
