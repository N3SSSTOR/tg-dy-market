from aiogram import Router, F 
from aiogram.types import CallbackQuery 

from motor.core import AgnosticDatabase as MDB 

import messages as msg 
from config import SUPPORT_USERNAME
from keyboards.builders import inline_builder

router = Router()


@router.callback_query(F.data == "to_main_menu")
async def support(callback: CallbackQuery, db: MDB):
    await callback.message.edit_text(**msg.main_menu_message_pattern)
    await callback.answer()


@router.callback_query(F.data == "support")
async def support(callback: CallbackQuery):
    await callback.message.edit_text(
        "Если у вас возникла проблема или появился вопрос — вы вcегда сможете обратиться в тех. поддержку\n\n"
        f"<em>Телеграм оператора</em>: <b>@{SUPPORT_USERNAME}</b>",
        reply_markup=inline_builder(
            text="В главное меню ⬅️",
            callback_data="to_main_menu"
        )
    )
    await callback.answer()