from babel.dates import format_date
from dateutil.parser import parse
from django.conf import settings
from jinja2.sandbox import SandboxedEnvironment


def dateformat(value, format="medium"):
    if value is None:
        return ""

    parsed_value = parse(value)
    return format_date(parsed_value, format, locale=settings.LANGUAGE_CODE)


def getwithdefault(value, default=""):
    if value is None:
        return default
    return value


def get_jinja_env():
    jinja_env = SandboxedEnvironment()
    jinja_env.filters["date"] = dateformat
    jinja_env.filters["getwithdefault"] = getwithdefault
    return jinja_env
