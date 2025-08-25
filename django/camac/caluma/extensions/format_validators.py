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


class EEBADeclarationFormatValidator(BaseFormatValidator):
    slug = "eeba-declaration"
    name = {
        "en": "eEBA Declaration format",
        "de": "eEBA-Erklärungsformat",
    }
    # The declaration must start with "GR-EBA-" followed by exactly 6 uppercase letters or digits
    regex = r"^GR-EBA-[A-Z0-9]{6}$"
    error_msg = {
        "en": "The declaration must start with 'GR-EBA-' followed by six capital letters or digits.",
        "de": "Die Erklärung muss mit 'GR-EBA-' beginnen, gefolgt von sechs Großbuchstaben oder Ziffern.",
    }
