from contextlib import suppress

from sqlalchemy.future import select

from bot import BOT
from db import BotSettings, SESSION
from texts.error_handler import Error


async def handle_error(exc_type, exc_value, _):
    print(exc_type)
    print(exc_value)
    async with SESSION() as session:
        settings = await session.scalar(
            select(BotSettings)
        )
    async for text in Error.message(exc_type, exc_value):
        with suppress(Exception):
            for admin in settings.admins:
                await BOT.send_message(
                    chat_id=admin,
                    text=text
                )
