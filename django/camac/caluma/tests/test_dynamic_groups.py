import pytest
from caluma.caluma_form.models import Form
from caluma.caluma_workflow.api import start_case
from caluma.caluma_workflow.factories import WorkItemFactory
from caluma.caluma_workflow.models import Workflow

from camac.caluma.extensions.dynamic_groups import CustomDynamicGroups


@pytest.mark.parametrize("has_group", [True, False])
def test_dynamic_group_bern(
    db,
    instance,
    service_factory,
    activation_factory,
    circulation_factory,
    instance_service_factory,
    caluma_admin_user,
    use_instance_service,
    has_group,
    caluma_publication,
):
    municipality = service_factory()
    construction_control = service_factory()
    service = service_factory()
    circulation_service = service_factory()

    use_instance_service(municipality.pk, construction_control.pk)

    context = {}

    if has_group:
        instance_service_factory(instance=instance, service=municipality, active=1)
        instance_service_factory(
            instance=instance, service=construction_control, active=1
        )

        circulation = circulation_factory(
            instance=instance, service=circulation_service
        )
        activation = activation_factory(
            circulation=circulation, service=service, service_parent=municipality
        )

        context["activation-id"] = activation.pk
        context["circulation-id"] = circulation.pk

    dynamic_groups = CustomDynamicGroups()

    case = start_case(
        workflow=Workflow.objects.get(pk="building-permit"),
        form=Form.objects.get(pk="main-form"),
        user=caluma_admin_user,
    )
    instance.case = case
    instance.save()

    for (name, expected) in [
        ("municipality", [str(municipality.pk)]),
        ("construction_control", [str(construction_control.pk)]),
        ("activation_service", [str(service.pk)]),
        ("activation_service_parent", [str(municipality.pk)]),
        ("circulation_service", [str(circulation_service.pk)]),
    ]:
        assert dynamic_groups.resolve(name)(None, case, None, None, context) == (
            expected if has_group else []
        )


@pytest.mark.parametrize("workflow", ["building-permit", "internal-document"])
def test_dynamic_group_schwyz(
    db, instance, caluma_admin_user, caluma_workflow_config_sz, workflow
):
    case = start_case(
        workflow=Workflow.objects.get(pk=workflow),
        form=Form.objects.get(pk="baugesuch"),
        user=caluma_admin_user,
        context={"instance": instance.pk},
    )
    instance.case = case
    instance.save()

    assert CustomDynamicGroups().resolve("municipality")(
        None, case, None, None, None
    ) == [str(instance.group.service.pk)]


@pytest.mark.parametrize("has_context", [True, False])
def test_dynamic_group_distribution_create_inquiry(
    db, be_instance, caluma_admin_user, service, service_factory, has_context
):
    prev_work_item = WorkItemFactory(
        case=be_instance.case, addressed_groups=[str(service.pk)]
    )
    context = {}

    if has_context:
        target_service = service_factory()
        target_subservice = service_factory(service_parent=service_factory())

        context = {
            "addressed_groups": [str(target_service.pk), str(target_subservice.pk)]
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
        assert str(service.pk) in resolved_groups
    else:
        assert (
            str(be_instance.responsible_service(filter_type="municipality").pk)
            in resolved_groups
        )
