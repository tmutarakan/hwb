from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlite.sqlite_db import sql_child, sql_parent
from collections import deque


class ButtonData:
    def __init__(self, message, name) -> None:
        self.message = message
        self.name = name


class TempData:
    def __init__(self) -> None:
        self.count = 0              # Количество кнопок в строке
        self.length = 0             # Суммарная длина текста кнопок
        self.list_length = []       # Длина текста каждой кнопки
        self.all_length = True      # Вмещается ли текст всех кнопок в строке
        self.list_button = []       # Список для кнопок


def create_keyboard(parent: str) -> InlineKeyboardMarkup:
    # Создаёт клавиатуру на основе запроса из базы данных
    inline_kbm = InlineKeyboardMarkup()
    msg_list = deque()
    for name, message in sql_child(parent):
        msg_list.append(ButtonData(message, name))

    while len(msg_list) > 0:
        temp = TempData()
        
        for elem in msg_list:
            elem_length = len(elem.message)
            elem_size = 36/(temp.count + 1)    # Максимальная длина сообщения в кнопке
            for temp_elem in temp.list_length:
                if temp_elem > elem_size:
                    temp.all_length = False
                    break
            
            if temp.length + elem_length > 36 or elem_length > elem_size or not temp.all_length:
                break                
            else:
                temp.count += 1
                temp.length += elem_length
                temp.list_length.append(elem_length)
            
        for _ in range(temp.count):
            b_data = msg_list.popleft()
            temp.list_button.append(InlineKeyboardButton(b_data.message, callback_data=b_data.name))
        inline_kbm.row(*temp.list_button)

    root = sql_parent(parent)
    if root:
        inline_kbm.add(InlineKeyboardButton("Назад", callback_data=root))
    return inline_kbm
