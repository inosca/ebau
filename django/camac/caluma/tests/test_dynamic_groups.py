import pytest
from caluma.caluma_form.models import Form
from caluma.caluma_workflow.api import start_case
from caluma.caluma_workflow.models import Workflow

from camac.caluma.extensions.dynamic_groups import CustomDynamicGroups


@pytest.mark.parametrize("has_group", [True, False])
def test_dynamic_group(
    db,
    caluma_workflow,
    instance,
    service_factory,
    instance_service_factory,
    caluma_admin_user,
    application_settings,
    has_group,
):

    municipality = service_factory()
    construction_control = service_factory()

    application_settings["ACTIVE_SERVICE_FILTERS"] = {"service__pk": municipality.pk}
    application_settings["ACTIVE_BAUKONTROLLE_FILTERS"] = {
        "service__pk": construction_control.pk
    }

    if has_group:
        instance_service_factory(instance=instance, service=municipality, active=1)
        instance_service_factory(
            instance=instance, service=construction_control, active=1
        )

    dynamic_groups = CustomDynamicGroups()

    case = start_case(
        workflow=Workflow.objects.get(pk="building-permit"),
        form=Form.objects.get(pk="main-form"),
        user=caluma_admin_user,
        meta={"camac-instance-id": instance.pk},
    )

    if has_group:
        assert dynamic_groups.resolve("municipality")(None, case, None, None) == [
            str(municipality.pk)
        ]
        assert dynamic_groups.resolve("construction_control")(
            None, case, None, None
        ) == [str(construction_control.pk)]
    else:
        assert len(dynamic_groups.resolve("municipality")(None, case, None, None)) == 0
        assert (
            len(dynamic_groups.resolve("construction_control")(None, case, None, None))
            == 0
        )
