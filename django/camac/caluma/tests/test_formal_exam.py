import pytest

from camac.caluma.extensions.events.formal_exam import post_complete_formal_exam


@pytest.mark.django_db
def test_post_complete_formal_exam_schedules_ag_smartservice_preliminary_check(
    ag_instance,
    ag_permissions_settings,
    caluma_admin_user,
    caluma_work_item_factory,
    mocker,
):
    complete_preliminary_check = mocker.patch(
        "camac.agsmartservice.api.complete_preliminary_check"
    )
    work_item = caluma_work_item_factory(task_id="formal-exam", case=ag_instance.case)

    post_complete_formal_exam(None, work_item=work_item, user=caluma_admin_user)

    complete_preliminary_check.assert_called_once_with(ag_instance)
