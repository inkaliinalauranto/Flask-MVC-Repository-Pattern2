import re
import httpx
from werkzeug.exceptions import NotFound
from models import User


class UserRepositoryJSONPH:
    # Metodi, joka muuttaa parametrina saadun käyttäjä-dictionaryn
    # User-luokan instanssiksi:
    def parse_to_user(self, user_dict):
        # Koska API:sta haettu name-avain sisältää sekä suku- että
        # etunimen, talletetaan nimen osat listaan omiksi alkioikseen
        # välilyönneistä katkaistuina:
        split_whole_name = user_dict.get("name").split(" ")

        # Hyödynnettään re-kirjaston (regular expressionin käyttämisen
        # lähdemateriaali: https://www.geeksforgeeks.org/python-regex/)
        # search-metodia, jonka avulla validoidaan nimen osat
        # sisältävän listan ensimmäistä alkiota. Jos alkio ei koostu
        # esim. merkkijonoista "MRS.", "Mr", "mrs" ym, annetaan
        # firstname-muuttujaksi tämä alkio ja lastname-muuttujan arvoksi
        # loput alkiot välilyönneillä yhdistettiynä.
        if re.search(r'[Mm][Rr][Ss]?\.?', split_whole_name[0]) is None:
            firstname = split_whole_name[0]
            lastname = " ".join(split_whole_name[1:])
        # Muussa tapauksessa annetaan firstname-muuttujan arvoksi
        # alkio 1, koska silloin etunimen edessä on siviilisäätyä
        # kuvaava kirjainyhdistelmä. lastname-muuttujan arvoksi
        # asetetaan listan loput alkiot välilyönneillä yhdistettyinä.
        else:
            firstname = split_whole_name[1]
            lastname = " ".join(split_whole_name[2:])

        return User(_id=user_dict.get("id"),
                    username=user_dict.get("username"),
                    firstname=firstname,
                    lastname=lastname)

    '''Rajapinnasta tietoja hakevat metodit ovat asynkronisia.'''

    # Metodi, joka hakee verkon yli kaikki käyttäjät. Käyttäjät palautetaan
    # listan alkioina, jotka on muutettu User-luokan instansseiksi:
    async def get_all(self):
        async with httpx.AsyncClient() as client:
            # httpx-kirjaston AsyncClient-instanssin avulla haetaan
            # käyttäjätiedot web-ohjelmointirajapinnasta:
            res = await client.get(url="https://jsonplaceholder.typicode.com/users")
            # Muutetaan haetut tiedot Python-formaattiin httpx-kirjaston
            # json-metodia hyödyntämällä
            # (lähde: https://mitjamartini.com/blog/2023/01/15/fetching-data-from-rest-apis-with-python-and-httpx/):
            user_dicts_list = res.json()

            # Käydään silmukassa läpi kunkin listassa olevan käyttäjän
            # dictionary-muotoiset tiedot. parse_to_user-metodia hyödyntämällä
            # lisätään kukin käyttäjä User-luokan instanssina
            # users_list-muuttujaan:
            users_list = [self.parse_to_user(user_dict)
                          for user_dict in user_dicts_list]

            # Palautetaan metodista lista, joka pitää sisällään käyttäjät
            # User-luokan instansseina:
            return users_list

    # Metodi, joka hakee verkon yli yksittäisen käyttäjän tiedot id:n
    # perusteella.
    async def get_by_id(self, user_id):
        async with httpx.AsyncClient() as client:
            res = await client.get(url=f"https://jsonplaceholder.typicode.com/users/{user_id}")
            user_dict = res.json()

            # Jos käyttäjää parametrina saadulla id:llä ei löydy, nostetaan
            # poikkeuksena NotFound-instanssi
            if user_dict == {}:
                raise NotFound()

            # Jos käyttäjä löytyy, se muutetaan User-luokan instanssiksi
            # parse_to_user-metodia hyödyntämällä. Asetetaan instanssi
            # paluuarvoksi:
            return self.parse_to_user(user_dict)
