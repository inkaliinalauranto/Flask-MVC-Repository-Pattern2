from flask import current_app

from decorators.db_conn_factory import init_db_conn
from functools import wraps


def get_db_conn(decorated_func):
    # ChatGPT: @wraps
    @wraps(decorated_func)
    def wrapper(*args, **kwargs):
        with init_db_conn() as con:
            # Lähde https://flask.palletsprojects.com/en/stable/async-await/
            return current_app.ensure_sync(decorated_func)(con, *args, **kwargs)

    return wrapper
