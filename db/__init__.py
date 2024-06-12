from os import getpid

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.future import select

from db.models import Base, BotSettings, Backup

__all__ = [
    "getpid",
    "ENGINE",
    "SESSION",
    "Base",
    "BotSettings",
    "Backup",
    "db_startup",
    "select"
]

ENGINE = create_async_engine("sqlite+aiosqlite:///IPVenom501.db")
SESSION = async_sessionmaker(ENGINE, autoflush=True, expire_on_commit=True)


async def db_startup():
    async with ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SESSION() as session:
        bot_settings = await session.scalar(select(BotSettings).filter_by(id=1))
        if bot_settings is None:
            bot_settings = BotSettings()
            session.add(bot_settings)
            await session.commit()
        backups = (await session.scalars(select(Backup).filter_by(id=1))).unique().all()
