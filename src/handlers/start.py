import contextlib
import time 

from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command

from motor.core import AgnosticDatabase as MDB
from pymongo.errors import DuplicateKeyError

from config import HOME_PATH 
from keyboards.inline import main_menu_kb

router = Router()


@router.message(CommandStart())
@router.message(Command("menu"))
async def cmd_start(message: Message, db: MDB):
    current_time = int(time.time()),

    pattern = dict(
        _id=message.from_user.id,
        username=message.from_user.username, 
        perm=0,
        history=[],
        code_id=0, 
        date=current_time,
        last_order_date=current_time
    )

    with contextlib.suppress(DuplicateKeyError):
        await db.users.insert_one(pattern)

    await message.answer_photo(
        photo=FSInputFile(HOME_PATH),
        caption="👋 Добро пожаловать в <b>D&Y Market</b> — магазин <b>Fortnite</b> товаров"
        "\n\n<em>Переоткрыть меню</em> — /menu"
        "\n\nУ нас самые демократичные цены, вы можете ознакомиться с каталогом ниже ⬇️",
        reply_markup=main_menu_kb
    )