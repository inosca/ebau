import pytest

from camac.deadlines import models as deadlines_models
from camac.instance.serializers import (
    CalumaInstanceSubmitSerializer,
)


@pytest.mark.parametrize(
    "service_group__name,role__name", [("municipality", "municipality-lead")]
)
def test_init_deadline_gr(
    db,
    admin_user,
    gr_instance,
    gr_deadlines_settings,
    gr_permissions_settings,
    set_application_gr,
    mocker,
):
    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=admin_user.groups.first().service,
    )
    serializer = CalumaInstanceSubmitSerializer()

    assert (
        deadlines_models.InstanceDeadline.objects.for_instance(
            instance=gr_instance
        ).count()
        == 0
    )
    serializer._init_deadline(gr_instance)
    assert (
        deadlines_models.InstanceDeadline.objects.for_instance(
            instance=gr_instance
        ).count()
        == 1
    )
