import pytest
from alexandria.core.factories import DocumentFactory, FileFactory
from alexandria.core.models import Document, File

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
    minio_mock,
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
    assert File.objects.count() == 2

    CreateInstanceLogic.copy_attachments(
        source_instance, target_instance, skip_exported_form_attachment
    )

    assert Document.objects.count() == 2 + expected_copies
    assert File.objects.count() == 2 + expected_copies

    new_document = (
        Document.objects.filter(title=docs[0].title).order_by("-created_at").first()
    )
    new_file = new_document.files.first()
    old_file = files[0]

    assert new_document.metainfo["camac-instance-id"] == str(target_instance.pk)
    assert new_document.instance_document.instance_id == target_instance.pk
    assert new_document.metainfo["caluma-document-id"] == str(
        target_instance.case.document.pk
    )

    assert new_file.name == old_file.name
    assert new_file.id != old_file.id
