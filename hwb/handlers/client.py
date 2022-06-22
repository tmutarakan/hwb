from aiogram import types, Dispatcher


async def commands_start(message: types.Message):
    await message.reply('Приятного аппетита')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])
