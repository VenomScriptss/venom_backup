from contextlib import suppress
from datetime import datetime
from uuid import uuid4

from aiogram import Router, F
from aiogram.types import InlineQuery, InlineQueryResultCachedDocument
from jdatetime import datetime as jdatetime
from sqlalchemy.future import select

from db import SESSION
from db.models import Backup

router = Router()


# j date time
@router.inline_query(F.query.startswith("1"))
async def jdate_backup_search(inline_query: InlineQuery):
    with suppress(Exception):
        dt = jdatetime.fromisoformat(inline_query.query)
    async with SESSION() as session:
        backup_files = await session.scalars(
            select(Backup)
            .where(Backup.timestamp <= dt.timestamp())
            .order_by(Backup.timestamp.desc())
            .limit(50)
        )

        backup_files = backup_files.unique().all()
        if len(backup_files) == 0:
            return
    results = []
    for backup_file in backup_files:
        file_dt = jdatetime.fromtimestamp(backup_file.timestamp).strftime(
            "%Y/%m/%d %H:%M:%S")
        results.append(

            InlineQueryResultCachedDocument(
                id=str(uuid4()),
                title=file_dt,
                document_file_id=backup_file.id,
                discription="برای ارسال کلیک کنید",
                caption=f"این فایل در تاریخ {file_dt} ساخته شده."
            )
        )
    await inline_query.answer(results, cache_time=1)


# date time
@router.inline_query(F.query.startswith("2"))
async def date_backup_search(inline_query: InlineQuery):
    with suppress(Exception):
        dt = datetime.fromisoformat(inline_query.query)
    async with SESSION() as session:
        backup_files = await session.scalars(
            select(Backup)
            .where(Backup.timestamp <= dt.timestamp())
            .order_by(Backup.timestamp.desc())
            .limit(50)
        )
        backup_files = backup_files.unique().all()
        if len(backup_files) == 0:
            return
    results = []
    for backup_file in backup_files:
        file_dt = datetime.fromtimestamp(backup_file.timestamp).strftime(
            "%Y/%m/%d %H:%M:%S")
        results.append(
            InlineQueryResultCachedDocument(id=str(backup_file.id),
                                            title=file_dt, document_file_id=backup_file.id,
                                            description="for send click here",
                                            caption=f"📅 This file was created on {file_dt}.")
        )
    await inline_query.answer(results)
