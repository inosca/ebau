from django.core.management import call_command

from camac.document.tests.data import django_file


def test_template_download(db, template_factory, capsys, snapshot):
    template_factory(path=django_file("template.docx"))

    call_command("legacy_templates", "extract_used_placeholders")

    assert capsys.readouterr().out == snapshot
