import pytest
from caluma.caluma_form.models import Form
from caluma.caluma_workflow.api import start_case
from caluma.caluma_workflow.models import Workflow

from camac.caluma.extensions.dynamic_groups import CustomDynamicGroups


@pytest.mark.parametrize("has_group", [True, False])
def test_dynamic_group_bern(
    db,
    caluma_workflow_config_be,
    instance,
    service_factory,
    activation_factory,
    instance_service_factory,
    caluma_admin_user,
    use_instance_service,
    has_group,
):
    municipality = service_factory()
    construction_control = service_factory()
    service = service_factory()

    use_instance_service(municipality.pk, construction_control.pk)

    context = {}

    if has_group:
        instance_service_factory(instance=instance, service=municipality, active=1)
        instance_service_factory(
            instance=instance, service=construction_control, active=1
        )

        activation = activation_factory(
            circulation__instance=instance, service=service, service_parent=municipality
        )

        context["activation-id"] = activation.pk

    dynamic_groups = CustomDynamicGroups()

    case = start_case(
        workflow=Workflow.objects.get(pk="building-permit"),
        form=Form.objects.get(pk="main-form"),
        user=caluma_admin_user,
        meta={"camac-instance-id": instance.pk},
    )

    for (name, expected) in [
        ("municipality", [str(municipality.pk)]),
        ("construction_control", [str(construction_control.pk)]),
        ("service", [str(service.pk)]),
        ("service_parent", [str(municipality.pk)]),
    ]:
        assert dynamic_groups.resolve(name)(None, case, None, None, context) == (
            expected if has_group else []
        )


def test_dynamic_group_schwyz(
    db, instance, caluma_admin_user, caluma_workflow_config_sz
):
    case = start_case(
        workflow=Workflow.objects.get(pk="building-permit"),
        form=Form.objects.get(pk="baugesuch"),
        user=caluma_admin_user,
        meta={"camac-instance-id": instance.pk},
    )

    assert CustomDynamicGroups().resolve("municipality")(
        None, case, None, None, None
    ) == [str(instance.group.service.pk)]
