import pytest
from alexandria.core.factories import FileFactory, MarkFactory
from pytest_lazy_fixtures import lf


@pytest.fixture
def file_attachment(db, communications_attachment):
    communications_attachment.file_attachment.name = "myfile.txt"
    communications_attachment.file_type = "text/plain"
    communications_attachment.document_attachment = None
    communications_attachment.save()

    return communications_attachment


@pytest.fixture
def document_attachment(db, file_attachment, attachment):
    attachment.name = "myotherfile.pdf"
    attachment.context = {"displayName": "My Attachment", "isReplaced": True}
    attachment.mime_type = "application/pdf"
    attachment.save()

    file_attachment.file_attachment = None
    file_attachment.document_attachment = attachment
    file_attachment.save()

    return file_attachment


@pytest.fixture
def alexandria_file(db):
    file = FileFactory(
        name="mydocument.docx",
        document__title="My Document",
        mime_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

    file.document.marks.add(MarkFactory(pk="void"))

    return file


@pytest.fixture
def alexandria_attachment(
    alexandria_file,
    application_settings,
    file_attachment,
    use_alexandria_backend,
):
    file_attachment.file_attachment = None
    file_attachment.alexandria_file = alexandria_file
    file_attachment.save()

    return file_attachment


@pytest.mark.parametrize(
    "model,expected",
    [
        (lf("file_attachment"), "myfile.txt"),
        (lf("document_attachment"), "myotherfile.pdf"),
        (lf("alexandria_attachment"), "mydocument.docx"),
    ],
)
def test_attachment_filename(db, model, expected):
    assert model.filename == expected


@pytest.mark.parametrize(
    "model,has_display_name,expected",
    [
        (lf("file_attachment"), None, "myfile.txt"),
        (lf("document_attachment"), True, "My Attachment"),
        (lf("document_attachment"), False, "myotherfile.pdf"),
        (lf("alexandria_attachment"), None, "My Document"),
    ],
)
def test_attachment_display_name(db, model, has_display_name, expected, attachment):
    if has_display_name is False:
        del attachment.context["displayName"]
        attachment.save()

    assert model.display_name == expected


@pytest.mark.parametrize(
    "model,has_is_replaced,expected",
    [
        (lf("file_attachment"), None, False),
        (lf("document_attachment"), True, True),
        (lf("document_attachment"), False, False),
        (lf("alexandria_attachment"), True, True),
        (lf("alexandria_attachment"), False, False),
    ],
)
def test_attachment_is_replaced(
    alexandria_file,
    attachment,
    expected,
    has_is_replaced,
    model,
):
    if has_is_replaced is False:
        if model.document_attachment is not None:
            del attachment.context["isReplaced"]
            attachment.save()
        elif model.alexandria_file is not None:
            alexandria_file.document.marks.clear()

    assert model.is_replaced == expected


@pytest.mark.parametrize(
    "model,expected",
    [
        (lf("file_attachment"), "text/plain"),
        (lf("document_attachment"), "application/pdf"),
        (
            lf("alexandria_attachment"),
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ),
    ],
)
def test_attachment_content_type(db, model, expected):
    assert model.content_type == expected
