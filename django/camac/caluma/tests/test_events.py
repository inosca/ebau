import pytest
from caluma.caluma_core.events import send_event
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from caluma.caluma_workflow.events import (
    post_complete_work_item,
    post_create_work_item,
    post_skip_work_item,
)
from django.conf import settings
from django.utils import timezone

from camac.constants.kt_bern import (
    DECISION_TYPE_BUILDING_PERMIT,
    DECISION_TYPE_CONSTRUCTION_TEE_WITH_RESTORATION,
    DECISIONS_ABGELEHNT,
    DECISIONS_BEWILLIGT,
)
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
):
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
            decision_factory(decision=DECISIONS_BEWILLIGT)

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
):
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
            decision_factory(decision=DECISIONS_BEWILLIGT)

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
):

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

    decision_factory(decision=DECISIONS_BEWILLIGT)

    workflow_api.complete_work_item(
        work_item=be_instance.case.work_items.get(task_id="decision"),
        user=caluma_admin_user,
    )
    assert (
        len(be_instance.tags.filter(service__trans__name="Baukontrolle Kirchberg")) == 1
    )


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
):
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
            decision_factory(decision=DECISIONS_BEWILLIGT)

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


def test_set_is_published(
    caluma_admin_user,
    application_settings,
    work_item_factory,
    service_factory,
    task_factory,
):
    application_settings["CALUMA"]["FILL_PUBLICATION_TASK"] = "fill-publication"

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
    "workflow,decision,decision_type,expected_instance_state,expected_text",
    [
        (
            "building-permit",
            DECISIONS_BEWILLIGT,
            DECISION_TYPE_BUILDING_PERMIT,
            "sb1",
            "Bauentscheid verfügt",
        ),
        (
            "building-permit",
            DECISIONS_ABGELEHNT,
            DECISION_TYPE_BUILDING_PERMIT,
            "finished",
            "Bauentscheid verfügt",
        ),
        (
            "building-permit",
            DECISIONS_ABGELEHNT,
            DECISION_TYPE_CONSTRUCTION_TEE_WITH_RESTORATION,
            "sb1",
            "Bauentscheid verfügt",
        ),
        (
            "migrated",
            DECISIONS_BEWILLIGT,
            DECISION_TYPE_BUILDING_PERMIT,
            "finished",
            "Beurteilung abgeschlossen",
        ),
        (
            "preliminary-clarification",
            DECISIONS_BEWILLIGT,
            DECISION_TYPE_BUILDING_PERMIT,
            "evaluated",
            "Beurteilung abgeschlossen",
        ),
        (
            "internal",
            DECISIONS_BEWILLIGT,
            DECISION_TYPE_BUILDING_PERMIT,
            "finished_internal",
            "Beurteilung abgeschlossen",
        ),
    ],
)
def test_complete_decision(
    db,
    be_instance,
    caluma_admin_user,
    application_settings,
    mailoutbox,
    group,
    role,
    instance_service_factory,
    notification_template,
    service_factory,
    work_item_factory,
    instance_state_factory,
    workflow,
    decision,
    decision_type,
    expected_instance_state,
    expected_text,
    multilang,
    use_instance_service,
    decision_factory,
):

    instance_state_factory(name=expected_instance_state)

    instance_service_factory(
        instance=be_instance,
        service=service_factory(
            trans__name="Leitbehörde Bern",
            trans__language="de",
            service_group__name="municipality",
        ),
        active=1,
    )

    construction_control = service_factory(
        trans__name="Baukontrolle Bern",
        trans__language="de",
        service_group__name="construction-control",
    )

    work_item = work_item_factory(case=be_instance.case, task_id="decision")

    application_settings["CALUMA"]["DECISION_TASK"] = work_item.task_id
    application_settings["NOTIFICATIONS"] = {
        "DECISION": [
            {
                "template_slug": notification_template.slug,
                "recipient_types": ["applicant"],
            }
        ],
        "DECISION_PRELIMINARY_CLARIFICATION": [
            {
                "template_slug": notification_template.slug,
                "recipient_types": ["applicant"],
            }
        ],
    }

    be_instance.case.workflow = caluma_workflow_models.Workflow.objects.get(pk=workflow)
    be_instance.case.save()

    decision_factory(decision=decision, decision_type=decision_type)

    if workflow == "internal":
        work_item_factory(case=be_instance.case)
        application_settings["CALUMA"]["EBAU_NUMBER_TASK"] = work_item.task_id

    send_event(
        post_complete_work_item,
        sender="post_complete_work_item",
        work_item=work_item,
        user=caluma_admin_user,
        context={},
    )

    be_instance.refresh_from_db()

    assert be_instance.instance_state.name == expected_instance_state
    assert len(mailoutbox) == 1
    assert HistoryEntryT.objects.filter(
        history_entry__instance=be_instance, title=expected_text, language="de"
    ).exists()

    if expected_instance_state == "sb1":
        assert be_instance.responsible_service() == construction_control


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
