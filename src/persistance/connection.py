import os
import sqlite3
import pymysql
from dotenv import load_dotenv

load_dotenv()


def get_engine():
    return os.getenv("DB_ENGINE", "sqlite").lower()


def prefix_sql():
    if get_engine() == "sqlite":
        return "?"
    return "%s"


def open_connection():
    engine = get_engine()
    if engine == "sqlite":
        connection = sqlite3.connect(os.getenv("DB_NAME", "ecotech.db"))
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    if engine == "mysql":
        return pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            charset="utf8mb4",
        )

    raise ValueError(f"Motor no soportado: {engine}")
