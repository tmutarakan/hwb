from email import message
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlite.sqlite_db import sql_child, sql_parent
from collections import deque


class ButtonData:
    def __init__(self, message: str, name: str) -> None:
        self.message: str = message
        self.name: str = name

    def __str__(self) -> str:
        return f'{self.name} {self.message}'

    def __repr__(self) -> str:
        return f'{self.name} {self.message}'


class TempData:
    def __init__(self) -> None:
        self.count: int = 0              # Количество кнопок в строке
        self.length: int = 0             # Суммарная длина текста кнопок
        self.list_length: list = []       # Длина текста каждой кнопки
        self.all_length: bool = True      # Вмещается ли текст всех кнопок в строке
        self.list_button: list = []       # Список для кнопок


class State:
    def __init__(self, rows: list, root: str) -> None:
        self.curr: int = 0
        self.root: str = root
        self.page: dict = {}

        i = 0
        if len(rows) < 5:
            self.page[i] = rows
        else:            
            self.page[i] = [_ for _ in rows[:5]]
            self.page[i].append([ButtonData('Вперёд', '/next')])
            rows = rows[5:]
            i += 1
            while len(rows) > 5:
                self.page[i] = [_ for _ in rows[:5]]
                self.page[i].append([ButtonData('Назад', '/prev'), ButtonData('Вперёд', '/next')])
                rows = rows[5:]
                i += 1
            self.page[i] = [_ for _ in rows]
            self.page[i].append([ButtonData('Назад', '/prev')])
        self.length: int = i + 1

    def __str__(self) -> str:
        return f'{self.page}'

    def __len__(self) -> int:
        return self.length


def create_rows(parent: str):
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
    rows = create_rows(parent)
    global st
    st = State(rows, root)
    print(st)
    for row in st.page[0]:
        temp = []
        for button_data in row:
            temp.append(InlineKeyboardButton(button_data.message, callback_data=button_data.name))
        inline_kbm.row(*temp)    
    #print(f'{page} {len(page)}')
    return inline_kbm


def edit_keyboard(data: str):
    global st
    if data == '/prev':
        st.curr -= 1
    else:
        st.curr += 1
    inline_kbm = InlineKeyboardMarkup()
    root = st.root
    if root:
        inline_kbm.add(InlineKeyboardButton("Вернуться", callback_data=root))

    pages = st.page[st.curr]
    for row in pages:
        temp = []
        for button in row:
            temp.append(InlineKeyboardButton(button.message, callback_data=button.name))
        inline_kbm.row(*temp)
    return inline_kbm
