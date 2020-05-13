from camac.constants.kt_bern import DECISION_JUDGEMENT_MAP


def xml_encode_strings(value):
    replace_map = (("\n", "&#10;"), ("\r", "&#13;"), ("\t", " "))
    for old, new in replace_map:
        value = value.replace(old, new)

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
