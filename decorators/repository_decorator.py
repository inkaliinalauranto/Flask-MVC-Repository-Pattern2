from functools import wraps
from flask import current_app
from repositories.repository_factory import users_repository_factory

''' Luodaan tuntiesimerkin mukainen parametrisoitu dekoraattorifunktio. 
Sen wrapper-funktiolle tarvitaan wraps-dekoraattori. wrapper-funktiosta 
palautetaan tämän dekoraattorifunktion varsinaisen dekoraattorifunktio-osuuden 
parametrina saama controller-funktio ensure_sync-metodin kautta. Tarkemmat 
selitykset ja lähteet wraps-dekoraattorin ja Flaskin current_appin 
ensure_sync-metodin käytöstä on dokumentoitu db_conn.py-tiedostoon.'''


def init_repository(repo_name):
    def decorator(route_handler_function):
        @wraps(route_handler_function)
        def wrapper(con, *args, **kwargs):
            repo = None
            if repo_name == "users_repo":
                repo = users_repository_factory(con)

            # Välitetään dekoroitavalle funktiolle eli tässä tapauksessa
            # controller-funktioille niiden mahdollisten omien parametrien
            # lisäksi repo-muuttujan arvo, joka pitää sisällään None-arvon tai
            # instanssin luokasta, jonka users_repository_factory-funktio
            # määrittelee. Arvo on None, jos tämän dekoraattorifunktion eli
            # init_repositoryn repo_name-parametri ei vastaa yllä olevaa ehtoa:
            return current_app.ensure_sync(route_handler_function)(repo, *args, **kwargs)

        return wrapper

    return decorator
