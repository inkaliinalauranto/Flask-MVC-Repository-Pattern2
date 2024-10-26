import os
import mysql.connector
from models import User
from repositories.users_repository import UsersRepository


# Luokka perii UsersRepository-luokan:
class UsersRepositoryMySQL(UsersRepository):
    # Rakentajametodi
    def __init__(self, con):
        # Avataan MySQL-tietokantayhteys .env-tiedostoon määritellyillä
        # MySQL-tietokannan tiedoilla:
        super().__init__(con)
        self.con = con

    # Käyttäjän tietokantaan lisäävä metodi on RUD-metodeista poiketen
    # määritelty aliluokassa, koska toteutus on erilainen riippuen siitä,
    # onko käyttöön valittu MySQL- vai PostgreSQL-tietokanta. Metodi lisää
    # käyttäjän tietokantaan parametreina saaduilla arvoilla. Metodista
    # palautetaan User-luokan instanssi uuden käyttäjän tiedoilla.
    def add(self, username, firstname, lastname):
        with self.con.cursor() as cur:
            cur.execute("INSERT INTO users (username, firstname, lastname) "
                        "VALUES (%s, %s, %s);", (username, firstname, lastname))

            self.con.commit()

            return User(_id=cur.lastrowid,
                        username=username,
                        firstname=firstname,
                        lastname=lastname)
