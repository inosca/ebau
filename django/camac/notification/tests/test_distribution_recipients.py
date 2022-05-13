import pytest
from caluma.caluma_form.factories import (
    AnswerFactory,
    QuestionFactory,
    QuestionOptionFactory,
)
from caluma.caluma_form.models import Question
from caluma.caluma_workflow.factories import CaseFactory
from caluma.caluma_workflow.models import WorkItem

from camac.notification.serializers import (
    PermissionlessNotificationTemplateSendmailSerializer,
)


@pytest.mark.parametrize("role__name", ["support"])
def test_recipient_unanswered_inquiries(
    db,
    active_inquiry_factory,
    be_instance,
    notification_template,
    service_factory,
    system_operation_user,
):
    service = service_factory(email="test@example.com")

    active_inquiry_factory(status=WorkItem.STATUS_COMPLETED)
    active_inquiry_factory(addressed_service=service, status=WorkItem.STATUS_SKIPPED)

    serializer = PermissionlessNotificationTemplateSendmailSerializer(
        data={
            "recipient_types": ["unanswered_inquiries"],
            "instance": {"type": "instances", "id": be_instance.pk},
            "notification_template": {
                "type": "notification-templates",
                "id": notification_template.pk,
            },
        }
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    assert serializer._get_recipients_unanswered_inquiries(be_instance) == [
        {"to": "test@example.com"}
    ]


@pytest.mark.parametrize("role__name", ["support"])
def test_recipient_inquiry(
    db,
    active_inquiry_factory,
    be_instance,
    notification_template,
    service_factory,
    system_operation_user,
):
    from_service = service_factory(email="from@example.com")
    to_service = service_factory(email="to@example.com")

    work_item = active_inquiry_factory(
        addressed_service=to_service, controlling_service=from_service
    )

    serializer = PermissionlessNotificationTemplateSendmailSerializer(
        data={
            "recipient_types": ["inquiry_addressed", "inquiry_controlling"],
            "instance": {"type": "instances", "id": be_instance.pk},
            "inquiry": {"type": "work-items", "id": work_item.pk},
            "notification_template": {
                "type": "notification-templates",
                "id": notification_template.pk,
            },
        }
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    assert serializer._get_recipients_inquiry_addressed(be_instance) == [
        {"to": "to@example.com"}
    ]
    assert serializer._get_recipients_inquiry_controlling(be_instance) == [
        {"to": "from@example.com"}
    ]


@pytest.mark.parametrize("role__name", ["support"])
def test_recipient_involved_in_distribution(
    db,
    active_inquiry_factory,
    be_instance,
    distribution_settings,
    service_factory,
    notification_template,
    system_operation_user,
):
    status_question = QuestionFactory(type=Question.TYPE_CHOICE)

    involved_option = QuestionOptionFactory(question=status_question).option
    not_involved_option = QuestionOptionFactory(question=status_question).option

    distribution_settings["QUESTIONS"]["STATUS"] = status_question
    distribution_settings["ANSWERS"]["STATUS"] = {
        "NOT_INVOLVED": not_involved_option.pk
    }

    involved_service = service_factory()
    not_involved_service = service_factory()

    for inquiry, option in [
        (active_inquiry_factory(addressed_service=involved_service), involved_option),
        (
            active_inquiry_factory(addressed_service=not_involved_service),
            not_involved_option,
        ),
    ]:
        answer = AnswerFactory(value=option.slug, question=status_question)

        inquiry.child_case = CaseFactory(document=answer.document)
        inquiry.save()

    serializer = PermissionlessNotificationTemplateSendmailSerializer(
        data={
            "recipient_types": ["involved_in_distribution"],
            "instance": {"type": "instances", "id": be_instance.pk},
            "notification_template": {
                "type": "notification-templates",
                "id": notification_template.pk,
            },
        }
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    recipients = [
        rec["to"]
        for rec in serializer._get_recipients_involved_in_distribution(be_instance)
    ]

    assert involved_service.email in recipients
    assert not_involved_service.email not in recipients
