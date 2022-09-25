from aiogram import types, Dispatcher
import os


async def commands_start(message: types.Message):
    # Возвращает последние 10 строк из лог файла
    text = ''
    with open('./log/info.log', 'rb') as f:
        try:  # catch OSError in case of a one line file 
            f.seek(-2, os.SEEK_END)
            for i in range(10):
                count = 0
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
                    count += 1
                text = f"{10 - i}){f.readline().decode()}{text}"
                f.seek(-1 * count - 3, os.SEEK_CUR)
        except OSError:
            f.seek(0)
    await message.answer(text=text)


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=['admin'])
