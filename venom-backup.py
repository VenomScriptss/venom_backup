import logging
import sys
import warnings
from asyncio import get_event_loop

from aiogram import Dispatcher
from aiogram.types import ErrorEvent

from bot import BOT
from bot.handlers import router
from db import db_startup
from error_handler import handle_error
from workers import run_all

loop = get_event_loop()
dp = Dispatcher()
dp.include_router(
    router
)


@dp.errors()
async def on_error(exception: ErrorEvent):
    await handle_error(type(exception.exception), exception.exception, exception.exception.__traceback__)


async def main():
    # await run_all()
    await dp.start_polling(BOT)


def handle_exception(loop, context):
    exception = context.get("exception")
    if exception:
        loop.create_task(handle_error(type(exception), exception, exception.__traceback__))


logging.basicConfig(level=logging.INFO)
loop.run_until_complete(db_startup())
warnings.showwarning = lambda message, category, filename, lineno, file=None, line=None: loop.create_task(
    handle_error(category, message, filename)).result()
sys.excepthook = lambda exc_type, exc_value, exc_traceback: loop.run_until_complete(
    handle_error(exc_type, exc_value, exc_traceback))
loop.set_exception_handler(handle_exception)
loop.create_task(run_all())
loop.run_until_complete(main())
