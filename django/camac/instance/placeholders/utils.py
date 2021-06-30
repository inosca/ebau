from datetime import date, datetime
from typing import Any, Optional, Union


def clean_join(*parts: Any, separator: Optional[str] = " ") -> str:
    """Join all truthy arguments as trimmed string with a given separator.

    >>> clean_join(" John", None, "", " Smith ")
    "John Smith"
    """

    return separator.join([str(part).strip() for part in parts if part]).strip()


def human_readable_date(value: Union[datetime, date, None]) -> str:
    """Format date or datetime to a human readable date.

    >>> human_readable_date(date(2021, 10, 4))
    "4. October 2021"
    """

    return value.strftime("%-d. %B %Y") if value else None
