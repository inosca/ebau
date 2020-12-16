import pytest
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Form, Question
from caluma.caluma_workflow.api import start_case
from caluma.caluma_workflow.models import Workflow

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
    instance,
    caluma_workflow_config_be,
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
    case = start_case(
        workflow=Workflow.objects.get(pk="building-permit"),
        form=Form.objects.get(pk="main-form"),
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )

    # create construction control service
    construction_control = service_factory(
        trans__name=expected_service_name,
        trans__language="de",
        service_group__name="construction-control",
    )

    # create currently responsible municipality or district
    instance_service_factory(
        instance=instance,
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
            instance=instance,
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
            document=case.document,
            question=Question.objects.get(pk="gemeinde"),
            value=str(caluma_service.pk),
            user=caluma_admin_user,
        )

    assert set_construction_control(instance) == construction_control
    assert instance.instance_services.filter(
        service__service_group__name="construction-control",
        active=1,
        service=construction_control,
    ).exists()
