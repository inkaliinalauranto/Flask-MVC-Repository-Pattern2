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
        user_info = httpx.get(url="https://jsonplaceholder.typicode.com/users").json()

        users = []

        for user in user_info:
            split_whole_name = user.get("name").split(" ")

            # findall palauttaa listan
            # https://www.geeksforgeeks.org/python-regex/
            if re.search(r'[Mm][Rr][Ss]?\.?', split_whole_name[0]) is None:
                firstname = split_whole_name[0]
                # Tänne lähteeksi LUT:n johdatus ohjelmointiin -oppaan arrayn käsittelykohta
                lastname = " ".join(split_whole_name[1:])
            else:
                firstname = split_whole_name[1]
                lastname = " ".join(split_whole_name[2:])

            users.append(User(_id=user.get("id"),
                              username=user.get("username"),
                              firstname=firstname,
                              lastname=lastname))

        return users

    @staticmethod
    def get_by_id(user_id):
        user_info = httpx.get(url=f"https://jsonplaceholder.typicode.com/users/{user_id}").json()

        if user_info == {}:
            return None

        split_whole_name = user_info.get("name").split(" ")

        # findall palauttaa listan
        # https://www.geeksforgeeks.org/python-regex/
        if re.search(r'[Mm][Rr][Ss]?\.?', split_whole_name[0]) is None:
            firstname = split_whole_name[0]
            # Tänne lähteeksi LUT:n johdatus ohjelmointiin -oppaan arrayn käsittelykohta
            lastname = " ".join(split_whole_name[1:])
        else:
            firstname = split_whole_name[1]
            lastname = " ".join(split_whole_name[2:])

        return User(_id=user_info.get("id"),
                    username=user_info.get("username"),
                    firstname=firstname,
                    lastname=lastname)
