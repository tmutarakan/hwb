# Модуль для базы данных
import sqlite3 as sq
import logging
from config import DB


FORMAT = "%(name)s %(asctime)s %(levelname)s %(message)s"
logging.basicConfig(
    filename='./log/info.log',
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]"
)
logger = logging.getLogger(__name__)


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
        SELECT photo
        FROM command
        WHERE name = ?;
        ''',
        (name, )).fetchone()
    conn.close()
    if res:
        return res[0]
