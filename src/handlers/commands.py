import contextlib
import asyncio 
import time 

from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command

from motor.core import AgnosticDatabase as MDB
from pymongo.errors import DuplicateKeyError

from config import HOME_PATH 
from keyboards.inline import main_menu_kb
from keyboards.builders import inline_builder

router = Router()


@router.message(CommandStart())
@router.message(Command("menu"))
async def cmd_start(message: Message, db: MDB):
    current_time = int(time.time())

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
        "\n<em>Все оплаченные заказы</em> — /get_orders"
        "\n\nУ нас самые демократичные цены, вы можете ознакомиться с каталогом ниже ⬇️",
        reply_markup=main_menu_kb
    )


@router.message(Command("get_orders"))
async def cmd_get_orders(message: Message, db: MDB):
    orders_cursor = db.orders.find({"user_id": message.from_user.id,
                                    "status": "hold"}) 
    orders = [order for order in await orders_cursor.to_list(100)]

    if orders:
        await message.answer("Ваши оплаченные заказы")
        for i, order in enumerate(orders):
            if i and i % 20 == 0:
                await asyncio.sleep(5)
            await message.answer(
                f"🆔: <code>{order['_id']}</code>"
                f"\n🌵 Товар: <b>{order['product']['title']}</b>"
                f"\n💸 Цена: <b>{order['product']['price']}</b>₽",
                reply_markup=inline_builder("👀 Скрыть", "hide")
            )
        await message.answer("Пока все...", reply_markup=inline_builder("Круто", "hide"))
        return 
    
    await message.answer("У вас нет оплаченных заказов")