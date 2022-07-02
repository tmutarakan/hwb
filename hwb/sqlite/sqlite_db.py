# Модуль для базы данных
import sqlite3 as sq
import logging
from rich.logging import RichHandler


FORMAT = "%(message)s"
logging.basicConfig(
    level=logging.INFO, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
logger = logging.getLogger(__name__)


DB = 'db/command.db'


def sql_open_conn(db: str):
    conn = sq.connect(db)
    cur = conn.cursor()
    return conn, cur


def sql_child(parent: str):
    # Возвращает данные необходимые для клавиатуры
    conn, cur = sql_open_conn(DB)
    return cur.execute('SELECT * FROM command WHERE parent = ?', (parent, )).fetchall()


def sql_read(name: str):
    # Возвращает данные для ответного сообщения
    conn, cur = sql_open_conn(DB)
    res = cur.execute('SELECT content FROM command WHERE name = ?', (name, )).fetchone()
    if res:
        return res[0]

def sql_parent(name: str):
    # Возвращает данные для кнопки Назад
    conn, cur = sql_open_conn(DB)
    logger.info(f'sql query {name}')
    res = cur.execute('SELECT parent FROM command WHERE name = ?', (name, )).fetchone()
    if res:
        return res[0]
