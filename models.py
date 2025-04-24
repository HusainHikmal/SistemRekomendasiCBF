import sqlite3
from config import Config




def create_db():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    # conn = sqlite3.connect('instance/smartphones.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Smartphone (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone TEXT,
        brand TEXT,
        chipset TEXT,
        ram TEXT,
        storage TEXT,
        performance INTEGER,
        prices TEXT,
        battery TEXT,
        main_camera TEXT,
        system_operation TEXT,
        size REAL,
        lcd TEXT,
        band_1 TEXT,
        images TEXT,
        release_month TEXT,
        release_year INTEGER,
        specification TEXT
    )''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
    print('Database schema created successfully.')