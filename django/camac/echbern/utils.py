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


def decision_to_judgement(decision: str, workflow_slug: str):
    return DECISION_JUDGEMENT_MAP[workflow_slug][decision]


def judgement_to_decision(judgement: int, workflow_slug: str):
    return {v: k for k, v in DECISION_JUDGEMENT_MAP[workflow_slug].items()}[judgement]
