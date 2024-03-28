import asyncio
from datetime import datetime

from asyncpg import InvalidCatalogNameError

from alterainvest.models_altera import AlteraModel
from alterainvest.logic_altera import get_altera_links, altera_pars, altera_output
from config import altera_settings
from engine import altera_db, create_db


async def cianstart():
    print('PRESS 1 TO PARSE\nPRESS 2 TO OUTPUT RESULT')
    try:
        choice = int(input())
        if choice == 1:
            try:
                async with altera_db.engine.begin() as async_connect:
                    await async_connect.run_sync(AlteraModel.metadata.create_all)
            except InvalidCatalogNameError:
                await create_db(new_db=altera_settings.database)
                async with altera_db.engine.begin() as async_connect:
                    await async_connect.run_sync(AlteraModel.metadata.create_all)
            await altera_pars()
        elif choice == 2:
            await altera_output()
        else:
            print('INCORRECT INPUT')
    except ValueError:
        print('INCORRECT INPUT!! PRESS 1 OR 2')


if __name__ == "__main__":
    try:
        print('script started', datetime.now())
        asyncio.run(cianstart())
    except (KeyboardInterrupt, SystemExit):
        print('script stopped')
