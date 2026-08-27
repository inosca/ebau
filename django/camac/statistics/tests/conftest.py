import datetime

import pytest
from caluma.caluma_workflow.models import WorkItem
from django.utils.timezone import make_aware

from camac.deadlines.factories import DeadlineTypeFactory, InstanceDeadlineFactory
from camac.statistics.filters import get_inquiry_service_id
from camac.tests.form_utils import FormUtils
from camac.user.factories import ServiceFactory, ServiceGroupFactory


@pytest.fixture(autouse=True)
def _clear_inquiry_service_cache():
    """Reset the lru_cache between tests."""
    get_inquiry_service_id.cache_clear()
    yield
    get_inquiry_service_id.cache_clear()


@pytest.fixture
def role(role):
    """Ensure role has a slug matching its name lowercase."""
    if not role.slug:
        role.slug = role.name.lower()
        role.save()
    return role


@pytest.fixture(autouse=True)
def municipality_service_group(db, group, role):
    """Ensure municipality groups have a service_group slug matching the config."""
    if role.name == "Municipality" and group.service and group.service.service_group:
        sg = group.service.service_group
        if not sg.slug:
            sg.slug = "municipality"
            sg.save()


@pytest.fixture
def statistics_ag_instance(
    db,
    ag_distribution_settings,
    ag_decision_settings,
    ag_statistics_settings,
    ag_master_data_case,
    caluma_document_factory,
    caluma_work_item_factory,
    instance_state_t_factory,
    multilang,
    responsible_service_factory,
    service,
    settings,
    form_utils: FormUtils,
    active_inquiry_factory,
    admin_client,
    mocker,
):
    """Fully set-up AG instance for statistics export tests.

    Provides an instance with:
    - dossier-number, submit-date, parcels, municipality (from ag_master_data_case)
    - instance state "In Zirkulation"
    - responsible user is admin_client user on the current service
    - a completed decision work item with answer + date
    - a completed inquiry with known timestamps
    - an InstanceDeadline with deterministic processing-time / on-time values
    """
    instance = ag_master_data_case.instance

    # Instance state
    instance.instance_state = instance_state_t_factory(
        name="In Zirkulation",
    ).instance_state
    instance.save()

    # Responsible user
    responsible_service_factory(
        responsible_user=admin_client.user,
        service=service,
        instance=instance,
    )

    # Decision work item with answer
    decision_work_item = caluma_work_item_factory(
        case=instance.case,
        task_id="decision",
        status=WorkItem.STATUS_COMPLETED,
        document=caluma_document_factory(form_id="entscheid"),
    )
    form_utils.add_answer(
        decision_work_item.document,
        "entscheid-entscheid",
        ag_decision_settings["ANSWERS"]["DECISION"]["APPROVED"],
    )
    form_utils.add_answer(
        decision_work_item.document,
        "entscheid-datum",
        datetime.date(2025, 5, 8),
    )

    # Inquiry
    active_inquiry_factory(
        for_instance=instance,
        addressed_service=service,
        status=WorkItem.STATUS_COMPLETED,
        created_at=make_aware(datetime.datetime(2025, 1, 1)),
        closed_at=make_aware(datetime.datetime(2025, 1, 30)),
        deadline=make_aware(datetime.datetime(2012, 2, 22)),
    )

    # InstanceDeadline — deterministic values for "Durchlaufzeit" / "Fristgerecht"
    # Prevent side-effect recalculation during factory creation
    mocker.patch(
        "camac.deadlines.models.InstanceDeadline.trigger_side_effect",
    )
    deadline_type = DeadlineTypeFactory(
        lead_time=30,
        exclude_weekends=False,
        exclude_public_holidays=False,
    )
    InstanceDeadlineFactory(
        instance=instance,
        service=service,
        deadline_type=deadline_type,
        start_date=datetime.date(2025, 1, 1),
        target_deadline_date=datetime.date(2025, 1, 31),
        process_deadline_date=datetime.date(2025, 1, 20),  # completed before target
        process_deadline_days=16,
    )

    return instance


@pytest.fixture
def statistics_ag_instance_by_role(statistics_ag_instance, ag_statistics_settings):
    """AG instance that resolves columns via by_role instead of by_service_group."""
    municipality_config = ag_statistics_settings.by_service_group.pop("municipality")
    ag_statistics_settings.by_role["municipality"] = municipality_config
    yield statistics_ag_instance
    ag_statistics_settings.by_service_group["municipality"] = municipality_config
    del ag_statistics_settings.by_role["municipality"]


@pytest.fixture
def statistics_ag_instance_afb(
    statistics_ag_instance,
    group,
    service,
):
    """AG instance for service-afb statistics export with deadline columns."""

    service_group = ServiceGroupFactory(slug="service-afb")
    afb_service = ServiceFactory(service_group=service_group, slug="afb")
    group.service = afb_service
    group.save()

    statistics_ag_instance.responsible_services.update(service=afb_service)

    # address inquiry work items to afb
    WorkItem.objects.filter(
        addressed_groups__contains=[str(service.pk)],
        case__family=statistics_ag_instance.case,
    ).update(addressed_groups=[str(afb_service.pk)])

    return statistics_ag_instance


@pytest.fixture
def rpg2_data(
    caluma_document_factory,
    caluma_work_item_factory,
    form_utils: FormUtils,
):
    """Attach an rpg2 work item with answers to the given instance."""

    def _add(instance, *, sealing="rpg2-versiegelt-oder-entsiegelt-ja"):
        work_item = caluma_work_item_factory(
            case=instance.case,
            task_id="rpg2",
            status=WorkItem.STATUS_READY,
            document=caluma_document_factory(form_id="rpg2"),
        )
        document = work_item.document

        form_utils.add_answer(
            document,
            "rpg2-versiegelt-oder-entsiegelt",
            sealing,
            options=[
                ("rpg2-versiegelt-oder-entsiegelt-ja", "Ja"),
                ("rpg2-versiegelt-oder-entsiegelt-nein", "Nein"),
            ],
        )
        form_utils.add_answer(
            document,
            "rpg2-bewilligungsgrund",
            "rpg2-bewilligungsgrund-a01",
            options=[("rpg2-bewilligungsgrund-a01", "A01 Grundlage")],
        )
        form_utils.add_answer(document, "rpg2-anzahl-neue-gebaeude", 3)
        form_utils.add_answer(document, "rpg2-anzahl-gebaeude-abbruch", 1)
        form_utils.add_answer(document, "rpg2-anzahl-gebaeude-unter-schutz", 2)
        form_utils.add_answer(
            document,
            "rpg2-realisiert",
            "rpg2-realisiert-ja",
            options=[
                ("rpg2-realisiert-ja", "Ja"),
                ("rpg2-realisiert-nein", "Nein"),
            ],
        )
        form_utils.add_table_answer(
            document,
            "rpg2-versiegelte-entsiegelte-flaechen",
            rows=[
                {
                    "rpg2-art-versiegelung-entsiegelung": {
                        "value": "rpg2-art-versiegelung-entsiegelung-neue-versiegelte-flaechen-gebaeude",
                        "options": [
                            (
                                "rpg2-art-versiegelung-entsiegelung-neue-versiegelte-flaechen-gebaeude",
                                "Neue versiegelte Fläche Gebäude",
                            ),
                        ],
                    },
                    "rpg2-flaeche-quadrat-meter": 120.5,
                    "rpg2-materialisierung-neu-versiegelten-flaechen": {
                        "value": "rpg2-materialisierung-neu-versiegelten-flaechen-beton",
                        "options": [
                            (
                                "rpg2-materialisierung-neu-versiegelten-flaechen-beton",
                                "Beton",
                            ),
                        ],
                    },
                    "rpg2-materialisierung-neu-versiegelten-flaechen-beschreibung": "Ortbeton",
                    "rpg2-nutzung-versiegelten-flaechen": {
                        "value": "rpg2-nutzung-versiegelten-flaechen-erschliessung-verkehr-kommunale-und-private-projekte",
                        "options": [
                            (
                                "rpg2-nutzung-versiegelten-flaechen-erschliessung-verkehr-kommunale-und-private-projekte",
                                "Erschliessung, Verkehr (kommunale und private Projekte)",
                            ),
                        ],
                    },
                    "rpg2-wann-wurde-flaeche-versiegelt": {
                        "value": "rpg2-wann-wurde-flaeche-versiegelt-neu",
                        "options": [
                            ("rpg2-wann-wurde-flaeche-versiegelt-neu", "Neu"),
                        ],
                    },
                },
                {
                    "rpg2-art-versiegelung-entsiegelung": {
                        "value": "rpg2-art-versiegelung-entsiegelung-entsiegelte-renaturierte-flaechen-gebaeude",
                        "options": [
                            (
                                "rpg2-art-versiegelung-entsiegelung-entsiegelte-renaturierte-flaechen-gebaeude",
                                "Entsiegelt Gebäude",
                            ),
                        ],
                    },
                    "rpg2-flaeche-quadrat-meter": 40.0,
                    "rpg2-materialisierung-neu-versiegelten-flaechen": {
                        "value": "rpg2-materialisierung-neu-versiegelten-flaechen-belag",
                        "options": [
                            (
                                "rpg2-materialisierung-neu-versiegelten-flaechen-belag",
                                "Belag",
                            ),
                        ],
                    },
                    "rpg2-materialisierung-neu-versiegelten-flaechen-beschreibung": "Asphalt",
                    "rpg2-nutzung-versiegelten-flaechen": {
                        "value": "rpg2-nutzung-versiegelten-flaechen-ausnahmebewilligung-artikel-24ff-rpg",
                        "options": [
                            (
                                "rpg2-nutzung-versiegelten-flaechen-ausnahmebewilligung-artikel-24ff-rpg",
                                "Ausnahmebewilligung Artikel 24ff RPG",
                            ),
                        ],
                    },
                    "rpg2-wann-wurde-flaeche-versiegelt": {
                        "value": "rpg2-wann-wurde-flaeche-versiegelt-neu",
                        "options": [
                            ("rpg2-wann-wurde-flaeche-versiegelt-neu", "Neu"),
                        ],
                    },
                },
            ],
            row_form_id="rpg2-versiegelte-entsiegelte-flaechen",
        )
        return work_item

    return _add
