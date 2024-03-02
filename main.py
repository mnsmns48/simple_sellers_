import asyncio
from asyncpg import InvalidCatalogNameError
from dobrotsen.config import hidden
from dobrotsen.crud import get_links_from_db
from engine import db, create_db
from dobrotsen.logic import write_dobrotsen_menu, pars_links
from dobrotsen.models import Base, Dobrotsen


async def main():
    try:
        async with db.engine.begin() as async_connect:
            await async_connect.run_sync(Base.metadata.create_all)
    except InvalidCatalogNameError:
        await asyncio.create_task(create_db())
        async with db.engine.begin() as async_connect:
            await async_connect.run_sync(Base.metadata.create_all)
    # await write_dobrotsen_menu(url=hidden.url)
    await pars_links()


if __name__ == "__main__":
    asyncio.run(main())
