"""
database.py — Conexão com MySQL via PyMySQL.
TODO: Para usar SQLite em vez de MySQL, troque get_connection() por sqlite3.connect().
"""
import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "the_keep"),
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": True,
}


def get_connection():
    """Retorna uma conexão nova. Feche após usar com conn.close()."""
    return pymysql.connect(**DB_CONFIG)


def query_one(sql: str, params=None):
    """Executa query e retorna um único resultado como dict (ou None)."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            return cur.fetchone()
    finally:
        conn.close()


def query_all(sql: str, params=None):
    """Executa query e retorna lista de dicts."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            return cur.fetchall()
    finally:
        conn.close()


def execute(sql: str, params=None):
    """Executa INSERT/UPDATE/DELETE. Retorna lastrowid."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            return cur.lastrowid
    finally:
        conn.close()
