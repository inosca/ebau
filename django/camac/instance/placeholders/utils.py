from datetime import date, datetime
from typing import List, Union

from babel.dates import format_date
from caluma.caluma_form.models import Document
from django.conf import settings
from django.utils.translation import get_language

from camac.caluma.utils import find_answer
from camac.utils import clean_join


def get_option_label(option: Union[dict, None]) -> Union[str, None]:
    """Get the label of an option.

    >>> get_option_label({"slug": "test-option", "label": "Test Option"})
    "Test Option"
    """
    return option.get("label") if option else None


def get_person_address_1(person: dict, use_representative: bool = False) -> str:
    """Extract the first address line from a person dictionary.

    >>> get_person_address_1({
        "street_name": "Test Avenue",
        "street_number": 10,
    })
    "Test Avenue 10"
    """
    prefix = "representative_" if use_representative else ""

    return clean_join(
        person.get(f"{prefix}street"),
        person.get(f"{prefix}street_number"),
    )


def get_person_address_2(person: dict, use_representative: bool = False) -> str:
    """Extract the second address line from a person dictionary.

    >>> get_person_address_1({
        "zip": 9999,
        "city": "Testcity"
    })
    "9999 Testcity"
    """
    prefix = "representative_" if use_representative else ""

    return clean_join(person.get(f"{prefix}zip"), person.get(f"{prefix}town"))


def get_tel_and_email(person):
    return clean_join(person.get("tel"), person.get("email"), separator=", ")


def get_person_name(
    person: dict,
    include_name: bool = True,
    include_juristic_name: bool = True,
    use_representative: bool = False,
) -> str:
    """Extract the name from a person dictionary.

    >>> get_person_name({
        "first_name": "John",
        "last_name": "Smith",
        "is_juristic_person": True,
        "juristic_name": "ACME Inc.",
    })
    "ACME Inc., John Smith"
    """

    prefix = "representative_" if use_representative else ""
    parts = []

    if include_juristic_name and person.get(f"{prefix}is_juristic_person"):
        parts.append(person.get(f"{prefix}juristic_name"))

    if include_name:
        parts.append(
            clean_join(
                person.get(f"{prefix}first_name"),
                person.get(f"{prefix}last_name"),
            )
        )

    return clean_join(*parts, separator=", ")


def get_person_first_name(person: dict, use_representative: bool = False) -> str:
    """Extract the first name from a person dictionary.

    >>> get_person_first_name({
        "first_name": "John",
    })
    "John"
    """
    prefix = "representative_" if use_representative else ""

    return person.get(f"{prefix}first_name")


def get_person_last_name(person: dict, use_representative: bool = False) -> str:
    """Extract the last name from a person dictionary.

    >>> get_person_last_name({
        "last_name": "Smith",
    })
    "Smith"
    """
    prefix = "representative_" if use_representative else ""

    return person.get(f"{prefix}last_name")


def enrich_personal_data(personal_data):
    return [clean_and_add_full_name(entry) for entry in personal_data]


def clean_and_add_full_name(entry):
    entry["full_name"] = get_person_name(entry)
    entry["address_1"] = get_person_address_1(entry)
    entry["address_2"] = get_person_address_2(entry)
    entry["full_address"] = clean_join(
        entry["address_1"], entry["address_2"], separator=", "
    )

    return {k: v if v is not None else "" for k, v in entry.items()}


def human_readable_date(value: Union[datetime, date, None]) -> str:
    """Format date or datetime to a human readable date.

    >>> human_readable_date(date(2021, 10, 4))
    "4. October 2021"
    """

    if not value:
        return None

    return format_date(value, "long", locale=get_language())


def row_to_person(document: Document) -> dict:
    if not settings.PLACEHOLDERS:  # pragma: no cover
        return None

    mapping = settings.PLACEHOLDERS["PERSON_MAPPING"]

    return {
        "salutation": find_answer(document, mapping["SALUTATION"])
        if "SALUTATION" in mapping
        else None,
        "first_name": find_answer(document, mapping["FIRST_NAME"]),
        "last_name": find_answer(document, mapping["LAST_NAME"]),
        "juristic_name": find_answer(document, mapping["JURISTIC_NAME"]),
        "is_juristic_person": find_answer(
            document, mapping["IS_JURISTIC"], raw_value=True
        )
        == mapping["IS_JURISTIC_YES"],
        "street": find_answer(document, mapping["STREET"]),
        "street_number": find_answer(document, mapping["STREET_NUMBER"]),
        "zip": find_answer(document, mapping["ZIP"]),
        "town": find_answer(document, mapping["TOWN"]),
    }


def parse_person_row(row: dict, keys: List[str]) -> dict:
    data = {}
    initial_data = {
        "NAME": get_person_name(row),
        "ADDRESS": clean_join(
            get_person_address_1(row),
            get_person_address_2(row),
            separator=", ",
        ),
        "REPRESENTATIVE_NAME": get_person_name(row, use_representative=True),
        "REPRESENTATIVE_ADDRESS": clean_join(
            get_person_address_1(row, use_representative=True),
            get_person_address_2(row, use_representative=True),
            separator=", ",
        ),
    }

    for key in keys:
        if key in initial_data:
            data[key] = initial_data.get(key)
        else:
            data[key] = row.get(key.lower())

    return data
