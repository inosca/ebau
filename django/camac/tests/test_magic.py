import magic

from camac.document.tests.data import django_file


def test_magic_libreoffice_template_after_dms():
    file = django_file("libreoffice-template-after-dms.docx").read()

    assert magic.from_buffer(file) == "Microsoft Word 2007+"
    assert (
        magic.from_buffer(file, mime=True)
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
