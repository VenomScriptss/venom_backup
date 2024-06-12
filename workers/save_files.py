from io import BytesIO
from os import walk
from os.path import join, relpath
from zipfile import ZipFile

from aiofiles import open as aio_open
from aiofiles.ospath import exists
from aiogram.types import BufferedInputFile
from sqlalchemy.future import select

from bot import BOT
from db import BotSettings, Backup, SESSION


async def add_folder_to_zip(zipf, folder_path, zip_folder_path):
    for root, dirs, files in walk(folder_path):
        for file in files:
            file_path = join(root, file)
            zip_file_path = join(zip_folder_path, relpath(file_path, folder_path))
            async with aio_open(file_path, 'rb') as f:
                data = await f.read()
                zipf.writestr(zip_file_path, data)


async def get_files_bytes():
    var_lib_marzban_path = '/var/lib/marzban'
    opt_marzban_path = '/opt/marzban'

    zip_buffer = BytesIO()

    with ZipFile(zip_buffer, 'w') as zipf:
        # Create the folder structure inside the zip file
        zipf.writestr('var/', '')
        zipf.writestr('var/lib/', '')
        zipf.writestr('var/lib/marzban/', '')
        zipf.writestr('opt/', '')
        zipf.writestr('opt/marzban/', '')

        # Add contents of /var/lib/marzban to the zip file
        if await exists(var_lib_marzban_path):
            await add_folder_to_zip(zipf, var_lib_marzban_path, 'var/lib/marzban')

        # Add contents of /opt/marzban to the zip file
        if await exists(opt_marzban_path):
            await add_folder_to_zip(zipf, opt_marzban_path, 'opt/marzban')

    zip_buffer.seek(0)
    return zip_buffer.getvalue()


async def save_backup():
    async with SESSION() as session:
        settings = await session.scalar(
            select(BotSettings)
        )
        assert settings.backup_chat_id is not None, "Backup chat id is not set"
        backup_bytes = await get_files_bytes()
        message = await BOT.send_document(chat_id=settings.backup_chat_id,
                                          document=BufferedInputFile(backup_bytes, filename='marzban_backup.zip'))
        model = Backup(
            id=message.document.file_id
        )
        session.add(model)
        await session.commit()
        return
