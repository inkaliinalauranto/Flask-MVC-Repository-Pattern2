import os
import psycopg2
from models import User
from repositories.users_repository import UsersRepository


# Luokka perii UsersRepository-luokan:
class UsersRepositoryPostgres(UsersRepository):
    def __init__(self, con):
        self.con = con
        super(UsersRepositoryPostgres, self).__init__(con)

    # Käyttäjän tietokantaan lisäävä metodi on RUD-metodeista poiketen
    # määritelty aliluokassa, koska toteutus on erilainen riippuen siitä,
    # onko käyttöön valittu MySQL- vai PostgreSQL-tietokanta. Metodi lisää
    # käyttäjän tietokantaan parametreina saaduilla arvoilla. Metodista
    # palautetaan User-luokan instanssi uuden käyttäjän tiedoilla.
    def add(self, username, firstname, lastname):
        try:
            with self.con.cursor() as cur:
                cur.execute("INSERT INTO users (username, firstname, lastname) "
                            "VALUES (%s, %s, %s) RETURNING *;",
                            (username, firstname, lastname))

                self.con.commit()
                user_tuple = cur.fetchone()

                return User(_id=user_tuple[0],
                            username=user_tuple[1],
                            firstname=user_tuple[2],
                            lastname=user_tuple[3])

        except Exception as e:
            self.con.rollback()
            raise e
