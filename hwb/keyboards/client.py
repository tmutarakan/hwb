from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlite.sqlite_db import sql_child, sql_parent


def create_keyboard(parent: str) -> InlineKeyboardMarkup:
    # Создаёт клавиатуру на основе запроса из базы данных
    inline_kbm = InlineKeyboardMarkup()
    msg_list = []
    for name, message in sql_child(parent):
        msg_list.append([message, name])

    while len(msg_list) > 0:
        temp = {
            'count': 0,
            'length': 0,
            'list_length': [],
            'all_length': True,
            'list_elem': [],
            'list_button': []
        }
        for elem in msg_list:
            elem_length = len(elem[0])
            elem_size = 36/(temp['count']+1)
            for temp_elem in temp['list_length']:
                if temp_elem > elem_size:
                    temp['all_length'] = False
            if temp['length'] + elem_length <= 36 and elem_length <= elem_size and temp['all_length']:
                temp['count'] += 1
                temp['length'] += elem_length
                temp['list_length'].append(elem_length)
                temp['list_elem'].append(elem)
            else:
                break
        for _ in range(temp['count']):
            temp['list_button'].append(InlineKeyboardButton(msg_list[0][0], callback_data=msg_list[0][1]))
            msg_list.pop(0)
        inline_kbm.row(*temp['list_button'])

    root = sql_parent(parent)
    if root:
        inline_kbm.add(InlineKeyboardButton("Назад", callback_data=root))
    return inline_kbm
