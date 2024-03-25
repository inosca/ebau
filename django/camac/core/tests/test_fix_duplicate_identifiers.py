from django.core.management import call_command


def test_fix_duplicate_identifiers(
    db,
    instance_with_case,
    instance_factory,
    case_factory,
    set_application_gr,
):
    cases = [
        case_factory(
            meta={"submit-date": "2019-03-28T09:40:00.000Z", "dossier-number": "2024-1"}
        ),
        case_factory(
            meta={"submit-date": "2019-03-28T09:43:00.000Z", "dossier-number": "2024-1"}
        ),
        case_factory(
            meta={"submit-date": "2019-03-28T09:41:00.000Z", "dossier-number": "2024-1"}
        ),
        case_factory(
            meta={"submit-date": "2019-03-28T09:42:00.000Z", "dossier-number": "2024-2"}
        ),
    ]
    for case in cases:
        instance = instance_factory()
        instance.case = case
        instance.save()
    call_command("fix_duplicate_identifiers")

    for case in cases:
        case.refresh_from_db()
    assert cases[0].meta["dossier-number"] == "2024-1"
    assert cases[1].meta["dossier-number"] == "2024-4"
    assert cases[2].meta["dossier-number"] == "2024-3"
    assert cases[3].meta["dossier-number"] == "2024-2"
