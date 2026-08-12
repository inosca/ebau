from enum import Enum
from typing import Any

from shapely import LineString, Point, Polygon
from shapely.geometry.base import BaseGeometry


class MergeStrategy(Enum):
    MERGE_FIRST = "merge_first"

    # actually not merge anything at all, give full control over return value
    # to each client (later clients can change output of previous clients)
    OVERRIDE = "override"


def build_shape(markers: list[dict], geometry_type: str) -> BaseGeometry:
    """Build the geometry the user drew on the map, in LV95 metres."""
    coords = [(marker["x"], marker["y"]) for marker in markers]

    if geometry_type == "POINT":
        return Point(coords[0])

    if geometry_type == "POLYGON":
        return Polygon(coords)

    return LineString(coords)


def buffered(shape: BaseGeometry, buffer: int = 0) -> BaseGeometry:
    """Widen a geometry by half the configured buffer, which is a total width."""
    return shape.buffer(buffer / 2) if buffer else shape


def to_query(query_params: dict) -> str:
    return "&".join(
        [f"{key}={value}" for key, value in query_params.items() if value is not None]
    )


def cast(value: Any, to_type: str) -> Any:
    if value is None:
        return None

    try:
        if to_type == "float":
            return float(value)
        elif to_type == "integer":
            return int(value)
        elif to_type == "string":
            return str(value)
    except ValueError:
        return None

    return value


def concat_values(*parts: Any) -> str:
    """Clean, deduplicate and concatenate values.

    This function cleans out empty values, deduplicates, and concatenates them
    using a comma as separator. If there is no meaningful value, it returns none
    and if there is only one value it returns it without converting it to a
    string.
    """

    # Filter out empty values
    non_empty_parts = [part for part in parts if part not in [None, ""]]

    # Return None if there are only empty values
    if len(non_empty_parts) == 0:
        return None
    # Return single value without joining to preserve the data type
    elif len(non_empty_parts) == 1:
        value = non_empty_parts[0]

        if isinstance(value, str):
            value = value.strip()

        return value

    clean_parts = [str(part).strip() for part in non_empty_parts]
    deduped_parts = sorted(set(clean_parts), key=clean_parts.index)

    return ", ".join(deduped_parts).strip()


def merge_table(
    existing_rows: list[dict],
    new_row: dict,
    merge_strategy: MergeStrategy,
) -> list[dict]:
    if merge_strategy == MergeStrategy.MERGE_FIRST:
        merge_data(existing_rows[0], new_row, merge_strategy)

    return existing_rows


def merge_data(data: dict, new_data: dict, merge_strategy: MergeStrategy) -> dict:
    for key, value in new_data.items():
        if key in data:
            if isinstance(data[key], list) and isinstance(value, list):
                for row in value:
                    value = merge_table(data[key], row, merge_strategy)
            elif merge_strategy == MergeStrategy.MERGE_FIRST:
                # If a previous data source already returned a value for a
                # certain question we concat the new and old value
                value = concat_values(data[key], value)

        data[key] = value
