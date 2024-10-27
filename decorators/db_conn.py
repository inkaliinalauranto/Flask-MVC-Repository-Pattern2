from flask import current_app
from decorators.db_conn_factory import init_db_conn
from functools import wraps


''' Luodaan tuntiesimerkin mukainen dekoraattorifunktio. 
Sen wrapper-funktiolle tarvitaan wraps-dekoraattori, jotta path paramien 
käyttö controller-funktioissa onnistuu. 

Tämän ratkaisun sain ChatGPT:ltä kysymällä ensin kysymyksen "Why this doesn't
work" ja syöttämällä kysymyksen perään get_user_by_id-kontrollerifunktion. 
ChatGPT ehdotti muuttamaan parametrien järjestystä siten, että 
alemmasta dekoraattorista saatu repo-parametri on ennen path paramia. Koska 
ongelma ei ratkennut, syötin ChatGPT:lle konsoliin tulostuneet virheviestit, 
joita ennen kirjoitin "I get these errors." Tähän sain ratkaisuksi 
wraps-dekoraattorin käytön, jolla itse tehdyn dekoraattorin sisään kätketty 
wrapper-funktio saadaan haettua Flaskille rekisteröitäväksi. 

wraps-dekoraattorille välitetään parametrina se funktio, jolle tämä 
get_db_conn-dekoraattori toimii dekoraattorina. wrapper-dekoraattorin käyttöä 
tukee myös Flask-dokumentaation Extension-otsikon alla oleva esimerkki:
https://flask.palletsprojects.com/en/stable/async-await/. 

Saman esimerkin kautta sain myös selville, että jotta asynkronisen 
controller-funktion käyttö onnistuu, on wrapper-funktiosta palautettava 
dekoraattorin parametrina saama dekoroitu funktio Flaskin current_appin 
ensure_sync-metodin parametrina.
'''


def get_db_conn(decorated_func):
    @wraps(decorated_func)
    def wrapper(*args, **kwargs):
        # Avataan mahdollinen tietokantayhteys init_db_conn-metodilla
        # con-muuttujaan:
        with init_db_conn() as con:
            # Välitetään dekoroitavalle funktiolle eli tässä tapauksessa
            # init_repository-dekoraattorifunktiolle sen mahdollisten omien
            # parametrien lisäksi con, joka pitää sisällään joko
            # tietokantayhteyden tai None-arvon:
            return current_app.ensure_sync(decorated_func)(con, *args, **kwargs)

    return wrapper
