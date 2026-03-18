import re
from typing import Any, List, Tuple, Union

import pyexcel_xlsx
from caluma.caluma_workflow.models import WorkItem
from django.utils.translation import gettext
from rapidfuzz import fuzz

from .exceptions import InvalidImportDataError


def get_similar_value(
    original_value: str,
    expected_values: List[str],
    similarity_score_threshold: int = 85,
) -> Union[str, None]:
    """Check if there's a similar expected value."""
    similarity_scores = reversed(
        sorted(
            (
                (expected_value, fuzz.ratio(original_value, expected_value))
                for expected_value in expected_values
            ),
            key=lambda i: i[1],
        )
    )

    return next(
        (
            expected_value
            for expected_value, score in similarity_scores
            if score >= similarity_score_threshold
        ),
        None,
    )


def clean_heading(value: str) -> str:
    """Remove all whitespace characters from headings."""
    return re.sub(r"\s", "", value).strip()


def clean_value(value: Any) -> Any:
    """Remove leading and trailing spaces from string values."""
    return value.strip() if isinstance(value, str) else value


def get_worksheet_headings_and_rows(file) -> Tuple[List[str], List[dict]]:
    """Get headings and rows of an XLSX file."""

    workbook = pyexcel_xlsx.get_data(file)

    if not workbook:
        # If a "strict Open XML" Excel file is uploaded, openpyxl just
        # drops all the sheets, resulting in an empty workbook:
        # https://foss.heptapod.net/openpyxl/openpyxl/-/issues/2170

        # There is no useful way to deal with this, apart from using
        # another excel parser that knows about this format, for example,
        # or waiting for openpyxl to implement support for it.
        raise InvalidImportDataError(
            gettext(
                "The dossiers.xlsx file was likely written in "
                "'Strict Open XML' mode, which is not yet supported. Please "
                "save the dossiers.xlsx file in the normal Excel file format"
            )
        )

    worksheet = workbook[list(workbook.keys())[0]]

    headings = [clean_heading(heading) for heading in worksheet[0]]
    rows = [
        {
            key: str(value) if key == "ID" else value
            for key, value in dict(
                zip(headings, [clean_value(cell) for cell in row])
            ).items()
        }
        for row in worksheet[1:]
    ]

    return headings, rows


def mark_work_items_as_imported(work_items: list[WorkItem]) -> None:
    """Mark all WorkItem's received as imported via `meta["imported"] = True`."""
    for work_item in work_items:
        work_item.meta = {**work_item.meta, "imported": True}
        work_item.save()
