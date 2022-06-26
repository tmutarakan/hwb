from aiogram import types, Dispatcher
from keyboards import client as kc
from create_bot import bot
from sqlite.sqlite_db import sql_read


async def commands_start(message: types.Message):
    await message.answer('Справочная', reply_markup=kc.create_keyboard(parent=''))


async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    if callback_query.data in ('', 'help'):
        # Возврат к началу
        await bot.send_message(callback_query.from_user.id, 'Справочная', reply_markup=kc.create_keyboard(parent=''))
    else:
        # Отправляет сообщение с новой клавиатурой
        await bot.send_message(callback_query.from_user.id, sql_read(callback_query.data), reply_markup=kc.create_keyboard(parent=callback_query.data))
    # Удаляет клавиатуру предыдущего сообщения
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=None)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_callback_query_handler(process_callback_button)
