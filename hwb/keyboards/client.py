from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlite.sqlite_db import sql_child, sql_parent
from collections import deque


class ButtonData:
    def __init__(self, message, name) -> None:
        self.message = message
        self.name = name

    def __str__(self) -> str:
        return f'{self.name} {self.message}'

    def __repr__(self) -> str:
        return f'{self.name} {self.message}'


class TempData:
    def __init__(self) -> None:
        self.count = 0              # Количество кнопок в строке
        self.length = 0             # Суммарная длина текста кнопок
        self.list_length = []       # Длина текста каждой кнопки
        self.all_length = True      # Вмещается ли текст всех кнопок в строке
        self.list_button = []       # Список для кнопок


class State:
    def __init__(self, rows) -> None:
        self.page = []
        if len(rows) < 5:
            p.rows.append(temp.list_button)
        else:
            p.rows.append([ButtonData('Вперёд', '/next')])

    def __str__(self) -> str:
        return f'{self.rows}'

    def __len__(self) -> int:
        return len(self.rows)


def create_page(parent):
    msg_list = deque()
    for name, message in sql_child(parent):
        msg_list.append(ButtonData(message, name))

    rows = []
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
            temp.list_button.append(msg_list.popleft())

        rows.append(temp.list_button)
    return rows


def create_keyboard(parent: str) -> InlineKeyboardMarkup:
    # Создаёт клавиатуру на основе запроса из базы данных
    inline_kbm = InlineKeyboardMarkup()
    root = sql_parent(parent)
    if root:
        inline_kbm.add(InlineKeyboardButton("Вернуться", callback_data=root))
    rows = create_page(parent)
    for row in rows:
        temp = []
        for button_data in row:
            temp.append(InlineKeyboardButton(button_data.message, callback_data=button_data.name))
        inline_kbm.row(*temp)    
    #print(f'{page} {len(page)}')
    return inline_kbm



def edit_keyboard(data):
    inline_kbm = InlineKeyboardMarkup()
    root = sql_read_current_parent()
    if root:
        inline_kbm.add(InlineKeyboardButton("Вернуться", callback_data=root))

    pages = sql_read_page(data)
    row_count = 1
    temp = []
    for row_number, name, message in pages:
        if row_number == row_count:
            temp.append(InlineKeyboardButton(message, callback_data=name))
        else:
            row_count += 1
            inline_kbm.row(*temp)
            temp = []
            temp.append(InlineKeyboardButton(message, callback_data=name))
    inline_kbm.row(*temp)
    inline_kbm.row(InlineKeyboardButton('Назад', callback_data='/prev'), InlineKeyboardButton('Вперёд', callback_data='/next'))
    return inline_kbm
