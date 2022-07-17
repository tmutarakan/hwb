from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlite.sqlite_db import sql_child, sql_create_pages, sql_parent, sql_read_page
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


class Page:
    def __init__(self) -> None:
        self.rows = []

    def __str__(self) -> str:
        return f'{self.rows}'

    def __len__(self) -> int:
        return len(self.rows)


def create_page(parent):
    msg_list = deque()
    for name, message in sql_child(parent):
        msg_list.append(ButtonData(message, name))

    p = Page()
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

        p.rows.append(temp.list_button)
    if len(p) > 5:
        sql_create_pages(p.rows)
        #p.rows = [p.rows[i] for i in range(5)]
        p.rows.append([ButtonData('Вперёд', '/next')])
        print(sql_read_page())

    return p


def create_keyboard(parent: str) -> InlineKeyboardMarkup:
    # Создаёт клавиатуру на основе запроса из базы данных
    inline_kbm = InlineKeyboardMarkup()
    root = sql_parent(parent)
    if root:
        inline_kbm.add(InlineKeyboardButton("Вернуться", callback_data=root))
    
    page = create_page(parent)
    for row in page.rows:
        temp = []
        for button_data in row:
            temp.append(InlineKeyboardButton(button_data.message, callback_data=button_data.name))
        inline_kbm.row(*temp)

    print(f'{page} {len(page)}')
    return inline_kbm
