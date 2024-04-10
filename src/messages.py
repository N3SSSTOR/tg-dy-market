from keyboards.inline import main_menu_kb

main_menu_message_pattern = dict(
    text="👋 Добро пожаловать в <b>D&Y Market</b> — магазин Fortnite-товаров"
    "\n\n<em>Переоткрыть меню</em> — /menu"
    "\n\nУ нас самые демократичные цены, вы можете ознакомиться с каталогом ниже ⬇️",
    reply_markup=main_menu_kb
)