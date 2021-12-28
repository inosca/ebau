import mimetypes

import pytest
from pytest_lazyfixture import lazy_fixture
from rest_framework import status
from rest_framework.reverse import reverse

from ..models import DossierImport
from .test_dossier_import_case import TEST_IMPORT_FILE_NAME


@pytest.mark.parametrize(
    "config,role__name,result_count",
    [
        ("kt_bern", "municipality-lead", 1),
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
@pytest.mark.parametrize("role__name", ["Gemeinde", "municipality-lead"])
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
        (
            "import-example-validation-errors.zip",
            "kt_bern",
            None,
            status.HTTP_201_CREATED,
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

    resp = admin_client.post(
        reverse("dossier-import-list"),
        data,
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
    "import_file,expected_status,expected_result",
    [
        (
            "import-missing-status-column.zip",
            status.HTTP_400_BAD_REQUEST,
            "Spalte {'STATUS'} fehlt in der Metadatendatei des Archivs.",
        ),
        ("import-example.zip", status.HTTP_201_CREATED, None),
        (
            "import-dossiers-file-wrong-format.zip",
            status.HTTP_400_BAD_REQUEST,
            "Die Metadatendatei `dossiers.xlsx` ist kein gültiges Xlsx-Format.",
        ),
        (
            "import-no-dossiers-file.zip",
            status.HTTP_400_BAD_REQUEST,
            "Metadatendatei `dossiers.xlsx` fehlt im hochgeladenen Archiv.",
        ),
        (
            "garbage.zip",
            status.HTTP_400_BAD_REQUEST,
            "Die hochgeladene Datei ist kein gültiges Zip-Format",
        ),
        (
            "import-missing-optional-columns.zip",
            status.HTTP_201_CREATED,
            {"error": []},
        ),
        (
            "import-example-sparse.zip",
            status.HTTP_201_CREATED,
            {"error": []},
        ),
        (
            "import-empty-headings.zip",
            status.HTTP_201_CREATED,
            {"error": []},
        ),
        (
            "import-example-validation-errors.zip",
            status.HTTP_201_CREATED,
            {
                "error": [
                    "1 Dossiers haben einen ungültigen Status. Betroffene Dossiers:\n2017-86: 'DONKED' (status)",
                    "2 Dossiers fehlt ein Wert in einem zwingenden Feld. Betroffene Dossiers:\n2017-87: status,\n9: submit_date",
                ]
            },
        ),
        (
            "import-example-orphan-dirs.zip",
            status.HTTP_201_CREATED,
            {
                "warning": [
                    "2 Dokumentenverzeichnisse haben keine Referenz in der Metadatendatei und werden nicht importiert:\n2017-11, 2017-22",
                    "2 Dossiers ohne Dokumentenverzeichnis.",
                ]
            },
        ),
        (
            None,
            status.HTTP_400_BAD_REQUEST,
            "Bitte eine Datei mitreichen, um einen Import zu starten.",
        ),
    ],
)
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
    expected_result,
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
        format="multipart",
    )
    assert resp.status_code == expected_status
    if resp.status_code != status.HTTP_201_CREATED:
        assert str(resp.data[0]["detail"]) == expected_result
    else:
        if expected_result is not None:
            for key, value in expected_result.items():
                assert sorted(value) == sorted(
                    resp.data["messages"]["validation"]["summary"][key]
                )
        admin_client.delete(reverse("dossier-import-detail", args=(resp.data["id"],)))


@pytest.mark.freeze_time("2021-12-12")
@pytest.mark.parametrize(
    "config,role__name,camac_instance",
    [
        ("kt_bern", "support", lazy_fixture("be_instance")),
        ("kt_schwyz", "Support", lazy_fixture("sz_instance")),
    ],
)
@pytest.mark.parametrize(
    "file_name,archive_is_valid,expected_status",
    [
        ("import-example.zip", True, status.HTTP_200_OK),
        ("import-example.zip", False, status.HTTP_400_BAD_REQUEST),
    ],
)
def test_importing(
    db,
    admin_client,
    group,
    admin_user,
    location,
    settings,
    archive_file,
    file_name,
    dossier_import_factory,
    setup_fixtures_required_by_application_config,
    make_workflow_items_for_config,
    config,
    camac_instance,
    archive_is_valid,
    expected_status,
):
    make_workflow_items_for_config(config)
    setup_fixtures_required_by_application_config(config)
    settings.APPLICATION = settings.APPLICATIONS[config]
    settings.Q_CLUSTER["sync"] = True
    dossier_import = dossier_import_factory(
        status=DossierImport.IMPORT_STATUS_VALIDATION_SUCCESSFUL
        if archive_is_valid
        else DossierImport.IMPORT_STATUS_VALIDATION_FAILED,
        source_file=archive_file(file_name),
    )

    resp = admin_client.post(
        reverse("dossier-import-import-archive", args=(dossier_import.pk,))
    )
    assert resp.status_code == expected_status
