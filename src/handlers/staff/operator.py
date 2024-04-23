import time 

from aiogram import Router, F 
from aiogram.types import Message, CallbackQuery 
from aiogram.filters import Command 

from motor.core import AgnosticDatabase as MDB 

from utils.middlewares import PermProtectMiddleware 
from keyboards.builders import inline_builder 

router = Router()
router.message.middleware(PermProtectMiddleware(1))
router.callback_query.middleware(PermProtectMiddleware(1))


@router.callback_query(F.data.startswith("catch_order_"))
async def catch_order(callback: CallbackQuery, db: MDB):
    order_id = callback.data.split("_")[2]
    order_filter = {"_id": order_id}
    order = await db.orders.find_one(order_filter)

    if order["operator_id"] and order["operator_id"] != callback.from_user.id:
        await callback.answer("Заказ взят другим оператором")
        return 
    
    if not order["operator_id"]:
        await db.orders.update_one(order_filter,
            {
                "$set": {"operator_id": callback.from_user.id}
            }
        )
        text = callback.message.html_text
        text = text.replace(
            "Новый заказ!", 
            f"<b>Заказ взят в обработку оператором <em>@{callback.from_user.username}</em></b>"
        )
        text = text.replace("Заказ еще не взят в обработку", "⚡️ Статус: <b>В процессе</b>")
        text += f"\n\n<em>Предоставленные данные:</em>\n\n{order['requirements']}"
        text += f"\n\n<em>(Если данные некорректны напишите об этом пользователю, сообщив ID заказа)</em>"
        await callback.message.edit_text(
            text,
            reply_markup=inline_builder(
                "Заказ исполнен", 
                f"pass_order_{order_id}"
            )
        )
        await callback.bot.send_message(
            order["user_id"], 
            f"<em>Оператор приступил к обработке заказа <code>{order['_id']}</code></em>"
        )


@router.callback_query(F.data.startswith("pass_order_"))
async def catch_order(callback: CallbackQuery, db: MDB):
    order_id = callback.data.split("_")[2]
    order_filter = {"_id": order_id}
    order = await db.orders.find_one(order_filter)

    if order["operator_id"] == callback.from_user.id:
        category = await db.categories.find_one({"_id": order["product"]["category_id"]})
        user = await db.users.find_one({"_id": order["user_id"]})

        await callback.message.edit_text(
            f"Заказ исполнен оператором <b>@{callback.from_user.username}</b>"
            f"\n\nID: <code>{order['_id']}</code>"
            f"\nТовар: <b>{order['product']['title']}</b>"
            f"\nКатегория: <b>{category['title']}</b>"
            f"\nЦена: <b>{order['product']['price']}</b>₽"
            f"\nИмя пользователя: <b>@{user['username']}</b>"
            f"\nID пользователя: <code>{user['_id']}</code>"
        )
        await callback.bot.send_message(
            user["_id"], 
            f"<em>Заказ <code>{order['_id']}</code> исполнен оператором! Приятной игры!</em>"
        )
    await callback.answer()


@router.message(Command("get_user_by_id"))
async def get_user_by_id(message: Message, db: MDB):
    data = message.text.split(" ")
    if len(data) != 2:
        await message.reply(
            "Неверно указаны аргументы:"
            "\n/get_user_by_id [ID-пользователя]"
        )
        return 
    
    try:
        int(data[1])
    except ValueError:
        await message.reply("Аргументы команды не могут содержать строки")
        return 
 
    user = await db.users.find_one({"_id": int(data[1])})
    if not user:
        await message.reply("Такого пользователя нет")
        return 
    
    total_amount = 0 
    for product in user['history']:
        total_amount += product["price"]

    days_in_market = (int(time.time()) - user["date"]) // (3600 * 24)
    
    await message.reply(
        f"Данные пользователя <b>@{user['username']}</b>"
        f"\n\nID: <code>{user['_id']}</code>"
        f"\nПрава: <b>{user['perm']}</b>"
        f"\nВсего покупок: <b>{len(user['history'])}</b>"
        f"\nОбщая сумма: <b>{total_amount}</b>₽"
        f"\nID промокода: <b>{user['code_id']}</b>"
        f"\nДней в магазине: <b>{days_in_market}</b>"
    )


@router.message(Command("get_user_by_username"))
async def get_user_by_username(message: Message, db: MDB):
    data = message.text.split(" ")
    if len(data) != 2:
        await message.reply(
            "Неверно указаны аргументы:"
            "\n/get_user_by_id [Username пользователя]"
        )
        return

    user = await db.users.find_one({"username": data[1]})
    if not user:
        await message.reply("Такого пользователя нет (Username пишется без \"@\")")
        return 
    
    total_amount = 0 
    for product in user['history']:
        total_amount += product["price"]

    days_in_market = (int(time.time()) - user["date"]) // (3600 * 24)
    
    await message.reply(
        f"Данные пользователя <b>@{user['username']}</b>"
        f"\n\nID: <code>{user['_id']}</code>"
        f"\nПрава: <b>{user['perm']}</b>"
        f"\nВсего покупок: <b>{len(user['history'])}</b>"
        f"\nОбщая сумма: <b>{total_amount}</b>₽"
        f"\nID промокода: <b>{user['code_id']}</b>"
        f"\nДней в магазине: <b>{days_in_market}</b>"
    )


@router.message(Command("get_order"))
async def get_order(message: Message, db: MDB):
    data = message.text.split(" ")
    if len(data) != 2:
        await message.reply(
            "Неверно указаны аргументы:"
            "\n/get_order [ID заказа]"
        )
        return
    
    order = await db.orders.find_one({"_id": data[1]})
    if not order:
        await message.reply("Такого заказа нет")
        return 
    
    await message.reply(
        f"Данные ордера <code>{order['_id']}</code>"
        f"\n\nID пользователя: <code>{order['user_id']}</code>"
        f"\nСсылка на оплату: {order['pay_url']}"
        f"\nСтатус (hold - значит оплачено): <b>{order['status']}</b>"
        f"\nДата: <b>{order['date']}</b>"
        f"\nЦена: <b>{order['product']['price']}</b>₽"
        f"\nТовар: <b>{order['product']['title']}</b>"
        f"\nПредоставленные данные: \n\n<code>{order['requirements']}</code>\n\n"
        f"\nID оператора: <code>{order['operator_id']}</code>"
    )