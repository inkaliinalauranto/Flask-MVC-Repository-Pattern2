import os
from repositories.user_repository_jsonph import UserRepositoryJSONPH
from repositories.users_repository_mysql import UsersRepositoryMySQL
from repositories.users_repository_postgres import UsersRepositoryPostgres


def users_repository_factory(con=None):
    _db = os.getenv("DB")

    if _db == "mysql":
        repo = UsersRepositoryMySQL(con)
    elif _db == "postgres":
        repo = UsersRepositoryPostgres(con)
    elif _db == "internet":
        repo = UserRepositoryJSONPH()
    else:
        repo = UsersRepositoryMySQL(con)

    return repo
