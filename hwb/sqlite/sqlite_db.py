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


def sql_open_conn(db: str) -> tuple(sq.Connection, sq.Cursor):
    conn = sq.connect(db)
    cur = conn.cursor()
    return conn, cur


def sql_child(parent: str) -> tuple:
    # Возвращает данные необходимые для клавиатуры
    conn, cur = sql_open_conn(DB)
    res =  cur.execute('SELECT name, message FROM command WHERE parent = ?', (parent, )).fetchall()
    conn.close()
    return res


def sql_read(name: str) -> str or None:
    # Возвращает данные для ответного сообщения
    conn, cur = sql_open_conn(DB)
    res = cur.execute('SELECT content FROM command WHERE name = ?', (name, )).fetchone()
    conn.close()
    if res:
        return res[0]


def sql_parent(name: str) -> str or None:
    # Возвращает данные для кнопки Назад
    conn, cur = sql_open_conn(DB)
    logger.info(f'sql query {name}')
    res = cur.execute('SELECT parent FROM command WHERE name = ?', (name, )).fetchone()
    conn.close()
    if res:
        return res[0]


def sql_path(name: str) -> str or None:
    # Возвращает путь к файлу
    conn, cur = sql_open_conn(DB)
    res = cur.execute('WITH _command AS (SELECT id FROM command WHERE name = ?)SELECT path FROM _command c JOIN file_path f ON c.id=f.command_id', (name, )).fetchone()
    conn.close()
    if res:
        return res[0]