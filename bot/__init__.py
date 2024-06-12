from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

from db.env import getenv

BOT = Bot(
    token=getenv('BOT_TOKEN'),
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    ),
    session=AiohttpSession(proxy=getenv('BOT_PROXY')),
)
