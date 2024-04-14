import time 
import os 

from aiogram import Router, F 
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile

from motor.core import AgnosticDatabase as MDB 

from config import SUPPORT_USERNAME, HOME_PATH, SUPPORT_PATH, ABOUT_PATH, CATALOG_PATH, FAQ_PATH
from keyboards.builders import inline_builder
from messages import main_menu_message_pattern
from utils.profile_img import generate_profile_img 

router = Router()


@router.callback_query(F.data == "to_main_menu")
async def support(callback: CallbackQuery, db: MDB):
    await callback.message.edit_media(
        InputMediaPhoto(
            media=FSInputFile(HOME_PATH),
            caption=main_menu_message_pattern["caption"]
        ),
        reply_markup=main_menu_message_pattern["reply_markup"]
    )
    await callback.answer()


@router.callback_query(F.data == "hide")
async def hide_message(callback: CallbackQuery):
    await callback.message.delete()


@router.callback_query(F.data == "support")
async def support(callback: CallbackQuery):
    await callback.message.edit_media(
        InputMediaPhoto(
            media=FSInputFile(SUPPORT_PATH), 
            caption="Если у вас возникла проблема или появился вопрос — "
            "вы вcегда можете обратиться в тех. поддержку\n\n"
            f"<em>Телеграм оператора</em>: <b>@{SUPPORT_USERNAME}</b>",
        ),
        reply_markup=inline_builder("В главное меню ⬅️", "to_main_menu")        
    )
    await callback.answer()


@router.callback_query(F.data == "about")
async def support(callback: CallbackQuery):
    await callback.message.edit_media(
        InputMediaPhoto(
            media=FSInputFile(ABOUT_PATH),
            caption="<b>D&Y Market</b> — 🚀 лучший магазин для покупки <b>Fortnite</b> товаров"
            "\n\n— <em>Самые низкие цены на рынке</em>"
            "\n— <em>Гарантия безопасности для ваших аккаунтов</em>"
            "\n— <em>Отзывчивая тех. поддержка и удобный интерфейс</em>"
            "\n\nВы можете посмотреть ответы на часто задаваемые вопросы перейдя в FAQ ⬇️"
        ),
        reply_markup=inline_builder(
            text=["⚡️ FAQ", "В главное меню ⬅️"],
            callback_data=["faq", "to_main_menu"]
        )
    )
    await callback.answer()


@router.callback_query(F.data == "profile")
async def support(callback: CallbackQuery, db: MDB):
    user = await db.users.find_one(dict(_id=callback.from_user.id))

    days_in_market = (int(time.time()) - user["date"]) // (3600 * 24)
    total_amount = 0 
    for product_id in user["history"]:
        product = await db.products.find_one(dict(_id=product_id))
        total_amount += product["price"]

    profile_img_path = generate_profile_img(
        username=f"@{callback.from_user.username}",
        days_in_market=days_in_market,
        total_purchases=len(user["history"]),
        total_amount=total_amount
    )

    await callback.message.edit_media(
        InputMediaPhoto(
            media=FSInputFile(profile_img_path),
            caption="Перейдите в каталог чтобы посмотреть доступные товары ⬇️"
        ),
        reply_markup=inline_builder(
            text=["🔮 Каталог", "В главное меню ⬅️"],
            callback_data=["catalog", "to_main_menu"]
        )
    )
    await callback.answer()

    os.remove(profile_img_path)


@router.callback_query(F.data == "catalog")
async def catalog(callback: CallbackQuery, db: MDB):
    categories_cursor = db.categories.find(dict(is_active=True))
    categories = [category for category in await categories_cursor.to_list(100)]

    await callback.message.edit_media(
        InputMediaPhoto(
            media=FSInputFile(CATALOG_PATH),
            caption="Вам доступны следующие категории ⬇️"
        ),
        reply_markup=inline_builder(
            text=[category["title"] for category in categories] + ["В главное меню ⬅️"],
            callback_data=[f"category_{category['_id']}" for category in categories] + ["to_main_menu"]
        )
    )
    await callback.answer()


@router.callback_query(F.data == "faq")
async def faq(callback: CallbackQuery):
    await callback.message.edit_media(
        InputMediaPhoto(
            media=FSInputFile(FAQ_PATH),
            caption="<b>Ответы на часто задаваемые вопросы</b>"

            "\n\nℹ️ <em>Как осуществляется процесс пополнения В-Баксов?</em>"

            "\n\nПеред оплатой товара, вы должны предоставить некоторые данные, "
            "которые оператор будет использовать для авторизации в <b>Epic Games</b>. Мы "
            "гарантируем, что ваш аккаунт не будет передан третьим лицам, и после "
            "предоставления услуги данные о вашей учетной записи будут очищены."

            "\n\nℹ️ <em>Как обеспечить безопасность при покупке товара?</em>"

            "\n\nПосле оплаты товара вашему заказу будет присвоен ID. Если у вас "
            "возникнут вопросы или вы обнаружите, что данные введены неверно — обратитесь "
            "в тех. поддержку, назвав ID заказа. Это оптимизирует процесс решения вашей "
            "проблемы и позволит избежать потенциальных угроз."
        ),
        reply_markup=inline_builder("В главное меню ⬅️", "to_main_menu")
    )
    await callback.answer()