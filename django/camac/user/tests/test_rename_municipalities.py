from django.core.management import call_command


def test_rename_municipalities(db, group_t_factory, service_t_factory):
    groupt = group_t_factory(name="Leitung Leitbehörde Solothurn")
    servicet = service_t_factory(name="Leitbehörde Solothurn")

    call_command("rename_municipalities")

    groupt.refresh_from_db()
    servicet.refresh_from_db()

    assert groupt.name == "Leitung Gemeinde Solothurn"
    assert servicet.name == "Gemeinde Solothurn"

    call_command("rename_municipalities", before="Gemeinde", after="Test")

    groupt.refresh_from_db()
    servicet.refresh_from_db()

    assert groupt.name == "Leitung Test Solothurn"
    assert servicet.name == "Test Solothurn"
