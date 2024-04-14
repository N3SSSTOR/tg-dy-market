import contextlib
import time 

from aiogram import Router
from aiogram.types import Message 
from aiogram.filters import CommandStart, Command

from motor.core import AgnosticDatabase as MDB
from pymongo.errors import DuplicateKeyError

from messages import main_menu_message_pattern

router = Router()


@router.message(CommandStart())
@router.message(Command("menu"))
async def cmd_start(message: Message, db: MDB):
    pattern = dict(
        _id=message.from_user.id,
        username=message.from_user.username, 
        perm=0,
        history=[],
        code_id=0, 
        date=int(time.time())
    )

    with contextlib.suppress(DuplicateKeyError):
        await db.users.insert_one(pattern)

    await message.answer_photo(**main_menu_message_pattern)