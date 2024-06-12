from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from sqlalchemy.future import select

from db import SESSION, BotSettings
from db.models import Language
from texts.bot.handlers import Settings
from utils import CallbackData

router = Router()


class BaseStates(StatesGroup):
    backup_interval = State()


@router.message(F.text.in_(Settings.keywords))
async def settings(message: Message, settings):
    dt = await Settings.create(settings)
    await message.answer(dt.text, reply_markup=dt.keyboard)


@router.callback_query(CallbackData(Settings.data).auto_filter())
async def settings(callback_query: CallbackQuery, settings):
    await callback_query.message.delete()
    dt = await Settings.create(settings)
    await callback_query.message.answer(dt.text, reply_markup=dt.keyboard)


@router.message(F.text.in_(Settings.Language.keywords))
async def language(message: Message, settings):
    dt = await Settings.Language.create(settings)
    pre = await message.answer(
        text=dt.text,
        reply_markup=ReplyKeyboardRemove()
    )
    await pre.delete()
    await message.answer(dt.text, reply_markup=dt.keyboard)


@router.callback_query(CallbackData("select-lang").auto_filter())
async def language(callback_query: CallbackQuery, settings, callback_data: CallbackData):
    await callback_query.answer()
    async with SESSION() as session:
        settings = await session.scalar(
            select(
                BotSettings
            )
        )
        if settings.language == Language(callback_data.attrs.language):
            return
        settings.language = Language(callback_data.attrs.language)
        await session.commit()
        await session.refresh(settings)
    dt = await Settings.Language.create(settings)
    await callback_query.message.edit_text(dt.text, reply_markup=dt.keyboard)


@router.message(F.chat_shared)
async def set_backup_group(message: Message):
    async with SESSION() as session:
        settings = await session.scalar(
            select(
                BotSettings
            )
        )
        settings.backup_chat_id = message.chat_shared.chat_id
        await session.commit()
        await session.refresh(settings)

    dt = await Settings.BackupChannel.create(settings, message.chat_shared)
    await message.answer(dt.text)


@router.message(F.text.in_(Settings.Admins.keywords))
async def admins(message: Message, settings):
    dt = await Settings.Admins.create(settings)
    await message.answer(dt.text, reply_markup=dt.keyboard)


@router.callback_query(CallbackData(Settings.Admins.AddAdmin.data).auto_filter())
async def admins(callback_query: CallbackQuery, settings, callback_data: CallbackData):
    await callback_query.message.delete()
    dt = await Settings.Admins.AddAdmin.create(settings)
    await callback_query.message.answer(dt.text, reply_markup=dt.keyboard)


@router.message(F.user_shared)
async def add_admin(message: Message):
    async with SESSION() as session:
        settings = await session.scalar(
            select(
                BotSettings
            )
        )
        settings._admins = settings._admins + [
            message.user_shared.user_id] if message.user_shared.user_id not in settings._admins else settings._admins
        await session.commit()
        await session.refresh(settings)
    dt = await Settings.Admins.AddAdmin.Add.create(settings, message.user_shared)
    await message.answer(dt.text)


@router.callback_query(CallbackData("remove-admin").auto_filter())
async def remove_admin(callback_query: CallbackQuery, settings, callback_data: CallbackData):
    await callback_query.answer()
    async with SESSION() as session:
        settings = await session.scalar(
            select(
                BotSettings
            )
        )
        settings._admins = [admin for admin in settings._admins if admin != int(callback_data.attrs.admin)]

        await session.commit()
        await session.refresh(settings)
    dt = await Settings.Admins.create(settings)
    await callback_query.message.edit_text(dt.text, reply_markup=dt.keyboard)


@router.message(F.text.in_(Settings.BackupInterval.keywords))
async def backup_channel(message: Message, settings, state: FSMContext):
    dt = await Settings.BackupInterval.create(settings)
    await message.answer(dt.text, reply_markup=dt.keyboard)
    await state.set_state(BaseStates.backup_interval)


@router.message(BaseStates.backup_interval)
async def backup_channel(message: Message, settings, state: FSMContext):
    async with SESSION() as session:
        settings = await session.scalar(
            select(
                BotSettings
            )
        )
        settings.backup_interval = int(message.text)
        await session.commit()
        await session.refresh(settings)

    dt = await Settings.create(settings)
    await message.answer(dt.text, reply_markup=dt.keyboard)
    await state.clear()
