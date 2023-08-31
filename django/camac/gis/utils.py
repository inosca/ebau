from typing import Any, Union

from django.utils.translation import gettext as _


def get_bbox(x: Union[float, str], y: Union[float, str], buffer: int = 0) -> str:
    delta = 0

    if buffer:
        delta = buffer / 2

    try:
        x = float(x)
        y = float(y)
    except ValueError:
        raise ValueError(_("Coordinates must be floats"))

    return ",".join(map(str, [x - delta, y - delta, x + delta, y + delta]))


def to_query(query_params: dict) -> str:
    return "&".join(
        [f"{key}={value}" for key, value in query_params.items() if value is not None]
    )


def cast(value: Any, type: str) -> Any:
    if value is None:
        return None

    try:
        if type == "float":
            return float(value)
        elif type == "integer":
            return int(value)
        elif type == "string":
            return str(value)
    except ValueError:
        return None

    return value


def join(*parts: Any) -> str:
    clean_parts = [str(part).strip() for part in parts if part not in [None, ""]]
    deduped_parts = sorted(set(clean_parts), key=clean_parts.index)

    if len(deduped_parts) == 0:
        return None

    return ", ".join(deduped_parts).strip()
