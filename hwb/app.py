from aiogram.utils import executor
import logging
from rich.logging import RichHandler
from create_bot import dp
from handlers import client


FORMAT = "%(name)s %(asctime)s %(levelname)s %(message)s"
logging.basicConfig(
    filename='./log/info.log',
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]"
)

client.register_handlers_client(dp)
executor.start_polling(dp)
