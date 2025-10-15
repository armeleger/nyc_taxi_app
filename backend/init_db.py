#!/usr/bin/env python3
import os
import sys
import psycopg2

HOST = os.getenv('PGHOST', 'localhost')
PORT = int(os.getenv('PGPORT', '5432'))
USER = os.getenv('PGUSER', 'postgres')
PASSWORD = os.getenv('PGPASSWORD')
DB_NAME = os.getenv('PGDATABASE', 'nyc_taxi')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')


def connect(dbname: str):
    kwargs = dict(host=HOST, port=PORT, dbname=dbname, user=USER)
    if PASSWORD:
        kwargs['password'] = PASSWORD
    return psycopg2.connect(**kwargs)


def ensure_database():
    with connect('postgres') as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname=%s", (DB_NAME,))
            exists = cur.fetchone() is not None
            if not exists:
                cur.execute(f"CREATE DATABASE {DB_NAME}")
                print(f"Created database {DB_NAME}")
            else:
                print(f"Database {DB_NAME} already exists")


def apply_schema():
    if not os.path.exists(SCHEMA_PATH):
        print(f"ERROR: schema.sql not found at {SCHEMA_PATH}", file=sys.stderr)
        sys.exit(2)
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        sql = f.read()
    with connect(DB_NAME) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
    print(f"Applied schema from {SCHEMA_PATH} to {DB_NAME}")


def main():
    try:
        ensure_database()
        apply_schema()
        print("DB initialization complete")
    except Exception as e:
        print("ERROR:", e, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
