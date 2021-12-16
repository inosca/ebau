import mimetypes

import pytest
from django.urls import reverse
from pytest_lazyfixture import lazy_fixture
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


@pytest.mark.freeze_time("2021-12-12")
@pytest.mark.parametrize("language", ["en"])
@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "import_file,config,location_id,expected_status",
    [
        (
            "import-example-validation-errors.zip",
            "kt_schwyz",
            lazy_fixture("location"),
            status.HTTP_201_CREATED,
        ),
        (
            "import-example-validation-errors.zip",
            "kt_schwyz",
            None,
            status.HTTP_400_BAD_REQUEST,
        ),
    ],
)
def test_validation_errors(
    db,
    admin_client,
    group,
    role,
    settings,
    archive_file,
    snapshot,
    import_file,
    config,
    language,
    location_id,
    expected_status,
):
    # create an import case with an uploaded file using the REST endpoint (POST)
    settings.APPLICATION = settings.APPLICATIONS[config]
    the_file = import_file and archive_file(import_file)
    data = {
        "source_file": (the_file and the_file.file) or "",
        "group": group.pk,
    }
    if location_id:
        data.update({"location_id": location_id.pk})

    admin_client.user.language = language
    resp = admin_client.post(
        reverse("dossier-import-list"),
        data=data,
        format="multipart",
    )
    assert resp.status_code == expected_status
    resp = resp.json()
    data = resp.get("data", None)
    if data:
        del data["attributes"]["source-file"]
        snapshot.assert_match(data["attributes"])
    else:
        snapshot.assert_match(resp)


@pytest.mark.parametrize("role__name", ["Support"])
@pytest.mark.parametrize(
    "import_file,expected_status",
    [
        ("import-example-no-errors.zip", status.HTTP_201_CREATED),
        ("import-example.zip", status.HTTP_201_CREATED),
        (
            "import-dossiers-file-wrong-format.zip",
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            "import-no-dossiers-file.zip",
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            "garbage.zip",
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            "import-example-validation-errors.zip",
            status.HTTP_201_CREATED,
        ),
        (
            "import-example-orphan-dirs.zip",
            status.HTTP_201_CREATED,
        ),
        (None, status.HTTP_400_BAD_REQUEST),
    ],
)
@pytest.mark.freeze_time("2021-12-12")
def test_file_validation(
    db,
    admin_client,
    group,
    admin_user,
    role,
    location,
    archive_file,
    import_file,
    expected_status,
    snapshot,
):
    # create an import case with an uploaded file using the REST endpoint (POST)
    the_file = import_file and archive_file(import_file)
    resp = admin_client.post(
        reverse("dossier-import-list"),
        {
            "source_file": (the_file and the_file.file) or "",
            "group": group.pk,
            "location_id": location.pk,
        },
        **{"HTTP_ACCEPT_LANGUAGE": "de"},
        format="multipart",
    )
    assert resp.status_code == expected_status
    snapshot.assert_match(str(resp.data))
    if resp.status_code == status.HTTP_201_CREATED:
        admin_client.delete(reverse("dossier-import-detail", args=(resp.data["id"],)))
