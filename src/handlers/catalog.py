from aiogram import Router, F 
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile

from motor.core import AgnosticDatabase as MDB

from config import ASSET_PATH
from keyboards.builders import inline_builder

router = Router()


@router.callback_query(F.data.startswith("category_"))
async def category(callback: CallbackQuery, db: MDB):
    category = await db.categories.find_one({"_id": int(callback.data.split("_")[1])})

    products_cursor = db.products.find({"category_id": category["_id"]})
    products = [products for products in await products_cursor.to_list(100)]
    
    await callback.message.edit_media(
        InputMediaPhoto(
            media=FSInputFile(ASSET_PATH + category["icon_path"]),
            caption=(
                f"ℹ️ <em>{category['description']}</em>"
                "\n\nВам доступны следующие товары ⬇️"
            )
        ),
        reply_markup=inline_builder(
            text=[product["title"] for product in products] + ["В главное меню ⬅️"],
            callback_data=[f"product_{product['_id']}" for product in products] + ["to_main_menu"],
            size=2
        )
    )
    await callback.answer()


@router.callback_query(F.data.startswith("product_"))
async def product(callback: CallbackQuery, db: MDB):
    product = await db.products.find_one({"_id": int(callback.data.split("_")[1])})
    category = await db.categories.find_one({"_id": product["category_id"]})
    
    await callback.message.edit_caption(
        caption=f"Название: <b>{product['title']}</b>"
                f"\nЦена: <b>{product['price']}</b>₽"
                f"\nКатегория: <b>{category['title']}</b>",
        reply_markup=inline_builder(
            text=["💳 Купить", "Назад ⬅️"],
            callback_data=[f"buy_{product['_id']}", f"category_{category['_id']}"]
        )
    )
    await callback.answer()