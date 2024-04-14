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
        perm=0,
        history=[],
        code_id=0, 
        date=int(time.time())
    )

    with contextlib.suppress(DuplicateKeyError):
        await db.users.insert_one(pattern)

    await message.answer_photo(**main_menu_message_pattern)


# @router.message(Command("test"))
# async def test(message: Message, db: MDB):
#     # user = await db.users.find_one(dict(_id=message.from_user.id))
#     # print(user["_id"])

#     item = {
#         "_id": 2,
#         "title": "5000 В-Баксов",
#         "amount": 4500 
#     }

#     await db.users.update_one(
#         dict(_id=message.from_user.id),
#         {
#             "$push": {"history": item}
#         }
#     )