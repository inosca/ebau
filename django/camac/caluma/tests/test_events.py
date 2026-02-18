from datetime import date

import pytest
from caluma.caluma_core.events import send_event
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_form.factories import AnswerFactory
from caluma.caluma_form.models import Question
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from caluma.caluma_workflow.events import (
    post_complete_work_item,
    post_create_work_item,
    post_skip_work_item,
)
from caluma.caluma_workflow.models import Task, WorkItem
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext as _
from pytest_lazy_fixtures import lf

from camac.caluma.extensions.events import bab, distribution
from camac.caluma.extensions.events.caluma_workflow_notifications import (
    post_complete_caluma_workflow_notifications,
    post_create_caluma_workflow_notifications,
)
from camac.caluma.extensions.events.check_gwr_relevancy import (
    suspend_task_for_additional_demand,
)
from camac.caluma.extensions.events.complete_check import (
    complete_rejection_work_item,
    send_notification_after_complete_check,
)
from camac.caluma.extensions.events.general import post_decision_ur
from camac.caluma.utils import save_answer
from camac.instance.models import HistoryActionConfig, HistoryEntry, HistoryEntryT
from camac.tests.form_utils import FormUtils
from camac.utils import (
    send_only_for_einfache_anfrage,
    should_notify_on_manual_workitems,
)


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
    form_utils: FormUtils,
):
    settings.APPLICATION_NAME = "kt_bern"
    application_settings["SHORT_NAME"] = "be"
    case = be_instance.case

    form_utils.set_is_paper(case.document, False)

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
    caluma_document_factory,
    service_factory,
    instance_service_factory,
    settings,
    application_settings,
    be_decision_settings,
    notification_template_factory,
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
    notification_template_factory(slug="create-manual-work-item")

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
    row_document = caluma_document_factory(
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
    be_ech0211_settings,
    form_utils: FormUtils,
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

    form_utils.set_is_paper(be_instance.case.document, False)

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
    be_ech0211_settings,
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
    caluma_question_factory,
    caluma_form_question_factory,
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
    caluma_form_question_factory(
        form=case.document.form,
        question=caluma_form_models.Question.objects.create(
            slug="lagerung-von-stoffen-v2",
            type=caluma_form_models.Question.TYPE_TABLE,
            row_form=table_form,
        ),
    )

    caluma_form_question_factory(
        form=table_form,
        question=caluma_form_models.Question.objects.create(
            slug="lagerstoff", type=caluma_form_models.Question.TYPE_TEXT
        ),
    )

    caluma_form_question_factory(
        form=table_form,
        question=caluma_form_models.Question.objects.create(
            slug="bewilligungspflichtig-v2",
            type=caluma_form_models.Question.TYPE_CHOICE,
            is_hidden=bewilligungspflichtig_hidden,
        ),
    )

    table = case.document.answers.create(question_id="lagerung-von-stoffen-v2")
    row = caluma_form_models.Document.objects.create(
        form_id="lagerung-von-stoffen-tabelle-v2", family=case.document
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
    caluma_work_item_factory,
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

    work_item = caluma_work_item_factory(
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


def test_notify_manual_work_item(
    db,
    caluma_admin_user,
    service_factory,
    instance,
    caluma_work_item_factory,
    mailoutbox,
    application_settings,
    notification_template_factory,
    caluma_task_factory,
):
    notification_template_created = notification_template_factory()
    notification_template_completed = notification_template_factory()
    application_settings["CALUMA"]["CALUMA_WORKFLOW_NOTIFICATIONS"][
        "create-manual-workitems"
    ] = [
        {
            "event": "created",
            "notification": {
                "template_slug": notification_template_created.slug,
                "recipient_types": ["work_item_addressed"],
            },
        },
        {
            "event": "completed",
            "notification": {
                "template_slug": notification_template_completed.slug,
                "recipient_types": ["work_item_controlling"],
            },
            "condition": lambda work_item: work_item.meta["notify-completed"],
        },
    ]

    controlling_service = service_factory()
    addressed_service = service_factory()

    deadline = timezone.now()
    task = caluma_task_factory(
        slug=application_settings["CALUMA"]["MANUAL_WORK_ITEM_TASK"],
    )
    work_item = caluma_work_item_factory(
        task=task,
        status="ready",
        addressed_groups=[str(addressed_service.pk)],
        controlling_groups=[str(controlling_service.pk)],
        child_case=None,
        deadline=deadline,
        meta={
            "ebau-number": "2020-01",
            "notify-completed": True,
            "notify-deadline": True,
        },
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
    assert mailoutbox[0].recipients()[0] == addressed_service.email

    send_event(
        post_complete_work_item,
        sender="test_notify_created_work_item",
        work_item=work_item,
        user=caluma_admin_user,
        context={},
    )

    assert len(mailoutbox) == 2
    assert mailoutbox[1].recipients()[0] == controlling_service.email

    # Test workitem with no deadline and complete notification
    mailoutbox.clear()
    work_item_only_create = caluma_work_item_factory(
        task=task,
        status="ready",
        addressed_groups=[str(addressed_service.pk)],
        controlling_groups=[str(controlling_service.pk)],
        child_case=None,
        deadline=deadline,
        meta={
            "ebau-number": "2020-01",
            "notify-completed": False,
            "notify-deadline": False,
        },
    )

    work_item_only_create.case = work_item.case
    work_item_only_create.save()

    send_event(
        post_create_work_item,
        sender="test_notify_created_work_item",
        work_item=work_item_only_create,
        user=caluma_admin_user,
        context={},
    )

    assert len(mailoutbox) == 1
    assert mailoutbox[0].recipients()[0] == addressed_service.email

    send_event(
        post_complete_work_item,
        sender="test_notify_created_work_item",
        work_item=work_item_only_create,
        user=caluma_admin_user,
        context={},
    )
    assert len(mailoutbox) == 1


def test_set_is_published(
    db,
    settings,
    application_settings,
    caluma_admin_user,
    caluma_work_item_factory,
    notification_template_factory,
    service_factory,
    caluma_task_factory,
    celery_fake_worker,
):
    work_item = caluma_work_item_factory(
        task=caluma_task_factory(slug="fill-publication"),
        status="ready",
        controlling_groups=[service_factory().pk],
        child_case=None,
        deadline=timezone.now(),
    )

    # Required to avoid guard in the post_complete_publication, which
    # we want to cover here
    notification_template = notification_template_factory()
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

    workflow_api.complete_work_item(work_item, user=caluma_admin_user)

    assert work_item.meta["is-published"]


def test_so_set_is_published_creates_history_entry(
    db,
    settings,
    application_settings,
    set_application_so,
    so_instance,
    caluma_question_factory,
    caluma_work_item_factory,
    caluma_case_factory,
    caluma_task_factory,
    user_factory,
):
    case_family = caluma_case_factory()
    so_instance.case = case_family
    work_item = caluma_work_item_factory(
        case=caluma_case_factory(family=case_family),
        task=Task.objects.get(slug="fill-publication"),
        status="ready",
        modified_by_user=user_factory().username,
    )
    caluma_question_factory(
        slug="publikation-start",
        label="",
        type=Question.TYPE_TEXT,
    )
    caluma_question_factory(
        slug="publikation-ende",
        label="",
        type=Question.TYPE_TEXT,
    )
    caluma_question_factory(
        slug="publikation-organ",
        label="",
        type=Question.TYPE_TEXT,
    )
    caluma_question_factory(
        slug="publikation-anzeiger",
        label="",
        type=Question.TYPE_TEXT,
    )
    mock_data = {
        "start": "start",
        "end": "end",
        "newspaper": "newspaper",
        "newspaper_date": "publication-date",
    }
    save_answer(work_item.document, "publikation-start", mock_data["start"])
    save_answer(work_item.document, "publikation-ende", mock_data["end"])
    save_answer(work_item.document, "publikation-organ", mock_data["newspaper"])
    save_answer(work_item.document, "publikation-anzeiger", mock_data["newspaper_date"])

    assert not HistoryEntry.objects.exists()

    work_item.meta["is-published"] = True
    work_item.save()
    assert HistoryEntry.objects.count() == 1
    he = HistoryEntry.objects.first()
    text = (
        _(
            "Publication created for %(start)s to %(end)s. Published in %(newspaper)s on %(newspaper_date)s."
        )
        % mock_data
    )
    assert he.trans.first().title == text

    work_item.meta["is-published"] = False
    work_item.save()
    assert HistoryEntry.objects.count() == 2
    assert (
        HistoryEntry.objects.filter(
            history_type=HistoryActionConfig.HISTORY_TYPE_PUBLICATION
        ).count()
        == 2
    )
    he = HistoryEntry.objects.order_by("-created_at").first()
    text = (
        _(
            "Publication from %(start)s to %(end)s cancelled. Published in %(newspaper)s on %(newspaper_date)s."
        )
        % mock_data
    )
    assert he.trans.first().title == text


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
    caluma_task_factory,
    caluma_work_item_factory,
    task_slug,
    existing_meta,
    context,
    expected_meta,
    application_settings,
):
    work_item = caluma_work_item_factory(task__slug=task_slug, meta=existing_meta)

    send_event(
        post_create_work_item,
        sender=test_set_meta_attributes,
        work_item=work_item,
        user=caluma_admin_user,
        context=context,
    )

    work_item.refresh_from_db()

    assert work_item.meta == expected_meta


@pytest.fixture
def user1(user_factory):
    return user_factory(username="user1")


@pytest.fixture
def user2(user_factory):
    return user_factory(username="user2")


@pytest.mark.parametrize(
    "addressed_service,assigned_user,responsible_user,bypass_responsible_user,expected_user",
    [
        (None, None, lf("user1"), False, None),
        (lf("service"), lf("user1"), lf("user2"), False, lf("user1")),
        (lf("service"), None, lf("user2"), False, lf("user2")),
        (lf("service"), None, None, False, None),
        (lf("service"), None, lf("user2"), True, None),
    ],
)
def test_set_assigned_user(
    db,
    addressed_service,
    assigned_user,
    bypass_responsible_user,
    caluma_admin_user,
    caluma_work_item_factory,
    expected_user,
    instance,
    responsible_service_factory,
    responsible_user,
):
    if addressed_service and responsible_user:
        responsible_service_factory(
            instance=instance,
            service=addressed_service,
            responsible_user=responsible_user,
        )

    work_item = caluma_work_item_factory(
        addressed_groups=[str(addressed_service.pk)] if addressed_service else [],
        assigned_users=[assigned_user.username] if assigned_user else [],
        meta={"bypass-responsible-user": bypass_responsible_user},
    )

    instance.case = work_item.case
    instance.save()

    send_event(
        post_create_work_item,
        sender="test_set_assigned_user",
        work_item=work_item,
        user=caluma_admin_user,
        context={},
    )

    work_item.refresh_from_db()

    if expected_user is None:
        assert work_item.assigned_users == []
    else:
        assert work_item.assigned_users == [expected_user.username]


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
    caluma_work_item_factory,
    process_type,
    expected_text,
    application_settings,
):
    work_item = caluma_work_item_factory()

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
    be_instance,
    admin_user,
    caluma_admin_user,
    caluma_config_be,
    group,
    role,
    multilang,
    instance_state_factory,
    caluma_work_item_factory,
    caluma_task_factory,
    task,
    notification_template,
    mailoutbox,
    role_factory,
    expected_instance_state,
    expected_history_text,
    be_ech0211_settings,
):
    work_item = caluma_work_item_factory(task_id=task, case=be_instance.case)
    instance_state = instance_state_factory(name=expected_instance_state)

    notification = {
        "template_slug": notification_template.slug,
        "recipient_types": ["applicant"],
    }
    application_settings["CALUMA"]["SIMPLE_WORKFLOW"][task]["notification"] = (
        notification
    )

    send_event(
        post_complete_work_item,
        sender="post_complete_work_item",
        work_item=work_item,
        user=caluma_admin_user,
        context={},
    )

    be_instance.refresh_from_db()

    assert be_instance.instance_state == instance_state
    assert HistoryEntryT.objects.filter(
        history_entry__instance=be_instance,
        title=expected_history_text,
        language="de",
    ).exists()
    assert len(mailoutbox) == 1

    del application_settings["CALUMA"]["SIMPLE_WORKFLOW"][task]["notification"]


def test_reopen_redo_unread(
    db, caluma_work_item_factory, caluma_case_factory, caluma_admin_user, mocker
):
    mocker.patch(
        "caluma.caluma_workflow.domain_logic.RedoWorkItemLogic.is_work_item_redoable",
        return_value=True,
    )

    case_to_reopen = caluma_case_factory(
        status=caluma_workflow_models.Case.STATUS_COMPLETED
    )
    case_work_items = caluma_work_item_factory.create_batch(
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

    work_item_to_redo = caluma_work_item_factory(
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
def test_role_dependent_default_leadtime_service_groups(
    caluma_admin_user,
    application_settings,
    caluma_work_item_factory,
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
    work_item = caluma_work_item_factory(
        task=inquiry_task,
        addressed_groups=[addressed_group.pk],
    )

    settings.DISTRIBUTION[
        "NOTIFICATIONS"
    ] = {}  # this short-circuits the notification logic which we dont want to test here
    settings.DISTRIBUTION["DEFAULT_DEADLINE_LEAD_TIME"] = 30
    settings.DISTRIBUTION["DEADLINE_LEAD_TIME_FOR_ADDRESSED_SERVICE_GROUPS"] = {
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


@pytest.mark.freeze_time("2023-01-01")
@pytest.mark.parametrize(
    "service_slug,expected_deadline",
    [
        ("afb", date(2023, 1, 31)),
        ("aew", date(2023, 1, 11)),
    ],
)
def test_role_dependent_default_leadtime_services(
    caluma_admin_user,
    application_settings,
    caluma_work_item_factory,
    settings,
    be_distribution_settings,
    be_instance,
    service_factory,
    service_slug,
    expected_deadline,
):
    inquiry_task = Task.objects.get(slug=settings.DISTRIBUTION["INQUIRY_TASK"])
    addressed_service = service_factory(
        slug=service_slug,
    )
    work_item = caluma_work_item_factory(
        task=inquiry_task,
        addressed_groups=[str(addressed_service.pk)],
    )

    settings.DISTRIBUTION[
        "NOTIFICATIONS"
    ] = {}  # this short-circuits the notification logic which we dont want to test here
    settings.DISTRIBUTION["DEFAULT_DEADLINE_LEAD_TIME"] = 30
    settings.DISTRIBUTION["DEADLINE_LEAD_TIME_FOR_ADDRESSED_SERVICES"] = {
        "afb": 30,
        "aew": 10,
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
    caluma_work_item_factory,
    so_instance,
    instance_state_factory,
):
    instance_state_factory(name=so_rejection_settings["WORK_ITEM"]["INSTANCE_STATE"])

    send_event(
        post_create_work_item,
        sender="post_create_work_item",
        work_item=caluma_work_item_factory(
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
    "question_slug,value,is_solaranlage,is_reklame,is_gebaeudetechnik",
    [
        (
            "solaranlage-art-des-gesuchs",
            "solaranlage-art-des-gesuchs-solaranlage-baubewilligungspflichtig",
            True,
            False,
            False,
        ),
        (
            "reklame-art-des-gesuchs",
            "reklame-art-des-gesuchs-reklamegesuch-baubewilligungspflichtig",
            False,
            True,
            False,
        ),
        (
            "gebaeudetechnik-art-des-gesuchs",
            "gebaeudetechnik-art-des-gesuchs-gebaeudetechnik-baubewilligungspflichtig",
            False,
            False,
            True,
        ),
    ],
)
def test_convert_special_form_to_construction_permit_ur(
    db,
    caluma_work_item_factory,
    caluma_question_factory,
    caluma_answer_factory,
    caluma_document_factory,
    ur_instance,
    caluma_admin_user,
    form_factory,
    mocker,
    is_solaranlage,
    is_reklame,
    is_gebaeudetechnik,
    set_application_ur,
    question_slug,
    value,
    instance_state_factory,
    notification_template_factory,
):
    notification_template_factory(slug="3-1-dossier-angenommen")
    form = form_factory()
    mocker.patch(
        "camac.constants.kt_uri.FORM_MELDUNG_SOLARANLAGE", form.pk
    ) if is_solaranlage else (
        mocker.patch("camac.constants.kt_uri.FORM_REKLAME", form.pk)
        if is_reklame
        else mocker.patch(
            "camac.constants.kt_uri.FORM_MELDUNG_GEBAEUDETECHNIK", form.pk
        )
    )
    mocker.patch(
        "camac.constants.kt_uri.CALUMA_SPECIAL_FORM_QUESTION_VALUE_MAP",
        {
            form.pk: {
                "question": "solaranlage-art-des-gesuchs"
                if is_solaranlage
                else (
                    "reklame-art-des-gesuchs"
                    if is_reklame
                    else "gebaeudetechnik-art-des-gesuchs"
                ),
                "value": "solaranlage-art-des-gesuchs-solaranlage-baubewilligungspflichtig"
                if is_solaranlage
                else (
                    "reklame-art-des-gesuchs-reklamegesuch-baubewilligungspflichtig"
                    if is_reklame
                    else "gebaeudetechnik-art-des-gesuchs-gebaeudetechnik-baubewilligungspflichtig"
                ),
            },
        },
    )
    instance_state_factory(name="comm")

    complete_check_document = caluma_document_factory()
    ur_instance.form_id = form.pk
    ur_instance.save()
    caluma_answer_factory(
        document=complete_check_document,
        question=caluma_question_factory(
            slug="complete-check-baubewilligungspflichtig"
        ),
        value="complete-check-baubewilligungspflichtig-baubewilligungspflichtig",
    )
    caluma_answer_factory(
        document=ur_instance.case.document,
        question_id="form-type",
        value="form-type-building-permit-canton",
    )
    caluma_question_factory(
        slug=question_slug,
        type=caluma_form_models.Question.TYPE_TEXT,
    )
    complete_check_work_item = caluma_work_item_factory(
        task_id="complete-check",
        document=complete_check_document,
        case=ur_instance.case,
    )
    send_event(
        post_complete_work_item,
        sender="post_complete_work_item",
        work_item=complete_check_work_item,
        user=caluma_admin_user,
        context={},
    )
    ur_instance.refresh_from_db()
    assert (
        ur_instance.case.document.answers.get(question_id=question_slug).value == value
    )


@pytest.mark.parametrize(
    "answer,expected_status",
    [
        (
            "complete-check-vollstaendigkeitspruefung-complete",
            caluma_workflow_models.WorkItem.STATUS_READY,
        ),
        (
            "complete-check-vollstaendigkeitspruefung-incomplete-wait",
            caluma_workflow_models.WorkItem.STATUS_SUSPENDED,
        ),
        (
            "complete-check-vollstaendigkeitspruefung-reject",
            caluma_workflow_models.WorkItem.STATUS_SUSPENDED,
        ),
    ],
)
def test_suspend_circulation_based_on_complete_check(
    answer,
    expected_status,
    distribution_settings,
    caluma_admin_user,
    set_application_ur,
    caluma_work_item_factory,
    caluma_document_factory,
    caluma_answer_factory,
    caluma_question_factory,
):
    distribution_init_work_item = caluma_work_item_factory(
        task__slug=distribution_settings["DISTRIBUTION_INIT_TASK"]
    )
    complete_check_work_item = caluma_work_item_factory(
        task__slug=settings.APPLICATION["CALUMA"]["COMPLETE_CHECK_TASK"],
        document=caluma_document_factory(),
        case=distribution_init_work_item.case,
    )
    caluma_answer_factory(
        document=complete_check_work_item.document,
        question=caluma_question_factory(
            slug="complete-check-vollstaendigkeitspruefung"
        ),
        value=answer,
    )

    send_event(
        post_create_work_item,
        sender="post_create_work_item",
        work_item=distribution_init_work_item,
        user=caluma_admin_user,
        context={},
    )
    distribution_init_work_item.refresh_from_db()
    assert distribution_init_work_item.status == expected_status


def test_post_create_review_building_commission(
    caluma_case_factory,
    caluma_work_item_factory,
    caluma_document_factory,
    caluma_answer_factory,
    caluma_admin_user,
    set_application_ur,
    application_settings,
):
    caluma_case = caluma_case_factory()
    application_settings["CALUMA"]["CALUMA_WORKFLOW_NOTIFICATIONS"] = {}
    release_work_item = caluma_work_item_factory(
        task__slug="release-for-bk",
        case=caluma_case,
        document=caluma_document_factory(),
    )
    review_work_item = caluma_work_item_factory(
        task__slug="review-building-commission",
        case=caluma_case,
        document=caluma_document_factory(),
    )
    caluma_answer_factory(
        document=release_work_item.document,
        question__slug="release-for-bk-meeting-date",
        date="2023-01-01",
    )

    desired_work_item_name = f"{review_work_item.name} (BK Sitzung: 01.01.2023)"

    send_event(
        post_create_work_item,
        sender="post_create_work_item",
        work_item=review_work_item,
        user=caluma_admin_user,
        context={},
    )

    assert review_work_item.name.de == desired_work_item_name


def test_post_decision_ur(
    db,
    caluma_admin_user,
    caluma_case_factory,
    caluma_work_item_factory,
    set_application_ur,
):
    settings.APPLICATION_NAME = "kt_uri"
    caluma_case = caluma_case_factory()
    decision_work_item = caluma_work_item_factory(
        case=caluma_case, task__slug="decision"
    )
    unfinished_release_for_bk_work_item = caluma_work_item_factory(
        case=caluma_case, task__slug="release-for-bk", child_case=None
    )
    unfininished_review_building_commission_work_item = caluma_work_item_factory(
        case=caluma_case, task__slug="review-building-commission", child_case=None
    )

    post_decision_ur(
        sender="post_decision_ur",
        work_item=decision_work_item,
        user=caluma_admin_user,
        context={},
    )

    unfinished_release_for_bk_work_item.refresh_from_db()
    unfininished_review_building_commission_work_item.refresh_from_db()

    assert unfinished_release_for_bk_work_item.status == WorkItem.STATUS_SKIPPED, (
        "any open release work items need to be skipped."
    )
    assert (
        unfininished_review_building_commission_work_item.status
        == WorkItem.STATUS_SKIPPED
    ), "any open review work items need to be completed."


def test_complete_check_ur(
    db,
    caluma_work_item_factory,
    caluma_document_factory,
    caluma_answer_factory,
    mocker,
    set_application_ur,
    ur_instance,
):
    work_item = caluma_work_item_factory(
        task_id="complete-check",
        document=caluma_document_factory(),
        case=ur_instance.case,
    )
    caluma_answer_factory(
        document=work_item.document,
        question__slug="complete-check-vollstaendigkeitspruefung",
        value="complete-check-vollstaendigkeitspruefung-complete",
    )

    send_notification_mock = mocker.patch(
        "camac.caluma.extensions.events.complete_check.send_notification"
    )

    send_notification_after_complete_check(
        sender=None,
        work_item=work_item,
        user=None,
        context={},
    )

    send_notification_mock.assert_called()


def test_post_create_caluma_workflow_notifications(
    db,
    application_settings,
    ur_instance,
    caluma_document_factory,
    caluma_work_item_factory,
    mocker,
):
    application_settings["CALUMA"]["CALUMA_WORKFLOW_NOTIFICATIONS"] = {
        "send-additional-demand": [
            {
                "event": "created",
                "notification": {
                    "template_slug": "2-1-nachforderung-eingegangen",
                    "recipient_types": ["applicant"],
                },
            }
        ]
    }
    work_item = caluma_work_item_factory(
        task_id="send-additional-demand",
        document=caluma_document_factory(),
        case=ur_instance.case,
    )
    send_notification_mock = mocker.patch(
        "camac.caluma.extensions.events.caluma_workflow_notifications.send_notification"
    )

    post_create_caluma_workflow_notifications(
        sender=None, work_item=work_item, user=None, context={}
    )
    send_notification_mock.assert_called()
    assert (
        send_notification_mock.call_args[0][0]["template_slug"]
        == "2-1-nachforderung-eingegangen"
    )
    assert send_notification_mock.call_args[0][0]["recipient_types"] == ["applicant"]


def test_post_complete_caluma_workflow_notifications(
    db,
    application_settings,
    ur_instance,
    caluma_document_factory,
    caluma_work_item_factory,
    mocker,
):
    application_settings["CALUMA"]["CALUMA_WORKFLOW_NOTIFICATIONS"] = {
        "complete-distribution": [
            {
                "event": "completed",
                "notification": {
                    "template_slug": "4-3-zirkulation-abgeschlossen",
                    "recipient_types": ["applicant"],
                },
            }
        ]
    }
    work_item = caluma_work_item_factory(
        task_id="complete-distribution",
        document=caluma_document_factory(),
        case=ur_instance.case,
    )
    send_notification_mock = mocker.patch(
        "camac.caluma.extensions.events.caluma_workflow_notifications.send_notification"
    )

    post_complete_caluma_workflow_notifications(
        sender=None, work_item=work_item, user=None, context={}
    )
    send_notification_mock.assert_called()
    assert (
        send_notification_mock.call_args[0][0]["template_slug"]
        == "4-3-zirkulation-abgeschlossen"
    )
    assert send_notification_mock.call_args[0][0]["recipient_types"] == ["applicant"]


def test_post_complete_caluma_workflow_notifications_for_einfache_anfrage(
    db,
    application_settings,
    ur_instance,
    caluma_document_factory,
    caluma_work_item_factory,
    mocker,
):
    ur_instance.case.document.form = caluma_form_models.Form.objects.get(
        slug="einfache-anfrage"
    )
    ur_instance.case.document.save()
    application_settings["CALUMA"]["CALUMA_WORKFLOW_NOTIFICATIONS"] = {
        "decision": [
            {
                "event": "completed",
                "notification": {
                    "template_slug": "5-eroeffnung-stellungnahme-vorentscheid",
                    "recipient_types": [
                        "municipality_users",
                    ],
                },
                "condition": lambda work_item: send_only_for_einfache_anfrage(
                    work_item
                ),
            }
        ]
    }
    work_item = caluma_work_item_factory(
        task_id="decision",
        document=caluma_document_factory(),
        case=ur_instance.case,
    )
    send_notification_mock = mocker.patch(
        "camac.caluma.extensions.events.caluma_workflow_notifications.send_notification"
    )

    post_complete_caluma_workflow_notifications(
        sender=None, work_item=work_item, user=None, context={}
    )
    send_notification_mock.assert_called()
    assert (
        send_notification_mock.call_args[0][0]["template_slug"]
        == "5-eroeffnung-stellungnahme-vorentscheid"
    )
    assert send_notification_mock.call_args[0][0]["recipient_types"] == [
        "municipality_users"
    ]


def test_complete_rejection_work_item(
    db,
    caluma_admin_user,
    set_application_ur,
    mailoutbox,
    caluma_work_item_factory,
    instance_state_factory,
    caluma_document_factory,
    notification_template_factory,
    ur_instance,
):
    notification_template_factory(slug="2-4-dossier-zurueckgewiesen")
    instance_state_factory(name="rejected")
    reject_work_item = caluma_work_item_factory(
        task_id="reject", case=ur_instance.case, child_case=None
    )
    complete_check_work_item = caluma_work_item_factory(
        task_id="complete-check",
        document=caluma_document_factory(),
        case=ur_instance.case,
    )
    AnswerFactory(
        document=complete_check_work_item.document,
        question__slug="rejection-feedback",
        value="Test feedback",
    )

    complete_rejection_work_item(
        sender=None, work_item=reject_work_item, user=caluma_admin_user, context={}
    )
    assert len(mailoutbox) == 1

    assert ur_instance.instance_state.name == "rejected"
    assert ur_instance.rejection_feedback == "Test feedback"


def test_suspend_task_for_additional_demand(
    db,
    set_application_ur,
    ur_instance,
    caluma_admin_user,
    caluma_work_item_factory,
    caluma_document_factory,
):
    complete_check_work_item = caluma_work_item_factory(
        task_id="complete-check",
        document=caluma_document_factory(),
        case=ur_instance.case,
    )
    check_gwr_relevancy_work_item = caluma_work_item_factory(
        task_id="check-gwr-relevancy",
        document=caluma_document_factory(),
        case=ur_instance.case,
    )
    AnswerFactory(
        document=complete_check_work_item.document,
        question__slug="complete-check-vollstaendigkeitspruefung",
        value="complete-check-vollstaendigkeitspruefung-incomplete-wait",
    )
    suspend_task_for_additional_demand(
        sender=None,
        work_item=check_gwr_relevancy_work_item,
        user=caluma_admin_user,
        context={},
    )
    check_gwr_relevancy_work_item.refresh_from_db()
    assert check_gwr_relevancy_work_item.status == WorkItem.STATUS_SUSPENDED


def test_create_bab_work_item_ur(
    db,
    set_application_ur,
    caluma_admin_user,
    ur_distribution_settings,
    ur_instance,
    caluma_work_item_factory,
    caluma_document_factory,
    service,
):
    service.slug = "bab-kreis-1"
    service.save()

    inquiry_work_item = caluma_work_item_factory(
        case=ur_instance.case,
        task_id=ur_distribution_settings["INQUIRY_TASK"],
        document=caluma_document_factory(form_id="inquiry"),
        addressed_groups=[str(service.pk)],
        controlling_groups=[str(service.pk)],
    )

    bab_work_item = caluma_work_item_factory(
        case=ur_instance.case,
        task_id="bab",
        addressed_groups=[str(service.pk)],
        controlling_groups=[str(service.pk)],
        status=WorkItem.STATUS_READY,
    )

    assert bab_work_item.deadline is None

    bab.set_bab_deadline(
        sender=None, work_item=inquiry_work_item, user=caluma_admin_user
    )

    bab_work_item.refresh_from_db()
    assert bab_work_item.deadline


def test_suspend_rpg_work_item_ur(
    db,
    set_application_ur,
    caluma_admin_user,
    ur_instance,
    caluma_work_item_factory,
    service,
):
    rpg_work_item = caluma_work_item_factory(
        case=ur_instance.case,
        task_id="rpg",
        addressed_groups=[str(service.pk)],
        controlling_groups=[str(service.pk)],
        status=WorkItem.STATUS_READY,
    )
    assert rpg_work_item.status == "ready"

    bab.suspend_rpg_work_item(
        sender=None, work_item=rpg_work_item, user=caluma_admin_user
    )

    rpg_work_item.refresh_from_db()
    assert rpg_work_item.status == "suspended"


def test_resume_rpg_work_item_ur(
    db,
    set_application_ur,
    ur_distribution_settings,
    caluma_admin_user,
    ur_instance,
    caluma_document_factory,
    caluma_work_item_factory,
    service,
):
    inquiry_work_item = caluma_work_item_factory(
        case=ur_instance.case,
        task_id=ur_distribution_settings["INQUIRY_TASK"],
        document=caluma_document_factory(form_id="inquiry"),
        addressed_groups=[str(service.pk)],
        controlling_groups=[str(service.pk)],
    )
    rpg_work_item = caluma_work_item_factory(
        case=ur_instance.case,
        task_id="rpg",
        addressed_groups=[str(service.pk)],
        controlling_groups=[str(service.pk)],
        status=WorkItem.STATUS_SUSPENDED,
    )

    assert rpg_work_item.status == "suspended"

    bab.resume_rpg_work_item(
        sender=None, work_item=inquiry_work_item, user=caluma_admin_user
    )

    rpg_work_item.refresh_from_db()
    assert rpg_work_item.status == "ready"


@pytest.mark.parametrize(
    ("ignore_addressed_self", "expected"),
    [(False, 1), (True, 0)],
)
def test_notify_manual_work_item_ignore_addressed_self(
    db,
    caluma_admin_user,
    service_factory,
    gr_instance,
    caluma_work_item_factory,
    mailoutbox,
    application_settings,
    notification_template_factory,
    ignore_addressed_self,
    expected,
):
    notification_template = notification_template_factory()
    application_settings["CALUMA"]["CALUMA_WORKFLOW_NOTIFICATIONS"][
        "create-manual-workitems"
    ] = [
        {
            "event": "created",
            "notification": {
                "template_slug": notification_template.slug,
                "recipient_types": ["work_item_addressed"],
            },
            "condition": lambda work_item: should_notify_on_manual_workitems(
                work_item,
                ignore_addressed_self=ignore_addressed_self,
            ),
        },
    ]

    controlling_service = service_factory()
    addressed_service = service_factory()

    deadline = timezone.now()

    caluma_work_item_factory(
        task_id=application_settings["CALUMA"]["MANUAL_WORK_ITEM_TASK"],
        status="ready",
        deadline=deadline,
        case=gr_instance.case,
    )
    work_item_addressed_self = caluma_work_item_factory(
        task_id=application_settings["CALUMA"]["MANUAL_WORK_ITEM_TASK"],
        status="ready",
        created_by_group=addressed_service.pk,
        addressed_groups=[str(addressed_service.pk)],
        controlling_groups=[str(controlling_service.pk)],
        child_case=None,
        deadline=deadline,
        meta={
            "notify-completed": True,
            "notify-deadline": True,
        },
        case=gr_instance.case,
    )

    send_event(
        post_create_work_item,
        sender="test_notify_created_work_item",
        work_item=work_item_addressed_self,
        user=caluma_admin_user,
        context={},
    )
    assert len(mailoutbox) == expected
    if expected > 0:
        assert mailoutbox[0].recipients()[0] == addressed_service.email


def test_post_resume_inquiry_ur(
    db,
    set_application_ur,
    ur_distribution_settings,
    disable_ech0211_settings,
    service,
    ur_instance,
    caluma_admin_user,
    caluma_work_item_factory,
    notification_template_factory,
    instance_state_factory,
):
    work_item = caluma_work_item_factory(
        task_id="inquiry",
        case=ur_instance.case,
        addressed_groups=[service.pk],
        controlling_groups=[service.pk],
    )
    work_item.document.answers.create(
        question_id="inquiry-deadline", date=date(2026, 4, 8)
    )
    notification_template_factory(slug="4-1-zirkulation-gemeinde-gestartet")

    ur_instance.previous_instance_state = instance_state_factory(name="nfd")
    ur_instance.instance_state = instance_state_factory(name="circ")
    ur_instance.save()

    distribution.post_resume_inquiry(
        sender=None, work_item=work_item, user=caluma_admin_user
    )
    ur_instance.refresh_from_db()

    assert ur_instance.instance_state.name == "nfd"
