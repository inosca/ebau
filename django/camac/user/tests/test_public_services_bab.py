from datetime import date, timedelta

import pytest
from caluma.caluma_workflow.models import WorkItem
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    "is_bab,is_bab_service,has_publication,expected_count",
    [
        (False, False, False, 11),
        (True, False, False, 7),
        (True, False, True, 8),
        (True, True, False, 10),
    ],
)
def test_public_services_available_in_distribution_for_instance(
    admin_client,
    expected_count,
    is_bab_service,
    service,
    has_publication,
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
        bab_service = service_factory()

    bab_settings["SERVICE_GROUP"] = bab_service.service_group.name

    # 7 not excluded
    service_factory.create_batch(7)
    # 3 excluded
    bab_settings["EXCLUDED_IN_DISTRIBUTION"] = [
        s.pk for s in service_factory.create_batch(3)
    ]

    if has_publication:
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
        utils.add_answer(
            work_item.document,
            "publikation-amtsblatt",
            date.today() - timedelta(days=8),
        )

    response = admin_client.get(
        reverse("publicservice-list"),
        {
            "available_in_distribution_for_instance": so_instance.pk,
            "exclude_own_service": True,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == expected_count
