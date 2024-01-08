import pyexcel
import pytest
from django.core.management import call_command

from camac.user.models import ServiceRelation


@pytest.mark.parametrize("do_clear_relations", [True, False])
@pytest.mark.parametrize("do_clear_geometers", [True, False])
def test_import_geometer(
    db,
    service_factory,
    service_group_factory,
    tmpdir,
    capsys,
    role_factory,
    do_clear_relations,
    do_clear_geometers,
    application_settings,
):
    # for logging/printing to use the right values.
    application_settings["IS_MULTILINGUAL"] = True

    # load data including test data
    some_municipality = service_factory(
        trans__name="Leitbehörde Testiswil",
        service_group__trans__name="Leitbehörde Gemeinde",
        service_group__trans__language="de",
    )

    role_l = role_factory(
        name="geometer-lead",
        trans__name="Leitung Nachführungsgeometer",
    )
    role_e = role_factory(
        name="geometer-readonly",
        trans__name="Einsichtsberechtigte Nachführungsgeometer",
    )
    role_a = role_factory(
        name="geometer-admin",
        trans__name="Administration Nachführungsgeometer",
    )
    role_s = role_factory(
        name="geometer-clerk",
        trans__name="Sachbearbeiter Nachführungsgeometer",
    )

    geometer_sg = service_group_factory(name="geometer")
    old_rel = ServiceRelation.objects.create(
        function="geometer",
        receiver=service_factory(),
        provider=service_factory(service_group=geometer_sg),
    )

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
        841,
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
        999,
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

    args = [filename]
    if do_clear_relations:
        args.append("--clear-relations")
    if do_clear_geometers:
        args.append("--clear-geometers")

    call_command("import_geometer", *args)

    # If we clear all relations, the "old" one should be gone, otherwise
    # we should have kept it. Note if we clear the geometers, the relations
    # will be dropped implicitly as well
    assert ServiceRelation.objects.filter(pk=old_rel.pk).exists() != (
        do_clear_relations or do_clear_geometers
    )

    out, err = capsys.readouterr()

    expect_success = (
        "Leitbehörde 'Leitbehörde Testiswil' found for 'Testiswil', assigning "
        "Geometer service: Nachführungsgeometer Peter Tester"
    )
    expect_fail = (
        "Municipality service for 'Fehlersberg' not found. Service "
        "'Nachführungsgeometer Anderer Tester' created but not assigned"
    )

    assert out.strip().splitlines() == [expect_success, expect_fail]

    qs = ServiceRelation.objects.filter(receiver=some_municipality, function="geometer")
    relation = qs.get()
    assert relation.provider.get_name() == "Nachführungsgeometer Peter Tester"

    # Groups required
    # Leitung Geometer, Einsichtberechtigte Geometer, Sachbearbeiter Geometer, Administration Geometer
    assert relation.provider.groups.count() == 4
    assert relation.provider.groups.filter(role=role_l).count() == 1
    assert relation.provider.groups.filter(role=role_e).count() == 1
    assert relation.provider.groups.filter(role=role_a).count() == 1
    assert relation.provider.groups.filter(role=role_s).count() == 1
