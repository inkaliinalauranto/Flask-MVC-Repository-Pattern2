from dotenv import load_dotenv
from flask import Flask
from controllers.users import get_all_users, get_user_by_id, add_user, update_user_by_id, update_user_lastname_by_id, \
    delete_user_by_id

app = Flask(__name__)

app.add_url_rule(rule="/api/users", view_func=get_all_users)

app.add_url_rule(rule="/api/users/<int:user_id>", view_func=get_user_by_id)

app.add_url_rule(rule="/api/users",
                 view_func=add_user,
                 methods=["POST"])

app.add_url_rule(rule="/api/users/<int:user_id>",
                 view_func=update_user_by_id,
                 methods=["PUT"])

app.add_url_rule(rule="/api/users/<int:user_id>",
                 view_func=update_user_lastname_by_id,
                 methods=["PATCH"])

app.add_url_rule(rule="/api/users/<int:user_id>",
                 view_func=delete_user_by_id,
                 methods=["DELETE"])

if __name__ == "__main__":
    load_dotenv()
    # debug-parametrin käyttö palvelimen uudelleen käynnistämiseksi
    # automaattisesti koodimuutosten yhteydessä on toteutettu seuraavasta
    # lähteestä löytyvän mallin mukaan:
    # https://www.geeksforgeeks.org/flask-app-routing/
    app.run(debug=True)
