from gc import callbacks
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlite.sqlite_db import sql_child, sql_parent


def create_button(parent: str):
    inline_kbm = InlineKeyboardMarkup()
    for ret in sql_child(parent):
        inline_btn = InlineKeyboardButton(ret[2], callback_data=ret[1])
        inline_kbm.insert(inline_btn)
    
    root = sql_parent(parent)
    if not root:
        root = 'help'
    inline_btn = InlineKeyboardButton("Назад", callback_data=root)
    inline_kbm.insert(inline_btn)
    return inline_kbm
