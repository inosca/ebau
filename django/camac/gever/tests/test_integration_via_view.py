import datetime

import pytest
from caluma.caluma_workflow import models as workflow_models
from caluma.caluma_workflow.api import (
    resume_work_item,
)
from django.urls import reverse
from django.utils.timezone import make_aware

from camac.core import utils as core_utils
from camac.gever import client


@pytest.mark.parametrize("service_group_name", ["municipality", "rsta"])
@pytest.mark.vcr
@pytest.mark.freeze_time("2025-05-12 15:15:15+02:00")
@pytest.mark.django_db(reset_sequences=True)
def test_gever_workflow(
    be_gever_settings,
    be_instance,
    attachment_factory,
    gever_config_data,
    gever_test_utils,
    be_gever_task,
    admin_client,
    gever_groups,
    service_group_name,
    service_factory,
    caluma_admin_user,
    be_distribution_settings,
    group_factory,
    active_inquiry_factory,
    user_factory,
    mocker,
    disable_ech0211_settings,
):
    """Test workflow from inviting AGR until GEVER geschaeft is created.

    We first invite the AGR, which should create the GEVER workitem and fill in
    it's data.

    Then, we "press the button" in the GEVER form and verify that it triggers
    the GEVER API to sync (We mock that part, as it's tested elsewhere)
    """
    # We need reset_sequences(see django_db mark above)
    # to ensure that VCR will properly replay our requests, and that our code
    # finds the data needed in the responses from VCR
    assert be_instance.pk == 1

    # Don't care about unrelated side effects today
    mocker.patch("camac.notification.utils.send_mail")

    attachment_factory.create_batch(2, instance=be_instance)
    responsible_user = user_factory()

    # TODO this should be factored into a utility function or fixture
    # TODO also: We need to use the AGR services (building or shooting noise)
    # instead of the lead authority
    be_instance.responsible_services.create(
        service=service_factory(service_group__name=service_group_name),
        responsible_user=responsible_user,
    )

    gever_test_utils.add_plot_data()
    # Instance needs eBau Number for this to work
    core_utils.assign_ebau_nr(be_instance)

    # "Our" admin user needs to be in the AGR groups to have permissions
    # to trigger the Sync
    agr_group, _ = gever_groups
    agr_group.users.add(admin_client.user, through_defaults={"default_group": False})

    # OK; setup is complete. Now invite AGR via inquiry

    # Invite AGR
    agr_inquiry_workitem = active_inquiry_factory(
        for_instance=be_instance,
        addressed_service=agr_group.service,
        status=workflow_models.WorkItem.STATUS_SUSPENDED,
        # created_at=make_aware(datetime.datetime(2020, 7, 11)),
        closed_at=make_aware(datetime.datetime(2020, 7, 15)),
        deadline=make_aware(datetime.datetime(2020, 7, 20)),
    )
    resume_work_item(agr_inquiry_workitem, user=caluma_admin_user)

    # Verify GEVER workitem is created
    assert be_instance.case.work_items.filter(task="gever").exists()
    # TODO verify form contents

    # Sync GEVER
    resp = admin_client.post(
        reverse("gever-sync", args=[be_instance.pk]),
        headers={"x-camac-group": str(agr_group.pk)},
    )
    assert resp.status_code == 200

    # Verify GEVER is synced

    gever = client.GEVERClient()
    be_instance.case.refresh_from_db()
    matching = gever.geschaeft.by_guid(be_instance.case.meta["gever_base_geschaeft_id"])
    assert matching

    # The Nones are OK, we just didn't fill out the full application form,
    # so some bits are missing here
    assert matching.titel == "None: BG eBau-Nr. 2025-1 , None None, None"
