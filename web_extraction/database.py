import sqlite3
import os

os.makedirs("../data", exist_ok=True)
DB_PATH = "../data/traffic_accident_data.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accidents (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   url TEXT UNIQUE,
                   location TEXT,
                   latitude REAL,
                   longitude REAL
        )
''')
    
    conn.commit()
    conn.close()
    print("Database has been successfully checked/initialized.")

def save_record(url, location, lat, lon):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO accidents (url, location, latitude, longitude)
            VALUES (?, ?, ?, ?)
''', (url, location, lat, lon))
        conn.commit()
        print(f"Successfully saved to the database: {location} ({lat}, {lon})")
    except sqlite3.IntegrityError:
        print("WARNING: This article already exists in the database, skip archiving.")
    finally:
        conn.close()