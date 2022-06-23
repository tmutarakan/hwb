from aiogram import types, Dispatcher
from keyboards import client as kc
from create_bot import bot


async def commands_start(message: types.Message):
    await message.answer('Начало', reply_markup=kc.inline_kb1)


#@dp.callback_query_handler(func=lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')
    await bot.edit_message_reply_markup(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        reply_markup=None)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_callback_query_handler(process_callback_button1, lambda c: c.data == 'button1')
