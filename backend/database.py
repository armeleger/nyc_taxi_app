import os
import psycopg2
from urllib.parse import urlparse


def get_conn():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("Set DATABASE_URL env var, e.g. postgres://user:pass@localhost:5432/dbname")
    parsed = urlparse(db_url)
    return psycopg2.connect(
        dbname=parsed.path[1:],
        user=parsed.username,
        password=parsed.password,
        host=parsed.hostname,
        port=parsed.port,
    )

