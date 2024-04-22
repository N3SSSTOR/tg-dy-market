from aiogram import Router, F 
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from motor.core import AgnosticDatabase as MDB 

from config import GROUP_ID 
from keyboards.builders import inline_builder
from utils.states import RequirementsState 

router = Router()


@router.message(RequirementsState.requirements_wait)
async def requirements_wait(message: Message, db: MDB, state: FSMContext):
    await state.update_data(requirements_input=message.text)
    await message.answer(
        "Ваши предоставленные данные:"
        f"\n\n<code>{message.text}</code>"
        "\n\n<em>Все верно?</em>",
        reply_markup=inline_builder(
            text=["Да", "Нет, перезаписать"],
            callback_data=["yes", "no"],
            size=2
        )
    )
    await message.delete()


@router.callback_query(F.data == "yes")
async def set_requirements(callback: CallbackQuery, db: MDB, state: FSMContext):
    data = await state.get_data()
    order_id = data["order_id"]
    requirements_input = data["requirements_input"]

    await state.clear()

    order_filter = {"_id": order_id}
    await db.orders.update_one(order_filter,
        {
            "$set": {"requirements": requirements_input}
        }
    )

    await callback.message.answer(
        f"<em>Оператор скоро приступит к обработке заказа <code>{order_id}</code></em>"
    )
    await callback.message.delete()
    await callback.answer()

    order = await db.orders.find_one(order_filter)
    category = await db.categories.find_one({"_id": order["product"]["category_id"]})
    user = await db.users.find_one({"_id": order["user_id"]})

    await callback.bot.send_message(
        GROUP_ID,
        f"Новый заказ!"
        f"\n\nID: <code>{order['_id']}</code>"
        f"\nТовар: <b>{order['product']['title']}</b>"
        f"\nКатегория: <b>{category['title']}</b>"
        f"\nЦена: <b>{order['product']['price']}</b>₽"
        f"\nИмя пользователя: <b>@{user['username']}</b>"
        f"\nID пользователя: <code>{user['_id']}</code>"
        f"\n\n<em>Заказ еще не взят в обработку</em>",
        reply_markup=inline_builder("Взять", f"catch_order_{order_id}")
    )


@router.callback_query(F.data == "no")
async def change_requirements(callback: CallbackQuery, db: MDB):
    await callback.message.edit_text("<em>Введите новые данные:</em>")