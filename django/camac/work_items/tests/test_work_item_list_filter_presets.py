import pytest
from django.urls import reverse
from rest_framework import status

from camac.work_items import serializers


@pytest.mark.parametrize(
    "role__name,expected_presets",
    [
        ("Applicant", set()),
        (
            "Municipality",
            {
                ("global", "STANDARD"),
                ("my-service", "SERVICE"),
                ("my-service-group", "SERVICE_GROUP"),
                ("my-service-and-service-group", "SERVICE"),
            },
        ),
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
        ("my-service-and-service-group", [service], [service_group]),
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
    assert {
        (e["attributes"]["name"]["de"], e["attributes"]["category"]) for e in data
    } == expected_presets


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


def test_preset_tasks(
    db,
    fake_request,
    work_item_list_filter_preset_factory,
    caluma_task_factory,
):
    preset = work_item_list_filter_preset_factory(prefilter_tasks=True)
    task = caluma_task_factory()
    preset.tasks.set([task])
    serializer = serializers.WorkItemListFilterPresetSerializer(
        context={"request": fake_request}
    )

    assert list(serializer.get_tasks(preset)) == [task.slug]

    preset.prefilter_tasks = False
    preset.save()

    assert list(serializer.get_tasks(preset)) == []


def test_preset_excluded_tasks(
    db,
    fake_request,
    work_item_list_filter_preset_factory,
    caluma_task_factory,
):
    preset = work_item_list_filter_preset_factory(prefilter_tasks=True)
    task_included = caluma_task_factory()
    task_excluded = caluma_task_factory()
    preset.tasks.set([task_included])
    serializer = serializers.WorkItemListFilterPresetSerializer(
        context={"request": fake_request}
    )

    assert list(serializer.get_excluded_tasks(preset)) == [task_excluded.slug]

    preset.prefilter_tasks = False
    preset.save()

    assert list(serializer.get_excluded_tasks(preset)) == []


def test_preset_excluded_work_item_templates(
    db,
    fake_request,
    work_item_list_filter_preset_factory,
    work_item_template_factory,
):
    preset = work_item_list_filter_preset_factory(prefilter_work_item_templates=True)
    template_included = work_item_template_factory()
    template_excluded = work_item_template_factory()
    preset.work_item_templates.set([template_included])
    serializer = serializers.WorkItemListFilterPresetSerializer(
        context={"request": fake_request}
    )

    assert list(serializer.get_excluded_work_item_templates(preset)) == [
        template_excluded.pk
    ]

    preset.prefilter_work_item_templates = False
    preset.save()

    assert list(serializer.get_excluded_work_item_templates(preset)) == []
