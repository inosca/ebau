import magic
import pytest

from camac.document.tests.data import django_file

TEST_FILES = {
    "/app/camac/document/tests/data/libreoffice-template-after-dms.docx": (
        "Microsoft Word 2007+",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ),
    "/app/camac/dossier_import/tests/data/import-example-orphan-dirs.zip": (
        "Zip archive data",
        "application/zip",
    ),
}


@pytest.mark.parametrize("file_name", TEST_FILES.keys())
def test_magic_types_buffer(file_name):
    human_type, expected_mime_type = TEST_FILES[file_name]

    file = django_file(file_name).read()

    assert magic.from_buffer(file).startswith(human_type)
    assert magic.from_buffer(file, mime=True) == expected_mime_type


@pytest.mark.parametrize("file_name", TEST_FILES.keys())
def test_magic_types_file(file_name):
    human_type, expected_mime_type = TEST_FILES[file_name]

    assert magic.from_file(file_name, mime=True) == expected_mime_type
    assert magic.from_file(file_name).startswith(human_type)
