from decorators.db_conn_factory import init_db_conn


def get_db_conn(decorated_func):
    def wrapper(*args, **kwargs):
        with init_db_conn() as con:
            return decorated_func(con, *args, **kwargs)

    return wrapper
