import mimetypes

import pytest
from caluma.caluma_workflow.models import Case
from pytest_lazyfixture import lazy_fixture
from rest_framework import status
from rest_framework.reverse import reverse

from camac.utils import build_url

from ...instance.serializers import CalumaInstanceSerializer
from ..domain_logic import transmit_import
from ..models import DossierImport
from .test_dossier_import_case import TEST_IMPORT_FILE_NAME


@pytest.mark.parametrize(
    "config,host,role__name,result_count",
    [
        ("kt_bern", "ebau-test.sycloud.ch", "municipality-lead", 1),
        ("kt_bern", "ebau.apps.be.ch", "municipality-lead", 0),
        ("kt_schwyz", "camac-schwyz.sycloud.ch", "Gemeinde", 1),
        ("kt_schwyz", "ebau-sz.ch", "Gemeinde", 0),
        ("kt_schwyz", "camac-schwyz.sycloud.ch", "Support", 2),
        ("kt_schwyz", "camac-schwyz.sycloud.ch", "Applicant", 0),
    ],
)
def test_api_get_views(
    db,
    dossier_import_factory,
    settings,
    admin_client,
    service,
    config,
    host,
    group_factory,
    role,
    archive_file,
    result_count,
):
    settings.APPLICATION = settings.APPLICATIONS[config]
    settings.INTERNAL_BASE_URL = host
    group = group_factory(role=role, service=service)
    dossier_import_factory(
        group=group,
        source_file=archive_file(TEST_IMPORT_FILE_NAME),
        mime_type=mimetypes.types_map[".zip"],
    )
    dossier_import_factory()
    resp = admin_client.get(reverse("dossier-import-list"))
    assert len(resp.json()["data"]) == result_count


@pytest.mark.parametrize("role__name", ["Support"])
def test_imported_instance_be_get_name(
    db, be_instance, form_factory, document_factory, question_factory, admin_client
):
    # for coverage CalumaInstanceSerializer.get_name()
    question = question_factory(pk="geschaeftstyp-import")
    be_instance.case.document = document_factory(form_id="migriertes-dossier")
    be_instance.case.document.answers.create(question=question, value="geschaeftstyp")

    serializer = CalumaInstanceSerializer()
    assert serializer.get_name(be_instance).startswith("geschaeftstyp")


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
    "config,camac_instance",
    [
        ("kt_bern", lazy_fixture("be_instance")),
        # ("kt_schwyz", "Support", lazy_fixture("sz_instance")),
    ],
)
@pytest.mark.parametrize(
    "action,host,role__name,status_before,expected_response_code,status_after",
    [
        (
            "start",
            "sycloud",
            "municipality-lead",
            DossierImport.IMPORT_STATUS_VALIDATION_SUCCESSFUL,
            status.HTTP_200_OK,
            DossierImport.IMPORT_STATUS_IMPORT_INPROGRESS,
        ),
        (
            "start",
            "prod",
            "municipality-lead",
            DossierImport.IMPORT_STATUS_VALIDATION_SUCCESSFUL,
            status.HTTP_404_NOT_FOUND,
            None,
        ),
        (
            "start",
            "sycloud",
            "municipality-lead",
            DossierImport.IMPORT_STATUS_VALIDATION_FAILED,
            status.HTTP_400_BAD_REQUEST,
            None,
        ),
        (
            "confirm",
            "sycloud",
            "municipality-lead",
            DossierImport.IMPORT_STATUS_IMPORTED,
            status.HTTP_200_OK,
            DossierImport.IMPORT_STATUS_CONFIRMED,
        ),
        (
            "confirm",
            "sycloud",
            "municipality-lead",
            DossierImport.IMPORT_STATUS_VALIDATION_SUCCESSFUL,
            status.HTTP_400_BAD_REQUEST,
            None,
        ),
        (
            "transmit",
            "sycloud",
            "support",
            DossierImport.IMPORT_STATUS_CONFIRMED,
            status.HTTP_200_OK,
            DossierImport.IMPORT_STATUS_TRANSMITTING,
        ),
        (
            "transmit",
            "prod",
            "support",
            DossierImport.IMPORT_STATUS_CONFIRMED,
            status.HTTP_403_FORBIDDEN,
            None,
        ),
        (
            "transmit",
            "sycloud",
            "municipality-lead",
            DossierImport.IMPORT_STATUS_CONFIRMED,
            status.HTTP_403_FORBIDDEN,
            None,
        ),
        (
            "transmit",
            "sycloud",
            "support",
            DossierImport.IMPORT_STATUS_IMPORTED,
            status.HTTP_400_BAD_REQUEST,
            None,
        ),
        (
            "undo",
            "sycloud",
            "support",
            DossierImport.IMPORT_STATUS_IMPORTED,
            status.HTTP_200_OK,
            "deleted",
        ),
        (
            "undo",
            "sycloud",
            "municipality-lead",
            DossierImport.IMPORT_STATUS_IMPORTED,
            status.HTTP_200_OK,
            "deleted",
        ),
        (
            "undo",
            "prod",
            "support",
            DossierImport.IMPORT_STATUS_IMPORTED,
            status.HTTP_403_FORBIDDEN,
            None,
        ),
        (
            "undo",
            "prod",
            "municipality-lead",
            DossierImport.IMPORT_STATUS_IMPORTED,
            status.HTTP_404_NOT_FOUND,
            None,
        ),
    ],
)
def test_state_transitions(
    db,
    admin_client,
    admin_user,
    location,
    settings,
    archive_file,
    dossier_import_factory,
    setup_fixtures_required_by_application_config,
    make_workflow_items_for_config,
    config,
    camac_instance,
    action,
    status_before,
    expected_response_code,
    status_after,
    case_factory,
    host,
    mailoutbox,
):
    make_workflow_items_for_config(config)
    setup_fixtures_required_by_application_config(config)
    settings.APPLICATION = settings.APPLICATIONS[config]
    settings.INTERNAL_BASE_URL = f"https://{host}.example.com"
    # settings.Q_CLUSTER["sync"] = True  # doesn't work, unfortunately

    dossier_import = dossier_import_factory(
        status=status_before,
        source_file=archive_file("import-example.zip"),
        group=admin_client.user.groups.first(),
    )

    if action == "undo":
        case_factory.create_batch(2, meta={"import-id": str(dossier_import.pk)})
        case_factory()  # unrelated case

    resp = admin_client.post(
        reverse(f"dossier-import-{action}", args=(dossier_import.pk,))
    )
    assert resp.status_code == expected_response_code
    if expected_response_code == status.HTTP_200_OK:
        if status_after == "deleted":
            assert not DossierImport.objects.filter(pk=dossier_import.pk).exists()
            assert not Case.objects.filter(
                **{"meta__import-id": str(dossier_import.pk)}
            ).exists()
        else:
            dossier_import.refresh_from_db()
            assert dossier_import.status == status_after
    if (
        action == "confirm"
        and dossier_import.status == DossierImport.IMPORT_STATUS_CONFIRMED
    ):
        assert len(mailoutbox) == 1


@pytest.mark.parametrize("location_required", [True, False])
def test_transmitting_logic(
    db,
    dossier_import_factory,
    archive_file,
    group,
    settings,
    application_settings,
    requests_mock,
    location_required,
):
    application_settings["DOSSIER_IMPORT"]["PROD_URL"] = "http://ebau.local"
    application_settings["DOSSIER_IMPORT"]["LOCATION_REQUIRED"] = location_required
    application_settings["DOSSIER_IMPORT"][
        "PROD_AUTH_URL"
    ] = settings.KEYCLOAK_OIDC_TOKEN_URL

    # set a real group ID - useful for testing without the mock
    group.pk = 22507  # Administration Leitbehörde Burgdorf
    group.save()

    # disabling the mocks will upload the file to the local dev env - useful for more realistic resting!
    requests_mock.register_uri(
        "POST",
        "/auth/realms/ebau/protocol/openid-connect/token",
        json={"access_token": "hello123"},
        complete_qs=True,
    )

    def matcher(request):
        assert bool(request.body.fields.get("location_id", False)) == location_required
        return True

    requests_mock.register_uri(
        "POST",
        build_url(settings.INTERNAL_BASE_URL, "/api/v1/dossier-imports"),
        json={
            "data": {
                "type": "dossier-imports",
                "id": "031562b0-aec8-4372-b1e6-c7ac909a6287",
                "attributes": {},
                "relationships": {},
            }
        },
        additional_matcher=matcher,
    )

    # Call domain logic directly, this can be removed once sync calls in Q cluster work
    dossier_import = dossier_import_factory(
        status=DossierImport.IMPORT_STATUS_CONFIRMED,
        source_file=archive_file("import-example-no-errors.zip"),
        group=group,
    )
    transmit_import(dossier_import)


def test_failing_transmission(db, application_settings, requests_mock, dossier_import):
    PROD_URL = "http://this-could-be-your-production-url.example.com"
    PROD_AUTH_URL = PROD_URL + "/auth/token"
    application_settings["DOSSIER_IMPORT"]["PROD_URL"] = PROD_URL
    application_settings["DOSSIER_IMPORT"]["PROD_AUTH_URL"] = PROD_AUTH_URL
    requests_mock.register_uri("POST", PROD_AUTH_URL, status_code=401)
    requests_mock.register_uri(
        "POST", PROD_URL + "/api/v1/dossier-imports", status_code=401
    )
    transmit_import(dossier_import)
    assert dossier_import.status == DossierImport.IMPORT_STATUS_TRANSMISSION_FAILED
