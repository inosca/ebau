from itertools import chain

import pytest
from caluma.caluma_core.relay import extract_global_id

from camac.caluma.extensions.visibilities import CustomVisibility, CustomVisibilityBE
from camac.user.models import Service


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_inquiry_visibility_be(
    db,
    caluma_admin_schema_executor,
    be_distribution_settings,
    active_inquiry_factory,
    role,
    mocker,
    service,
    be_instance,
    service_factory,
    settings,
    gql,
):
    settings.APPLICATION_NAME = "kt_bern"
    mocker.patch(
        "caluma.caluma_core.types.Node.visibility_classes", [CustomVisibilityBE]
    )

    other_service = service_factory()
    other_subservice = service_factory(service_parent=other_service)

    visible_inquiries = [
        active_inquiry_factory(controlling_service=c, addressed_service=a)
        for c, a in [
            (other_service, service),
            (service, other_service),
            (service_factory(), other_service),
        ]
    ]

    # An inquiry addressed to a subservice in which we are not involved should
    # not be visible to us
    invisible_inquiry = active_inquiry_factory(
        controlling_service=other_service, addressed_service=other_subservice
    )

    result = caluma_admin_schema_executor(
        gql("work-items-for-task"),
        variables={"task": be_distribution_settings["INQUIRY_TASK"]},
    )

    assert not result.errors

    ids = set(
        [
            extract_global_id(edge["node"]["id"])
            for edge in result.data["allWorkItems"]["edges"]
        ]
    )

    visible_ids = {str(i.pk) for i in visible_inquiries}

    assert len(ids) == 3
    assert visible_ids == ids
    assert str(invisible_inquiry.pk) not in ids


@pytest.mark.parametrize(
    "role__name,expected_count",
    [("service", 0), ("subservice", 3)],
)
def test_inquiry_visibility_gr(
    db,
    caluma_admin_schema_executor,
    gr_distribution_settings,
    active_inquiry_factory,
    role,
    mocker,
    service,
    gr_instance,
    service_factory,
    settings,
    expected_count,
    gql,
):
    settings.APPLICATION_NAME = "kt_gr"
    mocker.patch("caluma.caluma_core.types.Node.visibility_classes", [CustomVisibility])

    other_service = service_factory()
    other_subservice = service_factory(service_parent=other_service)

    [
        active_inquiry_factory(controlling_service=c, addressed_service=a)
        for c, a in [
            (other_service, service),
            (service, other_service),
            (other_service, other_subservice),
            (service_factory(), other_service),
        ]
    ]

    result = caluma_admin_schema_executor(
        gql("work-items-for-task"),
        variables={"task": gr_distribution_settings["INQUIRY_TASK"]},
    )

    assert not result.errors

    ids = set(
        [
            extract_global_id(edge["node"]["id"])
            for edge in result.data["allWorkItems"]["edges"]
        ]
    )

    assert len(ids) == expected_count


@pytest.fixture
def so_inquiries(
    service_factory, active_inquiry_factory, user_group_factory, admin_user, gr_instance
):
    root_service = service_factory(name="root_service")
    service_1 = service_factory(name="service_1")
    service_2 = service_factory(name="service_2")

    service_1_subservice_1 = service_factory(
        name="service_1_subservice_1", service_parent=service_1
    )
    service_1_subservice_2 = service_factory(
        name="service_1_subservice_2", service_parent=service_1
    )
    service_2_subservice_1 = service_factory(
        name="service_2_subservice_1", service_parent=service_2
    )

    [
        active_inquiry_factory(controlling_service=c, addressed_service=a)
        for c, a in [
            (root_service, service_1),
            (root_service, service_2),
            (service_1, service_1_subservice_1),
            (service_1, service_1_subservice_2),
            (service_2, service_2_subservice_1),
        ]
    ]

    def select_service(name):
        user_group = user_group_factory(
            user=admin_user, group__service=Service.objects.get(name=name)
        )

        return user_group.group

    return select_service


@pytest.mark.parametrize("service_name", ["service_1", "service_1_subservice_1"])
def test_inquiry_visibility_so(
    db,
    caluma_admin_schema_executor_for_group,
    so_distribution_settings,
    gr_instance,
    so_inquiries,
    service_name,
    mocker,
    settings,
    gql,
):
    settings.APPLICATION_NAME = "kt_so"
    mocker.patch("caluma.caluma_core.types.Node.visibility_classes", [CustomVisibility])
    mocker.patch(
        "camac.caluma.extensions.visibilities.CustomVisibility._all_visible_instances",
        return_value=[gr_instance.pk],
    )

    group = so_inquiries(service_name)

    result = caluma_admin_schema_executor_for_group(group.pk)(
        gql("work-items-for-task"),
        variables={"task": so_distribution_settings["INQUIRY_TASK"]},
    )

    assert not result.errors

    visible_service_ids = set(
        chain(
            *[
                [int(id) for id in edge["node"]["addressedGroups"]]
                for edge in result.data["allWorkItems"]["edges"]
            ]
        )
    )

    expected_service_ids = set(
        Service.objects.filter(
            name__in=[
                "service_1",
                "service_2",
                "service_1_subservice_1",
                "service_1_subservice_2",
            ]
        ).values_list("pk", flat=True)
    )

    assert expected_service_ids == visible_service_ids
