import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "traceability.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY, filename TEXT, phash TEXT)")

def add_image(filename, phash):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO images (filename, phash) VALUES (?, ?)", (filename, phash))

def get_all_images():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("SELECT filename, phash FROM images").fetchall()