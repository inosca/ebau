import pytest
from django.urls import reverse
from rest_framework import status

from camac.conftest import FakeRequest
from camac.work_items import models, serializers


@pytest.mark.parametrize(
    "role__name,expected_presets",
    [
        ("Applicant", set()),
        ("Municipality", {"global", "my-service", "my-service-group"}),
    ],
)
def test_work_item_filter_preset_list(
    work_item_list_filter_preset_factory,
    admin_client,
    expected_presets,
    service,
    service_group,
    service_factory,
    service_group_factory,
):
    for name, services, service_groups in [
        ("global", None, None),
        ("my-service", [service], None),
        ("my-service-group", None, [service_group]),
        ("other-service", [service_factory()], None),
        ("other-service-group", None, [service_group_factory()]),
    ]:
        preset = work_item_list_filter_preset_factory(name=name)
        if services:
            preset.services.set(services)
        if service_groups:
            preset.service_groups.set(service_groups)

    response = admin_client.get(reverse("work-item-list-filter-preset-list"))

    assert response.status_code == status.HTTP_200_OK

    data = response.json()["data"]

    assert len(data) == len(expected_presets)
    assert set([e["attributes"]["name"]["de"] for e in data]) == expected_presets


@pytest.mark.parametrize(
    "role__name,prefilter,is_included,expected_names",
    [
        ("Municipality", True, True, {"template-1"}),
        ("Municipality", True, False, set()),
        ("Municipality", False, True, {"template-1", "template-2"}),
        ("Municipality", False, False, {"template-1", "template-2"}),
    ],
)
def test_included_in_preset_filter(
    db,
    admin_client,
    work_item_template_factory,
    work_item_list_filter_preset_factory,
    prefilter,
    is_included,
    expected_names,
):
    template_1 = work_item_template_factory(name="template-1")
    work_item_template_factory(name="template-2")
    preset = work_item_list_filter_preset_factory(
        prefilter_work_item_templates=prefilter
    )
    if is_included:
        preset.work_item_templates.set([template_1])

    response = admin_client.get(
        reverse("work-item-template-list"), {"included_in_preset": preset.id}
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()["data"]

    assert len(data) == len(expected_names)
    assert set([e["attributes"]["name"] for e in data]) == expected_names


@pytest.mark.parametrize(
    "role__name,visible_to_service,visible_to_service_group,expected",
    [
        (
            "Municipality",
            False,
            False,
            models.WorkItemListFilterPreset.PresetCategoryChoices.STANDARD,
        ),
        (
            "Municipality",
            True,
            False,
            models.WorkItemListFilterPreset.PresetCategoryChoices.SERVICE,
        ),
        (
            "Municipality",
            False,
            True,
            models.WorkItemListFilterPreset.PresetCategoryChoices.SERVICE_GROUP,
        ),
        (
            "Municipality",
            True,
            True,
            models.WorkItemListFilterPreset.PresetCategoryChoices.SERVICE,
        ),
    ],
)
def test_preset_category(
    db,
    user_group,
    work_item_list_filter_preset_factory,
    visible_to_service,
    visible_to_service_group,
    expected,
):
    preset = work_item_list_filter_preset_factory()
    if visible_to_service:
        preset.services.set([user_group.group.service])
    if visible_to_service_group:
        preset.service_groups.set([user_group.group.service.service_group])

    serializer = serializers.WorkItemListFilterPresetSerializer(
        context={
            "request": FakeRequest(
                user=user_group.user,
                group=user_group.group,
            )
        }
    )

    assert serializer.get_category(preset) == expected
