from django.core.management import call_command


def test_fix_duplicate_identifiers(
    db,
    service,
    instance_factory,
    caluma_case_factory,
    mocker,
    set_application_gr,
):
    mocker.patch(
        "camac.instance.models.Instance.responsible_service", return_value=service
    )
    cases = [
        caluma_case_factory(
            meta={"submit-date": "2019-03-28T09:40:00.000Z", "dossier-number": "2024-1"}
        ),
        caluma_case_factory(
            meta={"submit-date": "2019-03-28T09:43:00.000Z", "dossier-number": "2024-1"}
        ),
        caluma_case_factory(
            meta={"submit-date": "2019-03-28T09:41:00.000Z", "dossier-number": "2024-1"}
        ),
        caluma_case_factory(
            meta={"submit-date": "2019-03-28T09:42:00.000Z", "dossier-number": "2025-1"}
        ),
        caluma_case_factory(
            meta={"submit-date": "2019-03-28T09:42:01.000Z", "dossier-number": "2025-1"}
        ),
    ]
    for case in cases:
        instance = instance_factory()
        instance.case = case
        instance.save()
    call_command("fix_duplicate_identifiers", "--add-history", "--add-keyword")

    for case in cases:
        case.refresh_from_db()

    # check changed dossier numbers, ordered by submit date,
    # new number should preserve original dossier year prefix.
    assert cases[0].meta["dossier-number"] == "2024-1"
    assert cases[1].meta["dossier-number"] == "2024-3"
    assert cases[2].meta["dossier-number"] == "2024-2"
    assert cases[3].meta["dossier-number"] == "2025-1"
    assert cases[4].meta["dossier-number"] == "2025-2"

    # check created history entries.
    assert cases[0].instance.history.count() == 0
    assert (
        cases[1]
        .instance.history.filter(
            trans__language="de",
            trans__title="Die Dossiernummer wurde von 2024-1 auf 2024-3 geändert.",
        )
        .exists()
    )
    assert (
        cases[2]
        .instance.history.filter(
            trans__language="de",
            trans__title="Die Dossiernummer wurde von 2024-1 auf 2024-2 geändert.",
        )
        .exists()
    )
    assert cases[3].instance.history.count() == 0
    assert (
        cases[4]
        .instance.history.filter(
            trans__language="de",
            trans__title="Die Dossiernummer wurde von 2025-1 auf 2025-2 geändert.",
        )
        .exists()
    )

    # check created keywords.
    assert not cases[0].instance.keywords.filter(name="2024-1").exists()
    assert cases[1].instance.keywords.filter(name="2024-1").exists()
    assert cases[2].instance.keywords.filter(name="2024-1").exists()
    assert not cases[3].instance.keywords.filter(name="2025-1").exists()
    assert cases[4].instance.keywords.filter(name="2025-1").exists()
