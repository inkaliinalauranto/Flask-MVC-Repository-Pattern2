import os
import mysql.connector
from models import User
from repositories.users_repository import UsersRepository


# Luokka perii UsersRepository-luokan:
class UsersRepositoryMySQL(UsersRepository):
    # Rakentajametodi, joka vastaanottaa parametrina tietokantayhteyden:
    def __init__(self, con):
        self.con = con
        # Kutsutaan yliluokan rakentajaa, jonka jäsenmuuttujaksi välitetään
        # tämän luokan jäsenmuuttuja eli avattu tietokantayhteys:
        super().__init__(con)

    # Käyttäjän tietokantaan lisäävä metodi on RUD-metodeista poiketen
    # määritelty aliluokassa, koska toteutus on erilainen riippuen siitä,
    # onko käyttöön valittu MySQL- vai PostgreSQL-tietokanta. Metodi lisää
    # käyttäjän tietokantaan parametreina saaduilla arvoilla. Metodista
    # palautetaan User-luokan instanssi uuden käyttäjän tiedoilla.
    async def add(self, username, firstname, lastname):
        try:
            with self.con.cursor() as cur:
                cur.execute("INSERT INTO users (username, firstname, lastname) "
                            "VALUES (%s, %s, %s);", (username, firstname, lastname))

                self.con.commit()

                return User(_id=cur.lastrowid,
                            username=username,
                            firstname=firstname,
                            lastname=lastname)

        except Exception as e:
            # Jos metodi epäonnistuu, perutaan tietokantaoperaatio:
            self.con.rollback()
            raise e
