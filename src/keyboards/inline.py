from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton 


main_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔮 Каталог", callback_data="catalog")],
    [
        InlineKeyboardButton(text="👤 Профиль", callback_data="profile"),
        InlineKeyboardButton(text="🐳 Тех. поддержка", callback_data="support"),
    ],
    [InlineKeyboardButton(text="🔍 О нас", callback_data="about")]
])