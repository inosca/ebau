import pytest

from camac.gis_export.models import AGGISExport
from camac.gis_export.tasks import export_agis_task


@pytest.mark.django_db
def test_export_agis_task(
    ag_instance,
    role,
    service_factory,
    instance_acl_factory,
    instance_state_t_factory,
):
    """Test agis export through the celery task."""

    afb_service = service_factory(slug="afb")
    role.name = "trusted-service-lead"
    role.save()
    instance_acl_factory(instance=ag_instance, service=afb_service)
    ag_instance.instance_state = instance_state_t_factory(
        name="Submitted"
    ).instance_state
    ag_instance.save()

    assert AGGISExport.objects.count() == 0

    export_agis_task()

    assert AGGISExport.objects.count() == 1
    exported = AGGISExport.objects.first()
    assert exported.instance_id == ag_instance.pk
