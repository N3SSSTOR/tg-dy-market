from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup 


def inline_builder(
    text: list[str] | str,
    callback_data: list[str] | str,
    size: int = 1
) -> InlineKeyboardMarkup:
    if isinstance(text, str):
        text = [text]
    if isinstance(callback_data, str):
        callback_data = [callback_data]

    builder = InlineKeyboardBuilder()

    for _text, _callback_data in zip(text, callback_data):
        builder.button(text=_text, callback_data=_callback_data)

    return builder.adjust(size).as_markup()