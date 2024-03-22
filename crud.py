from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept


async def write_data(session: AsyncSession, table: DeclarativeAttributeIntercept, data: list | dict):
    await session.execute(
        insert(table).values(data).on_conflict_do_nothing()
    )
    await session.commit()


async def del_data(session: AsyncSession, table: DeclarativeAttributeIntercept, condition: str | None):
    await session.execute(
        delete(table).filter(table.c.price == condition)
    )
    await session.commit()
