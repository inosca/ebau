import dataclasses
import datetime
import mimetypes

import pytest
from alexandria.core.models import Document
from caluma.caluma_workflow.models import Case
from django.urls import reverse
from django.utils import timezone
from pytest_lazy_fixtures import lf

from camac.dossier_import.domain_logic import (
    perform_import,
    transmit_import,
    undo_import,
)
from camac.dossier_import.dossier_classes import Dossier
from camac.dossier_import.messages import MessageCodes
from camac.dossier_import.models import DossierImport
from camac.instance.master_data import MasterData
from camac.instance.models import Instance
from camac.settings.modules.master_data import MASTER_DATA
from camac.tags.models import Keyword
from camac.utils import build_url


@pytest.mark.django_db
def test_undo_import(
    dossier_import,
    caluma_case_factory,
    instance_factory,
    keyword_factory,
    alexandria_document_factory,
    application_settings,
):
    application_settings["DOCUMENT_BACKEND"] = "alexandria"

    cases = caluma_case_factory.create_batch(
        2, meta={"import-id": str(dossier_import.pk)}
    )
    for case in cases:
        instance = instance_factory.create(case=case)
        keyword = keyword_factory.create()
        keyword.instances.set([instance])
        alexandria_document_factory(
            metainfo={"camac-instance-id": instance.pk},
        )

    unrelated_case = caluma_case_factory()
    unrelated_instance = instance_factory(case=unrelated_case)
    keyword = keyword_factory.create()
    keyword.instances.set([unrelated_instance])
    non_imported_doc = alexandria_document_factory(
        metainfo={"camac-instance-id": unrelated_instance.pk},
    )

    undo_import(dossier_import.pk)
    assert not Case.objects.filter(
        **{"meta__import-id": str(dossier_import.pk)}
    ).exists()
    assert not Instance.objects.filter(
        **{"case__meta__import-id": str(dossier_import.pk)}
    ).exists()
    assert Keyword.objects.count() == 1
    assert Keyword.objects.first().pk == keyword.pk
    assert Document.objects.count() == 1
    assert Document.objects.first().pk == non_imported_doc.pk


@pytest.mark.freeze_time("2023-4-1")
@pytest.mark.parametrize(
    ("first_import_file", "reimport_file"),
    [
        ("import-example-no-errors.zip", "import-example-no-errors.zip"),
        ("import-example-no-errors.zip", "import-example-no-errors-reimport.zip"),
    ],
)
# the dossier_id marks the tested re-import line in the import source file
@pytest.mark.parametrize("dossier_id", ["2017-84"])
# configurations of schwyz and bern have different setup requirements.
# in order to reuse the general test setup we'll
# cope with some redundancy with test setup and parametrization.
@pytest.mark.parametrize(
    "app",
    [
        lf("set_application_sz"),
        lf("set_application_be"),
        lf("set_application_so"),
    ],
)
@pytest.mark.django_db
def test_perform_reimport(  # noqa: C901
    master_data_is_visible_mock,
    admin_client,
    archive_file,
    dossier_import_factory,
    dossier_loader,
    dossier_id,
    setup_dossier_writer,
    first_import_file,
    reimport_file,
    freezer,
    tmpdir,
    app,
    settings,
    support_role,
):
    config = settings.APPLICATION_NAME

    writer = setup_dossier_writer(config)
    now = timezone.now()

    # perform an import
    first_import = dossier_import_factory(
        group=writer._group,
        user=writer._user,
        source_file=archive_file(first_import_file),
        mime_type=mimetypes.types_map[".zip"],
        # Since we don't use `schedule_import` we manually set the status to
        # in-progress
        status=DossierImport.Status.IMPORT_IN_PROGRESS,
    )

    perform_import(first_import.pk)

    imported_dossier = writer.find_existing_instance(
        Dossier(id=dossier_id, proposal=""), writer._caluma_user
    )

    if config == "kt_bern":
        # Ensure responsible user is imported. Currently only defined in BERN
        assert imported_dossier.responsible_services.filter(
            responsible_user__email="admin@example.com"
        ).exists()

    # The followup import should replace the file with the name Baugesuch.pdf
    # with something else.
    if config in ["kt_bern", "kt_schwyz"]:
        original_attachment_bytes = (
            imported_dossier.attachments.filter(name="Baugesuch.pdf")
            .first()
            .path.read()
        )
    if config == "kt_so":
        doc = Document.objects.filter(
            **{"metainfo__camac-instance-id": str(imported_dossier.pk)}
        ).first()
        original_attachment_bytes = doc.get_latest_original().content.read()
    freezer.move_to(now.replace(day=11))
    # perform the re-import with an import.zip file that features a line
    # referencing the dossier-id and changing values for all columns
    reimport = dossier_import_factory(
        group=writer._group,
        user=writer._user,
        source_file=archive_file(reimport_file),
        mime_type=mimetypes.types_map[".zip"],
        # Since we don't use `schedule_import` we manually set the status to
        # in-progress
        status=DossierImport.Status.IMPORT_IN_PROGRESS,
    )
    perform_import(reimport.pk)
    reimport.refresh_from_db()
    imported_dossier.refresh_from_db()
    md = MasterData(imported_dossier.case)
    # get an abstracted dataset for the dossier that we can work with
    updated_values = {key: getattr(md, key) for key in MASTER_DATA[config]["CONFIG"]}

    if config == "kt_bern" and reimport_file == "import-example-no-errors-reimport.zip":
        # in the reimport file, the user should be removed
        assert not imported_dossier.responsible_services.filter(
            responsible_user__isnull=False
        ).exists()
    elif config == "kt_bern" and reimport_file == "import-example-no-errors.zip":
        # Same value, should be kept
        assert imported_dossier.responsible_services.filter(
            responsible_user__email="admin@example.com"
        ).exists()

    # get the imported values from the secondary archive that should have
    # been written to the dossier
    dossier = next(dossier_loader.load_dossiers(reimport), None)
    dossier_dict = {
        field.name: getattr(dossier, field.name)
        for field in dataclasses.fields(dossier)
    }

    # assert that the updates from the secondary import have indeed been
    # persisted to the dossier
    for key in [
        "proposal",
        "city",
    ]:
        assert updated_values[key] == dossier_dict[key]
    for key in [
        "submit_date",
        "publication_date",
        "decision_date",
        "construction_start_date",
        "profile_approval_date",
        "final_approval_date",
        "completion_date",
    ]:
        # not all dates are dates
        if updated := updated_values[key]:
            if getattr(updated, "time", None):
                updated = updated.date()
            assert updated == dossier_dict[key].date()

    # some quirks
    if config != "kt_so":
        assert updated_values["usage_zone"] == dossier_dict["usage"]
    if config == "kt_schwyz":
        assert updated_values["street"] == " ".join(
            [dossier_dict["street"], dossier_dict["street_number"]]
        )
    else:
        assert updated_values["street"] == dossier_dict["street"]

    # some more: the import specifies only one person per role but allows
    # multiple entries for others like plot_data etc.
    # On top the configurations have divergent data structures for plot_data
    # hence the additional caveats.
    for key, prop in [
        ("applicants", "applicant"),
        ("landowners", "landowner"),
        ("project_authors", "project_author"),
        ("plot_data", "plot_data"),
        ("coordinates", "coordinates"),
    ]:
        imported = dataclasses.asdict(getattr(dossier, prop)[0])
        if config == "kt_schwyz":
            if imported.get("street"):
                imported["street"] = " ".join(
                    [imported["street"], imported["street_number"]]
                )
                del imported["street_number"]
            # coordinates for kt_schwyz are handled separately
            if key == "coordinates":
                continue
        diff = [
            (data, imported[k])
            for k in imported
            if (dataset := updated_values.get(key)) and (data := dataset[0].get(k))
        ]
        for d, u in diff:
            assert str(d) == str(u)

    # kt_schwyz: verify coordinates
    if config == "kt_schwyz":
        assert (
            imported_dossier.fields.get(name="punkte").value
            == updated_values["coordinates"]
        )

    # verify that the original attachment file has been replaced
    if config in ["kt_bern", "kt_schwyz"]:
        the_attachment = imported_dossier.attachments.filter(
            name="Baugesuch.pdf"
        ).first()
        current_attachment_bytes = the_attachment.path.read()
    else:
        doc = Document.objects.filter(
            title="Baugesuch.pdf",
            **{"metainfo__camac-instance-id": str(imported_dossier.pk)},
        ).first()
        the_attachment = doc.get_latest_original()
        current_attachment_bytes = the_attachment.content.read()
    if hasattr(the_attachment, "date"):
        modified_at = datetime.datetime.fromisoformat(
            the_attachment.date.isoformat()
        ).date()
    if hasattr(the_attachment, "modified_at"):
        modified_at = datetime.datetime.fromisoformat(
            the_attachment.modified_at.isoformat()
        ).date()
    assert the_attachment.size == len(current_attachment_bytes)
    # verify reimport actually differs from original import
    if first_import_file != reimport_file:
        assert original_attachment_bytes != current_attachment_bytes
        # if the attachment has been updated the so must have the timestamp:
        assert modified_at > now.date()
        # verifying that the the re-import creates the right messages.
        for message in reimport.messages["import"]["details"]:
            if message["dossier_id"] != dossier_id:
                continue
            for detail in message["details"]:
                if detail["code"] == MessageCodes.ATTACHMENT_UPDATED.value:
                    assert detail["detail"] == the_attachment.name
    else:
        # if the attachment was unchanged: assert that it is identical and that the date attribute hasn't changed
        assert original_attachment_bytes == current_attachment_bytes
        assert modified_at == now.date()


@pytest.mark.parametrize("location_required", [True, False])
@pytest.mark.django_db
def test_transmitting_logic(
    dossier_import_factory,
    archive_file,
    group,
    settings,
    requests_mock,
    location_required,
    dossier_import_settings,
):
    dossier_import_settings["PROD_URL"] = "http://ebau.localhost"
    dossier_import_settings["LOCATION_REQUIRED"] = location_required
    dossier_import_settings["PROD_AUTH_URL"] = settings.KEYCLOAK_OIDC_TOKEN_URL
    dossier_import_settings["PROD_SUPPORT_GROUP_ID"] = 99

    # set a real group ID - useful for testing without the mock
    group.pk = 22507  # Administration Leitbehörde Burgdorf
    group.save()

    # disabling the mocks will upload the file to the local dev env - useful for more realistic testing!
    requests_mock.register_uri(
        "POST",
        dossier_import_settings["PROD_AUTH_URL"],
        json={"access_token": "hello123"},
        complete_qs=True,
    )

    def matcher(request):
        assert bool(request.body.fields.get("location_id", False)) == location_required
        return True

    requests_mock.register_uri(
        "POST",
        build_url(dossier_import_settings["PROD_URL"], reverse("dossier-import-list")),
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
        status=DossierImport.Status.CONFIRMED,
        source_file=archive_file("import-example-no-errors.zip"),
        group=group,
    )
    assert transmit_import(dossier_import.pk) == DossierImport.Status.TRANSMITTED


@pytest.mark.django_db
def test_failing_transmission(requests_mock, dossier_import, dossier_import_settings):
    PROD_URL = "http://this-could-be-your-production-url.example.com"
    PROD_AUTH_URL = PROD_URL + "/auth/token"
    dossier_import_settings["PROD_URL"] = PROD_URL
    dossier_import_settings["PROD_AUTH_URL"] = PROD_AUTH_URL
    requests_mock.register_uri("POST", PROD_AUTH_URL, status_code=401)
    requests_mock.register_uri(
        "POST", PROD_URL + "/api/v1/dossier-imports", status_code=401
    )
    assert (
        transmit_import(dossier_import.pk) == DossierImport.Status.TRANSMISSION_FAILED
    )
