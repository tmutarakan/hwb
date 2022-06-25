from aiogram.utils import executor
import logging
from rich.logging import RichHandler
from create_bot import dp
from handlers import client


FORMAT = "%(message)s"
logging.basicConfig(
    level=logging.INFO, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)


client.register_handlers_client(dp)
executor.start_polling(dp)
