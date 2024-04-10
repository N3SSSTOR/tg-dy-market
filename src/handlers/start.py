import contextlib

from aiogram import Router
from aiogram.types import Message 
from aiogram.filters import CommandStart

from motor.core import AgnosticDatabase as MDB
from pymongo.errors import DuplicateKeyError

import messages as msg 

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, db: MDB):
    pattern = dict(
        _id=message.from_user.id,
        balance=0,
        permissions=0,
        history=[],
        code_id=0, 
    )

    with contextlib.suppress(DuplicateKeyError):
        await db.users.insert_one(pattern)

    await message.answer(**msg.main_menu_message_pattern)