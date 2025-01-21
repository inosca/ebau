from datetime import date, timedelta

import pytest
from caluma.caluma_workflow.models import WorkItem
from django.urls import reverse
from rest_framework import status


@pytest.fixture
def so_services(service_factory, service):
    service_factory(
        name="my-subservice",
        service_group=service.service_group,
        service_parent=service,
    )

    for service_group, name in [
        # Restricted BaB services
        ("service-bab", "arp-bab"),
        # Restricted cantonal services
        ("service-cantonal", "arp"),
        ("service-cantonal", "arp-naturschutz"),
        ("service-cantonal", "arp-heimatschutz"),
        ("service-cantonal", "arp-nutzungsplanung"),
        ("service-cantonal", "arp-fuss-und-wanderwege"),
        ("service-cantonal", "denkmalpflege"),
        ("service-cantonal", "afu"),
        ("service-cantonal", "awjf"),
        ("service-cantonal", "gesundheitsamt"),
        ("service-cantonal", "avt"),
        ("service-cantonal", "alw"),
        # Unrestricted services
        ("municipality", "some-municipality"),
        ("service-cantonal", "some-cantonal-service"),
        ("service-extra-cantonal", "some-extra-cantonal-service"),
    ]:
        parent_service = service_factory(
            name=name,
            slug=name,
            service_group__name=service_group,
        )

        service_factory(
            name=f"{name}-subservice",
            service_group__name=service_group,
            service_parent=parent_service,
        )


@pytest.mark.parametrize(
    "service_group__name,conditions,expected_count",
    [
        pytest.param("municipality", ["authority"], 14, id="authority_bib"),
        pytest.param("municipality", ["authority", "bab"], 4, id="authority_bab"),
        pytest.param(
            "municipality",
            ["authority", "bab", "appeal"],
            5,
            id="authority_bab_with_appeal",
        ),
        pytest.param(
            "municipality",
            ["authority", "bab", "completed_publication"],
            5,
            id="authority_bab_with_completed_publication",
        ),
        pytest.param(
            "municipality",
            ["authority", "bab", "running_publication"],
            4,
            id="authority_bab_with_running_publication",
        ),
        pytest.param(
            "municipality",
            ["authority", "bab", "completed_publication", "running_publication"],
            4,
            id="authority_bab_with_completed_and_running_publication",
        ),
        pytest.param("service-cantonal", [], 14, id="service-cantonal"),
        pytest.param("service-extra-cantonal", [], 14, id="service-extra-cantonal"),
        pytest.param("municipality", [], 1, id="municipality"),
        pytest.param("service-bab", [], 14, id="service-bab"),
    ],
)
def test_so_distribution_services(
    db,
    admin_client,
    conditions,
    expected_count,
    mocker,
    service_factory,
    service,
    snapshot,
    so_appeal_settings,
    so_bab_settings,
    so_distribution_settings,
    so_instance,
    so_publication_settings,
    so_services,
    utils,
    work_item_factory,
):
    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service if "authority" in conditions else service_factory(),
    )

    if "bab" in conditions:
        so_instance.case.meta["is-bab"] = True
        so_instance.case.save()

    if "appeal" in conditions:
        so_instance.case.meta["is-appeal"] = True
        so_instance.case.save()

    if "completed_publication" in conditions:
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

    if "running_publication" in conditions:
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

    data = response.json()["data"]

    assert len(data) == expected_count
    assert set([i["attributes"]["name"] for i in data]) == snapshot
