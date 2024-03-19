import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from asyncpg import InvalidCatalogNameError
from dobrotsen.config_dobrotsen import hidden
from engine import db, create_db
from dobrotsen.logic import write_dobrotsen_menu, pars_links
from dobrotsen.models_dobrotsen import Base


async def refresh_db():
    async with db.engine.begin() as async_connect:
        await async_connect.run_sync(Base.metadata.drop_all)
    print('Таблица удалена')
    try:
        async with db.engine.begin() as async_connect:
            await async_connect.run_sync(Base.metadata.create_all)
    except InvalidCatalogNameError:
        await create_db(new_db=hidden.db_name)
        async with db.engine.begin() as async_connect:
            await async_connect.run_sync(Base.metadata.create_all)
    await write_dobrotsen_menu(url=hidden.url)
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
