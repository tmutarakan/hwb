from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlite.sqlite_db import sql_child, sql_parent
from collections import deque
from keyboards.config import LIMIT_ROWS, MAX_STRING_LENGTH
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import pickle
import os
import json


storage = MemoryStorage()


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
        self.count: int = 0           # Количество кнопок в строке
        self.length: int = 0          # Суммарная длина текста кнопок
        self.list_length: list = []   # Длина текста каждой кнопки
        self.all_length: bool = True  # Вмещается ли текст всех кнопок в строке
        self.list_button: list = []   # Список для кнопок


class State:
    def __init__(self, rows: list, root: str, parent:str, user_id: int) -> None:
        self.root: str = root
        self.parent: str = parent
        self.user_id: int = user_id
        self.curr: int = 0
        self.length: int = 0
        self.page: list = []
        self.b_prev: ButtonData = ButtonData('Назад', '/prev')
        self.b_next: ButtonData = ButtonData('Вперёд', '/next')
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
            self.page[0].append([ButtonData('Вперёд', '/next')]) # не работает через атрибут
            [self.page[i].append([
                self.b_prev,
                self.b_next
                ]) for i in range(1, self.length)]
            self.page[self.length].append([self.b_prev])

    def __getstate__(self) -> dict:  # Как мы будем "сохранять" класс
        state = {}
        state["user_id"] = self.user_id
        state["curr"] = self.curr
        state["root"] = self.root
        state["parent"] = self.parent
        state["page"] = self.page
        state["length"] = self.length
        return state

    def __setstate__(self, state: dict):  # Восстанавливать класс из байтов
        self.user_id = state["user_id"]
        self.curr = state["curr"]
        self.root = state["root"]
        self.parent = state["parent"]
        self.page = state["page"]
        self.length = state["length"]

    def __str__(self) -> str:
        return f'{self.page}'

    def __len__(self) -> int:
        return self.length


def create_rows(parent: str) -> list:
    msg_list = deque()
    for name, message in sql_child(parent):
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
    root = sql_parent(parent)
    if root:
        inline_kbm.add(InlineKeyboardButton("Вернуться", callback_data=root))
    rows = create_rows(parent)
    st = State(rows, root, parent, user_id)
    if os.path.exists(f"temp/{user_id}_{parent[1:]}.pkl"):
        with open(f"temp/{user_id}_{parent[1:]}.pkl", "rb") as fp:
            prev_st = pickle.load(fp)
        if prev_st.parent == parent:
            st = prev_st
            print(f'{user_id}_{parent[1:]} {root} {parent} {st.curr}')
    with open(f"temp/{user_id}_{parent[1:]}.pkl", "wb") as fp:
        pickle.dump(st, fp)
    latest = {user_id: {'filename': f"temp/{user_id}_{parent[1:]}.pkl"}}
    with open("temp/current.json", "w") as fp:
        json.dump(latest, fp, ensure_ascii=False, indent=4)
    print(root, parent, st.curr)
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
    with open("temp/current.json", "r") as fp:
        latest = json.load(fp)
    with open(latest[str(user_id)]['filename'], "rb") as fp:
        st = pickle.load(fp)
    if data == '/prev':
        st.curr -= 1
    else:
        st.curr += 1
    with open(latest[str(user_id)]['filename'], "wb") as fp:
        pickle.dump(st, fp)
    inline_kbm = InlineKeyboardMarkup()
    root = st.root
    if root:
        inline_kbm.add(InlineKeyboardButton("Вернуться", callback_data=root))
    print(st.curr)
    pages = st.page[st.curr]
    for row in pages:
        temp = []
        for button in row:
            temp.append(
                InlineKeyboardButton(button.message, callback_data=button.name)
                )
        inline_kbm.row(*temp)
    return inline_kbm
