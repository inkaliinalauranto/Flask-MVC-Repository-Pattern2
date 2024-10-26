from dotenv import load_dotenv
from flask import Flask

from controllers.users import get_all_users, get_user_by_id, add_user

app = Flask(__name__)

app.add_url_rule(rule="/api/users", view_func=get_all_users)

app.add_url_rule(rule="/api/users/<int:user_id>", view_func=get_user_by_id)

app.add_url_rule(rule="/api/users", view_func=add_user, methods=["POST"])

if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True)