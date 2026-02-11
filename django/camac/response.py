from typing import Any

from django.http import FileResponse
from pyexcel import Sheet


def make_xlsx_response(data: list[list[Any]], filename: str) -> FileResponse:
    """
    Generate a django FileResponse containing an XLSX file.

    Creates and excel file from a two-dimentional list of data and returns it as
    a downloadable HTTP response.

    Args:
        data:
            A two-dimensional list representing rows and columns of the
            spreadsheet. For more information, check the docs of
            [`pyexcel.Sheet`](https://docs.pyexcel.org/en/latest/generated/pyexcel.Sheet.html)
            as we directly pass it.
        filename:
            The filename that will be used in the content disposition header.

    Returns:
        A django FileResponse containing the generated XLSX file.

    Examples:
        >>> make_xlsx_response(
        ...     [
        ...         ["Header A", "Header B"],
        ...         ["Cell A2", "Cell B2"],
        ...         ["Cell A3", "Cell B3"],
        ...     ],
        ...     "my-export.xlsx",
        ... )
    """

    return FileResponse(
        Sheet(data).save_to_memory("xlsx", None),
        as_attachment=True,
        filename=filename,
    )
