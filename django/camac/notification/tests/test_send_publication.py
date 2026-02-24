import pytest
from caluma.caluma_form.models import Question
from django.utils import timezone
from django_celery_beat.models import ClockedSchedule, PeriodicTask

from camac.notification.tasks import (
    send_notification_for_publication,
    send_notification_for_publication_end_legal_submissions,
)


@pytest.mark.freeze_time("2024-05-13")
@pytest.mark.parametrize("condition_match", [False, True])
@pytest.mark.parametrize("date_match", [False, True])
@pytest.mark.parametrize("is_published", [False, True])
@pytest.mark.parametrize("used_workitem_id", [None, "current", "other"])
@pytest.mark.parametrize("has_publication_start_config", [False, True])
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
    has_publication_start_config,
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
            and has_publication_start_config
        )
        else 0
    )
    settings.CELERY_TASK_ALWAYS_EAGER = True

    notification_template = notification_template_factory()
    publication_settings["PUBLISH_QUESTION"] = "oeffentliche-auflage"
    publication_settings["PUBLISH_ANSWER"] = ["oeffentliche-auflage-ja"]
    if has_publication_start_config:
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
    else:
        application_settings["NOTIFICATIONS"] = {}

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


@pytest.mark.freeze_time("2024-05-13")
@pytest.mark.parametrize(
    "date_match,is_published,is_bab,has_publication_end_config,is_inquired,has_submissions,expected_outbox",
    [
        [False, False, False, False, False, False, 0],
        [True, False, False, False, False, False, 0],
        [True, True, False, False, False, False, 0],
        [True, True, True, False, False, False, 0],
        [True, True, True, True, False, False, 0],
        [True, True, True, True, True, False, 0],
        # only when all conditions are met, the notification is sent
        [True, True, True, True, True, True, 1],
    ],
)
def test_send_notification_for_publication_end_legal_submissions(
    db,
    caluma_admin_user,
    instance,
    caluma_case_factory,
    caluma_work_item_factory,
    caluma_question_factory,
    caluma_question_option_factory,
    active_inquiry_factory,
    caluma_answer_factory,
    caluma_document_factory,
    service_factory,
    date_match,
    is_published,
    is_bab,
    is_inquired,
    has_publication_end_config,
    has_submissions,
    expected_outbox,
    mailoutbox,
    notification_template_factory,
    publication_settings,
    application_settings,
    settings,
    caluma_workflow_config_gr,
    support_role,
):
    settings.CELERY_TASK_ALWAYS_EAGER = True

    instance.case = caluma_case_factory()
    instance.save()
    instance.case.meta["is-bab"] = is_bab
    instance.case.save()

    service_are = service_factory(slug="are", email="are@example.ch")
    if is_inquired:
        active_inquiry_factory(addressed_service=service_are)

    notification_template = notification_template_factory()
    publication_settings["PUBLISH_QUESTION"] = "oeffentliche-auflage"
    publication_settings["PUBLISH_ANSWER"] = ["oeffentliche-auflage-ja"]
    if has_publication_end_config:
        application_settings["NOTIFICATIONS"] = {
            "PUBLICATION_END_LEGAL_SUBMISSION": {
                "date_question": "ende-publikation-kantonsamtsblatt",
                "notification": {
                    "template_slug": notification_template.slug,
                    "recipient_types": ["are_bab"],
                },
            }
        }
    else:
        application_settings["NOTIFICATIONS"] = {}

    date_question = caluma_question_factory(
        slug="ende-publikation-kantonsamtsblatt", type=Question.TYPE_DATE
    )
    publish_question = caluma_question_factory(
        slug=publication_settings["PUBLISH_QUESTION"],
        type=Question.TYPE_MULTIPLE_CHOICE,
    )
    caluma_question_option_factory(
        question_id=publication_settings["PUBLISH_QUESTION"],
        option__slug=publication_settings["PUBLISH_ANSWER"][0],
    )

    work_item = caluma_work_item_factory(
        task_id="fill-publication", case=caluma_case_factory(family=instance.case)
    )
    caluma_work_item_factory(
        task_id="fill-publication", case=caluma_case_factory(family=instance.case)
    )
    caluma_work_item_factory(
        task_id="some-other-task", case=caluma_case_factory(family=instance.case)
    )

    workitem_id = str(work_item.pk)
    caluma_answer_factory(
        question=publish_question,
        document=work_item.document,
        value=publication_settings["PUBLISH_ANSWER"] if is_published else [],
    )
    caluma_answer_factory(
        question=date_question,
        document=work_item.document,
        date="2024-05-12" if date_match else "2024-06-01",
    )

    einsprachen_doc = caluma_document_factory(form_id="einsprachen")
    beschwerden_doc = caluma_document_factory(form_id="beschwerden")
    caluma_work_item_factory(
        task_id="objections",
        case=caluma_case_factory(family=instance.case),
        document=einsprachen_doc,
    )
    caluma_work_item_factory(
        task_id="appeals",
        case=caluma_case_factory(family=instance.case),
        document=beschwerden_doc,
    )
    if has_submissions:
        caluma_document_factory(family=einsprachen_doc, form_id="einsprache")
        caluma_document_factory(family=einsprachen_doc, form_id="einsprache")

    task_name = "camac.notification.tasks.send_notification_for_publication_end_legal_submissions"
    clocked, _ = ClockedSchedule.objects.get_or_create(clocked_time=timezone.now())
    PeriodicTask.objects.create(
        clocked=clocked,
        name=f"{task_name}, This should send notifications.",
        task=task_name,
        one_off=True,
        enabled=True,
    )

    assert work_item.meta.get("publication_end_notification_sent_at") is None

    send_notification_for_publication_end_legal_submissions.delay(
        workitem_id=workitem_id
    )
    # run a second time to make sure no duplicate notifications are sent
    send_notification_for_publication_end_legal_submissions.delay(
        workitem_id=workitem_id
    )

    assert len(mailoutbox) == expected_outbox
    if expected_outbox:
        work_item.refresh_from_db()
        assert work_item.meta.get("publication_end_notification_sent_at") is not None

        mail = mailoutbox[0]
        assert notification_template.subject in mail.subject
        assert notification_template.body in mail.body
        assert mail.recipients()[0] == service_are.email
