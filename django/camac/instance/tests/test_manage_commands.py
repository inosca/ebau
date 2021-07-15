from io import StringIO

import pytest
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from django.core.management import call_command
from pytest_factoryboy import LazyFixture


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


@pytest.mark.parametrize(
    "instance__user,service_group__name", [(LazyFixture("admin_user"), "municipality")]
)
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
    instance,
    instance_state,
    case_factory,
    service_group,
    snapshot,
    role,
    premature_decision,
    docx_decision_factory,
    expected_case_status,
):
    case = case_factory.create(
        meta={"camac-instance-id": instance.pk},
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        status=caluma_workflow_models.Case.STATUS_COMPLETED,
    )
    wi = case.work_items.first()
    wi = workflow_api.complete_work_item(wi, caluma_admin_user)
    wi.task_id = "decision"
    wi.save()
    if not premature_decision:
        docx_decision_factory(instance=instance)

    call_fix_work_items("--premature-decision", instance=instance.pk)
    assert case.status == expected_case_status
