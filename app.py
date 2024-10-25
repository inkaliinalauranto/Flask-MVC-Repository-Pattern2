from flask import Flask

from controllers.users import get_all_users

app = Flask(__name__)

app.add_url_rule(rule="/api/users", view_func=get_all_users)

if __name__ == "__main__":
    app.run(debug=True)