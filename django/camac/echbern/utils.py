from camac.constants.kt_bern import DECISION_JUDGEMENT_MAP


def strip_whitespace(value):
    """Remove leading, trailing and multiple whitespaces."""
    return " ".join(value.split())


def xml_encode_strings(value):
    replace_map = (("\n", "&#10;"), ("\r", "&#13;"), ("\t", " "))
    for old, new in replace_map:
        value = value.replace(old, new)

    return value


def handle_string_values(value):
    if not isinstance(value, str):
        return value
    value = xml_encode_strings(value)
    # It's important to call strip_whitespace last, as it would also strip away any newlines
    value = strip_whitespace(value)
    return value


def decision_to_judgement(decision: str, form_slug: str):
    key = "baugesuch"
    if form_slug.startswith("vorabklaerung"):
        key = "vorabklaerung"
    return DECISION_JUDGEMENT_MAP[key][decision]


def judgement_to_decision(judgement: int, form_slug: str):
    key = "baugesuch"
    if form_slug.startswith("vorabklaerung"):
        key = "vorabklaerung"
    judgement_map = {v: k for k, v in DECISION_JUDGEMENT_MAP[key].items()}
    return judgement_map[judgement]
