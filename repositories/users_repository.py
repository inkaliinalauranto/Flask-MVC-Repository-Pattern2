from werkzeug.exceptions import NotFound

from models import User


# UsersRepositoryMySQL- ja UsersRepositoryPostgres-luokkien yliluokka:
class UsersRepository:
    # Rakentaja, joka saa (aliluokiltaan) parametrina con-jäsenmuuttujansa
    # arvon. Välitetty arvo on avattu tietokantayhteys.
    def __init__(self, con):
        self.con = con

    '''Jäsenmetodit on toteutettu yliluokkaan, koska ne toimivat sekä 
    MySQL- että PostgreSQL-tietokannoilla'''

    # Metodi, joka hakee tietokannasta kaikki käyttäjät. Käyttäjät palautetaan
    # listan alkioina, jotka on muutettu User-luokan instansseiksi:
    def get_all(self):
        with self.con.cursor() as cur:
            cur.execute("SELECT * FROM users;")
            users_tuple_list = cur.fetchall()

            users_list = [User(_id=user_tuple[0],
                               username=user_tuple[1],
                               firstname=user_tuple[2],
                               lastname=user_tuple[3])
                          for user_tuple in users_tuple_list]

            return users_list

    # Metodi, joka hakee tietokannasta käyttäjän id:n perusteella. Jos
    # käyttäjää ei haetulla id:llä löydy, palautetaan arvo None. Muussa
    # tapauksessa käyttäjä palautetaan User-luokan instanssina:
    def get_by_id(self, user_id):
        with self.con.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
            user_tuple = cur.fetchone()

            if user_tuple is None:
                raise NotFound()

            return User(_id=user_tuple[0],
                        username=user_tuple[1],
                        firstname=user_tuple[2],
                        lastname=user_tuple[3])

    # Metodi, joka päivittää käyttäjän tiedot tietokantaan id:n perusteella:
    '''alla oleviin rollbackit'''
    def update_by_id(self, user_id, username, firstname, lastname):
        # Tarkistetaan ensin, löytyykö käyttäjää välitetyllä id:llä:
        user = self.get_by_id(user_id)

        # Jos käyttäjää ei löydy, palataan metodista None-arvolla:
        if user is None:
            raise NotFound()

        try:
            # Muussa tapauksessa päivitetään käyttäjän tiedot parametreina
            # saaduilla arvoilla ja palautetaan metodista User-luokan instanssi
            # päivitetyillä tiedoilla:
            with self.con.cursor() as cur:
                cur.execute("UPDATE users "
                            "SET username = %s, firstname = %s, lastname = %s "
                            "WHERE id = %s;",
                            (username, firstname, lastname, user_id,))

                self.con.commit()

                return User(_id=user_id,
                            username=username,
                            firstname=firstname,
                            lastname=lastname)

        except Exception as e:
            self.con.rollback()
            raise e

    # Metodi, joka päivittää käyttäjän sukunimen tietokantaan id:n perusteella:
    def update_lastname_by_id(self, user_id, lastname):
        user = self.get_by_id(user_id)

        if user is None:
            raise NotFound

        try:
            # Jos käyttäjä on olemassa välitetyllä id:llä, päivitetään käyttäjän
            # sukunimi parametrina saadulla arvolla ja palautetaan metodista
            # User-luokan instanssi päivitetyllä sukunimellä:
            with self.con.cursor() as cur:
                cur.execute("UPDATE users SET lastname = %s WHERE id = %s;",
                            (lastname, user_id,))

                self.con.commit()

                return User(_id=user_id,
                            username=user.username,
                            firstname=user.firstname,
                            lastname=lastname)
        except Exception as e:
            self.con.rollback()
            raise e

    # Metodi, joka poistaa käyttäjän tietokannasta id:n perusteella:
    def delete_by_id(self, user_id):
        user = self.get_by_id(user_id)

        if user is None:
            return None

        # Jos käyttäjä on olemassa välitetyllä id:llä, poistetaan käyttäjä ja
        # palautetaan metodista User-luokan instanssi poistetun käyttäjän
        # tiedoilla:
        with self.con.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
            self.con.commit()

            return User(_id=user_id,
                        username=user.username,
                        firstname=user.firstname,
                        lastname=user.lastname)
