import json
from datetime import date
from pathlib import Path

import pytest
from django.core.serializers.json import DjangoJSONEncoder

from camac.dossier_import.exceptions import InvalidImportDataError
from camac.dossier_import.loaders import XlsxFileDossierLoader
from camac.dossier_import.utils import (
    get_or_create_ebau_nr,
    get_similar_value,
    get_worksheet_headings_and_rows,
)
from camac.dossier_import.validation import TargetStatus, validate_extra_columns

existing_columns = [e.value for e in XlsxFileDossierLoader.Column]
existing_status = [e.value for e in TargetStatus]


@pytest.mark.parametrize(
    ("value", "existing", "output"),
    [
        ("THIS_REALLY_DOESNT_EXIST", existing_columns, None),
        ("PUBLICATIONDATE", existing_columns, "PUBLICATION-DATE"),
        ("CONSTRUCTION_START_DATE", existing_columns, "CONSTRUCTION-START-DATE"),
        ("APLICANT-FIRSTNAME", existing_columns, "APPLICANT-FIRST-NAME"),
        ("WEIRD_STATUS", existing_status, None),
        ("SUBIMTTED", existing_status, "SUBMITTED"),
    ],
)
def test_similar_value(value, existing, output):
    assert get_similar_value(value, existing) == output


def test_validate_extra_columns(snapshot):
    assert (
        validate_extra_columns(
            [
                "APPLICANT-FIRST-NAME",
                "SOMEOTHERCOLUMN",
                "PUBLICATIONDATE",
                "SUBIMT-DATE",
            ]
        )
        == snapshot
    )


def normalize_structure(data):  # pragma: no cover
    """
    Recursive normalization of the structure:
    - Dictionaries are sorted by keys
    - Lists of strings are sorted alphabetically
    - Lists of dictionaries are sorted by their serialized value after normalizing them
    - Other lists are also sorted if possible.
    """  # noqa: D205
    if isinstance(data, dict):
        return {k: normalize_structure(v) for k, v in sorted(data.items())}
    elif isinstance(data, list):
        if all(isinstance(item, str) for item in data):
            return sorted(data)
        elif all(isinstance(item, dict) for item in data):
            return sorted(
                [normalize_structure(item) for item in data],
                key=lambda d: json.dumps(d, sort_keys=True, cls=DjangoJSONEncoder),
            )
        else:
            return sorted(
                normalize_structure(item) for item in data
            )  # pragma: no cover
    else:
        return data


def to_sorted_json(data):  # pragma: no cover
    """Converts the normalized structure into reproducible, sorted JSON."""  # noqa: D401
    normalized_data = normalize_structure(data)
    return json.dumps(
        normalized_data,
        indent=4,
        sort_keys=True,
        ensure_ascii=False,
        cls=DjangoJSONEncoder,
    )


def test_strict_open_xml_mode():
    """Ensure we detect "Strict Open XML" mode files.

    These cannot be parsed by openpyxl. Once they can, this test will
    fail and we can then change it to check for correct contents, or
    just simply drop it.
    """
    file = Path(__file__).parent / "data/dossiers-strict-for-import-test.xlsx"
    fh = file.open("rb")
    with pytest.raises(InvalidImportDataError) as exc:
        get_worksheet_headings_and_rows(fh)

    assert exc.match("Strict Open XML")


@pytest.mark.django_db
def test_get_or_create_ebau_nr(
    caluma_workflow_config_be,
    instance_factory,
    instance_service_factory,
    instance_with_case,
    service_factory,
):
    my_service = service_factory()
    other_service = service_factory()

    my_instance = instance_with_case(instance_factory())
    my_instance.case.meta["ebau-number"] = "2025-1"
    my_instance.case.save()
    instance_service_factory(instance=my_instance, service=my_service)

    other_instance = instance_with_case(instance_factory())
    other_instance.case.meta["ebau-number"] = "2025-2"
    other_instance.case.save()
    instance_service_factory(instance=other_instance, service=other_service)

    submit_date = date(2024, 1, 1)

    assert get_or_create_ebau_nr(None, my_service, submit_date) == "2024-1"
    assert get_or_create_ebau_nr("2025-2", my_service, submit_date) == "2024-1"
    assert get_or_create_ebau_nr("2025-1", my_service, submit_date) == "2025-1"
