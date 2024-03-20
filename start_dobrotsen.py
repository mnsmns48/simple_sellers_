import asyncio
from datetime import datetime
from asyncpg import InvalidCatalogNameError
from config import dobrotsen_settings
from engine import dobrotsen_db, create_db
from dobrotsen.logic import write_dobrotsen_menu, pars_links
from dobrotsen.models_dobrotsen import DobroBase


async def refresh_db():
    try:
        async with dobrotsen_db.engine.begin() as async_connect:
            await async_connect.run_sync(DobroBase.metadata.drop_all)
        print('Таблица удалена')
        async with dobrotsen_db.engine.begin() as async_connect:
            await async_connect.run_sync(DobroBase.metadata.create_all)
    except InvalidCatalogNameError:
        await create_db(new_db=dobrotsen_settings.database)
        async with dobrotsen_db.engine.begin() as async_connect:
            await async_connect.run_sync(DobroBase.metadata.create_all)
    await write_dobrotsen_menu(url=dobrotsen_settings.url)
    await pars_links()


# async def main():
#     scheduler = AsyncIOScheduler()
#     trigger = CronTrigger(
#         year="*", month="*", day="*", hour="03", minute="29", second="0"
#     )
#     scheduler.add_job(func=refresh_db, trigger=trigger)
#     scheduler.start()
#     while True:
#         await asyncio.sleep(1000)


if __name__ == "__main__":
    try:
        print('script started', datetime.now())
        asyncio.run(refresh_db())
    except (KeyboardInterrupt, SystemExit):
        print('script stopped')
