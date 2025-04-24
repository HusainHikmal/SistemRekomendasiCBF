import sqlite3
import pandas as pd
from config import Config

# Load CSV into DataFrame
DF = pd.read_csv('data/smartphones.csv')

def insert_data():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    cur = conn.cursor()
    for _, row in DF.iterrows():
        spec = row.get('specification', '')
        cur.execute('''
            INSERT INTO Smartphone (
                phone, brand, chipset, ram, storage, performance, prices, battery,
                main_camera, system_operation, size, lcd, band_1, images,
                release_month, release_year, specification
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
            row['Phone'], row['Brand'], row['Chipset'], row['RAM'], row['Storage'],
            row['Performance'], row['Prices'], row['Battery'], row['Main_Camera'],
            row['System_Operation'], row['Size'], row['LCD'], row['Band_1'], row['Images'],
            row['Release_Month'], row['Release_Year'], spec
        ))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    insert_data()
    print('CSV data loaded into database successfully.')