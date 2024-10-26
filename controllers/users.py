from flask import jsonify
from decorators.db_conn import get_db_conn
from decorators.repository_decorator import init_repository
from repositories.repository_factory import users_repository_factory


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


# Ei käytetty decorator injectionia, koska silloin path paramin suhteen tulee virhetilanne
# Jos käyttäjää ei löydy, tietokantakyselyyn palautevideon error.
def get_user_by_id(user_id):
    try:
        repo = users_repository_factory()
        user = repo.get_by_id(user_id)

        return jsonify({"id": user.id,
                        "username": user.username,
                        "firstname": user.firstname,
                        "lastname": user.lastname})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
