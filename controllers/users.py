import httpx
from flask import jsonify, request
from werkzeug.exceptions import NotFound
from decorators.db_conn import get_db_conn
from decorators.repository_decorator import init_repository

'''Controller-funktiot saavat init_repository-dekoraattorin kautta 
repo-parametrin, joka on instanssi DB-ympäristömuuttujan perusteella 
määritetystä repositorioluokasta. Repositorioluokkainstanssi saa puolestaan 
tietokantayhteyden get_db_conn-dekoraattorin kautta. Controller-funktiot ovat 
asynkronisia, koska niissä käytettävät tietokantaoperaatioita toteuttavat tai 
verkon yli dataa hakevat instanssimetodit ovat asynkronisia'''


@get_db_conn
@init_repository("users_repo")
async def get_all_users(repo):
    try:
        # Haetaan instanssin metodin palauttama lista user_list-muuttujaan.
        # Käytetään await-avainsanaa, koska get_all-metodit ovat asynkronisia.
        user_list = await repo.get_all()

        # Muutetaan listan sisällään pitämät User-luokan instanssit
        # dictionaryiksi User-luokan to_dict-metodia hyödyntämällä:
        user_dict_list = [user.to_dict() for user in user_list]

        # Muutetaan lista dictionary-alkioineen json-muotoon ja palautetaan se:
        return jsonify(user_dict_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@get_db_conn
@init_repository("users_repo")
async def get_user_by_id(repo, user_id):
    try:
        # repo-parametrissa olevan instanssin jäsenmetodia hyödyntämällä
        # haetaan user-muuttujaan User-luokan instanssi id:n perusteella:
        user = await repo.get_by_id(user_id)

        # Tehdään käyttäjäinstanssin tiedoista dictionary user-muuttujassa
        # olevan arvon edustaman luokan to_dict-metodia hyödyntämällä.
        # Palautetaan dictionary edelleen JSON-formaattiin muutettuna:
        return jsonify(user.to_dict())

    # Jos get_by_id-metodi palauttaa NotFound-poikkeuksen, palataan funktiosta
    # virheviestin sisältävällä JSON-objektilla ja 404-statuskoodilla:
    except NotFound:
        return jsonify({"error": f"Käyttäjää id:llä {user_id} ei ole olemassa"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@get_db_conn
@init_repository("users_repo")
async def add_user(repo):
    try:
        # Haetaan bodyssa saatavat tiedot request_data-muuttujaan Flaskin
        # request-ominaisuuden get_json()-metodia hyödyntämällä.
        request_data = request.get_json()
        username = request_data.get("username")
        firstname = request_data.get("firstname")
        lastname = request_data.get("lastname")

        # Jos request bodysta puuttuu yksi tai useampi tietokantahakua
        # varten tarvittava avain-arvo-pari, palataan funktiosta
        # json-muotoisella virheviestillä:
        if not username or not firstname or not lastname:
            return jsonify({"error": "Vääränlainen request body"}), 400

        # Talletetaan added_user-muuttujaan add-metodin palauttama
        # User-instanssi. Metodille välitetään bodysta saatavien avainten
        # arvot. Metodi lisää käyttäjän tietokantaan näillä tiedoilla.
        added_user = await repo.add(username, firstname, lastname)

        # Muutetaan User-instanssi dictionaryksi ja edelleen JSON-formaattiin,
        # ja palautetaan se resurssin luonnista kertovalla statuskoodilla:
        return jsonify(added_user.to_dict()), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@get_db_conn
@init_repository("users_repo")
async def update_user_by_id(repo, user_id):
    try:
        request_data = request.get_json()
        username = request_data.get("username")
        firstname = request_data.get("firstname")
        lastname = request_data.get("lastname")

        if not username or not firstname or not lastname:
            return jsonify({"error": "Vääränlainen request body"}), 400

        # Talletetaan updated_user-muuttujaan update_by_id-metodin palauttama
        # User-luokan instanssi. Metodille välitetään saatu id sekä bodysta
        # saatavien avainten arvot. Metodi päivittää käyttäjän tiedot
        # välitetyillä arvoilla välitetyn id:n perusteella.
        updated_user = await repo.update_by_id(user_id, username, firstname, lastname)

        return jsonify(updated_user.to_dict())

    except NotFound:
        return jsonify({"error": f"Käyttäjää id:llä {user_id} ei ole olemassa"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@get_db_conn
@init_repository("users_repo")
async def update_user_lastname_by_id(repo, user_id):
    try:
        request_data = request.get_json()
        lastname = request_data.get("lastname")

        if not lastname:
            return jsonify({"error": "Vääränlainen request body"}), 400

        # Talletetaan updated_user-muuttujaan update_lastname_by_id-metodin
        # palauttama User-luokan instanssi. Metodille välitetään saatu id sekä
        # bodysta saatavan avaimen arvo. Metodi päivittää käyttäjän sukunimen
        # välitetyllä arvolla välitetyn id:n perusteella.
        updated_user = await repo.update_lastname_by_id(user_id, lastname)

        return jsonify(updated_user.to_dict())

    except NotFound:
        return jsonify({"error": f"Käyttäjää id:llä {user_id} ei ole olemassa."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@get_db_conn
@init_repository("users_repo")
async def delete_user_by_id(repo, user_id):
    try:
        # Talletetaan removed_user-muuttujaan delete_by_id-metodin palauttama
        # User-luokan instanssi. Metodille välitetään saatu id, jonka
        # perusteella käyttäjä poistetaan.
        removed_user = await repo.delete_by_id(user_id)

        # Jos käyttäjän poistaminen onnistuu, palautetaan funktiosta vastaus.
        # Ei palauteta poistetun käyttäjän tietoja, koska käyttäjä on
        # poistettu.
        return jsonify({"response": f"Käyttäjä id:llä {removed_user.id} poistettu."})

    except NotFound:
        return jsonify({"error": f"Käyttäjää id:llä {user_id} ei ole olemassa."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
