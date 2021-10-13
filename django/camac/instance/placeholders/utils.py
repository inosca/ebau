from datetime import date, datetime
from typing import Any, Optional, Union


def clean_join(*parts: Any, separator: Optional[str] = " ") -> str:
    """Join all truthy arguments as trimmed string with a given separator.

    >>> clean_join(" John", None, "", " Smith ")
    "John Smith"
    """

    return separator.join([str(part).strip() for part in parts if part]).strip()


def get_option_label(option: Union[dict, None]) -> Union[str, None]:
    """Get the label of an option.

    >>> get_option_label({"slug": "test-option", "label": "Test Option"})
    "Test Option"
    """
    return option.get("label") if option else None


def get_person_address_1(person: dict) -> str:
    """Extract the first address line from a person dictionary.

    >>> get_person_address_1({
        "street_name": "Test Avenue",
        "street_number": 10,
    })
    "Test Avenue 10"
    """

    return clean_join(person.get("street"), person.get("street_number"))


def get_person_address_2(person):
    """Extract the second address line from a person dictionary.

    >>> get_person_address_1({
        "zip": 9999,
        "city": "Testcity"
    })
    "9999 Testcity"
    """

    return clean_join(person.get("zip"), person.get("town"))


def get_person_name(
    person: dict,
    include_name: bool = True,
    include_juristic_name: bool = True,
) -> str:
    """Extract the name from a person dictionary.

    >>> get_person_name({
        "first_name": "John",
        "last_name": "Smith",
        "is_juristic_person": True,
        "juristic_person_name": "ACME Inc.",
    })
    "ACME Inc., John Smith"
    """

    parts = []

    if include_juristic_name and person.get("is_juristic_person"):
        parts.append(clean_join(person.get("juristic_name")))

    if include_name:
        parts.append(clean_join(person.get("first_name"), person.get("last_name")))

    return clean_join(*parts, separator=", ")


def human_readable_date(value: Union[datetime, date, None]) -> str:
    """Format date or datetime to a human readable date.

    >>> human_readable_date(date(2021, 10, 4))
    "4. October 2021"
    """

    return value.strftime("%-d. %B %Y") if value else None
