from asyncio import sleep
from warnings import warn

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.future import select

from db import BotSettings, SESSION
from error_handler import handle_error
from .save_files import save_backup


async def run_all():
    scheduler = AsyncIOScheduler()

    async def dynamic_interval_job():

        async with SESSION() as session:
            settings = await session.scalar(
                select(BotSettings)
            )

        job.reschedule(trigger=IntervalTrigger(minutes=settings.backup_interval))
        try:
            await save_backup()
            # Update the job with the new interval
        except Exception as e:
            await handle_error(type(e), e, e.__traceback__)

    while True:
        async with SESSION() as session:
            settings = await session.scalar(
                select(BotSettings)
            )
        if settings.backup_interval is None:
            warn('Backup interval is set to 0, disabling backup')
            await sleep(60)
            continue
        break

    job = scheduler.add_job(dynamic_interval_job, 'interval', minutes=0.1)
    scheduler.start()
