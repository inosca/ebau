import json
from datetime import date

import pytest
from caluma.caluma_workflow.models import WorkItem

from camac.tests.data import so_personal_row_factory


def _parzellen_rows(count):
    return [
        {
            "parzellennummer": f"{1234 + index}",
            "e-grid": f"CH80730661346{index}",
            "lagekoordinaten-ost": 2607000.5 + index,
            "lagekoordinaten-nord": 1228500.5 + index,
        }
        for index in range(count)
    ]


def _gebaeude_rows(count):
    return [
        {
            "gebaeude-bezeichnung": f"Bauwerk {index}",
            "typ-des-bauwerks": {
                "value": "typ-des-bauwerks-parkhaus",
                "options": [("typ-des-bauwerks-parkhaus", "Parkhaus")],
            },
            "art-der-arbeiten": {
                "value": ["art-der-arbeiten-neubau", "art-der-arbeiten-umbau"],
                "options": [
                    ("art-der-arbeiten-neubau", "Neubau"),
                    ("art-der-arbeiten-umbau", "Umbau"),
                ],
            },
            "gebaeudekategorie": {
                "value": "gebaeudekategorie-ohne-wohnnutzung",
                "options": [
                    ("gebaeudekategorie-ohne-wohnnutzung", "Gebäude ohne Wohnnutzung"),
                ],
            },
            "egid": 1234 + index,
        }
        for index in range(count)
    ]


@pytest.fixture
def setup_so_instance(  # noqa: C901
    form_utils,
    instance_state_t_factory,
    caluma_workflow_config_so,
    caluma_work_item_factory,
    service_factory,
    responsible_service_factory,
    instance_acl_factory,
    access_level_factory,
):
    """Populate an SO dossier so the GIS export picks it up."""
    submitted = instance_state_t_factory(
        instance_state__name="subm", name="Submitted"
    ).instance_state
    distribution_services = [service_factory(slug=slug) for slug in ("afu", "arp")]
    # Two responsible municipal services (sharing one municipality group): an
    # instance can have more than one, so the Zustaendige_Person `[:1]` pick
    # must be deterministic.
    first_responsible = service_factory(service_group__slug="municipality")
    responsible_services = [
        first_responsible,
        service_factory(service_group=first_responsible.service_group),
    ]
    distribution_service = access_level_factory(slug="distribution-service")

    def setup(
        instance, dossier_number, *, full=False, parcels=2, buildings=2, gis_karte=None
    ):
        document = instance.case.document

        instance.instance_state = submitted
        instance.case.meta.update({"dossier-number": dossier_number})
        instance.case.save()
        instance.save()

        form_utils.add_answer(document, "gemeindenummer-bfs", 2601)

        if gis_karte is not None:
            # A str goes in verbatim so tests can produce an unreadable answer.
            form_utils.add_answer(
                document,
                "gis-karte",
                gis_karte if isinstance(gis_karte, str) else json.dumps(gis_karte),
            )

        form_utils.add_table_answer(document, "parzellen", _parzellen_rows(parcels))
        # Bauherrschaft is a BAG {1..*}: a second applicant (without a
        # representation) exercises the repeating Gesuchsteller mapping.
        form_utils.add_table_answer(
            document,
            "bauherrin",
            [
                so_personal_row_factory(has_representation=True),
                so_personal_row_factory(),
            ],
        )
        # Required (and thus present) in every SO dossier form, so even a minimal
        # dossier produces a Bauprojekt with a Beschreibung.
        form_utils.add_answer(
            document, "umschreibung-bauprojekt", "Neubau Mehrfamilienhaus"
        )

        if full:
            _setup_full(instance, document, buildings=buildings)

        return instance

    def _setup_full(instance, document, *, buildings=2):
        instance.case.meta.update({"is-bab": True})
        instance.case.save()

        # The gebaeude form is only rendered when Hochbaute is chosen.
        # A Tiefbaute-only project therefore has a Bauprojekt but zero gebaeude.
        bauwerk_arten = [("art-der-bauwerke-tiefbaute", "Tiefbaute")]
        if buildings:
            bauwerk_arten.insert(0, ("art-der-bauwerke-hochbaute", "Hochbaute"))
        form_utils.add_answer(
            document,
            "art-der-bauwerke",
            [slug for slug, _label in bauwerk_arten],
            options=bauwerk_arten,
            question_type="multiple_choice",
        )
        form_utils.add_answer(
            document,
            "nutzungszwecke",
            ["nutzungszwecke-wohnen", "nutzungszwecke-arbeiten"],
            options=[
                ("nutzungszwecke-wohnen", "Wohnen"),
                ("nutzungszwecke-arbeiten", "Arbeiten"),
            ],
            question_type="multiple_choice",
        )

        for table in (
            "projektverfasserin",
            "rechnungsempfaengerin",
            "grundeigentuemerin",
        ):
            form_utils.add_answer(
                document,
                f"{table}-abweichend",
                f"{table}-abweichend-ja",
                options=[f"{table}-abweichend-nein", f"{table}-abweichend-ja"],
                question_type="choice",
            )
            # One table holds juristic persons so the `juristische-person-ja`
            # branch of the annotation is exercised; the others stay natural.
            is_juristic = table == "grundeigentuemerin"
            form_utils.add_table_answer(
                document,
                table,
                [
                    so_personal_row_factory(is_juristic=is_juristic),
                    so_personal_row_factory(is_juristic=is_juristic),
                ],
            )

        if buildings:
            form_utils.add_table_answer(document, "gebaeude", _gebaeude_rows(buildings))

        # Lokalisation
        for question, value in (
            ("strasse-flurname", "Baustellenweg"),
            ("strasse-nummer", "12"),
            ("plz", "4500"),
            ("ort", "Solothurn"),
        ):
            form_utils.add_answer(document, question, value)

        _setup_work_items(instance)

    def _setup_work_items(instance):
        decision = caluma_work_item_factory(
            task_id="decision", case=instance.case, status=WorkItem.STATUS_COMPLETED
        )
        form_utils.add_answer(
            decision.document,
            "entscheid-entscheid",
            "entscheid-entscheid-zustimmung",
            options=[("entscheid-entscheid-zustimmung", "Zustimmung")],
        )
        form_utils.add_answer(decision.document, "entscheid-datum", date(2026, 5, 1))

        # A dossier can have several publications; the export takes one, so the
        # `[:1]` pick must be deterministic.
        for start, end in (
            (date(2026, 5, 1), date(2026, 5, 31)),
            (date(2026, 6, 1), date(2026, 6, 30)),
        ):
            publication = caluma_work_item_factory(
                task_id="fill-publication",
                case=instance.case,
                status=WorkItem.STATUS_COMPLETED,
            )
            form_utils.add_answer(publication.document, "publikation-start", start)
            form_utils.add_answer(publication.document, "publikation-ende", end)

        # D: services with a distribution-service ACL on the instance
        for service in distribution_services:
            instance_acl_factory(
                instance=instance,
                grant_type="SERVICE",
                service=service,
                access_level=distribution_service,
            )

        # Zustaendige_Personen
        for service in responsible_services:
            responsible_service_factory(instance=instance, service=service)

    return setup


@pytest.fixture
def sogis_client(admin_client, admin_user, so_gis_export_settings):
    admin_client.force_authenticate(
        user=admin_user, token={"azp": so_gis_export_settings.keycloak_client}
    )

    return admin_client
