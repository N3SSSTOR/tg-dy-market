import uuid 
import time 

from aiogram import Router, F 
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile

from motor.core import AgnosticDatabase as MDB 

from .nav import to_main_menu
from keyboards.builders import inline_builder 

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
        f"💸 <em>Оплата товара <b>{product['title']}</b></em>"
        f"\nК оплате — <b>{product['price']}</b>₽",
        reply_markup=inline_builder(
            text=["Начать оплату", "Отменить"],
            callback_data=[f"start_pay_{product['_id']}", "hide"]
        )
    )

    await to_main_menu(callback, db)


@router.callback_query(F.data.startswith("start_pay_"))
async def start_pay(callback: CallbackQuery, db: MDB):
    # product_filter = {"_id": int(callback.data.split("_")[2])}
    # product = await db.products.find_one(product_filter)

    # if not product:
    #     callback.answer("Товар не найден")
    #     callback.message.delete() 

    # pattern = dict(
    #     _id=str(uuid.uuid4()),
    #     user_id=callback.from_user.id,
    #     amount=product["price"],
    # )
    await callback.answer("Coming soon...")