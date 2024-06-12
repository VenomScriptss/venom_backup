from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from texts.bot.handlers import Start
from utils import CallbackData

router = Router()


@router.message(CommandStart())
@router.message(F.text.in_(Start.keywords))
async def start(message: Message, settings, state):
    td = await Start.create(settings)
    await message.answer(
        text=td.text,
        reply_markup=td.keyboard,
    )
    await state.clear()


@router.callback_query(CallbackData(Start.data).auto_filter())
async def start(callback_query: CallbackQuery, settings):
    dt = await Start.create(settings)
    await callback_query.message.delete()
    await callback_query.message.answer(
        text=dt.text,
        reply_markup=dt.keyboard,
    )
