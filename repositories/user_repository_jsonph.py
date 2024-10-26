import re
import httpx
from werkzeug.exceptions import NotFound

from models import User


class UserRepositoryJSONPH:
    # Tähän rakentaja, jossa kutsutaan yliluokkaa, välitetään None-yhteys
    def get_all(self):
        user_info = httpx.get(url="https://jsonplaceholder.typicode.com/users").json()

        users = []

        for user in user_info:
            split_whole_name = user.get("name").split(" ")

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

    def get_by_id(self, user_id):
        user_info = httpx.get(url=f"https://jsonplaceholder.typicode.com/users/{user_id}").json()

        if user_info == {}:
            raise NotFound()

        split_whole_name = user_info.get("name").split(" ")

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
