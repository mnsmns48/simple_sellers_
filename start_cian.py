import asyncio
from datetime import datetime

from asyncpg import InvalidCatalogNameError

from cian.cian_models import CianModel
from cian.logic_cian import cian_parsing
from config import cian_settings
from engine import cian_db, create_db


async def cianstart():
    try:
        async with cian_db.engine.begin() as async_connect:
            await async_connect.run_sync(CianModel.metadata.create_all)
    except InvalidCatalogNameError:
        await create_db(new_db=cian_settings.database)
        async with cian_db.engine.begin() as async_connect:
            await async_connect.run_sync(CianModel.metadata.create_all)
    await cian_parsing()


if __name__ == "__main__":
    try:
        print('script started', datetime.now())
        asyncio.run(cianstart())
    except (KeyboardInterrupt, SystemExit):
        print('script stopped')
