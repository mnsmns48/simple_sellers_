from sqlalchemy import select, Result
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept


async def write_data(session: AsyncSession, table: DeclarativeAttributeIntercept, data: list | dict):
    await session.execute(
        insert(table).values(data).on_conflict_do_nothing()
    )
    await session.commit()


async def get_links_from_db(session: AsyncSession, table: DeclarativeAttributeIntercept) -> dict:
    result_dict = dict()
    query = select(table.link, table.id).filter(table.parent != 0)
    result: Result = await session.execute(query)
    for line in result.fetchall():
        result_dict.update(
            {
                line[0]: line[1]
            }
        )
    return result_dict
