from typing import List, Tuple

import pyexcel_xlsx


def clean_value(value):
    if isinstance(value, str):
        value = value.strip()

    return value


def get_worksheet_headings_and_rows(file) -> Tuple[List[str], List[dict]]:
    """Get headings and rows of an XLSX file."""

    workbook = pyexcel_xlsx.get_data(file)
    worksheet = workbook[list(workbook.keys())[0]]

    headings = [clean_value(heading) for heading in worksheet[0]]
    rows = [
        dict(zip(headings, [clean_value(cell) for cell in row]))
        for row in worksheet[1:]
    ]

    return headings, rows
