"""
Convenience script to initialize (and optionally seed) the database
using the same env vars as the Flask backend. This is an alternative
to running init.sql / seed.sql manually with psql.

Usage (from the backend's virtualenv, so psycopg2 is available):

    python database/init_db.py            # creates schema only
    python database/init_db.py --seed      # creates schema + sample data
"""
import argparse
import os
import sys

import psycopg2

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_connection_kwargs():
    return {
        "host": os.environ.get("DB_HOST", "localhost"),
        "port": os.environ.get("DB_PORT", "5432"),
        "dbname": os.environ.get("DB_NAME", "taskdb"),
        "user": os.environ.get("DB_USER", "taskuser"),
        "password": os.environ.get("DB_PASSWORD", "taskpassword"),
    }


def run_sql_file(cur, filename):
    path = os.path.join(SCRIPT_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()
    cur.execute(sql)


def main():
    parser = argparse.ArgumentParser(description="Initialize the task management database.")
    parser.add_argument("--seed", action="store_true", help="Also insert sample data.")
    args = parser.parse_args()

    try:
        conn = psycopg2.connect(**get_connection_kwargs())
    except psycopg2.OperationalError as exc:
        print(f"Could not connect to PostgreSQL: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        with conn:
            with conn.cursor() as cur:
                print("Creating schema (init.sql)...")
                run_sql_file(cur, "init.sql")
                if args.seed:
                    print("Inserting sample data (seed.sql)...")
                    run_sql_file(cur, "seed.sql")
        print("Database initialization complete.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
