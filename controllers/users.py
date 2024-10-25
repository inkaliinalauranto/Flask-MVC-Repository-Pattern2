from flask import jsonify

from user_repository_json_placeholder import UserRepositoryJSONPlaceholder


def get_all_users():
    try:
        user_list = UserRepositoryJSONPlaceholder.get_all()
        user_dict_list = []

        for user in user_list:
            user_dict_list.append({"id": user.id, "username": user.username, "firstname": user.firstname, "lastname": user.lastname})

        return jsonify(user_dict_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
