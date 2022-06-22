from aiogram.utils import executor
import logging
from rich.logging import RichHandler
from create_bot import dp

FORMAT = "%(message)s"
logging.basicConfig(
    level=logging.INFO, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

executor.start_polling(dp)
