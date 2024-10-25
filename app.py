from flask import Flask

from controllers.users import get_all_users, get_user_by_id

app = Flask(__name__)

app.add_url_rule(rule="/api/users", view_func=get_all_users)

app.add_url_rule(rule="/api/users/<int:user_id>", view_func=get_user_by_id)

if __name__ == "__main__":
    app.run(debug=True)