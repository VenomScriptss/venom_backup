from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from texts.bot.handlers import Files
from utils import CallbackData

router = Router()


@router.message(F.text.in_(Files.keywords))
async def files(message: Message, settings):
    dt = await Files.create(settings)
    await message.answer(dt.text, reply_markup=dt.keyboard)


@router.callback_query(CallbackData(Files.data).auto_filter())
async def files(callback_query: CallbackQuery, settings, callback_data: CallbackData):
    await callback_query.answer()
    dt = await Files.create(settings, start=int(callback_data.attrs.start), end=int(callback_data.attrs.end))
    await callback_query.message.edit_text(dt.text, reply_markup=dt.keyboard)


@router.callback_query(CallbackData(Files.GetFile.data).auto_filter())
async def get_file(callback_query: CallbackQuery, settings, callback_data: CallbackData):
    # file = await callback_query.bot.get_file(file_id=callback_data.attrs.file_id)
    dt = await Files.GetFile.create(settings, file_timestamp=callback_data.attrs.timestamp)
    await callback_query.message.answer_document(callback_data.attrs.file_id, caption=dt.caption)
