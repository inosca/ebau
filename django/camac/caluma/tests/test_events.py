from datetime import date

import pytest
from caluma.caluma_core.events import send_event
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import (
    api as workflow_api,
    events as workflow_events,
    models as caluma_workflow_models,
)
from caluma.caluma_workflow.events import (
    post_complete_work_item,
    post_create_work_item,
    post_skip_work_item,
)
from caluma.caluma_workflow.models import Task
from django.conf import settings
from django.utils import timezone

from camac.instance.models import HistoryEntryT


@pytest.mark.parametrize("expected_value", ["is-paper-yes", "is-paper-no"])
def test_copy_papierdossier(
    db,
    be_instance,
    instance_service,
    caluma_admin_user,
    caluma_workflow_config_be,
    expected_value,
    decision_factory,
    application_settings,
    be_decision_settings,
):
    application_settings["SHORT_NAME"] = "be"
    case = be_instance.case

    case.document.answers.create(question_id="is-paper", value=expected_value)

    for task_id in [
        "submit",
        "ebau-number",
        "distribution",
        "decision",
        "sb1",
    ]:
        # skip case to sb2
        if task_id == "decision":
            decision_factory(
                decision=be_decision_settings["ANSWERS"]["DECISION"]["APPROVED"]
            )

        workflow_api.skip_work_item(
            work_item=case.work_items.get(task_id=task_id), user=caluma_admin_user
        )

    for task_id in settings.APPLICATION["CALUMA"]["COPY_PAPER_ANSWER_TO"]:
        assert (
            case.work_items.get(task_id=task_id)
            .document.answers.get(question_id="is-paper")
            .value
            == expected_value
        )


@pytest.mark.parametrize("use_fallback", [True, False])
def test_copy_sb_personalien(
    db,
    be_instance,
    instance_service,
    caluma_admin_user,
    caluma_workflow_config_be,
    use_fallback,
    decision_factory,
    application_settings,
    be_decision_settings,
):
    settings.APPLICATION_NAME = "kt_bern"
    application_settings["SHORT_NAME"] = "be"
    case = be_instance.case

    case.document.answers.create(question_id="is-paper", value="is-paper-no")

    if use_fallback:
        table = case.document.answers.create(question_id="personalien-gesuchstellerin")
        row = caluma_form_models.Document.objects.create(form_id="personalien-tabelle")
        row.answers.create(question_id="name-applicant", value="Foobar")
        table.documents.add(row)
    else:
        table = case.document.answers.create(question_id="personalien-sb")
        row = caluma_form_models.Document.objects.create(form_id="personalien-tabelle")
        row.answers.create(question_id="name-sb", value="Test123")
        table.documents.add(row)

    for task_id in [
        "submit",
        "ebau-number",
        "distribution",
        "decision",
    ]:
        if task_id == "decision":
            decision_factory(
                decision=be_decision_settings["ANSWERS"]["DECISION"]["APPROVED"]
            )

        workflow_api.skip_work_item(
            work_item=case.work_items.get(task_id=task_id), user=caluma_admin_user
        )

    sb1_row = (
        case.work_items.get(task_id="sb1")
        .document.answers.get(question_id="personalien-sb1-sb2")
        .documents.first()
    )

    if use_fallback:
        assert sb1_row.answers.get(question_id="name-applicant").value == "Foobar"
    else:
        assert sb1_row.answers.get(question_id="name-sb").value == "Test123"

    workflow_api.complete_work_item(
        work_item=case.work_items.get(task_id="sb1"), user=caluma_admin_user
    )

    sb2_row = (
        case.work_items.get(task_id="sb2")
        .document.answers.get(question_id="personalien-sb1-sb2")
        .documents.first()
    )

    if use_fallback:
        assert sb2_row.answers.get(question_id="name-applicant").value == "Foobar"
    else:
        assert sb2_row.answers.get(question_id="name-sb").value == "Test123"


@pytest.mark.freeze_time("2023-01-01")
def test_post_complete_sb1(
    db,
    be_instance,
    decision_factory,
    caluma_admin_user,
    document_factory,
    service_factory,
    instance_service_factory,
    settings,
    application_settings,
    be_decision_settings,
):
    settings.APPLICATION_NAME = "kt_bern"
    application_settings["SHORT_NAME"] = "be"
    case = be_instance.case

    service = service_factory(
        service_group__name="construction-control",
        trans__name="Baukontrolle Burgdorf",
        trans__language="de",
    )
    instance_service_factory(instance=be_instance, service=service, active=1)

    for task_id in ["submit", "ebau-number", "distribution", "decision"]:
        if task_id == "decision":
            decision_factory(
                decision=be_decision_settings["ANSWERS"]["DECISION"]["APPROVED"]
            )

        workflow_api.skip_work_item(
            work_item=case.work_items.get(task_id=task_id), user=caluma_admin_user
        )

    work_item = caluma_workflow_models.WorkItem.objects.filter(
        task_id="legal-submission"
    ).first()
    row_document = document_factory(
        form_id="legal-submission-form", family=work_item.document
    )
    document_answer = work_item.document.answers.create(
        question_id="legal-submission-table"
    )
    caluma_form_models.Answer.objects.create(
        value="legal-submission-type-load-compensation-request",
        document=row_document,
        question_id="legal-submission-type",
    )
    document_answer.documents.add(row_document)

    workflow_api.complete_work_item(
        work_item=case.work_items.get(task_id="sb1"), user=caluma_admin_user
    )

    manual_workitem = caluma_workflow_models.WorkItem.objects.filter(
        task_id="create-manual-workitems", name="Lastenausgleichstellende informieren"
    ).first()

    assert manual_workitem.deadline.strftime("%d.%m.%Y") == "11.01.2023"
    assert str(service.pk) in manual_workitem.addressed_groups
    assert str(service.pk) in manual_workitem.controlling_groups


def test_copy_municipality_tags_for_sb1(
    db,
    be_instance,
    caluma_admin_user,
    caluma_workflow_config_be,
    decision_factory,
    service_factory,
    tag_factory,
    instance_service_factory,
    instance_state_factory,
    settings,
    application_settings,
    be_decision_settings,
):
    settings.APPLICATION_NAME = "kt_bern"
    application_settings["SHORT_NAME"] = "be"
    municipality_burgdorf = service_factory(
        service_group__name="municipality",
        trans__language="de",
        trans__name="Leitbehörde Burgdorf",
    )
    municipality_kirchberg = service_factory(
        service_group__name="municipality",
        trans__language="de",
        trans__name="Leitbehörde Kirchberg",
    )
    construction_control_kirchberg = service_factory(
        trans__name="Baukontrolle Kirchberg",
        trans__language="de",
        service_group__name="construction-control",
    )

    instance_service_factory(
        instance=be_instance, service=municipality_burgdorf, active=0
    )
    instance_service_factory(
        instance=be_instance, service=municipality_kirchberg, active=1
    )
    instance_service_factory(
        instance=be_instance, service=construction_control_kirchberg, active=0
    )

    tag_factory(name="Foobar", instance=be_instance, service=municipality_burgdorf)
    tag_factory(name="Baz", instance=be_instance, service=municipality_kirchberg)

    be_instance.case.document.answers.create(
        question_id="is-paper", value="is-paper-no"
    )

    for task_id in [
        "submit",
        "ebau-number",
        "distribution",
    ]:
        workflow_api.skip_work_item(
            work_item=be_instance.case.work_items.get(task_id=task_id),
            user=caluma_admin_user,
        )
    be_instance.instance_state = instance_state_factory(name="sb1")
    be_instance.save()

    decision_factory(decision=be_decision_settings["ANSWERS"]["DECISION"]["APPROVED"])

    workflow_api.complete_work_item(
        work_item=be_instance.case.work_items.get(task_id="decision"),
        user=caluma_admin_user,
    )
    assert (
        len(be_instance.tags.filter(service__trans__name="Baukontrolle Kirchberg")) == 1
    )


def test_copy_responsible_person_lead_authority(
    db,
    be_instance,
    caluma_admin_user,
    decision_factory,
    instance_service_factory,
    instance_state_factory,
    responsible_service_factory,
    service_factory,
    user_factory,
    settings,
    application_settings,
    be_decision_settings,
):
    settings.APPLICATION_NAME = "kt_bern"
    application_settings["SHORT_NAME"] = "be"
    instance_state_factory(name="sb1")

    construction_control = service_factory(
        service_group__name="construction-control",
        trans__language="de",
        trans__name="Baukontrolle Test",
    )
    lead_authority = service_factory(
        service_group__name="municipality",
        trans__language="de",
        trans__name="Leitbehörde Test",
        responsibility_construction_control=True,
    )
    responsible_user = user_factory()

    responsible_service_factory(
        instance=be_instance, service=lead_authority, responsible_user=responsible_user
    )
    instance_service_factory(instance=be_instance, service=lead_authority, active=1)

    for task_id in [
        "submit",
        "ebau-number",
        "distribution",
    ]:
        workflow_api.skip_work_item(
            work_item=be_instance.case.work_items.get(task_id=task_id),
            user=caluma_admin_user,
        )

    decision_factory(decision=be_decision_settings["ANSWERS"]["DECISION"]["APPROVED"])

    workflow_api.complete_work_item(
        work_item=be_instance.case.work_items.get(task_id="decision"),
        user=caluma_admin_user,
    )

    assert be_instance.responsible_services.filter(
        service=construction_control, responsible_user=responsible_user
    ).exists()


@pytest.mark.parametrize(
    "bewilligungspflichtig_hidden,expect_copy", [("true", True), ("false", False)]
)
def test_copy_tank_installation(
    db,
    be_instance,
    caluma_admin_user,
    caluma_workflow_config_be,
    question_factory,
    form_question_factory,
    bewilligungspflichtig_hidden,
    expect_copy,
    decision_factory,
    application_settings,
    be_decision_settings,
):
    application_settings["SHORT_NAME"] = "be"

    case = be_instance.case

    table_form = caluma_form_models.Form.objects.create(
        slug="lagerung-von-stoffen-tabelle-v2"
    )
    form_question_factory(
        form=case.document.form,
        question=caluma_form_models.Question.objects.create(
            slug="lagerung-von-stoffen-v2",
            type=caluma_form_models.Question.TYPE_TABLE,
            row_form=table_form,
        ),
    )

    form_question_factory(
        form=table_form,
        question=caluma_form_models.Question.objects.create(
            slug="lagerstoff", type=caluma_form_models.Question.TYPE_TEXT
        ),
    )

    form_question_factory(
        form=table_form,
        question=caluma_form_models.Question.objects.create(
            slug="bewilligungspflichtig-v2",
            type=caluma_form_models.Question.TYPE_CHOICE,
            is_hidden=bewilligungspflichtig_hidden,
        ),
    )

    table = case.document.answers.create(question_id="lagerung-von-stoffen-v2")
    row = caluma_form_models.Document.objects.create(
        form_id="lagerung-von-stoffen-tabelle-v2"
    )

    row.answers.create(question_id="lagerstoff", value="Ethanol")
    row.answers.create(
        question_id="bewilligungspflichtig-v2", value="bewilligungspflichtig-v2-ja"
    )
    table.documents.add(row)

    for task_id in [
        "submit",
        "ebau-number",
        "publication",
        "audit",
        "distribution",
        "decision",
        "sb1",
    ]:
        if task_id == "decision":
            decision_factory(
                decision=be_decision_settings["ANSWERS"]["DECISION"]["APPROVED"]
            )

        workflow_api.skip_work_item(
            work_item=case.work_items.get(task_id=task_id), user=caluma_admin_user
        )

    sb2_row = caluma_form_models.Document.objects.filter(
        form=table_form, family=case.work_items.get(task_id="sb2").document
    ).first()

    if expect_copy:
        assert sb2_row
        assert sb2_row.answers.get(question_id="lagerstoff").value == "Ethanol"
    else:
        assert not sb2_row


@pytest.mark.parametrize("notify_completed", [True, False])
def test_notify_completed_work_item(
    db,
    caluma_admin_user,
    service_factory,
    user_factory,
    instance,
    work_item_factory,
    mailoutbox,
    application_settings,
    notify_completed,
    notification_template,
):
    application_settings["NOTIFICATIONS"]["COMPLETE_MANUAL_WORK_ITEM"] = [
        {
            "template_slug": notification_template.slug,
            "recipient_types": ["work_item_controlling"],
        }
    ]

    service = service_factory()

    work_item = work_item_factory(
        status="ready",
        controlling_groups=[str(service.pk)],
        child_case=None,
        deadline=timezone.now(),
        meta={"notify-completed": notify_completed},
    )

    work_item.case.meta = {
        **work_item.case.meta,
        "ebau-number": "2020-01",
    }
    work_item.case.save()

    instance.case = work_item.case
    instance.save()

    workflow_api.complete_work_item(work_item, user=caluma_admin_user)

    if not notify_completed:
        assert len(mailoutbox) == 0
    else:
        assert len(mailoutbox) == 1


def test_notify_created_work_item(
    db,
    caluma_admin_user,
    service_factory,
    instance,
    work_item_factory,
    mailoutbox,
    application_settings,
    notification_template,
    task_factory,
):
    application_settings["NOTIFICATIONS"]["CREATE_MANUAL_WORK_ITEM"] = [
        {
            "template_slug": notification_template.slug,
            "recipient_types": ["work_item_addressed"],
        }
    ]

    service = service_factory()

    work_item = work_item_factory(
        task=task_factory(
            slug=application_settings["CALUMA"]["MANUAL_WORK_ITEM_TASK"],
        ),
        status="ready",
        addressed_groups=[str(service.pk)],
        child_case=None,
        deadline=timezone.now(),
        meta={"ebau-number": "2020-01"},
    )

    instance.case = work_item.case
    instance.save()

    send_event(
        post_create_work_item,
        sender="test_notify_created_work_item",
        work_item=work_item,
        user=caluma_admin_user,
        context={},
    )

    assert len(mailoutbox) == 1
    assert mailoutbox[0].recipients()[0] == service.email


def test_set_is_published(
    caluma_admin_user,
    work_item_factory,
    service_factory,
    task_factory,
):
    work_item = work_item_factory(
        task=task_factory(slug="fill-publication"),
        status="ready",
        controlling_groups=[service_factory().pk],
        child_case=None,
        deadline=timezone.now(),
    )

    workflow_api.complete_work_item(work_item, user=caluma_admin_user)

    assert work_item.meta["is-published"]


@pytest.mark.parametrize(
    "task_slug,existing_meta,context,expected_meta",
    [
        (
            "some-slug",
            {},
            {},
            {"not-viewed": True, "notify-deadline": True, "notify-completed": False},
        ),
        (
            "some-slug",
            {"not-viewed": False, "notify-deadline": False, "notify-completed": False},
            {},
            {"not-viewed": False, "notify-deadline": False, "notify-completed": False},
        ),
    ],
)
def test_set_meta_attributes(
    db,
    caluma_admin_user,
    task_factory,
    work_item_factory,
    task_slug,
    existing_meta,
    context,
    expected_meta,
    application_settings,
):
    work_item = work_item_factory(task__slug=task_slug, meta=existing_meta)

    send_event(
        post_create_work_item,
        sender=test_set_meta_attributes,
        work_item=work_item,
        user=caluma_admin_user,
        context=context,
    )

    work_item.refresh_from_db()

    assert work_item.meta == expected_meta


@pytest.mark.parametrize("application_name", ["kt_bern", "kt_schwyz"])
@pytest.mark.parametrize("has_assigned_users", [True, False])
@pytest.mark.parametrize(
    "has_addressed_groups,expected_users",
    [(False, 0), (True, 1)],
)
def test_set_assigned_user(
    db,
    instance,
    caluma_admin_user,
    user,
    user_factory,
    work_item_factory,
    instance_responsibility_factory,
    responsible_service_factory,
    has_assigned_users,
    has_addressed_groups,
    expected_users,
    application_name,
):
    service = None
    addressed_groups = []
    assigned_users = [user_factory().username] if has_assigned_users else []

    service = responsible_service_factory(
        instance=instance, responsible_user=user
    ).service

    if has_addressed_groups:
        addressed_groups = [service.pk] if service else [123]

    work_item = work_item_factory(
        addressed_groups=addressed_groups, assigned_users=assigned_users
    )

    case = work_item.case
    instance.case = case
    instance.save()

    send_event(
        post_create_work_item,
        sender="test_set_assigned_user",
        work_item=work_item,
        user=caluma_admin_user,
        context={},
    )

    work_item.refresh_from_db()

    if has_assigned_users:
        assert work_item.assigned_users == assigned_users
    else:
        assert len(work_item.assigned_users) == expected_users
        if expected_users:
            assert work_item.assigned_users == [user.username]


@pytest.mark.parametrize(
    "process_type,expected_text",
    [
        ("complete", "Dossierprüfung abgeschlossen"),
        ("skip", "Dossierprüfung übersprungen"),
    ],
)
def test_audit_history(
    db,
    instance,
    caluma_admin_user,
    work_item_factory,
    process_type,
    expected_text,
    application_settings,
):
    work_item = work_item_factory()

    application_settings["CALUMA"]["AUDIT_TASK"] = work_item.task_id

    case = work_item.case
    instance.case = case
    instance.save()

    if process_type == "skip":
        send_event(
            post_skip_work_item,
            sender="post_skip_work_item",
            work_item=work_item,
            user=caluma_admin_user,
            context={},
        )
    elif process_type == "complete":
        send_event(
            post_complete_work_item,
            sender="post_complete_work_item",
            work_item=work_item,
            user=caluma_admin_user,
            context={},
        )

    assert (
        HistoryEntryT.objects.filter(history_entry__instance=instance, language="de")
        .first()
        .title
        == expected_text
    )


@pytest.mark.parametrize(
    "task,expected_instance_state,expected_history_text",
    [("complete", "finished", "Baugesuchsverfahren abgeschlossen")],
)
def test_complete_simple_workflow(
    application_settings,
    db,
    instance,
    admin_user,
    caluma_admin_user,
    caluma_config_be,
    group,
    role,
    multilang,
    instance_state_factory,
    work_item_factory,
    task_factory,
    task,
    notification_template,
    mailoutbox,
    role_factory,
    expected_instance_state,
    expected_history_text,
):
    work_item = work_item_factory(task=task_factory(slug=task))
    instance_state = instance_state_factory(name=expected_instance_state)

    notification = {
        "template_slug": notification_template.slug,
        "recipient_types": ["applicant"],
    }
    application_settings["CALUMA"]["SIMPLE_WORKFLOW"][task][
        "notification"
    ] = notification

    case = work_item.case
    instance.case = case
    instance.save()

    send_event(
        post_complete_work_item,
        sender="post_complete_work_item",
        work_item=work_item,
        user=caluma_admin_user,
        context={},
    )

    instance.refresh_from_db()

    assert instance.instance_state == instance_state
    assert HistoryEntryT.objects.filter(
        history_entry__instance=instance,
        title=expected_history_text,
        language="de",
    ).exists()
    assert len(mailoutbox) == 1

    del application_settings["CALUMA"]["SIMPLE_WORKFLOW"][task]["notification"]


def test_reopen_redo_unread(
    db, work_item_factory, case_factory, caluma_admin_user, mocker
):
    mocker.patch(
        "caluma.caluma_workflow.domain_logic.RedoWorkItemLogic.is_work_item_redoable",
        return_value=True,
    )

    case_to_reopen = case_factory(status=caluma_workflow_models.Case.STATUS_COMPLETED)
    case_work_items = work_item_factory.create_batch(
        2,
        case=case_to_reopen,
        meta={"not-viewed": False},
        status=caluma_workflow_models.WorkItem.STATUS_COMPLETED,
    )

    workflow_api.reopen_case(
        case=case_to_reopen, work_items=case_work_items, user=caluma_admin_user
    )

    for work_item in case_work_items:
        assert work_item.status == caluma_workflow_models.WorkItem.STATUS_READY
        assert work_item.meta["not-viewed"]

    work_item_to_redo = work_item_factory(
        child_case=None,
        meta={"not-viewed": False},
        status=caluma_workflow_models.WorkItem.STATUS_COMPLETED,
    )

    workflow_api.redo_work_item(work_item=work_item_to_redo, user=caluma_admin_user)

    assert work_item.status == caluma_workflow_models.WorkItem.STATUS_READY
    assert work_item.meta["not-viewed"]


@pytest.mark.freeze_time("2023-01-01")
@pytest.mark.parametrize(
    "service_group_name,expected_deadline",
    [
        ("service-with-no-custom-deadline", date(2023, 1, 31)),
        ("municipality", date(2023, 1, 11)),
        ("service", date(2023, 1, 8)),
    ],
)
def test_role_dependent_default_leadtime(
    caluma_admin_user,
    application_settings,
    work_item_factory,
    settings,
    be_distribution_settings,
    be_instance,
    service_factory,
    service_group_name,
    expected_deadline,
):
    inquiry_task = Task.objects.get(slug=settings.DISTRIBUTION["INQUIRY_TASK"])
    addressed_group = service_factory(
        service_group__name=service_group_name,
    )
    work_item = work_item_factory(
        task=inquiry_task,
        addressed_groups=[addressed_group.pk],
    )

    settings.DISTRIBUTION[
        "NOTIFICATIONS"
    ] = {}  # this short-circuits the notification logic which we dont want to test here
    settings.DISTRIBUTION["DEFAULT_DEADLINE_LEAD_TIME"] = 30
    settings.DISTRIBUTION["DEADLINE_LEAD_TIME_FOR_ADDRESSED_SERVICES"] = {
        "municipality": 10,
        "service": 7,
    }

    assert work_item.document.answers.count() == 0

    send_event(
        post_create_work_item,
        sender="post_create_work_item",
        work_item=work_item,
        user=caluma_admin_user,
        context={},
    )

    deadline_answer = work_item.document.answers.get(
        question__pk=settings.DISTRIBUTION["QUESTIONS"]["DEADLINE"]
    )

    assert deadline_answer.date == expected_deadline


def test_post_create_reject_work_item(
    caluma_admin_user,
    so_rejection_settings,
    work_item_factory,
    so_instance,
    instance_state_factory,
):
    instance_state_factory(name=so_rejection_settings["WORK_ITEM"]["INSTANCE_STATE"])

    send_event(
        post_create_work_item,
        sender="post_create_work_item",
        work_item=work_item_factory(
            task_id=so_rejection_settings["WORK_ITEM"]["TASK"],
            case=so_instance.case,
        ),
        user=caluma_admin_user,
        context={},
    )

    so_instance.refresh_from_db()

    assert (
        so_instance.instance_state.name
        == so_rejection_settings["WORK_ITEM"]["INSTANCE_STATE"]
    )


@pytest.mark.parametrize(
    "notification_template__slug", ["notify-geometer-sb2-complete"]
)
@pytest.mark.parametrize("has_geometer", [True, False])
def test_geometer_complete_sb2(
    db,
    set_application_be,
    caluma_workflow_config_be,
    be_instance,
    work_item_factory,
    notification_template,
    application_settings,
    caluma_admin_user,
    instance_state_factory,
    mailoutbox,
    instance_acl_factory,
    access_level_factory,
    permissions_settings,
    service_factory,
    has_geometer,
    configure_custom_notification_types,
):
    complete_state = instance_state_factory(name="complete")
    instance_state_factory(name="finished")
    be_instance.instance_state = complete_state
    be_instance.save()

    configure_custom_notification_types()

    work_item = work_item_factory(task_id="sb2", case=be_instance.case)

    if has_geometer:
        geometer_service = service_factory()
        instance_acl_factory(
            instance=be_instance,
            access_level=access_level_factory(slug="geometer"),
            service=geometer_service,
            metainfo={"disable-notification-on-creation": True},
        )
        permissions_settings["geometer"] = [("foo", ["*"])]

    # We don't play though the whole workflow, but just trigger the
    # corresponding event directly. We can get away with this as
    # the notification doesn't need any specific information
    send_event(
        workflow_events.post_complete_work_item,
        sender="test",
        work_item=work_item,
        user=caluma_admin_user,
        context={},
    )

    assert len(mailoutbox) == (1 if has_geometer else 0)
    if has_geometer:
        assert notification_template.subject in mailoutbox[0].subject
