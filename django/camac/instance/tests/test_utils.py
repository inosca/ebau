import pytest
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Question

from camac.instance.utils import (
    be_should_prevent_process_step_for_deactivated_municipality,
    set_construction_control,
)


@pytest.mark.parametrize(
    "current_service_name,is_rsta,involved_municipality_name,caluma_form_municipality_name,expected_service_name",
    [
        ("Leitbehörde Bern", False, None, None, "Baukontrolle Bern"),
        (
            "Regierungsstatthalteramt Bern-Mittelland",
            True,
            "Leitbehörde Bern",
            None,
            "Baukontrolle Bern",
        ),
        (
            "Regierungsstatthalteramt Bern-Mittelland",
            True,
            None,
            "Leitbehörde Bern",
            "Baukontrolle Bern",
        ),
    ],
)
def test_set_construction_control(
    db,
    be_instance,
    caluma_admin_user,
    multilang,
    service_factory,
    instance_service_factory,
    current_service_name,
    is_rsta,
    involved_municipality_name,
    caluma_form_municipality_name,
    expected_service_name,
):
    # create construction control service
    construction_control = service_factory(
        trans__name=expected_service_name,
        trans__language="de",
        service_group__name="construction-control",
    )

    # create currently responsible municipality or district
    instance_service_factory(
        instance=be_instance,
        active=1,
        service=service_factory(
            trans__name=current_service_name,
            trans__language="de",
            service_group__name=("district" if is_rsta else "municipality"),
        ),
    )

    if involved_municipality_name:
        # create involved but not active municipality
        instance_service_factory(
            instance=be_instance,
            active=0,
            service=service_factory(
                trans__name=involved_municipality_name,
                trans__language="de",
                service_group__name="municipality",
            ),
        )

    if caluma_form_municipality_name:
        # create municipality filled in caluma form
        caluma_service = service_factory(
            trans__name=caluma_form_municipality_name,
            trans__language="de",
            service_group__name="municipality",
        )
        save_answer(
            document=be_instance.case.document,
            question=Question.objects.get(pk="gemeinde"),
            value=str(caluma_service.pk),
            user=caluma_admin_user,
        )

    assert set_construction_control(be_instance) == construction_control
    assert be_instance.instance_services.filter(
        service__service_group__name="construction-control",
        active=1,
        service=construction_control,
    ).exists()


@pytest.mark.freeze_time("2025-11-05 15:15:15+02:00")
@pytest.mark.parametrize(
    "service_group_name,meta_config,expected_result",
    [
        # No configuration (not deactivated)
        ("municipality", {}, False),
        # Faulty configuration (not deactivated)
        ("municipality", {"deactivated-municipality-at": True}, False),
        ("municipality", {"deactivated-municipality-at": "test"}, False),
        # No time given, defaults to midnight (start) of given date
        # in current timezone (deactivated)
        ("municipality", {"deactivated-municipality-at": "2025-11-05"}, True),
        # Not timezone aware, defaults to current timezone (not deactivated)
        ("municipality", {"deactivated-municipality-at": "2025-11-05T18:15:15"}, False),
        # Deactivation on or before current time (deactivated)
        (
            "municipality",
            {"deactivated-municipality-at": "2025-11-05T15:14:15+02:00"},
            True,
        ),
        (
            "municipality",
            {"deactivated-municipality-at": "2025-11-05T15:15:15+02:00"},
            True,
        ),
        (
            "municipality",
            {"deactivated-municipality-at": "2025-11-04T15:15:15+02:00"},
            True,
        ),
        # Deactivation after current time (not deactivated)
        (
            "municipality",
            {"deactivated-municipality-at": "2025-11-05T15:16:15+02:00"},
            False,
        ),
        (
            "municipality",
            {"deactivated-municipality-at": "2025-11-06T15:15:15+02:00"},
            False,
        ),
        # Active service isn't a municipality (not deactivated)
        (
            "district",
            {"deactivated-municipality-at": "2025-11-04T15:15:15+02:00"},
            False,
        ),
    ],
)
def test_deactivated_municipality(
    db,
    be_instance,
    service_factory,
    instance_service_factory,
    freezer,
    service_group_name,
    meta_config,
    expected_result,
):
    lead_auth = service_factory(
        service_group__name=service_group_name, meta=meta_config
    )
    be_instance.instance_services.all().delete()
    be_instance.instance_services.add(instance_service_factory(service=lead_auth))

    assert (
        be_should_prevent_process_step_for_deactivated_municipality(be_instance)
        == expected_result
    )
