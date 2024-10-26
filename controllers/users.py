from flask import jsonify, request
from werkzeug.exceptions import NotFound
from decorators.db_conn import get_db_conn
from decorators.repository_decorator import init_repository


# Näiden on oltava ehkä asynceja
@get_db_conn
@init_repository("users_repo")
def get_all_users(repo):
    try:
        user_list = repo.get_all()
        user_dict_list = [{"id": user.id,
                           "username": user.username,
                           "firstname": user.firstname,
                           "lastname": user.lastname}
                          for user in user_list]

        return jsonify(user_dict_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@get_db_conn
@init_repository("users_repo")
def get_user_by_id(repo, user_id):
    try:
        user = repo.get_by_id(user_id)

        return jsonify({"id": user.id,
                        "username": user.username,
                        "firstname": user.firstname,
                        "lastname": user.lastname})

    except NotFound:
        return jsonify({"error": f"Käyttäjää id:llä {user_id} ei ole olemassa"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Kommentit reposta ####
@get_db_conn
@init_repository("users_repo")
def add_user(repo):
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
        # instanssi. Metodille välitetään bodysta saatavien avainten arvot.
        # Metodi lisää käyttäjän tietokantaan näillä tiedoilla.
        added_user = repo.add(username, firstname, lastname)

        # Jos käyttäjäinstanssin id indikoi epäonnistuneesta
        # tietokantaoperaatiosta, poistutaan funktiosta virheestä kertovalla
        # json-viestillä:
        if added_user.id < 1:
            return jsonify({"error": "Käyttäjän lisääminen ei onnistu"}), 500

        added_user_dict = {"id": added_user.id,
                           "username": added_user.username,
                           "firstname": added_user.firstname,
                           "lastname": added_user.lastname}

        return jsonify(added_user_dict), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
