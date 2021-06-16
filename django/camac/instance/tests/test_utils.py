import pytest
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Question

from camac.instance.utils import set_construction_control


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
