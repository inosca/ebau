from babel.dates import format_date
from dateutil.parser import parse
from django.conf import settings
from jinja2 import Environment


def dateformat(value, format="medium"):
    if value is None:
        return ""

    parsed_value = parse(value)
    return format_date(parsed_value, format, locale=settings.LANGUAGE_CODE)


def emptystring(value):
    if value is None:
        return ""
    return value


def get_jinja_env():
    jinja_env = Environment()
    jinja_env.filters["date"] = dateformat
    jinja_env.filters["emptystring"] = emptystring
    return jinja_env
