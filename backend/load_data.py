#!/usr/bin/env python3
import argparse
import csv
import os
import sys
from typing import List

import psycopg2
from psycopg2.extras import execute_batch

EXPECTED_COLUMNS: List[str] = [
    "pickup_datetime",
    "dropoff_datetime",
    "pickup_lat",
    "pickup_lon",
    "dropoff_lat",
    "dropoff_lon",
    "trip_distance_km",
    "trip_duration_sec",
    "fare_amount",
    "tip_amount",
    "passenger_count",
    "payment_type",
    "avg_speed_kmh",
    "fare_per_km",
    "pickup_hour",
    "weekday",
    "is_weekend",
    "haversine_km",
]


def parse_args():
    p = argparse.ArgumentParser(description="Load cleaned NYC taxi CSV into Postgres trips table")
    p.add_argument("--csv", default=os.path.join("data", "cleaned_data.csv"), help="Path to cleaned CSV (default: data/cleaned_data.csv)")
    p.add_argument("--host", default=os.getenv("PGHOST", "localhost"))
    p.add_argument("--port", type=int, default=int(os.getenv("PGPORT", "5432")))
    p.add_argument("--dbname", default=os.getenv("PGDATABASE", "nyc_taxi"))
    p.add_argument("--user", default=os.getenv("PGUSER", "postgres"))
    p.add_argument("--password", default=os.getenv("PGPASSWORD"), help="Postgres password (or set PGPASSWORD env)")
    p.add_argument("--table", default="trips", help="Target table (default: trips)")
    p.add_argument("--truncate", action="store_true", help="Truncate table before load")
    p.add_argument("--skip-header-check", action="store_true", help="Skip CSV header validation")
    return p.parse_args()


def read_csv_header(csv_path: str) -> List[str]:
    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None:
            raise ValueError("CSV appears to be empty or missing a header row")
        return [h.strip() for h in header]


def validate_header(found: List[str], expected: List[str]):
    if found != expected:
        missing = [c for c in expected if c not in found]
        extra = [c for c in found if c not in expected]
        raise ValueError(
            "CSV header does not match expected columns.\n"
            f"Expected (order-sensitive): {expected}\n"
            f"Found: {found}\n"
            f"Missing: {missing}\n"
            f"Extra: {extra}"
        )


def main():
    args = parse_args()

    if not os.path.exists(args.csv):
        print(f"ERROR: CSV not found at {args.csv}", file=sys.stderr)
        sys.exit(1)

    if not args.skip_header_check:
        found = read_csv_header(args.csv)
        validate_header(found, EXPECTED_COLUMNS)
        print("Header validation: OK")

    dsn_parts = [
        f"host={args.host}",
        f"port={args.port}",
        f"dbname={args.dbname}",
        f"user={args.user}",
    ]
    if args.password:
        dsn_parts.append(f"password={args.password}")
    dsn = " ".join(dsn_parts)

    copy_sql = (
        f"COPY {args.table} (" + ",".join(EXPECTED_COLUMNS) + ") "
        "FROM STDIN WITH (FORMAT csv, HEADER true)"
    )

    try:
        with psycopg2.connect(dsn) as conn:
            conn.autocommit = True
            with conn.cursor() as cur:
                if args.truncate:
                    print(f"Truncating table {args.table} ...")
                    cur.execute(f"TRUNCATE TABLE {args.table};")
                print(f"Loading {args.csv} into {args.table} ...")
                with open(args.csv, "r", encoding="utf-8") as f:
                    cur.copy_expert(copy_sql, f)
                # Quick count
                cur.execute(f"SELECT COUNT(*) FROM {args.table};")
                total = cur.fetchone()[0]
                print(f"Load complete. Row count: {total}")
    except Exception as e:
        print("ERROR during load:", e, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
