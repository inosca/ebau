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


class EvenProjectNumberFormatValidator(BaseFormatValidator):
    slug = "even-project-number"
    name = {
        "en": "EVEN project number format",
        "de": "Format der EVEN-Projektnummer",
    }
    regex = r"^[A-Z]{2}-[A-Z0-9]{5}$"
    error_msg = {
        "en": "The marking must consist of two capital letters for the canton abbreviation, a hyphen and five letters/numbers.",
        "de": "Die Kennzeichnung muss aus zwei Grossbuchstaben für das Kantonskürzel, einen Bindestrich und fünf Buchstaben/Zahlen bestehen.",
    }
