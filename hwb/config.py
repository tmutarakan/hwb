from os import getenv, environ


# keyboards/client.py
LIMIT_ROWS = 5
MAX_STRING_LENGTH = 36
NEXT_BUTTON = 'Вперёд \u27A1'
PREV_BUTTON = '\u2B05 Назад'
BACK_BUTTON = '\u2B06 Вернуться'

# handlers/client.py
DEFAULT_PATH_JPG = "./static/default.jpg"
DEFAULT_PATH_WITHOUT_PHOTO = "./static/without.png"

# sqlite/sqlite_db.py
DB = getenv('DB')

# create_bot.py
TOKEN = getenv('TOKEN')

# keyboards/client.py
REDIS_CONTAINER_NAME = getenv('REDIS_CONTAINER_NAME')
REDIS_CONTAINER_PORT = getenv('REDIS_CONTAINER_PORT')
