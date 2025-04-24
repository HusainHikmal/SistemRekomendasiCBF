import sqlite3
from config import Config


def get_db_connection():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_all_smartphones():
    with get_db_connection() as conn:
        return conn.execute(
            'SELECT id, phone, ram, storage, specification, chipset, prices, release_month, release_year, images FROM smartphone'
        ).fetchall()


def get_smartphone_by_id(phone_id):
    with get_db_connection() as conn:
        return conn.execute(
            'SELECT id, phone, ram, storage, specification FROM smartphone WHERE id = ?',
            (phone_id,)
        ).fetchone()


def get_unique_values(col):
    with get_db_connection() as conn:
        rows = conn.execute(f'SELECT DISTINCT {col} FROM smartphone').fetchall()
    return [r[0] for r in rows]