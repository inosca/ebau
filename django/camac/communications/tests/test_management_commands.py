import pytest
from alexandria.core.factories import FileFactory
from django.core.management import call_command

from camac.document.tests.data import django_file


@pytest.mark.parametrize("backend", ["camac-ng", "alexandria"])
def test_convert_communication_attachment_links_to_files(
    db,
    application_settings,
    backend,
    communications_attachment_factory,
    attachment_factory,
):
    application_settings["DOCUMENT_BACKEND"] = backend

    if backend == "camac-ng":
        attachment = communications_attachment_factory(
            file_attachment="",
            document_attachment=attachment_factory(
                path=django_file("multiple-pages.pdf"),
                context={"displayName": "Doc"},
                name="file.pdf",
            ),
        )
        attachment2 = communications_attachment_factory(
            file_attachment="",
            document_attachment=attachment_factory(
                path=django_file("multiple-pages.pdf"),
                context={"displayName": "Doc2.pdf"},
                name="Foo",
            ),
        )
    else:
        attachment = communications_attachment_factory(
            file_attachment="",
            alexandria_file=FileFactory(document__title="Doc", name="file.pdf"),
        )
        attachment2 = communications_attachment_factory(
            file_attachment="",
            alexandria_file=FileFactory(document__title="Doc2.pdf", name="file.pdf"),
        )

    call_command("convert_communication_attachment_links_to_files")

    attachment.refresh_from_db()
    assert attachment.file_attachment.name.endswith("Doc.pdf")
    assert attachment.file_attachment.read()
    attachment2.refresh_from_db()
    assert attachment2.file_attachment.name.endswith("Doc2.pdf")


def test_convert_communication_attachment_links_to_files_error(
    db,
    application_settings,
    communications_attachment_factory,
    attachment_factory,
    capsys,
):
    attachment = communications_attachment_factory(
        file_attachment="",
        document_attachment=attachment_factory(
            context={"displayName": "Doc"}, path="non_existent_file.pdf"
        ),
    )

    call_command("convert_communication_attachment_links_to_files")
    captured = capsys.readouterr()
    assert f"Error processing attachment {attachment.pk}" in captured.err
