import re
from datetime import date
from typing import Any

import pyexcel_xlsx
import requests
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.utils.translation import gettext
from rapidfuzz import fuzz

from camac.core.models import InstanceService
from camac.core.utils import generate_ebau_nr
from camac.user.models import Service

from .exceptions import InvalidImportDataError


def get_similar_value(
    original_value: str,
    expected_values: list[str],
    similarity_score_threshold: int = 85,
) -> str | None:
    """Check if there's a similar expected value."""
    similarity_scores = sorted(
        (
            (expected_value, fuzz.ratio(original_value, expected_value))
            for expected_value in expected_values
        ),
        key=lambda i: i[1],
        reverse=True,
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


def get_worksheet_headings_and_rows(file) -> tuple[list[str], list[dict]]:
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
                zip(headings, [clean_value(cell) for cell in row], strict=False)
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


def get_token_for_transmission() -> str:
    """Fetch a bearer token for the transmission to the production system."""

    request = requests.post(
        settings.DOSSIER_IMPORT["PROD_AUTH_URL"],
        {
            "grant_type": "client_credentials",
            "client_id": settings.DOSSIER_IMPORT_CLIENT_ID,
            "client_secret": settings.DOSSIER_IMPORT_CLIENT_SECRET,
            "scope": "openid",
        },
    )
    request.raise_for_status()
    return request.json()["access_token"]


def get_or_create_ebau_nr(
    ebau_number: str | None,
    service: Service,
    submit_date: date,
) -> str:
    """Validate a proposed eBau number to match its service domain or generate a new one.

    In order to actually assign an eBau number, we need to verify that it's
    owned by the service - if not, we need to generate a new one.
    """
    if ebau_number and (result := re.search(r"[0-9]{4}-[1-9][0-9]*", ebau_number)):
        match = result.group()

        if InstanceService.objects.filter(
            **{
                "instance__case__meta__ebau-number": match,
                "service": service,
            }
        ).exists():
            return match

    return generate_ebau_nr(None, submit_date.year)
