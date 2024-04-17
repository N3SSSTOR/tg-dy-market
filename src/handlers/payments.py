import random 
import uuid 
import time 

from aiogram import Router, F 
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile

from motor.core import AgnosticDatabase as MDB 
from AaioAsync import AaioAsync 

from config import AAIO_API_KEY, AAIO_SHOP_ID, AAIO_SECRET_KEY_1, ORDER_CREATION_DELAY
from .nav import to_main_menu
from keyboards.builders import inline_builder 
from keyboards.inline import get_pay_kb

router = Router()


@router.callback_query(F.data.startswith("buy_"))
async def buy(callback: CallbackQuery, db: MDB):
    product_filter = {"_id": int(callback.data.split("_")[1])}
    product = await db.products.find_one(product_filter)

    category = await db.categories.find_one({"_id": product["category_id"]})

    if not product or not category["is_active"]:
        await to_main_menu(callback, db, answer_text="Товар не найден")
        return 
    
    await callback.message.answer(
        f"Оплата товара <b>{product['title']}</b>"
        f"\nК оплате — <b>{product['price']}</b>₽",
        reply_markup=inline_builder(
            text=["🔥 Начать оплату", "Назад ⬅️"],
            callback_data=[f"start_pay_{product['_id']}", "hide"]
        )
    )

    await to_main_menu(callback, db)


@router.callback_query(F.data.startswith("start_pay_"))
async def start_pay(callback: CallbackQuery, db: MDB):
    product_filter = {"_id": int(callback.data.split("_")[2])}
    product = await db.products.find_one(product_filter)

    if not product:
        await callback.answer("Товар не найден")
        await callback.message.delete() 
        return 

    user_filter = {"_id": callback.from_user.id}
    user = await db.users.find_one(user_filter)
    if (int(time.time()) - user["last_order_date"]) < ORDER_CREATION_DELAY:
        await callback.answer("Вы слишком часто создаете заказы, попробуйте через 60 секунд")
        await callback.message.delete() 
        return 

    await db.users.update_one(user_filter,
        {
            "$set": {"last_order_date": int(time.time())}
        }
    )

    aaio = AaioAsync(apikey=AAIO_API_KEY, shopid=AAIO_SHOP_ID, secretkey=AAIO_SECRET_KEY_1)

    order_id = str(uuid.uuid4())
    pay_url = await aaio.generatepaymenturl(amount=product["price"], order_id=order_id, desc=product["title"])

    pattern = dict(
        _id=order_id,
        user_id=callback.from_user.id,
        product=product,
        pay_url=pay_url,
        status="in_process"
    )
    await db.orders.insert_one(pattern)

    await callback.message.edit_text(
        f"Заказ создан 🥳"
        f"\n\nID: <code>{order_id}</code>"
        f"\nСтатус: <b>В процессе</b>"
        f"\nЦена: <b>{product['price']}</b>₽"
        f"\n\n<em>У вас есть 6 часов чтобы оплатить заказ</em>",
        reply_markup=get_pay_kb(pay_url, order_id)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("check_order_"))
async def cancel_order(callback: CallbackQuery, db: MDB):
    order_id = callback.data.split("_")[2]
    order_filter = {"_id": order_id}
    
    order = await db.orders.find_one(order_filter)
    product = order["product"]

    aaio = AaioAsync(apikey=AAIO_API_KEY, shopid=AAIO_SHOP_ID, secretkey=AAIO_SECRET_KEY_1)

    order = await aaio.getorderinfo(order_id)
    order_data = order.model_dump()

    if order_data["status"] == "hold":
        await db.orders.update_one(order_filter,
            {
                "$set": {"status": "hold"}
            }
        )
        await callback.message.edit_text(
            f"Заказ оплачен 🥳"
            f"\n\nID: <code>{order_id}</code>"
            f"\nНазвание товара: <b>{product['title']}</b>"
            f"\nЦена: <b>{product['price']}</b>₽"
        )
        return 
    
    emoji = ["🙁", "😕", "😟", "😔", "😞", "😒"]
    # emoji = ["/", "—", "\\", "|"]
    edit_text = callback.message.text

    if "Заказ еще не оплачен" not in edit_text:
        edit_text += f"<em>Заказ еще не оплачен</em> {random.choice(emoji)}"

    for char in edit_text:
        if char in emoji:
            new_emoji = random.choice(emoji)
            while new_emoji == char:
                new_emoji = random.choice(emoji)
            edit_text.replace(char, new_emoji)

    await callback.message.edit_text(edit_text)
    await callback.answer("Заказ еще не оплачен")


@router.callback_query(F.data.startswith("cancel_order_"))
async def cancel_order(callback: CallbackQuery, db: MDB):
    order_filter = {"_id": callback.data.split("_")[2]}

    await db.orders.update_one(order_filter,
        {
            "$set": {"status": "canceled"}
        }
    )

    await callback.answer("Заказ отменен")
    await callback.message.delete()