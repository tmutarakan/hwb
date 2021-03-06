from aiogram import types, Dispatcher
from aiogram.types import InputFile
from keyboards import client as kc
from create_bot import bot
from sqlite.sqlite_db import sql_read, sql_path


async def commands_start(message: types.Message):
    user_id = message.from_user.id
    await message.answer(
        f'{message.from_user.full_name} вас приветствует справочная.',
        reply_markup=kc.create_keyboard(parent='root', user_id=user_id)
        )


async def delete_prev_markup(user_id, message_id):
    # Удаляет клавиатуру предыдущего сообщения
    await bot.edit_message_reply_markup(
        chat_id=user_id,
        message_id=message_id,
        reply_markup=None)


async def root_callback_button(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    fn = callback_query.from_user.full_name
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        user_id,
        f'{fn} вас приветствует бот - справочная.',
        reply_markup=kc.create_keyboard(parent='root', user_id=user_id)
        )
    await delete_prev_markup(user_id, callback_query.message.message_id)


async def file_callback_button(callback_query: types.CallbackQuery):
    data = callback_query.data
    user_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    await bot.send_document(
        user_id,
        InputFile(sql_path(data)),
        reply_markup=kc.create_keyboard(parent=data, user_id=user_id)
        )
    await delete_prev_markup(user_id, callback_query.message.message_id)


async def photo_callback_button(callback_query: types.CallbackQuery):
    data = callback_query.data
    user_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    await bot.send_photo(
        user_id,
        InputFile(sql_path(data)),
        caption=sql_read(data),
        reply_markup=kc.create_keyboard(parent=data, user_id=user_id)
        )
    await delete_prev_markup(user_id, callback_query.message.message_id)


async def page_callback_button(callback_query: types.CallbackQuery):
    data = callback_query.data
    user_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_reply_markup(
        chat_id=user_id,
        message_id=callback_query.message.message_id,
        reply_markup=kc.edit_keyboard(data=data, user_id=user_id))


async def process_callback_button(callback_query: types.CallbackQuery):
    data = callback_query.data
    user_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    # Отправляет сообщение с новой клавиатурой
    await bot.send_message(
        user_id, sql_read(data),
        reply_markup=kc.create_keyboard(parent=data, user_id=user_id)
        )
    await delete_prev_markup(user_id, callback_query.message.message_id)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_callback_query_handler(
        root_callback_button,
        lambda callback_query: callback_query.data == 'root'
        )
    dp.register_callback_query_handler(
        page_callback_button,
        lambda callback_query: callback_query.data == '/next'
        )
    dp.register_callback_query_handler(
        page_callback_button,
        lambda callback_query: callback_query.data == '/prev'
        )
    dp.register_callback_query_handler(
        file_callback_button,
        lambda callback_query: '_file' in callback_query.data
        )
    dp.register_callback_query_handler(
        photo_callback_button,
        lambda callback_query: '_photo' in callback_query.data
        )
    dp.register_callback_query_handler(
        root_callback_button,
        lambda callback_query: callback_query.data == '/prev'
        or callback_query.data == '/next', state='*'
        )
    dp.register_callback_query_handler(process_callback_button)
