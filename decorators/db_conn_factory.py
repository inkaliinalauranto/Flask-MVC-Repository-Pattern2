import contextlib
import os
import mysql.connector
import psycopg2


@contextlib.contextmanager
def init_db_conn():
    conn = None
    try:
        _db = os.getenv("DB")
        if _db == "mysql":
            conn = mysql.connector.connect(user=os.getenv("MYSQL_USER"),
                                           database=os.getenv("DB_NAME"),
                                           password=os.getenv("MYSQL_PW"))
        elif _db == "postgres":
            conn = psycopg2.connect(f"dbname={os.getenv('DB_NAME')} "
                                    f"user={os.getenv('POSTGRES_USER')} "
                                    f"host={os.getenv('POSTGRES_HOST')} "
                                    f"password={os.getenv('POSTGRES_PW')}")

        yield conn
    finally:
        if conn is not None:
            conn.close()
