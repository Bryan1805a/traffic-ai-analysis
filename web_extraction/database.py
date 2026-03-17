import sqlite3
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "traffic_accident_data.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accidents (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   url TEXT UNIQUE,
                   location TEXT,
                   latitude REAL,
                   longitude REAL,
                   deaths INTEGER,
                   injuries INTEGER,
                   vehicles TEXT
        )
''')
    
    conn.commit()
    conn.close()
    print("Database has been successfully checked/initialized.")

def save_record(url, location, lat, lon, deaths, injuries, vehicles):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO accidents (url, location, latitude, longitude, deaths, injuries, vehicles)
            VALUES (?, ?, ?, ?, ?, ?, ?)
''', (url, location, lat, lon, deaths, injuries, vehicles))
        conn.commit()
        print("SUCCESSFULLY SAVED TO DATABASE.")
        print(f"Location: {location} ({lat}, {lon})")
        print(f"Deaths: {deaths}")
        print(f"Injuries: {injuries}")
        print(f"Vehicles: {vehicles}")
    except sqlite3.IntegrityError:
        print("WARNING: This article already exists in the database, skip archiving.")
    finally:
        conn.close()