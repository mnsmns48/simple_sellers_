from sqlalchemy import select, Result, text
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
    subq1 = select(table.parent).scalar_subquery()
    q1 = select(table.link, table.parent).filter(table.id.not_in(subq1))
    q2 = select(table.link, table.parent).filter(table.parent != 0)
    query = q1.union(q2).order_by(text("1"))
    result: Result = await session.execute(query)
    for line in result.fetchall():
        result_dict.update(
            {
                line[0]: line[1]
            }
        )
    return result_dict
