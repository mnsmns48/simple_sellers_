import asyncio
from datetime import datetime

from asyncpg import InvalidCatalogNameError

from engine import db, create_db
from stomatolog_msk_1.config_stomatology import hidden_s
from stomatolog_msk_1.models_stomatology import StomatBase


async def main():
    try:
        async with db.engine.begin() as async_connect:
            await async_connect.run_sync(StomatBase.metadata.create_all)
    except InvalidCatalogNameError:
        await create_db(new_db=hidden_s.db_name)
        async with db.engine.begin() as async_connect:
            await async_connect.run_sync(StomatBase.metadata.create_all)


if __name__ == "__main__":
    try:
        print('script started', datetime.now())
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('script stopped')
