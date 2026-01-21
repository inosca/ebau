import pytest
from caluma.caluma_form.models import Question
from django.utils import timezone
from django_celery_beat.models import ClockedSchedule, PeriodicTask

from camac.notification.tasks import send_notification_for_publication


@pytest.mark.freeze_time("2024-05-13")
@pytest.mark.parametrize("condition_match", [False, True])
@pytest.mark.parametrize("date_match", [False, True])
@pytest.mark.parametrize("is_published", [False, True])
@pytest.mark.parametrize("used_workitem_id", [None, "current", "other"])
def test_notify_publication_start(
    db,
    caluma_admin_user,
    instance,
    caluma_work_item_factory,
    caluma_question_factory,
    caluma_question_option_factory,
    caluma_answer_factory,
    condition_match,
    date_match,
    is_published,
    used_workitem_id,
    mailoutbox,
    notification_template_factory,
    publication_settings,
    application_settings,
    settings,
    caluma_workflow_config_gr,
    support_role,
):
    expected_outbox = (
        1
        if (
            condition_match
            and date_match
            and is_published
            and used_workitem_id in [None, "current"]
        )
        else 0
    )
    settings.CELERY_TASK_ALWAYS_EAGER = True

    notification_template = notification_template_factory()
    publication_settings["PUBLISH_QUESTION"] = "oeffentliche-auflage"
    publication_settings["PUBLISH_ANSWER"] = ["oeffentliche-auflage-ja"]
    application_settings["NOTIFICATIONS"] = {
        "PUBLICATION_START": {
            "condition": {
                "question": "oeffentliche-auflage-informieren",
                "answer": ["oeffentliche-auflage-informieren-ja"],
            },
            "date_question": "beginn-publikationsorgan-gemeinde",
            "notification": {
                "template_slug": notification_template.slug,
                "recipient_types": ["applicant"],
            },
        }
    }

    date_question = caluma_question_factory(
        slug="beginn-publikationsorgan-gemeinde", type=Question.TYPE_DATE
    )
    publish_question = caluma_question_factory(
        slug=publication_settings["PUBLISH_QUESTION"],
        type=Question.TYPE_MULTIPLE_CHOICE,
    )
    caluma_question_option_factory(
        question_id=publication_settings["PUBLISH_QUESTION"],
        option__slug=publication_settings["PUBLISH_ANSWER"][0],
    )
    inform_question = caluma_question_factory(
        slug="oeffentliche-auflage-informieren", type=Question.TYPE_MULTIPLE_CHOICE
    )
    caluma_question_option_factory(
        question_id="oeffentliche-auflage-informieren",
        option__slug="oeffentliche-auflage-informieren-ja",
    )

    work_item = caluma_work_item_factory(task_id="fill-publication")
    caluma_work_item_factory(task_id="fill-publication")
    caluma_work_item_factory(task_id="some-other-task")

    if used_workitem_id == "current":
        workitem_id = str(work_item.pk)
    elif used_workitem_id == "other":
        other_work_item = caluma_work_item_factory(task_id="fill-publication")
        workitem_id = str(other_work_item.pk)
    else:
        workitem_id = None

    instance.case = work_item.case
    instance.save()

    caluma_answer_factory(
        question=inform_question,
        document=work_item.document,
        value=["oeffentliche-auflage-informieren-ja"] if condition_match else [],
    )
    caluma_answer_factory(
        question=publish_question,
        document=work_item.document,
        value=publication_settings["PUBLISH_ANSWER"] if is_published else [],
    )
    caluma_answer_factory(
        question=date_question,
        document=work_item.document,
        date="2024-05-13" if date_match else "2024-06-01",
    )

    task_name = "camac.notification.tasks.send_notification_for_publication"
    clocked, _ = ClockedSchedule.objects.get_or_create(clocked_time=timezone.now())
    PeriodicTask.objects.create(
        clocked=clocked,
        name=f"{task_name}, This should send notifications.",
        task=task_name,
        one_off=True,
        enabled=True,
    )

    assert work_item.meta.get("publication_start_notification_sent_at") is None

    send_notification_for_publication.delay(workitem_id=workitem_id)
    # run a second time to make sure no duplicate notifications are sent
    send_notification_for_publication.delay(workitem_id=workitem_id)

    assert len(mailoutbox) == expected_outbox
    if expected_outbox:
        work_item.refresh_from_db()
        assert work_item.meta.get("publication_start_notification_sent_at") is not None

        mail = mailoutbox[0]
        assert notification_template.subject in mail.subject
        assert notification_template.body in mail.body
        assert (
            mail.recipients()[0]
            == work_item.case.family.instance.involved_applicants.all()[0].invitee.email
        )
