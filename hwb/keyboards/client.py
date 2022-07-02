from gc import callbacks
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlite.sqlite_db import sql_child, sql_parent


def create_keyboard(parent: str):
    # Создаёт клавиатуру на основе запроса из базы данных
    inline_kbm = InlineKeyboardMarkup()
    for ret in sql_child(parent):
        inline_btn = InlineKeyboardButton(ret[2], callback_data=ret[1])
        inline_kbm.insert(inline_btn)
    
    root = sql_parent(parent)
    if root:
        inline_kbm.add(InlineKeyboardButton("Назад", callback_data=root))
    return inline_kbm
