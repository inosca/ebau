import mimetypes

import pytest
from django.urls import reverse
from rest_framework import status

from .test_dossier_import_case import TEST_IMPORT_FILE_NAME


@pytest.mark.parametrize(
    "config,role__name,result_count",
    [
        ("kt_schwyz", "Gemeinde", 1),
        ("kt_schwyz", "Support", 2),
        ("kt_schwyz", "Applicant", 0),
    ],
)
def test_api_get_views(
    db,
    dossier_import_factory,
    settings,
    admin_client,
    service,
    config,
    group_factory,
    role,
    archive_file,
    result_count,
):
    settings.APPLICATION = settings.APPLICATIONS[config]
    group = group_factory(role=role, service=service)
    dossier_import_factory(
        group=group,
        service=group.service,
        source_file=archive_file(TEST_IMPORT_FILE_NAME),
        mime_type=mimetypes.types_map[".zip"],
    )
    dossier_import_factory()
    resp = admin_client.get(reverse("dossier-import-list"))
    assert len(resp.json()["data"]) == result_count


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "import_file",
    ["import-example-validation-errors.zip"],
)
def test_validation_errors(
    db, admin_client, group, role, location, archive_file, snapshot, import_file
):
    # create an import case with an uploaded file using the REST endpoint (POST)
    the_file = import_file and archive_file(import_file)
    resp = admin_client.post(
        reverse("dossier-import-list"),
        data={
            "source_file": (the_file and the_file.file) or "",
            "group": group.pk,
            "location_id": location.pk,
        },
        format="multipart",
    )
    assert resp.status_code == status.HTTP_201_CREATED
    snapshot.assert_match(resp.json()["data"]["attributes"]["messages"])


@pytest.mark.parametrize("role__name", ["Support"])
@pytest.mark.parametrize(
    "import_file,expected_status,expected_result",
    [
        ("import-example-no-errors.zip", status.HTTP_201_CREATED, None),
        ("import-example.zip", status.HTTP_201_CREATED, None),
        (
            "import-dossiers-file-wrong-format.zip",
            status.HTTP_400_BAD_REQUEST,
            "Metadata file `dossiers.xlsx` is not a valid .xlsx file.",
        ),
        (
            "import-no-dossiers-file.zip",
            status.HTTP_400_BAD_REQUEST,
            "No metadata file 'dossiers.xlsx' found in uploaded archive.",
        ),
        (
            "garbage.zip",
            status.HTTP_400_BAD_REQUEST,
            "Uploaded file is not a valid .zip file",
        ),
        (
            "import-example-orphan-dirs.zip",
            status.HTTP_201_CREATED,
            "Missing metadata for documents dirs: 2017-11, 2017-22",
        ),
        (None, status.HTTP_400_BAD_REQUEST, "To start an import please upload a file."),
    ],
)
def test_file_validation(
    db,
    admin_client,
    group,
    role,
    location,
    archive_file,
    import_file,
    expected_status,
    expected_result,
):
    # create an import case with an uploaded file using the REST endpoint (POST)
    the_file = import_file and archive_file(import_file)
    resp = admin_client.post(
        reverse("dossier-import-list"),
        data={
            "source_file": (the_file and the_file.file) or "",
            "group": group.pk,
            "location_id": location.pk,
        },
        format="multipart",
    )
    assert resp.status_code == expected_status
    if resp.status_code != status.HTTP_201_CREATED:
        assert str(resp.data[0]["detail"]) == expected_result
    else:
        admin_client.delete(reverse("dossier-import-detail", args=(resp.data["id"],)))
