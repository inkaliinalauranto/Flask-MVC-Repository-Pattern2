from flask import jsonify
from werkzeug.exceptions import NotFound

from decorators.db_conn import get_db_conn
from decorators.db_conn_factory import init_db_conn
from decorators.repository_decorator import init_repository
from repositories.repository_factory import users_repository_factory


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
