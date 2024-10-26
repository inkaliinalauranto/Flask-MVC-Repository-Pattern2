import os

from repositories.user_repository_jsonph import UserRepositoryJSONPH


def users_repository_factory(con):
    _db = os.getenv("DB")

    repo = UserRepositoryJSONPH()

    if _db == "mysql":
        pass
    elif _db == "postgres":
        pass
    else:
        pass

    return repo