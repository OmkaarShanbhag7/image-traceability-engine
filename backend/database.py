import sqlite3
from datetime import datetime

DB_NAME = "traceability.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        phash TEXT,
        upload_time TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert_image(filename, phash):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO images (filename, phash, upload_time)
        VALUES (?, ?, ?)
        """, (filename, phash, datetime.now().isoformat()))

        conn.commit()
        conn.close()
    except Exception as e:
        print("DB insert error:", e)
        
def get_all_images():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT filename, phash, upload_time FROM images")
        data = cursor.fetchall()

        conn.close()
        return data
    except Exception as e:
        print("DB read error:", e)
        return []