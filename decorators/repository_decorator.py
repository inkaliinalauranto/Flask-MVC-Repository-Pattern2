from functools import wraps

from repositories.repository_factory import users_repository_factory


def init_repository(repo_name):
    def decorator(route_handler_function):
        # ChatGPT: @wraps
        @wraps(route_handler_function)
        def wrapper(con, *args, **kwargs):
            repo = None
            if repo_name == "users_repo":
                repo = users_repository_factory(con)

            return route_handler_function(repo, *args, **kwargs)

        return wrapper

    return decorator
