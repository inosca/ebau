import pytest
from caluma.caluma_workflow.models import WorkItem

from camac.permissions import api as permissions_api
from camac.permissions.models import InstanceACL


@pytest.mark.django_db
def test_create_afu_work_item_so(
    set_application_so,
    caluma_admin_user,
    so_instance,
    service,
    user,
    access_level,
    caluma_document_factory,
    caluma_work_item_factory,
    caluma_case_factory,
    service_factory,
    instance_state_factory,
    so_ech0211_settings,
):
    not_afu = service_factory()

    service.slug = "afu"
    service.save()

    # Make sure we only look at work_items form the current case
    caluma_work_item_factory(
        task_id="afu-form", case=caluma_case_factory(), status=WorkItem.STATUS_READY
    )

    afu_workitem = WorkItem.objects.filter(
        task_id="afu-form", case=so_instance.case, status=WorkItem.STATUS_READY
    )

    def _grant(service=None, user=None) -> InstanceACL:
        return permissions_api.grant(
            instance=so_instance,
            access_level=access_level,
            **(
                {"user": user, "grant_type": "USER"}
                if user
                else {"service": service, "grant_type": "SERVICE"}
            ),
        )

    # Fails check that instance state is not finished
    so_instance.instance_state = instance_state_factory(name="finished")
    so_instance.save()
    _grant(service=service)
    assert not afu_workitem.exists()
    so_instance.instance_state = instance_state_factory()
    so_instance.save()

    # Fails check that the acl has a service
    _grant(user=user)
    assert not afu_workitem.exists()

    # Fails check that the service has "afu" slug
    not_afu.slug = "notafu"
    not_afu.save()
    acl = _grant(service=not_afu)
    assert not afu_workitem.exists()

    # Only run on ACL creation
    acl.service = service
    acl.save()
    assert not afu_workitem.exists()

    # Success
    _grant(service=service)
    assert afu_workitem.count() == 1
    assert afu_workitem.first().addressed_groups == [str(service.pk)]
    assert afu_workitem.first().status == WorkItem.STATUS_READY

    # Fails check for pre-existing work item already addressed to current service
    service.slug = "afu"
    service.save()
    _grant(service=service)
    assert afu_workitem.count() == 1
