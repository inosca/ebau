import re
from typing import Any, List, Tuple, Union

import pyexcel_xlsx
from rapidfuzz import fuzz


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
    worksheet = workbook[list(workbook.keys())[0]]

    headings = [clean_heading(heading) for heading in worksheet[0]]
    rows = [
        dict(zip(headings, [clean_value(cell) for cell in row]))
        for row in worksheet[1:]
    ]

    return headings, rows
