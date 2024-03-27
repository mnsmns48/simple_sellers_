from sqlalchemy import delete, select, Result, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept


async def write_data(session: AsyncSession, table: DeclarativeAttributeIntercept, data: list | dict) -> None:
    await session.execute(
        insert(table).values(data).on_conflict_do_nothing()
    )
    await session.commit()


async def del_data(session: AsyncSession, table: DeclarativeAttributeIntercept, condition: str | None) -> None:
    await session.execute(
        delete(table).filter(table.c.price == condition)
    )
    await session.commit()


async def get_data(session: AsyncSession, table: DeclarativeAttributeIntercept):
    res = await session.execute(
        select(table).order_by(table.c.id)
    )
    return res.fetchall()


async def update_region(session: AsyncSession, table: DeclarativeAttributeIntercept, id_: int, region: str):
    await session.execute(
        update(table).filter(table.c.id == id_).values(region=region))
    await session.commit()
