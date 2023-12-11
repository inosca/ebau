from caluma.caluma_form.format_validators import BaseFormatValidator


class IntegerListFormatValidator(BaseFormatValidator):
    slug = "integer-list"
    name = {
        "en": "Comma separated list of integers",
        "de": "Komma separierte Liste von Integers",
    }
    regex = r"(^(\d+(,?|,\s?))+$)"
    error_msg = {
        "en": "Only comma separated intergers are permited",
        "de": "Nur Komma separierte Integers sind erlaubt",
    }
