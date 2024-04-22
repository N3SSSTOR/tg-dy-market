from aiogram import Router, F 
from aiogram.types import Message, CallbackQuery 

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