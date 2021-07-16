from io import StringIO

import pytest
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from django.core.management import call_command


def call_fix_work_items(*args, **kwargs):
    out = StringIO()
    call_command(
        "fix_work_items",
        *args,
        stdout=out,
        stderr=StringIO(),
        **kwargs,
    )
    return out.getvalue()


@pytest.mark.parametrize("role__name", ["Support"])
@pytest.mark.parametrize("instance_state__name", ["subm"])
@pytest.mark.parametrize(
    "premature_decision,expected_case_status",
    [
        (True, caluma_workflow_models.Case.STATUS_RUNNING),
        (False, caluma_workflow_models.Case.STATUS_COMPLETED),
    ],
)
def test_fix_work_items_premature_decision(
    db,
    admin_client,
    admin_user,
    caluma_admin_user,
    caluma_workflow_config_be,
    instance_service_factory,
    instance_state,
    service_group,
    role,
    premature_decision,
    docx_decision_factory,
    expected_case_status,
):
    # failing to set up the instance_service correctly would fail the test
    # when the command prints to stdout, requiring the case's `responsible_service`
    # which requires some hard coded values found in APPLICATIONS[<deployment>]["ACTIVE_SERVICES"]
    inst_serv = instance_service_factory(
        instance__user=admin_user,
        service__pk=2,
        service__service_group__name="municipality",
        active=1,
    )

    instance = inst_serv.instance

    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )

    # completing work items using workflow_api.complete_workflow creates
    # new incomplete workflows which causes fix_work_items.Command.handle to
    # reopen the case regardless.
    workitem = case.work_items.first()
    workitem.status = "completed"
    workitem.task_id = "decision"
    workitem.save()

    if not premature_decision:
        docx_decision_factory(instance=instance)

    case.status = caluma_workflow_models.Case.STATUS_COMPLETED
    case.save()

    call_fix_work_items("--premature-decision", instance=instance.pk)

    case.refresh_from_db()
    assert case.status == expected_case_status
