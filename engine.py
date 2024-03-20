from asyncio import current_task
from contextlib import asynccontextmanager

import asyncpg
from sqlalchemy import NullPool, URL
from sqlalchemy.ext.asyncio import async_scoped_session, AsyncSession, async_sessionmaker, create_async_engine

from config import general_settings, dobrotsen_settings, Settings


def get_url(settings: Settings) -> URL:
    url_object = URL.create(
        drivername=settings.driver_name,
        username=settings.username,
        password=settings.password.get_secret_value(),
        host=settings.host,
        database=settings.database,
        port=settings.port
    )
    return url_object


class DataBase:
    def __init__(self, url: URL, echo: bool = False):
        self.engine = create_async_engine(
            url=url,

            echo=echo,
            poolclass=NullPool
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def scoped_session(self) -> AsyncSession:
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        try:
            async with session() as s:
                yield s
        finally:
            await session.remove()


async def create_db(new_db: str):
    conn = await asyncpg.connect(database='postgres',
                                 user=general_settings.username,
                                 password=general_settings.password.get_secret_value(),
                                 host=general_settings.host,
                                 port=general_settings.port
                                 )
    sql = f'CREATE DATABASE "{new_db}"'
    await conn.execute(sql)
    await conn.close()
    print(f"DB <{new_db}> success created")


general_db = DataBase(get_url(general_settings), echo=True)
dobrotsen_db = DataBase(get_url(dobrotsen_settings), echo=dobrotsen_settings.echo)
