import pytest
from caluma.caluma_form.models import Form
from caluma.caluma_workflow.api import start_case
from caluma.caluma_workflow.models import Workflow
from django.conf import settings

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
    application_settings,
    has_group,
):
    settings.APPLICATION_NAME = "kt_bern"

    municipality = service_factory()
    construction_control = service_factory()
    service = service_factory()

    context = {}

    application_settings["ACTIVE_SERVICE_FILTERS"] = {"service__pk": municipality.pk}
    application_settings["ACTIVE_BAUKONTROLLE_FILTERS"] = {
        "service__pk": construction_control.pk
    }

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
    db, caluma_workflow_config_be, instance, caluma_admin_user, settings
):
    settings.APPLICATION_NAME = "kt_schwyz"

    dynamic_groups = CustomDynamicGroups()

    case = start_case(
        workflow=Workflow.objects.get(pk="building-permit"),
        form=Form.objects.get(pk="main-form"),
        user=caluma_admin_user,
        meta={"camac-instance-id": instance.pk},
    )

    assert dynamic_groups.resolve("municipality")(None, case, None, None, None) == [
        str(instance.group.service.pk)
    ]
