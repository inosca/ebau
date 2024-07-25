import dataclasses
import datetime
import mimetypes

import pytest
from alexandria.core.models import Document
from caluma.caluma_workflow.models import Case
from django.utils import timezone

from camac.dossier_import.domain_logic import perform_import, undo_import
from camac.dossier_import.messages import MessageCodes
from camac.instance.master_data import MasterData
from camac.settings.modules.master_data import MASTER_DATA


def test_undo_import(db, dossier_import, case_factory, instance_with_case):
    case_factory.create_batch(2, meta={"import-id": str(dossier_import.pk)})
    case_factory()  # unrelated case
    undo_import(dossier_import)
    assert not Case.objects.filter(
        **{"meta__import-id": str(dossier_import.pk)}
    ).exists()


@pytest.mark.freeze_time("2023-4-1")
@pytest.mark.parametrize(
    "first_import_file,reimport_file",
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
    "config",
    [
        "kt_schwyz",
        "kt_bern",
        "kt_so",
    ],
)
def test_perform_reimport(  # noqa: C901
    db,
    master_data_is_visible_mock,
    admin_client,
    archive_file,
    dossier_import_factory,
    dossier_loader,
    config,
    dossier_id,
    setup_dossier_writer,
    first_import_file,
    reimport_file,
    freezer,
    tmpdir,
):
    writer = setup_dossier_writer(config)
    now = timezone.now()

    # perform an import
    first_import = dossier_import_factory(
        group=writer._group,
        user=writer._user,
        source_file=archive_file(first_import_file),
        mime_type=mimetypes.types_map[".zip"],
    )
    perform_import(first_import)

    imported_dossier = writer.existing_dossier(dossier_id)

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
    )
    perform_import(reimport)
    imported_dossier.refresh_from_db()
    md = MasterData(imported_dossier.case)
    # get an abstracted dataset for the dossier that we can work with
    updated_values = {
        key: getattr(md, key) for key in MASTER_DATA[config]["CONFIG"].keys()
    }

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
    reimport.source_file.file.seek(0)
    dossier = next(dossier_loader.load_dossiers(reimport.get_archive()), None)
    dossier_dict = dict(
        (field.name, getattr(dossier, field.name))
        for field in dataclasses.fields(dossier)
    )

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
        if config == "kt_schwyz" and imported.get("street"):
            imported["street"] = " ".join(
                [imported["street"], imported["street_number"]]
            )
            del imported["street_number"]
        diff = [
            (data, imported[k])
            for k in imported.keys()
            if (dataset := updated_values.get(key)) and (data := dataset[0].get(k))
        ]
        for d, u in diff:
            assert str(d) == str(u)
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
