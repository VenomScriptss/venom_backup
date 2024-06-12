from aiogram import Router, BaseMiddleware
from sqlalchemy.future import select

from db import BotSettings, SESSION
from .files import router as files_router
from .search import router as search_router
from .settings import router as settings_router
from .start import router as start_router


class AMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler,
            event,
            data
    ):
        async with SESSION() as session:
            settings = await session.scalar(
                select(BotSettings)
            )
        if event.from_user.id in settings.admins:
            data["settings"] = settings
            await handler(event, data)


router = Router(
    name="main[handlers]"
)
router.message.middleware(AMiddleware())
router.callback_query.middleware(AMiddleware())
router.inline_query.middleware(AMiddleware())
router.include_routers(
    files_router,
    start_router,
    settings_router,
    search_router
)
