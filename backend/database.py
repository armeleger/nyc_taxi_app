import os
import sqlite3


def get_conn():
    db_path = os.getenv("SQLITE_PATH", os.path.join(os.path.dirname(__file__), "nyc_taxi.db"))
    conn = sqlite3.connect(db_path)
    return conn
