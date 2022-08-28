from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlite.sqlite_db import get_childrens, get_parent
from collections import deque
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
import json
from dataclasses import dataclass, field
from keyboards.config import (
    LIMIT_ROWS, MAX_STRING_LENGTH, BACK_BUTTON, PREV_BUTTON, NEXT_BUTTON)
import redis


r = redis.Redis(host='redis7', port=6379)


@dataclass
class ButtonData:
    message: str
    name: str


@dataclass
class TempData:
    count: int = 0              # Количество кнопок в строке
    length: int = 0             # Суммарная длина текста кнопок
    list_length: list = field(
        default_factory=list)   # Длина текста каждой кнопки
    all_length: bool = True     # Вмещается ли текст всех кнопок в строке
    list_button: list = field(
        default_factory=list)   # Список для кнопок


class State:
    def __init__(
        self, rows: list = [],
        root: str = '',
        parent: str = '',
        user_id: int = 0
    ):
        self.root: str = root        # родитель
        self.parent: str = parent    # имя команды
        self.user_id: int = user_id  # идентификатор пользователя
        self.curr: int = 0           # номер текущей страницы
        self.length: int = 0         # количество страниц
        self.page: list = []         # содержимое страниц
        self.b_prev: ButtonData = ButtonData(PREV_BUTTON, '/prev')
        self.b_next: ButtonData = ButtonData(NEXT_BUTTON, '/next')
        self.create_paginator(rows)

    def create_paginator(self, rows):
        i = 0
        if len(rows) <= LIMIT_ROWS:
            self.page.append(rows)
        else:
            self.page.append([_ for _ in rows[:LIMIT_ROWS]])
            rows = rows[LIMIT_ROWS:]
            i += 1
            while len(rows) > LIMIT_ROWS:
                self.page.append([_ for _ in rows[:LIMIT_ROWS]])
                rows = rows[LIMIT_ROWS:]
                i += 1
            self.page.append([_ for _ in rows])
        self.length = i
        if self.length:
            self.page[0].append([self.b_next])
            [self.page[i].append([
                self.b_prev,
                self.b_next
                ]) for i in range(1, self.length)]
            self.page[self.length].append([self.b_prev])

    def to_dict(self) -> dict:
        return self.__getstate__()

    def from_dict(self, state: dict):
        self.__setstate__(state)

    def __getstate__(self) -> dict:  # Как мы будем "сохранять" класс
        state = {}
        state["user_id"] = self.user_id
        state["curr"] = self.curr
        state["root"] = self.root
        state["parent"] = self.parent
        state["page"] = [
            [
                [
                    {
                        'message': button.message,
                        'name': button.name
                    } for button in row
                ] for row in page
            ] for page in self.page
        ]
        # state["page"] = self.page
        state["length"] = self.length
        return state

    def __setstate__(self, state: dict):  # Восстанавливать класс из байтов
        self.user_id = state["user_id"]
        self.curr = state["curr"]
        self.root = state["root"]
        self.parent = state["parent"]
        self.page = [
            [
                [
                    ButtonData(
                        button['message'], button['name']
                        ) for button in row
                ] for row in page
            ] for page in state["page"]
        ]
        # self.page = state["page"]
        self.length = state["length"]

    def __str__(self) -> str:
        return f'{self.page}'

    def __len__(self) -> int:
        return self.length


def create_rows(parent: str) -> list:
    msg_list = deque()
    for name, message in get_childrens(parent):
        msg_list.append(ButtonData(message, name))

    rows = []
    while len(msg_list) > 0:
        temp = TempData()
        for elem in msg_list:
            elem_length = len(elem.message)
            # Максимальная длина сообщения в кнопке
            elem_size = MAX_STRING_LENGTH/(temp.count + 1)
            for temp_elem in temp.list_length:
                if temp_elem > elem_size:
                    temp.all_length = False
                    break
            if temp.length + elem_length > MAX_STRING_LENGTH or \
               elem_length > elem_size or \
               not temp.all_length:
                break
            else:
                temp.count += 1
                temp.length += elem_length
                temp.list_length.append(elem_length)
        for _ in range(temp.count):
            temp.list_button.append(msg_list.popleft())
        rows.append(temp.list_button)
    return rows


def create_keyboard(parent: str, user_id: int) -> InlineKeyboardMarkup:
    # Создаёт клавиатуру на основе запроса из базы данных
    inline_kbm = InlineKeyboardMarkup()
    root = get_parent(parent)
    rows = create_rows(parent)
    st = State(rows, root, parent, user_id)
    if str.encode(f"{user_id}_{parent[1:]}") in r.keys():
        prev_st = State()
        prev_st.from_dict(json.loads(r.get(f"{user_id}_{parent[1:]}")))
        if prev_st.parent == parent:
            st = prev_st
    r.set(f"{user_id}_{parent[1:]}", json.dumps(st.to_dict()))
    r.set(user_id, f"{user_id}_{parent[1:]}")
    if st.root:
        inline_kbm.add(
            InlineKeyboardButton(BACK_BUTTON, callback_data=st.root)
            )
    for row in st.page[st.curr]:
        temp = []
        for button_data in row:
            temp.append(
                InlineKeyboardButton(
                    button_data.message,
                    callback_data=button_data.name
                    )
                )
        inline_kbm.row(*temp)
    return inline_kbm


def edit_keyboard(data: str, user_id: int) -> InlineKeyboardMarkup:
    latest = r.get(user_id)
    st = State()
    st.from_dict(json.loads(r.get(latest)))
    if data == '/prev':
        st.curr -= 1
    else:
        st.curr += 1
    r.set(latest, json.dumps(st.to_dict()))
    inline_kbm = InlineKeyboardMarkup()
    root = st.root
    if root:
        inline_kbm.add(InlineKeyboardButton(BACK_BUTTON, callback_data=root))
    pages = st.page[st.curr]
    for row in pages:
        temp = []
        for button in row:
            temp.append(
                InlineKeyboardButton(button.message, callback_data=button.name)
                )
        inline_kbm.row(*temp)
    return inline_kbm
