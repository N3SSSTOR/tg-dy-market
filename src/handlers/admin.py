import json 
import time 
import os 

from aiogram import Router, F 
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command

from motor.core import AgnosticDatabase as MDB 

from utils.middlewares import PermProtectMiddleware 
from keyboards.builders import inline_builder

router = Router()
router.message.middleware(PermProtectMiddleware(2))
router.callback_query.middleware(PermProtectMiddleware(2))


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    await message.answer("Вы админ")


@router.message(Command("get_categories"))
async def get_categories(message: Message, db: MDB):
    categories_cursor = db.categories.find()
    categories = [category for category in await categories_cursor.to_list(100)]

    for category in categories:
        await message.answer(
            f"ID: <code>{category['_id']}</code>"
            f"\nНазвание: <b>{category['title']}</b>"
            f"\nПуть до картинки: <code>{category['icon_path']}</code>",
            reply_markup=inline_builder(
                text=[
                    "✅ Активна" if category["is_active"] else "❌ Неактивна", 
                    "🛍 Товары этой категории", 
                    "👀 Скрыть"
                ], 
                callback_data=[
                    f"admin_category_active_reverse_{category['_id']}", 
                    f"admin_category_products_{category['_id']}", 
                    "hide"
                ]
            )
        )


@router.callback_query(F.data.startswith("admin_category_products_"))
async def category_products(callback: CallbackQuery, db: MDB):
    category = await db.categories.find_one(dict(_id=int(callback.data.split("_")[3])))

    products_cursor = db.products.find(dict(category_id=category["_id"])) 
    products = [product for product in await products_cursor.to_list(100)]

    text = f"Товары категории <b>{category['title']}</b>\n\n"
    for product in products:
        text += (
            f"ID: <code>{product['_id']}</code>"
            f"\nНазвание: <b>{product['title']}</b>"
            f"\nЦена: <b>{product['price']}</b>₽\n\n"
        )

    await callback.message.edit_text(text, reply_markup=inline_builder("👀 Скрыть", "hide"))
    await callback.answer()


@router.callback_query(F.data.startswith("admin_category_active_reverse_"))
async def category_products(callback: CallbackQuery, db: MDB):
    category = await db.categories.find_one(dict(_id=int(callback.data.split("_")[4])))
    
    await db.categories.update_one(
        dict(_id=int(callback.data.split("_")[4])),
        {
            "$set": {"is_active": not category["is_active"]}
        }
    )

    category = await db.categories.find_one(dict(_id=int(callback.data.split("_")[4])))

    await callback.message.edit_text(
        f"ID: <code>{category['_id']}</code>"
        f"\nНазвание: <b>{category['title']}</b>"
        f"\nПуть до картинки: <code>{category['icon_path']}</code>"
        f"\n\n<em>Вы изменили статус категории</em>",
        reply_markup=inline_builder(
            text=[
                "✅ Активна" if category["is_active"] else "❌ Неактивна", 
                "🛍 Товары этой категории", 
                "👀 Скрыть"
            ], 
            callback_data=[
                f"admin_category_active_reverse_{category['_id']}", 
                f"admin_category_products_{category['_id']}", 
                "hide"
            ]
        )
    )
    await callback.answer()


@router.message(Command("get_users"))
async def get_users(message: Message, db: MDB):
    users_query = dict(perm = 0)

    users_count = await db.users.count_documents(users_query)

    users_cursor = db.users.find(users_query)
    users = [user for user in await users_cursor.to_list(users_count)]

    file_path = f"upload/{int(time.time())}.json"
    with open(file_path, "w") as f:
        f.write(json.dumps(users, indent=4))
    
    await message.answer_document(
        FSInputFile(file_path),
        caption=f"На данный момент в магазине заригестрировано <b>{users_count}</b> пользователей"
    )
    os.remove(file_path)


@router.message(Command("set_perm"))
async def set_perm(message: Message, db: MDB):
    data = message.text.split(" ")
    
    if len(data) != 3:
        await message.reply(
            "Неверно указаны аргументы:"
            "\n/set_perm [ID-пользователя] [права (0-2)]"
        )
        return 
    
    try:
        if int(data[2]) not in (0, 1, 2):
            await message.reply("Права должны быть от 0 до 2")
            return 
    except ValueError:
        await message.reply("Права должны быть от 0 до 2")
        return 
    
    user_filter = dict(_id=int(data[1]))
    user = await db.users.find_one(user_filter)
    if not user:
        await message.reply("Такого пользователя нет")
        return 
    
    await db.users.update_one(user_filter,
        {
            "$set": {"perm": int(data[2])}
        }
    )
    await message.reply(f"Права пользователя @{user['username']} теперь {data[2]}")


@router.message(Command("set_price"))
async def set_price(message: Message, db: MDB):
    data = message.text.split(" ")
    
    if len(data) != 3:
        await message.reply(
            "Неверно указаны аргументы:"
            "\n/set_price [ID-товара] [цена без \"₽\"]"
        )
        return 
    
    try:
        int(data[1])
        int(data[2])
    except ValueError:
        await message.reply("Агрументы команды не могут содержать строки")
        return 
    
    product_filter = dict(_id=int(data[1]))
    product = await db.products.find_one(product_filter)
    if not product:
        await message.reply("Такого товара нет")
        return 
    
    await db.products.update_one(product_filter,
        {
            "$set": {"price": int(data[2])}
        }
    )

    product = await db.products.find_one(product_filter)
    await message.reply(
        "<em>Товар изменен:</em>"
        f"\n\nНазвание: <b>{product['title']}</b>"
        f"\nЦена: <b>{product['price']}</b>₽"
    )