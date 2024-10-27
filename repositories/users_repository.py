from werkzeug.exceptions import NotFound

from models import User


# UsersRepositoryMySQL- ja UsersRepositoryPostgres-luokkien yliluokka:
class UsersRepository:
    # Rakentaja, joka saa (aliluokiltaan) parametrina con-jäsenmuuttujansa
    # arvon. Välitetty arvo on avattu tietokantayhteys.
    def __init__(self, con):
        self.con = con

    '''Jäsenmetodit on toteutettu yliluokkaan, koska ne toimivat sekä 
    MySQL- että PostgreSQL-tietokannoilla. Metodit ovat asynkronisia, 
    koska niissä toteutetaan tietokantaoperaatioita tietokantapalvelimelle.'''

    # Metodi, joka hakee tietokannasta kaikki käyttäjät. Käyttäjät palautetaan
    # listan alkioina, jotka on muutettu User-luokan instansseiksi:
    async def get_all(self):
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
    # käyttäjää ei haetulla id:llä löydy, palautetaan NotFound-poikkeus.
    # Muussa tapauksessa käyttäjä palautetaan User-luokan instanssina:
    async def get_by_id(self, user_id):
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
    async def update_by_id(self, user_id, username, firstname, lastname):
        try:
            # Tarkistetaan ensin, löytyykö käyttäjää välitetyllä id:llä:
            await self.get_by_id(user_id)

            # Jos käyttäjä löytyy, päivitetään käyttäjän tiedot parametreina
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
            # Jos metodi epäonnistuu, perutaan tietokantaoperaatio:
            self.con.rollback()
            raise e

    # Metodi, joka päivittää käyttäjän sukunimen tietokantaan id:n perusteella:
    async def update_lastname_by_id(self, user_id, lastname):
        try:
            user = await self.get_by_id(user_id)

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
            # Jos metodi epäonnistuu, perutaan tietokantaoperaatio:
            self.con.rollback()
            raise e

    # Metodi, joka poistaa käyttäjän tietokannasta id:n perusteella:
    async def delete_by_id(self, user_id):
        try:
            user = await self.get_by_id(user_id)

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

        except Exception as e:
            # Jos metodi epäonnistuu, perutaan tietokantaoperaatio:
            self.con.rollback()
            raise e
