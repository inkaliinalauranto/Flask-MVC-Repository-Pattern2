import contextlib
import os
import mysql.connector
import psycopg2


# Funktio, jota käytetään get_db_conn-dekoraattorifunktiossa.
@contextlib.contextmanager
def init_db_conn():
    # Alustetaan tietokantayhteyttä kuvaavan muuttujan arvo Noneksi:
    conn = None
    try:
        # Haetaan _db-muuttujaan DB-muuttujan arvo ympäristömuuttujista:
        _db = os.getenv("DB")

        # Jos _db-muuttujan arvo on mysql, conn-muuttujaan avataan
        # MySQL-tietokantayhteys ympäristömuuttujista haetuilla tiedoilla:
        if _db == "mysql":
            conn = mysql.connector.connect(user=os.getenv("MYSQL_USER"),
                                           database=os.getenv("DB_NAME"),
                                           password=os.getenv("MYSQL_PW"))
        # Jos _db-muuttujan arvo taas on postgres, conn-muuttujaan avataan
        # PostgreSQL-tietokantayhteys ympäristömuuttujista haettujen tietojen
        # avulla:
        elif _db == "postgres":
            conn = psycopg2.connect(f"dbname={os.getenv('DB_NAME')} "
                                    f"user={os.getenv('POSTGRES_USER')} "
                                    f"host={os.getenv('POSTGRES_HOST')} "
                                    f"password={os.getenv('POSTGRES_PW')}")

        # Palautetaan mahdollisen tietokantayhteyden sisällään pitävä
        # conn-muuttuja yieldin avulla, jolloin tähän funktioon palataan,
        # kun palautettua arvoa ei enää tarvita.
        yield conn
    finally:
        # Kun palautettua conn-muuttujan arvoa eli mahdollista
        # tietokantayhteyttä ei enää tarvita, suljetaan se, jos
        # tietokantayhteys on olemassa.
        if conn is not None:
            conn.close()
