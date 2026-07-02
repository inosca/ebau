import json

import pytest
from django.core.management import call_command

from camac.document.tests.data import django_file


@pytest.mark.django_db
def test_template_download(template_factory, capsys, snapshot):
    template_factory(path=django_file("template.docx"))

    call_command("legacy_templates", "extract_used_placeholders")

    assert capsys.readouterr().out == snapshot


@pytest.mark.django_db(transaction=True, reset_sequences=True)
def test_template_export(template_factory, tmp_path, settings, capsys, snapshot):
    settings.APPLICATION_DIR = tmp_path

    out_file = tmp_path / "legacy_templates" / "test_dms_templates_fixture.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)

    template_factory(path=django_file("template.docx"))

    call_command(
        "legacy_templates", "export_templates", f"--out_file={out_file.as_posix()}"
    )

    assert capsys.readouterr().err == ""

    assert json.load(out_file.open("r"))[0] == snapshot


@pytest.mark.django_db
def test_remove_dangling(template_factory, settings):
    tmpl1 = template_factory()
    tmpl2 = template_factory()
    tmpl2.delete()
    templates_dir = settings.MEDIA_ROOT / "templates"
    len(templates_dir.listdir()) == 2
    call_command("legacy_templates", "remove_dangling", "--run")
    assert len(templates_dir.listdir()) == 1
    assert (settings.MEDIA_ROOT / tmpl1.path.name).exists()
