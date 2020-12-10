import pytest
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status


@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
@pytest.mark.parametrize(
    "role__name,expected_status",
    [
        ("Support", status.HTTP_204_NO_CONTENT),
        ("Municipality", status.HTTP_403_FORBIDDEN),
    ],
)
def test_archive(
    db,
    admin_client,
    admin_user,
    caluma_admin_user,
    caluma_workflow_config_be,
    instance,
    instance_service,
    role,
    instance_state_factory,
    expected_status,
):
    instance_state_factory(name="archived")
    workflow = caluma_workflow_models.Workflow.objects.get(pk="building-permit")

    case = workflow_api.start_case(
        workflow=workflow,
        form=workflow.allow_forms.first(),
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )

    response = admin_client.post(reverse("instance-archive", args=[instance.pk]))

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        case.refresh_from_db()
        instance.refresh_from_db()

        assert case.status == caluma_workflow_models.Case.STATUS_CANCELED
        assert instance.instance_state.name == "archived"


@pytest.mark.parametrize("instance__user", [LazyFixture("admin_user")])
@pytest.mark.parametrize(
    "role__name,current_form_slug,new_form_slug,expected_status",
    [
        ("Support", "baugesuch", "baugesuch-generell", status.HTTP_204_NO_CONTENT),
        ("Support", "baugesuch", "baugesuch-mit-uvp", status.HTTP_204_NO_CONTENT),
        ("Support", "baugesuch-generell", "baugesuch", status.HTTP_204_NO_CONTENT),
        (
            "Support",
            "baugesuch-generell",
            "baugesuch-mit-uvp",
            status.HTTP_204_NO_CONTENT,
        ),
        ("Support", "baugesuch-mit-uvp", "baugesuch", status.HTTP_204_NO_CONTENT),
        (
            "Support",
            "baugesuch-mit-uvp",
            "baugesuch-generell",
            status.HTTP_204_NO_CONTENT,
        ),
        ("Support", "einfache-vorabklaerung", "baugesuch", status.HTTP_400_BAD_REQUEST),
        ("Support", "baugesuch", "einfache-vorabklaerung", status.HTTP_400_BAD_REQUEST),
        ("Municipality", "baugesuch", "baugesuch-generell", status.HTTP_403_FORBIDDEN),
    ],
)
def test_change_form(
    db,
    admin_client,
    admin_user,
    caluma_admin_user,
    caluma_workflow_config_be,
    instance,
    instance_service,
    role,
    current_form_slug,
    new_form_slug,
    expected_status,
):
    current_form, _ = caluma_form_models.Form.objects.get_or_create(
        pk=current_form_slug
    )
    new_form, _ = caluma_form_models.Form.objects.get_or_create(pk=new_form_slug)

    workflow = caluma_workflow_models.Workflow.objects.get(pk="building-permit")
    workflow.allow_forms.add(current_form, new_form)

    case = workflow_api.start_case(
        workflow=workflow,
        form=current_form,
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )

    response = admin_client.post(
        reverse("instance-change-form", args=[instance.pk]),
        {
            "data": {
                "type": "instance-change-forms",
                "id": instance.pk,
                "attributes": {"form": new_form_slug},
            }
        },
    )

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        case.refresh_from_db()

        assert case.document.form_id == new_form_slug
