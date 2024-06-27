from datetime import date, timedelta

import pytest
from caluma.caluma_workflow.models import WorkItem
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    "is_bab,is_bab_service,has_completed_publication,has_running_publication,expected_services",
    [
        (False, False, False, False, {"excluded", "not-excluded", "bab-service"}),
        (True, False, False, False, {"not-excluded"}),
        (True, False, True, False, {"not-excluded", "bab-service"}),
        (True, False, True, True, {"not-excluded"}),
        (True, True, False, False, {"not-excluded", "excluded"}),
    ],
)
def test_public_services_available_in_distribution_for_instance(
    admin_client,
    expected_services,
    is_bab_service,
    service,
    has_running_publication,
    has_completed_publication,
    service_factory,
    so_instance,
    bab_settings,
    is_bab,
    so_publication_settings,
    work_item_factory,
    utils,
):
    if is_bab:
        so_instance.case.meta["is-bab"] = True
        so_instance.case.save()

    if is_bab_service:
        bab_service = service
    else:
        bab_service = service_factory(name="bab-service")

    bab_settings["SERVICE_GROUP"] = bab_service.service_group.name

    service_factory(name="not-excluded")
    bab_settings["EXCLUDED_IN_DISTRIBUTION"] = [service_factory(name="excluded").pk]

    if has_completed_publication:
        work_item = work_item_factory(
            task_id=so_publication_settings["FILL_TASKS"][0],
            status=WorkItem.STATUS_COMPLETED,
            case=so_instance.case,
            meta={"is-published": True},
        )
        utils.add_answer(
            work_item.document,
            "publikation-ende",
            date.today() - timedelta(days=1),
        )

    if has_running_publication:
        work_item = work_item_factory(
            task_id=so_publication_settings["FILL_TASKS"][0],
            status=WorkItem.STATUS_COMPLETED,
            case=so_instance.case,
            meta={"is-published": True},
        )
        utils.add_answer(
            work_item.document,
            "publikation-ende",
            date.today() + timedelta(days=1),
        )
        utils.add_answer(
            work_item.document,
            "publikation-start",
            date.today() - timedelta(days=1),
        )

    response = admin_client.get(
        reverse("publicservice-list"),
        {
            "available_in_distribution_for_instance": so_instance.pk,
            "exclude_own_service": True,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert (
        set([i["attributes"]["name"] for i in response.json()["data"]])
        == expected_services
    )
