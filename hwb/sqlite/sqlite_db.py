# Модуль для базы данных
import sqlite3 as sq
import logging
from rich.logging import RichHandler


FORMAT = "%(message)s"
logging.basicConfig(
    level=logging.INFO, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
logger = logging.getLogger(__name__)


DB = 'db/sqlite/command.db'


def _sql_open_conn(db: str) -> tuple():
    conn = sq.connect(db)
    cur = conn.cursor()
    return conn, cur


def get_childrens(parent: str) -> tuple:
    # Возвращает имя команды и текст для кнопки
    conn, cur = _sql_open_conn(DB)
    res = cur.execute(
        'SELECT name, message FROM command WHERE parent = ? ORDER BY name;',
        (parent, )).fetchall()
    conn.close()
    return res


def get_content(name: str) -> str or None:
    # Возвращает данные для ответного сообщения
    conn, cur = _sql_open_conn(DB)
    res = cur.execute(
        'SELECT content FROM command WHERE name = ?;',
        (name, )).fetchone()
    conn.close()
    if res:
        return res[0]


def get_parent(name: str) -> str or None:
    # Возвращает данные для кнопки "Вернуться"
    conn, cur = _sql_open_conn(DB)
    logger.info(f'sql query {name}')
    res = cur.execute(
        'SELECT parent FROM command WHERE name = ?;',
        (name, )).fetchone()
    conn.close()
    if res:
        return res[0]


def get_path(name: str) -> str or None:
    # Возвращает путь к файлу
    conn, cur = _sql_open_conn(DB)
    res = cur.execute(
        '''
        WITH _command AS (
            SELECT id
            FROM command
            WHERE name = ?)
        SELECT path
        FROM
            _command c
            JOIN file_path f ON c.id=f.command_id;
        ''',
        (name, )).fetchone()
    conn.close()
    if res:
        return res[0]
