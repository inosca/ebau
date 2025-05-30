import pytest
from alexandria.core.factories import FileFactory
from django.core.management import call_command


@pytest.mark.parametrize("backend", ["camac-ng", "alexandria"])
def test_fix_communication_attachment_files(
    db,
    application_settings,
    backend,
    communications_attachment_factory,
    attachment,
):
    application_settings["DOCUMENT_BACKEND"] = backend

    if backend == "camac-ng":
        attachment = communications_attachment_factory(
            file_attachment="", document_attachment=attachment
        )
    else:
        attachment = communications_attachment_factory(
            file_attachment="", alexandria_file=FileFactory()
        )

    call_command("convert_communication_attachment_links_to_files")

    attachment.refresh_from_db()
    assert attachment.file_attachment != ""
