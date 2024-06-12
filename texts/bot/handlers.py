from datetime import datetime
from typing import Optional

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, \
    KeyboardButtonRequestChat, ChatAdministratorRights, ChatShared, UserShared, \
    KeyboardButtonRequestUser
from aiogram.utils.markdown import hbold
from jdatetime import datetime as jdatetime

from db import BotSettings, SESSION, select, Backup
from db.models import Language
from utils import CallbackData


class Start:
    data = "start"
    keywords = [
        "🏘"
    ]
    text: str
    keyboard: ReplyKeyboardMarkup

    def __init__(self, text: str, keyboard: ReplyKeyboardMarkup):
        self.text = text
        self.keyboard = keyboard

    @classmethod
    async def create(cls, settings: BotSettings):
        if settings.language == Language.en:
            text = hbold("""
👋 Welcome, Admin!

You can manage the bot using the buttons below. 🚀
""")
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(
                            text="Files | 🗂"
                        ),
                        KeyboardButton(
                            text="⚙️ | Settings"
                        )
                    ]
                ],
                resize_keyboard=True
            )
        else:
            text = hbold("""
👋 خوش آمدید، مدیر!

از دکمه های زیر برای مدیریت ربات استفاده کنید. 🚀
""")
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(
                            text="🗂 | فایل"
                        ),
                        KeyboardButton(
                            text="تنظیمات | ⚙️"
                        )
                    ]
                ],
                resize_keyboard=True
            )
        return cls(text=text, keyboard=keyboard)


class Files:
    data = "files"
    keywords = [
        "Files | 🗂",
        "🗂 | فایل"
    ]
    text: str
    keyboard: InlineKeyboardMarkup

    def __init__(self, text: str, keyboard: Optional[InlineKeyboardMarkup]):
        self.text = text
        self.keyboard = keyboard

    @classmethod
    async def create(
            cls,
            settings: BotSettings,
            start: int = 0,
            end: int = 10
    ):
        async with SESSION() as session:
            backup_files = await session.scalars(
                select(
                    Backup
                )
                .order_by(Backup.timestamp.desc())
            )
            backup_files = backup_files.unique().all()
        if not backup_files:
            if settings.language == Language.en:
                text = hbold("❌ | No backups found")
                keyboard = None
            else:
                text = hbold("❌ | هیچ بکاپی یافت نشد")
                keyboard = None
            return cls(text=text, keyboard=keyboard)
        if start >= (files_count := len(backup_files)):
            start = 0
            end = 9
        if end > files_count:
            end = files_count
        if settings.language == Language.en:
            dt = datetime
        else:
            dt = jdatetime
        keys = [
            [
                InlineKeyboardButton(
                    text=f"total: {files_count}",
                    callback_data="none"
                )
            ]
        ]
        for file in backup_files[start:end]:
            keys.append(
                [
                    InlineKeyboardButton(
                        text=f"{dt.fromtimestamp(file.timestamp).strftime('%Y-%m-%d %H:%M:%S')}",
                        callback_data=await CallbackData("get-file", file_id=file.id, timestamp=file.timestamp).pack()
                    )
                ]
            )

        last_row = []
        next_start = end if end != files_count else 0
        prev_start = (start - 10 if start - 10 >= 0 else 0) if start != 0 else files_count - (
            files_count % 10 if files_count % 10 != 0 else 10) if files_count >= 10 else 0
        next_end = (end + 10 if end + 10 <= files_count else files_count) if end != files_count else 10
        prev_end = prev_start + 10 if prev_start + 10 <= files_count else files_count

        last_row.append(
            InlineKeyboardButton(
                text=f"⬅️",
                callback_data=await CallbackData("files", start=prev_start, end=prev_end).pack())
        )

        current_page = end // 10
        if end % 10 != 0:
            current_page += 1
        max_page = files_count // 10
        if files_count % 10 != 0:
            max_page += 1

        available_pages = [num for num in range(1, max_page + 1)]
        if len(available_pages) in [0, 1]:
            last_row.append(
                InlineKeyboardButton(
                    text=f"«{current_page}»",
                    callback_data=await CallbackData("none").pack()
                )
            )
        elif len(available_pages) == 2:
            available_pages.remove(current_page)
            if current_page < available_pages[0]:
                last_row.append(
                    InlineKeyboardButton(
                        text=f"«{current_page}»",
                        callback_data=await CallbackData("none").pack()
                    )
                )
                last_row.append(
                    InlineKeyboardButton(
                        text=str(available_pages[0]),
                        callback_data=await CallbackData("files", start=next_start, end=next_end).pack()
                    )
                )
            else:
                last_row.append(
                    InlineKeyboardButton(
                        text=str(available_pages[0]),
                        callback_data=await CallbackData("files", start=prev_start, end=prev_end).pack()
                    )
                )
                last_row.append(
                    InlineKeyboardButton(
                        text=f"«{current_page}»",
                        callback_data=await CallbackData("none").pack()
                    )
                )
        elif len(available_pages) >= 3:
            available_pages.remove(current_page)
            first_page = current_page if current_page == 1 else current_page - 1
            second_page = current_page if current_page == max_page else current_page + 1
            if current_page == 1:
                next_start1 = next_end if next_end != files_count else 0
                next_end1 = (
                    next_end + 10 if next_end + 10 <= files_count else files_count) if next_end != files_count else 10
                last_row.append(
                    InlineKeyboardButton(
                        text=f"«{current_page}»",
                        callback_data=await CallbackData("none").pack()
                    )
                )
                last_row.append(
                    InlineKeyboardButton(
                        text=str(current_page + 1),
                        callback_data=await CallbackData("files", start=next_start, end=next_end).pack()
                    )
                )
                last_row.append(
                    InlineKeyboardButton(
                        text=str(current_page + 2),
                        callback_data=await CallbackData("files", start=next_start1, end=next_end1).pack()
                    )
                )
            elif current_page == max_page:
                prev_start1 = start - 20
                prev_end1 = end - 20
                last_row.append(
                    InlineKeyboardButton(
                        text=str(current_page - 2),
                        callback_data=await CallbackData("files", start=prev_start1, end=prev_end1).pack()
                    )
                )
                last_row.append(
                    InlineKeyboardButton(
                        text=str(current_page - 1),
                        callback_data=await CallbackData("files", start=prev_start, end=prev_end).pack()
                    )
                )
                last_row.append(
                    InlineKeyboardButton(
                        text=f"«{current_page}»",
                        callback_data=f"none"
                    )
                )
            else:
                last_row.append(
                    InlineKeyboardButton(
                        text=str(current_page - 1),
                        callback_data=await CallbackData("files", start=prev_start, end=prev_end).pack()
                    )
                )
                last_row.append(
                    InlineKeyboardButton(
                        text=f"«{current_page}»",
                        callback_data=f"none"
                    )
                )
                last_row.append(
                    InlineKeyboardButton(
                        text=str(current_page + 1),
                        callback_data=await CallbackData("files", start=next_start, end=next_end).pack()
                    )
                )

        last_row.append(
            InlineKeyboardButton(
                text=f"➡️",
                callback_data=await CallbackData("files", start=next_start, end=next_end).pack()
            )
        )
        keys.append(last_row)
        if settings.language == Language.en:
            text = hbold("📅 Please select the desired date to receive the files of that date. 📂")
            keys.append(
                [
                    InlineKeyboardButton(
                        text="🔙 Back",
                        callback_data=await CallbackData("start").pack()
                    )
                ]
            )
        else:
            text = hbold("📅 لطفاً تاریخ مورد نظر را برای دریافت فایل های آن انتخاب کنید. 📂")
            keys.append(
                [
                    InlineKeyboardButton(
                        text="🔙 بازگشت",
                        callback_data=await CallbackData("start").pack()
                    )
                ]
            )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=keys
        )
        return cls(text=text, keyboard=keyboard)

    class GetFile:
        data = "get-file"
        caption: str
        keyboard: ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text="🏘",
                    )
                ]
            ],
            resize_keyboard=True
        )

        def __init__(self, caption: str):
            self.caption = caption

        @classmethod
        async def create(
                cls,
                settings: BotSettings,
                file_timestamp: int
        ):
            if settings.language == Language.en:
                dt = datetime.fromtimestamp(file_timestamp).strftime("%Y-%m-%d %H:%M:%S")
                text = hbold(f"📅 This file was created on {dt}.")
            else:
                dt = jdatetime.fromtimestamp(file_timestamp).strftime("%H:%M:%S %d-%m-%Y")
                text = hbold(f"📅 این فایل در تاریخ {dt} ایجاد شده است.")

            return cls(caption=text)


class Settings:
    data = "settings"
    keywords = [
        "تنظیمات | ⚙️",
        "⚙️ | Settings"
    ]
    text: str
    keyboard: ReplyKeyboardMarkup

    def __init__(self, text: str, keyboard: ReplyKeyboardMarkup):
        self.text = text
        self.keyboard = keyboard

    @classmethod
    async def create(
            cls,
            settings: BotSettings
    ):
        if settings.language == Language.en:
            text = hbold("⚙️ Settings")
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(
                            text="Language | 〽️"
                        ),
                        KeyboardButton(
                            text="♻️ | Backup Channel",
                            request_chat=KeyboardButtonRequestChat(
                                request_id=1,
                                chat_is_channel=True,
                                user_administrator_rights=ChatAdministratorRights(
                                    is_anonymous=False,
                                    can_manage_chat=True,
                                    can_delete_messages=False,
                                    can_restrict_members=False,
                                    can_promote_members=False,
                                    can_change_info=False,
                                    can_invite_users=False,
                                    can_post_stories=False,
                                    can_edit_stories=False,
                                    can_delete_stories=False,
                                    can_manage_video_chats=False
                                ),
                                bot_administrator_rights=ChatAdministratorRights(
                                    is_anonymous=False,
                                    can_manage_chat=True,
                                    can_delete_messages=False,
                                    can_restrict_members=False,
                                    can_promote_members=False,
                                    can_change_info=False,
                                    can_invite_users=False,
                                    can_post_stories=False,
                                    can_edit_stories=False,
                                    can_delete_stories=False,
                                    can_manage_video_chats=False
                                ),
                                request_title=True,
                                request_username=True
                            )
                        )
                    ],
                    [
                        KeyboardButton(
                            text="Backup Interval | 🛄"
                        ),
                        KeyboardButton(
                            text="👨‍💻 | Admins"
                        )
                    ],
                    [
                        KeyboardButton(
                            text="🏘"
                        )
                    ]
                ],
                resize_keyboard=True
            )
        else:
            text = hbold("⚙️ تنظیمات")
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(
                            text="زبان | 〽️"
                        ),
                        KeyboardButton(
                            text="♻️ | کانال بکاپ",
                            request_chat=KeyboardButtonRequestChat(
                                request_id=1,
                                chat_is_channel=True,
                                user_administrator_rights=ChatAdministratorRights(
                                    is_anonymous=False,
                                    can_manage_chat=True,
                                    can_delete_messages=False,
                                    can_restrict_members=False,
                                    can_promote_members=False,
                                    can_change_info=False,
                                    can_invite_users=False,
                                    can_post_stories=False,
                                    can_edit_stories=False,
                                    can_delete_stories=False,
                                    can_manage_video_chats=False,
                                    can_post_messages=True,
                                    can_edit_messages=True
                                ),
                                bot_administrator_rights=ChatAdministratorRights(
                                    is_anonymous=False,
                                    can_manage_chat=True,
                                    can_delete_messages=False,
                                    can_restrict_members=False,
                                    can_promote_members=False,
                                    can_change_info=False,
                                    can_invite_users=False,
                                    can_post_stories=False,
                                    can_edit_stories=False,
                                    can_delete_stories=False,
                                    can_manage_video_chats=False,
                                    can_post_messages=True,
                                    can_edit_messages=True
                                ),
                                request_title=True,
                                request_username=True
                            )
                        )
                    ],
                    [
                        KeyboardButton(
                            text="تاخیر بکاپ | 🛄"
                        ),
                        KeyboardButton(
                            text="👨‍💻 | ادمین ها"
                        )
                    ],
                    [
                        KeyboardButton(
                            text="🏘"
                        )
                    ]
                ],
                resize_keyboard=True
            )
        return cls(text=text, keyboard=keyboard)

    class Language:
        keywords = [
            "Language | 〽️",
            "زبان | 〽️"
        ]
        text: str
        keyboard: InlineKeyboardMarkup

        def __init__(self, text: str, keyboard: InlineKeyboardMarkup):
            self.text = text
            self.keyboard = keyboard

        @classmethod
        async def create(
                cls,
                settings: BotSettings
        ):
            if settings.language == Language.en:
                text = hbold("🔸 Please select the new language.")
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="🇮🇷 | فارسی",
                                callback_data=await CallbackData("select-lang", language=Language.fa.value).pack()
                            ),
                            InlineKeyboardButton(
                                text="🇺🇸 | English",
                                callback_data=await CallbackData("select-lang", language=Language.en.value).pack()
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                text="⤵️ | Back",
                                callback_data="settings"
                            )
                        ]
                    ]
                )
            else:
                text = hbold("🔸 لطفاً زبان جدید را انتخاب کنید.")
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton(
                                text="🇮🇷 | فارسی",
                                callback_data=await CallbackData("select-lang", language=Language.fa.value).pack()
                            ),
                            InlineKeyboardButton(
                                text="🇺🇸 | English",
                                callback_data=await CallbackData("select-lang", language=Language.en.value).pack()
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                text="⤵️ | بازگشت",
                                callback_data="settings"
                            )
                        ]
                    ]
                )
            return cls(text=text, keyboard=keyboard)

    class BackupChannel:
        text: str

        def __init__(self, text: str):
            self.text = text

        @classmethod
        async def create(
                cls,
                settings: BotSettings,
                chat: ChatShared
        ):
            if settings.language == Language.en:
                text = f"""<b>
✅ New Chat to Save Backup Set:

Here are the details of the chat:

🆔 <u>ID:</u> <code>{chat.chat_id}</code>
📛 <u>Title:</u> <code>{chat.title if chat.title else 'N/A'}</code>
👤 <u>Username:</u> <code>{f"@{chat.username}" if chat.username else 'N/A'}</code>


From Now, the backup files will be send in this channel and you can leave the channel. 🚀
</b>
"""

            else:
                text = f"""<b>
✅ کانال جدید برای ذخیره بکاپ ها:

اطلاعات کانال:

🆔 <u>شناسه:</u> <code>{chat.chat_id}</code>
📛 <u>عنوان:</u> <code>{chat.title if chat.title else 'N/A'}</code>
👤 <u>نام کاربری:</u> <code>{f"@{chat.username}" if chat.username else 'N/A'}</code>

از اکنون فایل های بکاپ در این کانال ارسال خواهد و شما می توانید کانال خارج شوید. 🚀
</b>
"""

            return cls(text=text)

    class BackupInterval:
        keywords = [
            "Backup Interval | 🛄",
            "تاخیر بکاپ | 🛄"
        ]
        text: str
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text="🏘"
                    )
                ]
            ],
            resize_keyboard=True
        )

        def __init__(
                self,
                text: str
        ):
            self.text = text

        @classmethod
        async def create(
                cls,
                settings: BotSettings
        ):
            if settings.language == Language.en:
                text = hbold(f"🔸 Please set the new backup interval(now: every {settings.backup_interval} minutes).")
            else:
                text = hbold(f"🔸 لطفاً تاخیر بکاپ جدید را تنظیم کنید(فعلی: هر {settings.backup_interval} دقیقه).")

            return cls(text=text)

    class Admins:
        keywords = [
            "👨‍💻 | Admins",
            "👨‍💻 | ادمین ها"
        ]
        text: str
        keyboard: InlineKeyboardMarkup

        def __init__(
                self,
                text: str,
                keyboard: InlineKeyboardMarkup
        ):
            self.text = text
            self.keyboard = keyboard

        @classmethod
        async def create(
                cls,
                settings: BotSettings
        ):
            if settings.language == Language.en:
                text = hbold("""
👥 Admins

Click on an admin to remove them or click "Add Admin" to add a new admin.
""")
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(
                                                text=str(admin),
                                                callback_data=await CallbackData("remove-admin",
                                                                                 admin=admin).pack()
                                            )
                                        ] for admin in settings.admins
                                    ] +
                                    [
                                        [
                                            InlineKeyboardButton(
                                                text="➕ Add Admin",
                                                callback_data=await CallbackData("add-admin").pack()
                                            )
                                        ],
                                        [
                                            InlineKeyboardButton(
                                                text="🔙 Back",
                                                callback_data=await CallbackData("settings").pack()
                                            )
                                        ]
                                    ]

                )
            else:
                text = hbold("""
👥 ادمین ها

برای حذف یک ادمین روی آن کلیک کنید یا برای افزودن ادمین جدید روی "افزودن ادمین" کلیک کنید.
""")
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(
                                                text=str(admin),
                                                callback_data=await CallbackData("remove-admin",
                                                                                 admin=admin).pack()
                                            )
                                        ] for admin in settings.admins
                                    ] +
                                    [
                                        [
                                            InlineKeyboardButton(
                                                text="➕ افزودن ادمین",
                                                callback_data=await CallbackData("add-admin").pack()
                                            )
                                        ],
                                        [
                                            InlineKeyboardButton(
                                                text="🔙 بازگشت",
                                                callback_data=await CallbackData("settings").pack()
                                            )
                                        ]
                                    ]
                )
            return cls(text=text, keyboard=keyboard)

        class AddAdmin:
            data = "add-admin"
            text: str
            keyboard: ReplyKeyboardMarkup

            def __init__(
                    self,
                    text: str,
                    keyboard: ReplyKeyboardMarkup
            ):
                self.text = text
                self.keyboard = keyboard

            @classmethod
            async def create(
                    cls,
                    settings: BotSettings
            ):
                if settings.language == Language.en:
                    text = hbold("🔸 Please select the new admin.")
                    keyboard = ReplyKeyboardMarkup(
                        keyboard=[
                            [
                                KeyboardButton(
                                    text="🔍 | select",
                                    request_user=KeyboardButtonRequestUser(
                                        request_id=1,
                                        user_is_bot=False
                                    )
                                )
                            ],
                            [
                                KeyboardButton(
                                    text="🏘"
                                )
                            ]
                        ],
                        resize_keyboard=True
                    )
                else:
                    text = hbold("🔸 لطفاً ادمین جدید را انتخاب کنید.")
                    keyboard = ReplyKeyboardMarkup(
                        keyboard=[
                            [
                                KeyboardButton(
                                    text="🔍 | انتخاب",
                                    request_user=KeyboardButtonRequestUser(
                                        request_id=1,
                                        user_is_bot=False
                                    )
                                )
                            ],
                            [
                                KeyboardButton(
                                    text="🏘"
                                )
                            ]
                        ],
                        resize_keyboard=True
                    )
                return cls(text=text, keyboard=keyboard)

            class Add:
                text: str

                def __init__(
                        self,
                        text: str
                ):
                    self.text = text

                @classmethod
                async def create(
                        cls,
                        settings: BotSettings,
                        admin: UserShared
                ):
                    if settings.language == Language.en:
                        text = f"""<b>
✅ New admin added:

<u>ID:</u> <code>{admin.user_id}</code>
</b>
"""
                    else:
                        text = f"""<b>
✅ ادمین جدید اضافه شد:

<u>شناسه:</u> <code>{admin.user_id}</code>
</b>
"""
                    return cls(text=text)
