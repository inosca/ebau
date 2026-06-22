import pytest
from caluma.caluma_workflow.models import WorkItem
from django.urls import reverse
from django.utils.timezone import make_aware
from faker import Faker
from rest_framework import status

from camac.settings.modules.work_item_list_schema import WorkItemListConfig
from camac.work_items.available_tasks import get_task_options, get_template_options

fake = Faker()


@pytest.fixture
def task_setup(
    caluma_task_factory,
    caluma_work_item_factory,
    service,
    work_item_list_filter_preset,
    work_item_list_settings: WorkItemListConfig,
):
    default_task = caluma_task_factory(pk="default-task")
    role_task = caluma_task_factory(pk="role-task")
    other_role_task = caluma_task_factory(pk="other-role-task")
    service_group_task = caluma_task_factory(pk="service-group-task")
    other_service_group_task = caluma_task_factory(pk="other-service-group-task")

    work_item_list_settings.available_tasks_default = [default_task.pk]
    work_item_list_settings.available_tasks_for_role = {
        "municipality": [role_task.pk],
        "service": [other_role_task.pk],
    }
    work_item_list_settings.available_tasks_for_service_group = {
        "municipality": [service_group_task.pk],
        "cantonal-service": [other_service_group_task.pk],
    }

    caluma_work_item_factory.create_batch(
        1,
        deadline=make_aware(fake.date_time()),
        addressed_groups=[str(service.pk)],
        task=default_task,
    )
    caluma_work_item_factory.create_batch(
        2,
        deadline=make_aware(fake.date_time()),
        addressed_groups=[str(service.pk)],
        task=role_task,
    )
    caluma_work_item_factory.create_batch(
        3,
        deadline=make_aware(fake.date_time()),
        addressed_groups=[str(service.pk)],
        task=service_group_task,
    )

    work_item_list_filter_preset.tasks.add("default-task")


@pytest.fixture
def template_setup(
    caluma_work_item_factory,
    service_factory,
    service_group_factory,
    service_group,
    service,
    work_item_list_filter_preset,
    work_item_template_factory,
):
    service_template = work_item_template_factory(
        pk=fake.uuid4(), name="service-template"
    )
    other_service_template = work_item_template_factory(
        pk=fake.uuid4(), name="other-template"
    )
    service_group_template = work_item_template_factory(
        pk=fake.uuid4(), name="service-group-template"
    )
    other_service_group_template = work_item_template_factory(
        pk=fake.uuid4(), name="other-service-group-template"
    )
    global_template = work_item_template_factory(
        pk=fake.uuid4(), name="global-template"
    )

    service_template.services.add(service)
    other_service_template.services.add(service_factory())
    service_group_template.service_groups.add(service_group)
    other_service_group_template.service_groups.add(service_group_factory())

    caluma_work_item_factory.create_batch(
        1,
        deadline=make_aware(fake.date_time()),
        addressed_groups=[str(service.pk)],
        meta={"template-id": str(service_template.pk)},
    )
    caluma_work_item_factory.create_batch(
        2,
        deadline=make_aware(fake.date_time()),
        addressed_groups=[str(service.pk)],
        meta={"template-id": str(service_group_template.pk)},
    )
    caluma_work_item_factory.create_batch(
        3,
        deadline=make_aware(fake.date_time()),
        addressed_groups=[str(service.pk)],
        meta={"template-id": str(global_template.pk)},
    )

    work_item_list_filter_preset.work_item_templates.add(global_template)

    return service_template, service_group_template, global_template


@pytest.mark.parametrize(
    "role__name,service_group__name", [("Municipality", "municipality")]
)
@pytest.mark.parametrize(
    "include_count,with_preset,expected",
    [
        (
            False,
            False,
            {("default-task", None), ("role-task", None), ("service-group-task", None)},
        ),
        (
            False,
            True,
            {("default-task", None)},
        ),
        (
            True,
            False,
            {("default-task", 1), ("role-task", 2), ("service-group-task", 3)},
        ),
    ],
)
@pytest.mark.django_db
def test_get_task_options(
    expected,
    group,
    include_count,
    task_setup,
    with_preset,
    work_item_list_filter_preset,
    work_item_list_settings: WorkItemListConfig,
):
    work_item_list_settings.available_tasks_include_count = include_count

    work_item_list_filter_preset.prefilter_tasks = with_preset
    work_item_list_filter_preset.save()

    result = get_task_options(
        group,
        WorkItem.objects.all(),
        work_item_list_filter_preset,
    )

    assert {(i["id"], i["count"]) for i in result} == expected


@pytest.mark.parametrize(
    "include_templates,include_count,with_preset,expected",
    [
        (False, False, False, set()),
        (
            True,
            False,
            False,
            {
                ("service-template", None),
                ("service-group-template", None),
                ("global-template", None),
            },
        ),
        (
            True,
            False,
            True,
            {
                ("global-template", None),
            },
        ),
        (
            True,
            True,
            False,
            {
                ("service-template", 1),
                ("service-group-template", 2),
                ("global-template", 3),
            },
        ),
    ],
)
@pytest.mark.django_db
def test_get_template_options(
    expected,
    group,
    include_count,
    include_templates,
    template_setup,
    with_preset,
    work_item_list_filter_preset: WorkItemListConfig,
    work_item_list_settings,
):
    work_item_list_settings.available_tasks_include_templates = include_templates
    work_item_list_settings.available_tasks_include_count = include_count

    work_item_list_filter_preset.prefilter_work_item_templates = with_preset
    work_item_list_filter_preset.save()

    result = get_template_options(
        group,
        WorkItem.objects.all(),
        work_item_list_filter_preset,
    )

    assert {(i["label"], i["count"]) for i in result} == expected


@pytest.mark.parametrize(
    "role__name,service_group__name", [("Municipality", "municipality")]
)
@pytest.mark.django_db
def test_work_item_list_task_option_list(
    admin_client,
    django_assert_num_queries,
    snapshot,
    task_setup,
    template_setup,
    work_item_list_settings: WorkItemListConfig,
):
    work_item_list_settings.available_tasks_include_count = True
    work_item_list_settings.available_tasks_include_templates = True

    with django_assert_num_queries(4):
        response = admin_client.get(reverse("work-item-list-task-option-list"))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == snapshot
