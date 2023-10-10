from functools import wraps

from django.db import transaction
from django.db.utils import ProgrammingError
from psycopg2.errors import UndefinedTable


def dynamic_default_value(default_value=None):
    """Handle dynamic field default values in migrations.

    This decorator wraps the dynamic default value function for model fields and
    handles errors with non existing tables gracefully. This is necessary
    because django tries to evaluate the function to write as default on the
    database while creating the migrations.
    """

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                with transaction.atomic():
                    return function(*args, **kwargs)
            except ProgrammingError as e:
                if isinstance(e.__cause__, UndefinedTable):
                    return default_value
                raise  # pragma: no cover

        return wrapper

    return decorator
