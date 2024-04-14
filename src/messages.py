from aiogram.types import FSInputFile

from config import HOME_PATH
from keyboards.inline import main_menu_kb

main_menu_message_pattern = dict(
    photo=FSInputFile(HOME_PATH),
    caption="👋 Добро пожаловать в <b>D&Y Market</b> — магазин <b>Fortnite</b> товаров"
    "\n\n<em>Переоткрыть меню</em> — /menu"
    "\n\nУ нас самые демократичные цены, вы можете ознакомиться с каталогом ниже ⬇️",
    reply_markup=main_menu_kb
)