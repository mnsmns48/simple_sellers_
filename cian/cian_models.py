from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from config import cian_settings


class CianModel(DeclarativeBase):
    __abstract__ = True


class Regions(CianModel):
    __tablename__ = cian_settings.table_reg
    id: Mapped[Optional[int]] = mapped_column(primary_key=True, unique=True)
    region: Mapped[str] = mapped_column(primary_key=True, unique=True)
