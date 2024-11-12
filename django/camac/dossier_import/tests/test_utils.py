import pytest

from camac.dossier_import.loaders import XlsxFileDossierLoader
from camac.dossier_import.utils import get_similar_value
from camac.dossier_import.validation import TargetStatus, validate_extra_columns

existing_columns = [e.value for e in XlsxFileDossierLoader.Column]
existing_status = [e.value for e in TargetStatus]


@pytest.mark.parametrize(
    "input,existing,output",
    [
        ("THIS_REALLY_DOESNT_EXIST", existing_columns, None),
        ("PUBLICATIONDATE", existing_columns, "PUBLICATION-DATE"),
        ("CONSTRUCTION_START_DATE", existing_columns, "CONSTRUCTION-START-DATE"),
        ("APLICANT-FIRSTNAME", existing_columns, "APPLICANT-FIRST-NAME"),
        ("WEIRD_STATUS", existing_status, None),
        ("SUBIMTTED", existing_status, "SUBMITTED"),
    ],
)
def test_similar_value(input, existing, output):
    assert get_similar_value(input, existing) == output


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
