import pytest
from caluma.caluma_workflow.models import WorkItem

from camac.caluma.extensions.dynamic_groups import CustomDynamicGroups
from camac.user.models import ServiceRelation


def test_dynamic_group_municipality_be(db, be_instance):
    assert CustomDynamicGroups().resolve("municipality")(
        None, be_instance.case, None, None, None
    ) == [str(be_instance.responsible_service(filter_type="municipality").pk)]


@pytest.mark.parametrize("workflow", ["building-permit", "internal-document"])
def test_dynamic_group_municipality_sz(
    db, caluma_workflow_config_sz, instance_with_case, instance, workflow
):
    instance = instance_with_case(instance=instance, workflow=workflow)

    assert CustomDynamicGroups().resolve("municipality")(
        None, instance.case, None, None, None
    ) == [str(instance.group.service.pk)]


def test_dynamic_group_construction_control(db, be_instance):
    assert CustomDynamicGroups().resolve("construction_control")(
        None, be_instance.case, None, None, None
    ) == [str(be_instance.responsible_service(filter_type="construction_control").pk)]


@pytest.mark.parametrize("has_context", [True, False])
def test_dynamic_group_distribution_create_inquiry(
    db,
    be_instance,
    caluma_admin_user,
    distribution_settings,
    has_context,
    service_factory,
    service,
    work_item_factory,
):
    prev_work_item = work_item_factory(
        case=be_instance.case, addressed_groups=[str(service.pk)]
    )
    context = {}

    if has_context:
        target_service = service_factory()
        target_subservice = service_factory(service_parent=service_factory())
        target_existing = service_factory()

        work_item_factory(
            task_id=distribution_settings["INQUIRY_CREATE_TASK"],
            case=be_instance.case,
            addressed_groups=[str(target_existing.pk)],
            status=WorkItem.STATUS_READY,
        )

        context = {
            "addressed_groups": [
                str(target_service.pk),
                str(target_subservice.pk),
                str(target_existing.pk),
            ]
        }

    resolved_groups = CustomDynamicGroups().resolve("distribution_create_inquiry")(
        task=None,
        case=be_instance.case,
        user=caluma_admin_user,
        prev_work_item=prev_work_item,
        context=context,
    )

    if has_context:
        assert str(target_service.pk) in resolved_groups
        assert str(target_subservice.pk) not in resolved_groups
        assert str(target_existing.pk) not in resolved_groups
        assert str(service.pk) in resolved_groups
    else:
        assert (
            str(be_instance.responsible_service(filter_type="municipality").pk)
            in resolved_groups
        )


@pytest.mark.parametrize("allow_subservices", [True, False])
def test_dynamic_create_additional_demand(
    db,
    work_item_factory,
    service_factory,
    distribution_settings,
    additional_demand_settings,
    caluma_admin_user,
    be_instance,
    application_settings,
    allow_subservices,
):
    target_service = service_factory()
    target_subservice = service_factory(service_parent=service_factory())
    target_existing = service_factory()

    additional_demand_settings["ALLOW_SUBSERVICES"] = allow_subservices

    # create already existing "init-additional-demand" work item
    work_item_factory(
        task_id=additional_demand_settings["CREATE_TASK"],
        case=be_instance.case,
        addressed_groups=[str(target_existing.pk)],
        status=WorkItem.STATUS_READY,
    )

    # context for when the "init-additional-demand" work item is created through
    # completion of a "create-inquiry" work item
    context = {
        "addressed_groups": [
            str(target_service.pk),
            str(target_subservice.pk),
            str(target_existing.pk),
        ]
    }

    groups_without_prev = set(
        CustomDynamicGroups().resolve("create_init_additional_demand")(
            task=None,
            case=be_instance.case,
            user=caluma_admin_user,
            prev_work_item=None,
            context={},
        )
    )

    # if no previous work item is given, fallback to municipality
    assert (
        str(be_instance.responsible_service(filter_type="municipality").pk)
        in groups_without_prev
    )

    groups_submit = set(
        CustomDynamicGroups().resolve("create_init_additional_demand")(
            task=None,
            case=be_instance.case,
            user=caluma_admin_user,
            prev_work_item=work_item_factory(
                task_id=application_settings["CALUMA"]["SUBMIT_TASKS"][0],
            ),
            context={},
        )
    )

    # if previous work item is submit, fallback to municipality
    assert (
        str(be_instance.responsible_service(filter_type="municipality").pk)
        in groups_submit
    )

    groups_additional_demand = set(
        CustomDynamicGroups().resolve("create_init_additional_demand")(
            task=None,
            case=be_instance.case,
            user=caluma_admin_user,
            prev_work_item=work_item_factory(
                task_id=additional_demand_settings["CREATE_TASK"],
                addressed_groups=[
                    str(target_service.pk),
                    str(target_subservice.pk),
                    str(target_existing.pk),
                ],
            ),
            context={},
        )
    )

    # if previous work item is "init-additional-demand" return addressed_groups
    # of previous work item exluding services that already have a ready
    # "init-additional-demand" work items and subservices
    assert str(target_service.pk) in groups_additional_demand
    assert (str(target_subservice.pk) in groups_additional_demand) == allow_subservices

    groups_inquiry = set(
        CustomDynamicGroups().resolve("create_init_additional_demand")(
            task=None,
            case=be_instance.case,
            user=caluma_admin_user,
            prev_work_item=work_item_factory(
                task_id=distribution_settings["INQUIRY_CREATE_TASK"]
            ),
            context=context,
        )
    )

    # if previous work item is "create-inquiry" return addressed_groups from
    # context exluding services that already have a ready
    # "init-additional-demand" work items and subservices
    assert str(target_service.pk) in groups_inquiry
    assert (str(target_subservice.pk) in groups_inquiry) == allow_subservices


def test_dynamic_group_geometer_be(
    db,
    be_instance,
    service_factory,
    instance_service_factory,
    use_instance_service,
    application_settings,
):
    geometer_service = service_factory(
        service_group__name="geometer",
    )

    municipality_service = service_factory(
        service_group__name="municipality",
    )

    instance_service_factory(
        instance=be_instance, service=municipality_service, active=1
    )

    ServiceRelation.objects.create(
        function=ServiceRelation.FUNCTION_GEOMETER,
        receiver=be_instance.responsible_service(filter_type="municipality"),
        provider=geometer_service,
    )

    application_settings["ACTIVE_SERVICES"]["MUNICIPALITY"]["FILTERS"] = {
        "service__service_group__name__in": [
            "municipality",
        ]
    }

    assert CustomDynamicGroups().resolve("geometer")(
        None, be_instance.case, None, None, None
    ) == [
        str(
            be_instance.responsible_service(filter_type="municipality")
            .functional_services.values_list("pk", flat=True)
            .first()
        )
    ]
