from aiogram import types, Dispatcher
from aiogram.types import InputFile
from keyboards import client as kc
from create_bot import bot
from sqlite.sqlite_db import sql_read, sql_path, sql_parent


async def commands_start(message: types.Message):
    await message.answer(f'{message.from_user.full_name} вас приветствует справочная.', reply_markup=kc.create_keyboard(parent='help'))


async def process_callback_button(callback_query: types.CallbackQuery):
    data = callback_query.data
    await bot.answer_callback_query(callback_query.id)
    if data == 'help':
        # Возврат к началу
        await bot.send_message(
            callback_query.from_user.id,
            f'{callback_query.from_user.full_name} вас приветствует справочная.',
            reply_markup=kc.create_keyboard(parent='help'))
    elif '_file' in data:
        await bot.send_document(callback_query.from_user.id, InputFile(sql_path(data)))
        data = sql_parent(data)
        await bot.send_message(callback_query.from_user.id, sql_read(data), reply_markup=kc.create_keyboard(parent=data))
    else:
        # Отправляет сообщение с новой клавиатурой
        await bot.send_message(callback_query.from_user.id, sql_read(data), reply_markup=kc.create_keyboard(parent=data))
    # Удаляет клавиатуру предыдущего сообщения
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=None)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_callback_query_handler(process_callback_button)
