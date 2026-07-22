import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from camac.gis_export.models import SOGISExport


@pytest.mark.django_db
def test_sogis_export_mark_exported_requires_commit():
    with pytest.raises(CommandError, match="--mark-exported requires --commit"):
        call_command("sogis_export", "--mark-exported")


@pytest.mark.django_db
def test_sogis_export_writes_the_xtf(
    instance_factory, instance_with_case, setup_so_instance, tmp_path, capsys
):
    setup_so_instance(instance_with_case(instance_factory()), "2601-2026-1", full=True)
    output = tmp_path / "export.xtf"

    call_command("sogis_export", "--output", str(output))

    # The XML itself is asserted where it is built, not here.
    assert output.read_text().startswith("<?xml")
    assert "1 exportable, 0 invalid" in capsys.readouterr().err


@pytest.mark.django_db
def test_sogis_export_reports_invalid_dossiers(
    instance_factory, instance_with_case, setup_so_instance, capsys
):
    instance = setup_so_instance(instance_with_case(instance_factory()), "2601-2026-1")
    # Without the applicant the dossier cannot be exported.
    instance.case.document.answers.filter(question_id="bauherrin").delete()

    call_command("sogis_export", "--validate-only")

    assert "0 exportable, 1 invalid" in capsys.readouterr().err


@pytest.mark.django_db
def test_sogis_export_does_not_touch_the_db_without_commit(
    instance_factory, instance_with_case, setup_so_instance
):
    setup_so_instance(instance_with_case(instance_factory()), "2601-2026-1", full=True)

    call_command("sogis_export", "--validate-only")

    assert not SOGISExport.objects.exists()


@pytest.mark.django_db
def test_sogis_export_commits_and_marks_exported(
    instance_factory, instance_with_case, setup_so_instance
):
    setup_so_instance(instance_with_case(instance_factory()), "2601-2026-1", full=True)

    call_command("sogis_export", "--commit", "--mark-exported")

    assert SOGISExport.objects.get().exported_at is not None
    assert not SOGISExport.objects.pending().exists()
