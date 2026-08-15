"""
PostgreSQL connection handling using a simple psycopg2 connection pool.

Only the backend talks to the database - the pool is created once when the
Flask app starts and reused across requests.
"""
import logging

import psycopg2
import psycopg2.extras
from psycopg2 import pool

logger = logging.getLogger(__name__)

_connection_pool = None


def init_pool(app_config, minconn=1, maxconn=10):
    """Initialize the global connection pool. Call once at app startup."""
    global _connection_pool
    if _connection_pool is not None:
        return _connection_pool

    try:
        _connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn, maxconn, **app_config.db_connection_kwargs()
        )
        logger.info("Database connection pool created successfully.")
    except psycopg2.OperationalError as exc:
        # We don't crash the app on startup if the DB isn't reachable yet -
        # requests that need the DB will surface a 500 with a clear message,
        # and /health can be used to check readiness.
        logger.error("Could not create database connection pool: %s", exc)
        _connection_pool = None

    return _connection_pool


def get_connection():
    """Get a connection from the pool. Raises RuntimeError if unavailable."""
    if _connection_pool is None:
        raise RuntimeError("Database connection pool is not initialized.")
    return _connection_pool.getconn()


def put_connection(conn):
    """Return a connection to the pool."""
    if _connection_pool is not None and conn is not None:
        _connection_pool.putconn(conn)


def is_database_available():
    """Lightweight check used by /health to report DB reachability."""
    if _connection_pool is None:
        return False
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
        return True
    except Exception as exc:  # noqa: BLE001 - health check should never raise
        logger.error("Database health check failed: %s", exc)
        return False
    finally:
        if conn is not None:
            put_connection(conn)


class get_cursor:
    """
    Context manager that yields a RealDictCursor and handles
    commit/rollback + returning the connection to the pool.

    Usage:
        with get_cursor() as cur:
            cur.execute("SELECT * FROM tasks;")
            rows = cur.fetchall()
    """

    def __init__(self, commit=False):
        self.commit = commit
        self.conn = None
        self.cur = None

    def __enter__(self):
        self.conn = get_connection()
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None and self.commit:
                self.conn.commit()
            else:
                self.conn.rollback()
        finally:
            if self.cur is not None:
                self.cur.close()
            put_connection(self.conn)
        # Don't suppress exceptions
        return False
