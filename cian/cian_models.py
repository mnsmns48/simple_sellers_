from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from config import cian_settings


class CianModel(DeclarativeBase):
    __abstract__ = True


class Regions(CianModel):
    __tablename__ = cian_settings.table_reg
    id: Mapped[Optional[int]] = mapped_column(primary_key=True, unique=True)
    region: Mapped[str] = mapped_column(primary_key=True, unique=True)


class Data(CianModel):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    region: Mapped[str]
    location: Mapped[Optional[str]]
    type: Mapped[Optional[str]]
    title: Mapped[Optional[str]]
    specific: Mapped[Optional[str]]
    profit: Mapped[Optional[str]]
    price: Mapped[Optional[str]]
    address: Mapped[Optional[str]]
    desc: Mapped[Optional[str]]
    phone: Mapped[Optional[str]]
    img: Mapped[Optional[str]]
    link: Mapped[Optional[str]]
