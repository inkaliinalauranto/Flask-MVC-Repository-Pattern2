# Tarkoituksena on, että valmiissa koodissa ylikirjoitetaan
# UsersRepositoryn (yliluokan) get_all-metodi tämän luokan toteutuksella
import re

import httpx

from models import User


class UserRepositoryJSONPlaceholder:
    def __init__(self):
        pass

    @staticmethod
    def get_all():
        user_info = httpx.get(url="https://jsonplaceholder.typicode.com/users",
                              headers={"Accept": "application/json"}).json()

        users = []

        for user in user_info:
            splitted_whole_name = user.get("name").split(" ")

            # findall palauttaa listan
            # https://www.geeksforgeeks.org/python-regex/
            if re.search(r'[Mm][Rr][Ss]?\.', splitted_whole_name[0]) is None:
                firstname = splitted_whole_name[0]
                # Tänne lähteeksi LUT:n johdatus ohjelmointiin -oppaan arrayn käsittelykohta
                lastname = " ".join(splitted_whole_name[1:])
            else:
                firstname = splitted_whole_name[1]
                lastname = " ".join(splitted_whole_name[2:])

            users.append(
                User(
                    _id=user.get("id"),
                    username=user.get("username"),
                    firstname=firstname,
                    lastname=lastname
                )
            )

        return users
