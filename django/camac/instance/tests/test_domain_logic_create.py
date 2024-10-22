import pytest
from alexandria.core.factories import DocumentFactory, FileFactory
from alexandria.core.models import Document, File
from rest_framework.exceptions import ValidationError

from camac.instance.domain_logic.create import CreateInstanceLogic


@pytest.mark.parametrize(
    "skip_exported_form_attachment,expected_copies",
    [
        (False, 2),
        (True, 1),
    ],
)
def test_copy_attachments(
    db,
    instance_factory,
    application_settings,
    instance_with_case,
    caluma_workflow_config_gr,
    skip_exported_form_attachment,
    expected_copies,
):
    application_settings["DOCUMENT_BACKEND"] = "alexandria"

    source_instance = instance_with_case(instance_factory())
    target_instance = instance_with_case(instance_factory())
    docs = [
        DocumentFactory(
            title="some-doc",
            metainfo={
                "camac-instance-id": str(source_instance.pk),
                "caluma-document-id": str(source_instance.case.document.pk),
            },
        ),
        DocumentFactory(
            title="baugesuch",
            metainfo={
                "camac-instance-id": str(source_instance.pk),
                "system-generated": True,
            },
        ),
    ]
    files = [FileFactory(document=doc) for doc in docs]

    assert Document.objects.count() == 2
    assert File.objects.filter(variant=File.Variant.ORIGINAL).count() == 2

    CreateInstanceLogic.copy_attachments(
        source_instance, target_instance, skip_exported_form_attachment
    )

    assert Document.objects.count() == 2 + expected_copies
    assert (
        File.objects.filter(variant=File.Variant.ORIGINAL).count()
        == 2 + expected_copies
    )

    new_document = (
        Document.objects.filter(title=docs[0].title).order_by("-created_at").first()
    )
    new_file = new_document.get_latest_original()
    old_file = files[0]

    assert new_document.metainfo["camac-instance-id"] == str(target_instance.pk)
    assert new_document.instance_document.instance_id == target_instance.pk
    assert new_document.metainfo["caluma-document-id"] == str(
        target_instance.case.document.pk
    )

    assert new_file.name == old_file.name
    assert new_file.id != old_file.id


def test_copy_applicants(
    db,
    caluma_workflow_config_gr,
    gr_permissions_settings,
    instance_factory,
    applicant_factory,
    access_level_factory,
    instance_with_case,
    user,
    user_factory,
):
    access_level_factory(slug="applicant")
    source_instance = instance_with_case(instance_factory())
    target_instance = instance_with_case(instance_factory())
    target_instance.involved_applicants.all().delete()
    applicant_factory(instance=source_instance, invitee=user, role="EDITOR")
    applicant_factory(
        instance=source_instance, invitee=user_factory(), role="READ_ONLY"
    )
    applicant_factory(
        instance=source_instance, invitee=None, email="1@test.test", role="READ_ONLY"
    )
    applicant_factory(
        instance=source_instance, invitee=None, email="2@test.test", role="READ_ONLY"
    )

    CreateInstanceLogic.copy_applicants(source_instance, target_instance)

    assert (
        target_instance.involved_applicants.count()
        == source_instance.involved_applicants.count()
    )
    for applicant in source_instance.involved_applicants.all():
        if applicant.invitee:
            copy = target_instance.involved_applicants.filter(invitee=applicant.invitee)
            assert target_instance.acls.filter(
                access_level="applicant", user=applicant.invitee
            ).exists()
        else:
            copy = target_instance.involved_applicants.filter(email=applicant.email)
        assert copy.exists()
        assert copy.first().role == applicant.role


@pytest.mark.parametrize("service__external_identifier", ["2601"])
@pytest.mark.parametrize(
    "existing_dossier_numbers,expected_dossier_number",
    [
        (None, "2601-2024-1"),
        (["2601-2024-1", "2602-2024-2"], "2601-2024-2"),
        (
            ["2601-1999-9999", "2601-2022-99999", "2601-2024-9", "2601-2024-10"],
            "2601-2024-11",
        ),
    ],
)
@pytest.mark.freeze_time("2024-4-17")
def test_instance_generate_identifier_so(
    db,
    so_instance,
    case_factory,
    service,
    existing_dossier_numbers,
    expected_dossier_number,
    application_settings,
):
    application_settings["SHORT_NAME"] = "so"

    if existing_dossier_numbers:
        for nr in existing_dossier_numbers:
            case_factory(meta={"dossier-number": nr})

    assert (
        CreateInstanceLogic.generate_identifier(so_instance) == expected_dossier_number
    )


def test_instance_generate_identifier_so_exceptions(
    db,
    application_settings,
    instance_service_factory,
    service_factory,
    so_instance,
    mocker,
):
    application_settings["SHORT_NAME"] = "so"

    mocker.patch(
        "camac.instance.models.Instance.responsible_service", return_value=None
    )

    with pytest.raises(ValidationError) as e1:
        CreateInstanceLogic.generate_identifier(so_instance)

    assert str(e1.value.detail[0]) == "Instance does not have a responsible service"

    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service_factory(
            service_group__name="municipality",
            external_identifier=None,
        ),
    )

    with pytest.raises(ValidationError) as e2:
        CreateInstanceLogic.generate_identifier(so_instance)

    assert (
        str(e2.value.detail[0])
        == "Responsible service does not have an external identifier"
    )
