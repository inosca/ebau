import pytest
from alexandria.core.factories import CategoryFactory, DocumentFactory, FileFactory
from alexandria.core.models import Document, File
from pytest_lazy_fixtures import lf
from rest_framework.exceptions import ValidationError

from camac.document.models import Attachment
from camac.instance.domain_logic.create import CreateInstanceLogic
from camac.timelines.models import FormTimeline


@pytest.mark.parametrize(
    "args,expected_copies",
    [
        (
            {"skip_exported_form_attachment": False, "copy_attachments_from": [99]},
            1,
        ),
        (
            {
                "skip_exported_form_attachment": False,
                "copy_attachments_from": [],
            },
            5,
        ),
        (
            {
                "skip_exported_form_attachment": True,
                "copy_attachments_from": [],
            },
            4,
        ),
    ],
)
@pytest.mark.django_db
def test_copy_attachments_camac_ng(
    application_settings,
    args,
    expected_copies,
    be_instance,
    instance_with_case,
    instance_factory,
    attachment_factory,
    attachment_section_factory,
):
    application_settings["DOCUMENT_BACKEND"] = "camac-ng"
    source_instance = be_instance
    source_instance.case.document.form.name = "test"
    source_instance.case.document.form.save()
    target_instance = instance_with_case(instance_factory())

    attachment_section_other = attachment_section_factory(pk=100)
    docs = [
        attachment_factory(
            name="important-doc",
            instance=source_instance,
        ),
        attachment_factory(
            name="some-doc",
            instance=source_instance,
        ),
        attachment_factory(
            name="baugesuch",
            instance=source_instance,
        ),
        attachment_factory(
            name=f"{source_instance.pk}-{source_instance.case.document.form.name}.pdf",
            instance=source_instance,
        ),
    ]
    for doc in docs:
        doc.attachment_sections.add(attachment_section_other)

    applicant_attachment = attachment_factory(
        name="only_applicant",
        instance=source_instance,
    )
    attachment_section_applicant = attachment_section_factory(pk=99)
    applicant_attachment.attachment_sections.add(attachment_section_applicant)
    docs.append(applicant_attachment)

    total_docs = len(docs)
    assert Attachment.objects.count() == total_docs

    CreateInstanceLogic.copy_attachments(source_instance, target_instance, **args)

    assert Attachment.objects.count() == total_docs + expected_copies

    new_attachment = Attachment.objects.last()

    assert new_attachment.instance_id == target_instance.pk

    old_attachment = [d for d in docs if d.name == new_attachment.name][0]

    assert new_attachment.name == old_attachment.name
    assert new_attachment.attachment_id != old_attachment.attachment_id


@pytest.mark.parametrize(
    "application_short_name,caluma_workflow_config,args,expected_copies",
    [
        # default/SO with alexandria attachments
        (
            "so",
            lf("caluma_workflow_config_so"),
            {"skip_exported_form_attachment": False, "is_modification": False},
            3,
        ),
        (
            "so",
            lf("caluma_workflow_config_so"),
            {"skip_exported_form_attachment": True, "is_modification": False},
            2,
        ),
        # GR with alexandria and no copy for modifications
        (
            "gr",
            lf("caluma_workflow_config_gr"),
            {"skip_exported_form_attachment": True, "is_modification": False},
            2,
        ),
        (
            "gr",
            lf("caluma_workflow_config_gr"),
            {"skip_exported_form_attachment": False, "is_modification": True},
            0,
        ),
    ],
)
@pytest.mark.django_db
def test_copy_attachments_alexandria(
    instance_factory,
    application_settings,
    instance_with_case,
    caluma_workflow_config,
    application_short_name,
    args,
    expected_copies,
):
    application_settings["SHORT_NAME"] = application_short_name
    application_settings["DOCUMENT_BACKEND"] = "alexandria"

    source_instance = instance_with_case(instance_factory())
    target_instance = instance_with_case(instance_factory())
    category = CategoryFactory(slug="beilagen-zum-gesuch")
    docs = [
        DocumentFactory(
            title="important-doc",
            metainfo={
                "camac-instance-id": str(source_instance.pk),
                "caluma-document-id": str(source_instance.case.document.pk),
            },
            category=category,
        ),
        DocumentFactory(
            title="some-doc",
            metainfo={
                "camac-instance-id": str(source_instance.pk),
                "caluma-document-id": str(source_instance.case.document.pk),
            },
            category=CategoryFactory(parent=category),
        ),
        DocumentFactory(
            title="baugesuch",
            metainfo={
                "camac-instance-id": str(source_instance.pk),
                "system-generated": True,
            },
            category=category,
        ),
        DocumentFactory(
            title="other-doc",
            metainfo={
                "camac-instance-id": str(source_instance.pk),
            },
        ),
    ]
    files = [FileFactory(document=doc) for doc in docs]

    total_docs = len(docs)
    assert Document.objects.count() == total_docs
    assert File.objects.filter(variant=File.Variant.ORIGINAL).count() == total_docs

    CreateInstanceLogic.copy_attachments(
        source_instance,
        target_instance,
        **args,
    )

    assert Document.objects.count() == total_docs + expected_copies
    assert (
        File.objects.filter(variant=File.Variant.ORIGINAL).count()
        == total_docs + expected_copies
    )

    if expected_copies > 0:
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


@pytest.mark.django_db
def test_copy_applicants(
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
@pytest.mark.django_db
def test_instance_generate_identifier_so(
    so_instance,
    caluma_case_factory,
    service,
    existing_dossier_numbers,
    expected_dossier_number,
    application_settings,
):
    application_settings["SHORT_NAME"] = "so"

    if existing_dossier_numbers:
        for nr in existing_dossier_numbers:
            caluma_case_factory(meta={"dossier-number": nr})

    assert (
        CreateInstanceLogic.generate_identifier(so_instance) == expected_dossier_number
    )


@pytest.mark.django_db
def test_instance_generate_identifier_so_exceptions(
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


@pytest.mark.parametrize(
    "has_source,was_rejected,expected_count,expected_type",
    [
        (False, False, 0, None),
        (False, True, 0, None),
        (True, False, 1, FormTimeline.Type.PROJECT_CHANGE.value),
        (True, True, 1, FormTimeline.Type.SUBMIT_AFTER_REJECTION.value),
    ],
)
@pytest.mark.django_db
def test_instance_create_source_timeline(
    caluma_case_factory,
    instance_factory,
    instance_state_factory,
    gr_instance,
    has_source,
    was_rejected,
    expected_count,
    expected_type,
    timelines_settings,
    rejection_settings,
    set_application_gr,
):
    timelines_settings.enabled = True
    assert FormTimeline.objects.count() == 0
    source_instance = (
        instance_factory(case=caluma_case_factory()) if has_source else None
    )
    if was_rejected and source_instance:
        source_instance.instance_state = instance_state_factory(
            name=rejection_settings["INSTANCE_STATE"]
        )
        source_instance.save()

    CreateInstanceLogic.initialize_camac(
        gr_instance,
        source_instance=source_instance,
        is_modification=not was_rejected,
        is_paper=False,
        extend_validity_for=None,
        case=None,
        user=None,
        group=None,
        skip_exported_form_attachment=False,
        copy_attachments_from=[],
    )
    assert FormTimeline.objects.count() == expected_count
    if expected_count > 0:
        timeline = FormTimeline.objects.first()
        assert timeline.instance_id == gr_instance.pk
        assert timeline.timeline_type == expected_type
