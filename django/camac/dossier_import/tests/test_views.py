import mimetypes

import pytest
from django.utils import timezone
from django_q.brokers import get_broker
from django_q.signing import SignedPackage
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
        ("kt_bern", "test.ebau.ch", "municipality-lead", 1),
        ("kt_bern", "ebau.apps.be.ch", "municipality-lead", 0),
        ("kt_schwyz", "test.ebau.ch", "Gemeinde", 1),
        ("kt_schwyz", "ebau-sz.ch", "Gemeinde", 0),
        ("kt_schwyz", "test.ebau.ch", "Support", 2),
        ("kt_schwyz", "test.ebau.ch", "Applicant", 0),
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
    application_settings,
):
    application_settings["ROLE_PERMISSIONS"] = settings.APPLICATIONS[config][
        "ROLE_PERMISSIONS"
    ]
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
            lazy_fixture("sz_dossier_import_settings"),
            lazy_fixture("location"),
            status.HTTP_201_CREATED,
        ),
        (
            "import-example-validation-errors.zip",
            lazy_fixture("sz_dossier_import_settings"),
            None,
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            "import-example-validation-errors.zip",
            lazy_fixture("be_dossier_import_settings"),
            None,
            status.HTTP_201_CREATED,
        ),
        (
            "import-example-validation-errors.zip",
            lazy_fixture("so_dossier_import_settings"),
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
    archive_file,
    snapshot,
    import_file,
    config,
    location_id,
    expected_status,
):
    # create an import case with an uploaded file using the REST endpoint (POST)
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
@pytest.mark.parametrize("dossier_exists", [False, lazy_fixture("instance")])
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
    settings,
    mocker,
    admin_client,
    group,
    admin_user,
    role,
    location,
    dossier_exists,
    archive_file,
    import_file,
    expected_status,
    expected_result,
    snapshot,
    dossier_import_settings,
):
    # create an import case with an uploaded file using the REST endpoint (POST)
    mocker.patch(
        f"{dossier_import_settings['WRITER_CLASS']}.existing_dossier",
        lambda self, dossier_id: dossier_exists,
    )
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
        assert expected_result in str(resp.data[0]["detail"])
    else:
        if expected_result is not None:
            for key, value in expected_result.items():
                for left, right in zip(
                    sorted(value),
                    sorted(resp.data["messages"]["validation"]["summary"][key]),
                ):
                    assert left in right
        admin_client.delete(reverse("dossier-import-detail", args=(resp.data["id"],)))


@pytest.mark.freeze_time("2021-12-12")
@pytest.mark.parametrize(
    "config,camac_instance",
    [
        ("kt_bern", lazy_fixture("be_instance")),
        # ("kt_schwyz", lazy_fixture("sz_instance")),
    ],
)
@pytest.mark.parametrize(
    "action,host,role__name,status_before,expected_response_code,status_after",
    [
        (
            "start",
            "test",
            "Municipality",
            DossierImport.IMPORT_STATUS_VALIDATION_SUCCESSFUL,
            status.HTTP_200_OK,
            DossierImport.IMPORT_STATUS_IMPORT_IN_PROGRESS,
        ),
        (
            "start",
            "prod",
            "Municipality",
            DossierImport.IMPORT_STATUS_VALIDATION_SUCCESSFUL,
            status.HTTP_404_NOT_FOUND,
            None,
        ),
        (
            "start",
            "test",
            "Municipality",
            DossierImport.IMPORT_STATUS_VALIDATION_FAILED,
            status.HTTP_400_BAD_REQUEST,
            None,
        ),
        (
            "confirm",
            "test",
            "Municipality",
            DossierImport.IMPORT_STATUS_IMPORTED,
            status.HTTP_204_NO_CONTENT,
            DossierImport.IMPORT_STATUS_CONFIRMED,
        ),
        (
            "confirm",
            "test",
            "Municipality",
            DossierImport.IMPORT_STATUS_VALIDATION_SUCCESSFUL,
            status.HTTP_400_BAD_REQUEST,
            None,
        ),
        (
            "transmit",
            "test",
            "Support",
            DossierImport.IMPORT_STATUS_CONFIRMED,
            status.HTTP_200_OK,
            DossierImport.IMPORT_STATUS_TRANSMITTING,
        ),
        (
            "transmit",
            "prod",
            "Support",
            DossierImport.IMPORT_STATUS_CONFIRMED,
            status.HTTP_403_FORBIDDEN,
            None,
        ),
        (
            "transmit",
            "test",
            "Municipality",
            DossierImport.IMPORT_STATUS_CONFIRMED,
            status.HTTP_403_FORBIDDEN,
            None,
        ),
        (
            "transmit",
            "test",
            "Support",
            DossierImport.IMPORT_STATUS_IMPORTED,
            status.HTTP_400_BAD_REQUEST,
            None,
        ),
        (
            "undo",
            "test",
            "Support",
            DossierImport.IMPORT_STATUS_IMPORTED,
            status.HTTP_200_OK,
            DossierImport.IMPORT_STATUS_UNDO_IN_PROGRESS,
        ),
        (
            "undo",
            "test",
            "Municipality",
            DossierImport.IMPORT_STATUS_IMPORTED,
            status.HTTP_200_OK,
            DossierImport.IMPORT_STATUS_UNDO_IN_PROGRESS,
        ),
        (
            "undo",
            "prod",
            "Support",
            DossierImport.IMPORT_STATUS_IMPORTED,
            status.HTTP_200_OK,
            DossierImport.IMPORT_STATUS_UNDO_IN_PROGRESS,
        ),
        (
            "undo",
            "prod",
            "Municipality",
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
    setup_dossier_writer,
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
    setup_dossier_writer(config)
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
    dossier_import.refresh_from_db()
    if expected_response_code == status.HTTP_200_OK:
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
    requests_mock,
    location_required,
    dossier_import_settings,
):
    dossier_import_settings["PROD_URL"] = "http://ebau.local"
    dossier_import_settings["LOCATION_REQUIRED"] = location_required
    dossier_import_settings["PROD_AUTH_URL"] = settings.KEYCLOAK_OIDC_TOKEN_URL

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


def test_failing_transmission(
    db, requests_mock, dossier_import, dossier_import_settings
):
    PROD_URL = "http://this-could-be-your-production-url.example.com"
    PROD_AUTH_URL = PROD_URL + "/auth/token"
    dossier_import_settings["PROD_URL"] = PROD_URL
    dossier_import_settings["PROD_AUTH_URL"] = PROD_AUTH_URL
    requests_mock.register_uri("POST", PROD_AUTH_URL, status_code=401)
    requests_mock.register_uri(
        "POST", PROD_URL + "/api/v1/dossier-imports", status_code=401
    )
    transmit_import(dossier_import)
    assert dossier_import.status == DossierImport.IMPORT_STATUS_TRANSMISSION_FAILED


@pytest.mark.parametrize("role__name", ["Support"])
def test_download_import(db, admin_client, archive_file, dossier_import_factory):
    dossier_import = dossier_import_factory(
        source_file=archive_file("import-example.zip"),
        group=admin_client.user.groups.first(),
    )
    resp = admin_client.get(
        reverse("dossier-import-download", args=(dossier_import.pk,))
    )
    assert resp.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("role__name", ["Support"])
def test_clean_import(db, admin_client, archive_file, dossier_import_factory):
    dossier_import = dossier_import_factory(
        source_file=archive_file("import-example.zip"),
        group=admin_client.user.groups.first(),
    )
    resp = admin_client.post(reverse("dossier-import-clean", args=(dossier_import.pk,)))
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    dossier_import.refresh_from_db()
    assert not dossier_import.source_file


@pytest.mark.parametrize(
    "has_case,expected_status",
    [(False, status.HTTP_204_NO_CONTENT), (True, status.HTTP_400_BAD_REQUEST)],
)
@pytest.mark.parametrize("role__name", ["Support"])
def test_delete_import(
    db,
    admin_client,
    archive_file,
    dossier_import,
    case_factory,
    instance_with_case,
    has_case,
    expected_status,
):
    if has_case:
        case_factory(meta={"import-id": str(dossier_import.pk)})
    resp = admin_client.delete(
        reverse("dossier-import-detail", args=(str(dossier_import.pk),))
    )
    assert resp.status_code == expected_status


@pytest.mark.parametrize("role__name", ["Support"])
@pytest.mark.parametrize(
    "task_state,expected_status",
    [
        ("queued", DossierImport.IMPORT_STATUS_IMPORT_IN_PROGRESS),
        ("timed-out", DossierImport.IMPORT_STATUS_IMPORT_FAILED),
        (
            DossierImport.IMPORT_STATUS_IMPORT_IN_PROGRESS,
            DossierImport.IMPORT_STATUS_IMPORT_IN_PROGRESS,
        ),
        (None, DossierImport.IMPORT_STATUS_IMPORT_FAILED),
        (DossierImport.IMPORT_STATUS_IMPORTED, DossierImport.IMPORT_STATUS_IMPORTED),
    ],
)
def test_import_status(
    db, admin_client, dossier_import, task_state, expected_status, settings, mocker
):
    lock = timezone.now()
    dossier_import.status = DossierImport.IMPORT_STATUS_IMPORT_IN_PROGRESS
    dossier_import.save()
    if not task_state:
        # verify that an in progres status and no task-id results in failed status
        assert "failed" in dossier_import.update_async_status()
        return
    if task_state == "queued":
        lock = lock - timezone.timedelta(2 * settings.Q_CLUSTER["timeout"])
    task = {
        "id": "abba1221acab1312",
        "name": "one-task",
        "func": "some-func",
        "args": {},
    }
    other_task = {
        "id": "1234abcd5678efgh",
        "name": "other-task",
        "func": "some-func",
        "args": {},
    }
    broker = get_broker()
    if task_state not in ("timed-out", DossierImport.IMPORT_STATUS_IMPORTED):
        broker.get_connection().create(
            key=broker.list_key, payload=SignedPackage.dumps(task), lock=lock
        )
    dossier_import.task_id = task["id"]
    dossier_import.save()
    broker.get_connection().create(
        key=broker.list_key,
        payload=SignedPackage.dumps(other_task),
        lock=timezone.now(),
    )
    if task_state in (
        DossierImport.IMPORT_STATUS_IMPORT_IN_PROGRESS,
        DossierImport.IMPORT_STATUS_IMPORTED,
    ):
        mocker.patch("camac.dossier_import.models.fetch", return_value=task)
    dossier_import.update_async_status()
    dossier_import.status == expected_status
    resp = admin_client.get(reverse("dossier-import-detail", args=(dossier_import.pk,)))
    assert resp.status_code == status.HTTP_200_OK
    # status is only changed by the update_async_status method if import times out
    assert (
        resp.json()["data"]["attributes"]["status"]
        == DossierImport.IMPORT_STATUS_IMPORT_FAILED
        if expected_status == "timed-out"
        else DossierImport.IMPORT_STATUS_IMPORTED
    )
