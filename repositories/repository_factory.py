import os
from repositories.users_repository_jsonph import UserRepositoryJSONPH
from repositories.users_repository_mysql import UsersRepositoryMySQL
from repositories.users_repository_postgres import UsersRepositoryPostgres


# Repository factory, jota käytetään init_repository-dekoraattorifunktiossa
# luomaan .env-tiedoston DB-muuttujan arvon määrittelemän luokan instanssi
# käyttäjärepositoriosta. Annetaan funktion parametrille oletusarvo,
# jottei parametria tarvitse välttämättä välittää tätä funktiota kutsuttaessa.
# Näin on, kun tarkoituksena on tehdä instanssi UserRepositoryJSONPH:sta.
def users_repository_factory(con=None):
    _db = os.getenv("DB")

    # Jos tietokantaohjelmistoksi on määritelty .env-tiedostossa MySQL,
    # repo-muuttujaan luodaan instanssi MySQL-repositoriosta:
    if _db == "mysql":
        repo = UsersRepositoryMySQL(con)
    # Jos taas tietokantaohjelmistoksi on määritelty PostgreSQL, luodaan
    # repo-muuttujaan instanssi PostgreSQL-repositoriosta:
    elif _db == "postgres":
        repo = UsersRepositoryPostgres(con)
    # Jos puolestaan tarkoituksena on hakea käyttäjätietoja verkon yli,
    # luodaan repo-muuttujaan instanssi UserRepositoryJSONPH-luokasta:
    elif _db == "internet":
        repo = UserRepositoryJSONPH()
    # Ehdoissa on oltava myös else-haara, jotta repo-muuttujalle saadaan arvo
    # kaikenlaisissa tilanteissa:
    else:
        repo = UsersRepositoryMySQL(con)

    return repo
