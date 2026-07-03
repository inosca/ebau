import pytest
from caluma.caluma_workflow.models import WorkItem
from django.utils import timezone

from camac.notification.tasks import (
    automatic_inquiry_answer_for_expired_uso_inquiries,
)


@pytest.fixture
def test_inquiry_factory(
    instance,
    service,
    caluma_work_item_factory,
    active_inquiry_factory,
    gr_distribution_settings,
):
    """Helper factory to create inquiry with fill work item."""

    def factory(
        for_instance=instance,
        addressed_service=service,
        controlling_service=service,
        **kwargs,
    ):
        status = kwargs.pop("status", WorkItem.STATUS_READY)
        inquiry = active_inquiry_factory(
            for_instance=for_instance,
            addressed_service=addressed_service,
            controlling_service=controlling_service,
            status=status,
            **kwargs,
        )
        caluma_work_item_factory(
            task_id=gr_distribution_settings["INQUIRY_ANSWER_FILL_TASK"],
            case=inquiry.child_case,
            child_case=None,
            status=status,
        )

        return inquiry

    return factory


@pytest.mark.freeze_time("2026-02-01")
@pytest.mark.django_db
def test_send_automatic_expired_inquiry_answer(
    gr_instance,
    test_inquiry_factory,
    user_factory,
    service,
    user_group_factory,
    service_factory,
    role_factory,
    set_application_gr,
    caluma_workflow_config_gr,
    gr_ech0211_settings,
    gr_distribution_settings,
    mocker,
    celery_fake_worker,
):
    # disable emails during this test
    mocker.patch("camac.notification.utils.send_mail", return_value=None)

    # setup base instance/user and responsible service
    mocker.patch(
        "camac.instance.models.Instance.responsible_service", return_value=service
    )
    user_factory(username="service-account-camac-admin")

    # setup different services for different roles.
    role_uso = role_factory(name="uso")
    role_are = role_factory(name="are")
    service_uso = service_factory(slug="uso", service_group__slug="uso")
    service_are = service_factory(slug="other", service_group__slug="service-lead")
    user_group_factory(group__service=service_uso, group__role=role_uso)
    user_group_factory(group__service=service_are, group__role=role_are)

    # setup example inquiries, for different services, status and deadlines.
    today = timezone.now()
    date_future = today + timezone.timedelta(days=1)
    date_past = today - timezone.timedelta(days=1)
    inquiry_are_expired = test_inquiry_factory(
        gr_instance,
        addressed_service=service_are,
        deadline=date_past,
    )
    inquiry_uso_pending = test_inquiry_factory(
        gr_instance,
        addressed_service=service_uso,
        deadline=date_future,
    )
    inquiry_uso_expired = test_inquiry_factory(
        gr_instance,
        addressed_service=service_uso,
        deadline=date_past,
    )
    inquiry_uso_expired_completed = test_inquiry_factory(
        gr_instance,
        addressed_service=service_uso,
        deadline=date_past,
        status=WorkItem.STATUS_COMPLETED,
    )

    question_status = gr_distribution_settings["QUESTIONS"]["STATUS"]
    question_remark = gr_distribution_settings["QUESTIONS"]["COMMENTS"]
    answer_auto_renounced = gr_distribution_settings[
        "INQUIRY_ANSWER_AUTOMATIC_RENOUNCED"
    ]

    # initial inquiry status should be ready, except for the last one which is already completed.
    assert inquiry_are_expired.status == "ready"
    assert inquiry_uso_pending.status == "ready"
    assert inquiry_uso_expired.status == "ready"
    assert inquiry_uso_expired_completed.status == "completed"

    # run the automatic accept task.
    automatic_inquiry_answer_for_expired_uso_inquiries.delay()
    celery_fake_worker.run_tasks()

    # refresh inquiries and assert the status is updated.
    for inquiry in [
        inquiry_are_expired,
        inquiry_uso_pending,
        inquiry_uso_expired,
        inquiry_uso_expired_completed,
    ]:
        inquiry.refresh_from_db()

    # the following inquiries must stay unchanged, as they are either:
    # - not expired
    # - not addressed to USO
    # - already completed before
    assert inquiry_are_expired.status == "ready"
    assert inquiry_uso_pending.status == "ready"
    assert inquiry_uso_expired_completed.status == "completed"
    for inquiry in [
        inquiry_are_expired,
        inquiry_uso_pending,
        inquiry_uso_expired_completed,
    ]:
        answerdoc = inquiry.child_case.document
        assert not answerdoc.answers.filter(question_id=question_status).exists()
        assert not answerdoc.answers.filter(question_id=question_remark).exists()

    # the following inquiry must be updated with the answers, and
    # set to status completed.
    assert inquiry_uso_expired.status == "completed"
    for inquiry in [inquiry_uso_expired]:
        answerdoc = inquiry.child_case.document
        assert answerdoc.answers.filter(
            question_id=question_status,
            value=answer_auto_renounced,
        ).exists()
        assert answerdoc.answers.filter(question_id=question_remark).exists()
