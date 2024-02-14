import pytest


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


@pytest.mark.parametrize(
    "model,expected",
    [
        (pytest.lazy_fixture("file_attachment"), "myfile.txt"),
        (pytest.lazy_fixture("document_attachment"), "myotherfile.pdf"),
    ],
)
def test_attachment_filename(db, model, expected):
    assert model.filename == expected


@pytest.mark.parametrize(
    "model,has_display_name,expected",
    [
        (pytest.lazy_fixture("file_attachment"), None, "myfile.txt"),
        (pytest.lazy_fixture("document_attachment"), True, "My Attachment"),
        (pytest.lazy_fixture("document_attachment"), False, "myotherfile.pdf"),
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
        (pytest.lazy_fixture("file_attachment"), None, False),
        (pytest.lazy_fixture("document_attachment"), True, True),
        (pytest.lazy_fixture("document_attachment"), False, False),
    ],
)
def test_attachment_is_replaced(db, model, has_is_replaced, expected, attachment):
    if has_is_replaced is False:
        del attachment.context["isReplaced"]
        attachment.save()

    assert model.is_replaced == expected


@pytest.mark.parametrize(
    "model,expected",
    [
        (pytest.lazy_fixture("file_attachment"), "text/plain"),
        (pytest.lazy_fixture("document_attachment"), "application/pdf"),
    ],
)
def test_attachment_content_type(db, model, expected):
    assert model.content_type == expected
