import asyncio
import time
from datetime import datetime
from asyncpg import InvalidCatalogNameError
from engine import stomat_db, create_db

from config import stomat_settings
from stomatolog_msk_1.logic_stom_1 import work, output
from stomatolog_msk_1.models_stomatology import Stomat


async def main():
    print('PRESS 1 TO PARSE\nPRESS 2 TO OUTPUT RESULT')
    try:
        choice = int(input())
        if choice == 1:
            try:
                async with stomat_db.engine.begin() as async_connect:
                    await async_connect.run_sync(Stomat.metadata.create_all)
            except InvalidCatalogNameError:
                await create_db(new_db=stomat_settings.database)
                async with stomat_db.engine.begin() as async_connect:
                    await async_connect.run_sync(Stomat.metadata.create_all)

            await work()
        elif choice == 2:
            await output()
        else:
            print('INCORRECT INPUT')
    except ValueError:
        print('INCORRECT INPUT!! PRESS 1 OR 2')


if __name__ == "__main__":
    try:
        start = time.time()
        print('script started', datetime.now())
        asyncio.run(main())
        print(f"Скрипт завершен за {int(time.time() - start)} секунд")
    except (KeyboardInterrupt, SystemExit):
        print('script stopped')
