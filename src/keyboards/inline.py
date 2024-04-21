import random 

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from aiogram.utils.keyboard import InlineKeyboardBuilder

main_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔮 Каталог", callback_data="catalog")],
    [
        InlineKeyboardButton(text="👻 Профиль", callback_data="profile"),
        InlineKeyboardButton(text="🐳 Тех. поддержка", callback_data="support"),
    ],
    [
        InlineKeyboardButton(text="🔍 О нас", callback_data="about"),
        InlineKeyboardButton(text="⚡️ FAQ", callback_data="faq"),
    ]
])


def get_pay_kb(pay_url: str, order_id: str) -> InlineKeyboardMarkup:
    emoji = ["👍", "✅", "🤝", "👋"]

    builder = InlineKeyboardBuilder()

    builder.button(text="💳 Оплатить", url=pay_url)
    builder.button(text=f"{random.choice(emoji)} Я Оплатил", callback_data=f"check_order_{order_id}")
    builder.button(text="Отменить заказ", callback_data=f"cancel_order_{order_id}")

    return builder.adjust(2).as_markup()