from aiogram.utils.markdown import hbold, hpre
from sqlalchemy.future import select

from db import BotSettings, SESSION
from db.models import Language


class Error:
    @classmethod
    async def create_message(cls, error: Exception):

        async with SESSION() as session:
            settings = await session.scalar(
                select(BotSettings)
            )
        if settings.language == Language.en:
            text = f"""
❌ An error occurred while performing the operation.

Error Type: {hbold(type(error).__name__)}
Error Message: {hpre(str(error))}
"""
        else:
            text = f"""
❌ خطا در انجام عملیات.

نوع خطا: {hbold(type(error).__name__)}
پیام خطا: {hpre(str(error))}
"""
        for i in range(0, len(text), 1024):
            yield text[i:i + 1024]

    @classmethod
    async def message(cls, exc_type, exc_value):
        async with SESSION() as session:
            settings = await session.scalar(
                select(BotSettings)
            )
        if settings.language == Language.en:
            text = f"""
❌ An error occurred while performing the operation.

Error Type: {hbold(exc_type.__name__)}
Error Message: {hpre(str(exc_value))}
"""
        else:
            text = f"""
❌ خطا در انجام عملیات.

نوع خطا: {hbold(exc_type.__name__)}
پیام خطا: {hpre(str(exc_value))}
"""
        for i in range(0, len(text), 1024):
            yield text[i:i + 1024]
