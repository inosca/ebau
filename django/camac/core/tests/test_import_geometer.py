import pyexcel
from django.core.management import call_command

from camac.user.models import ServiceRelation


def test_import_geometer(db, service_factory, service_group_factory, tmpdir, capsys):
    # load data including test data
    some_municipality = service_factory(
        trans__name="Leitbehörde Testiswil",
        service_group__trans__name="Leitbehörde Gemeinde",
        service_group__trans__language="de",
    )

    service_group_factory(name="Nachführungsgeometer")

    import_header = [
        "bfs",
        "Gemeinde",
        "Name eBAU",
        "Nachführungsgeometer de/fr",
        "Geometer",
        "FirmaName",
        "FirmaStrasse",
        "FirmaPlzOrt",
        "FirmaTelefon",
        "FirmaTelefonLink",
        "FirmaFax",
        "FirmaFaxLink",
        "FirmaEmail",
    ]
    import_line = [
        "841",
        "Testiswil",
        "Nachführungsgeometer Peter Tester",
        "Nachführungsgeometer",
        "Peter Tester",
        "Testhans Vermessungen",
        "Rüeblistrasse 5",
        "1234 Testiswil",
        "+41 33 111 22 33",
        "",
        "+41 33 111 22 33",
        "",
        "info@example.ch",
    ]
    fail_import_line = [
        "999",
        "Fehlersberg",
        "Nachführungsgeometer Anderer Tester",
        "Nachführungsgeometer",
        "Anderer Tester",
        "Andere Vermessungen",
        "Kabisgasse 99",
        "1234 Testiswil",
        "+41 33 111 22 33",
        "",
        "+41 33 111 22 33",
        "",
        "info@example.ch",
    ]

    filename = str(tmpdir / "test.xlsx")

    pyexcel.save_as(
        array=[import_header, import_line, fail_import_line], dest_file_name=filename
    )

    call_command("import_geometer", filename)

    out, err = capsys.readouterr()

    expected_lines = [
        "Leitbehörde found for Testiswil, updating/creating Geometer service",
        "Could not find municipality Fehlersberg, skipping Geometer import",
    ]
    assert expected_lines == out.strip().splitlines()

    qs = ServiceRelation.objects.filter(receiver=some_municipality, function="geometer")
    assert qs.exists()
    assert qs.get().provider.get_name() == "Nachführungsgeometer Peter Tester"
