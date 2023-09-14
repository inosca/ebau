import pytest
from caluma.caluma_workflow.models import WorkItem

from camac.caluma.extensions.dynamic_groups import CustomDynamicGroups


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


def test_dynamic_create_additional_demand(
    db,
    work_item_factory,
    service_factory,
    distribution_settings,
    additional_demand_settings,
    caluma_admin_user,
    be_instance,
):
    target_service = service_factory()
    target_subservice = service_factory(service_parent=service_factory())
    target_existing = service_factory()

    inquiry_work_item = work_item_factory(
        task_id=distribution_settings["INQUIRY_CREATE_TASK"],
        case=be_instance.case,
        addressed_groups=[str(target_existing.pk)],
        status=WorkItem.STATUS_READY,
    )

    additional_demand_work_item = work_item_factory(
        task_id=additional_demand_settings["ADDITIONAL_DEMAND_CREATE_TASK"],
        case=be_instance.case,
        addressed_groups=[str(target_existing.pk)],
        status=WorkItem.STATUS_READY,
    )

    context = {
        "addressed_groups": [
            str(target_service.pk),
            str(target_subservice.pk),
        ]
    }

    assert set(
        CustomDynamicGroups().resolve("create_init_additional_demand")(
            task=None,
            case=be_instance.case,
            user=caluma_admin_user,
            prev_work_item=None,
            context=context,
        )
    ) == {str(caluma_admin_user.group)}

    assert set(
        CustomDynamicGroups().resolve("create_init_additional_demand")(
            task=None,
            case=be_instance.case,
            user=caluma_admin_user,
            prev_work_item=inquiry_work_item,
            context=context,
        )
    ) == {str(target_service.pk)}

    assert set(
        CustomDynamicGroups().resolve("create_init_additional_demand")(
            task=None,
            case=be_instance.case,
            user=caluma_admin_user,
            prev_work_item=additional_demand_work_item,
            context=context,
        )
    ) == {str(target_existing.pk)}
