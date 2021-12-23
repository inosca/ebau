import faker
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
from django.urls import reverse
from django.utils import timezone
from pytest_factoryboy import LazyFixture

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
    instance,
    instance_service,
    caluma_admin_user,
    caluma_workflow_config_be,
    expected_value,
    circulation,
    docx_decision_factory,
):
    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        user=caluma_admin_user,
    )
    instance.case = case
    instance.save()

    docx_decision_factory(decision=DECISIONS_BEWILLIGT, instance=instance)

    case.document.answers.create(question_id="is-paper", value=expected_value)

    for task_id in [
        "submit",
        "ebau-number",
        "publication",
        "audit",
        "init-circulation",
        "circulation",
        "start-decision",
        "decision",
        "sb1",
    ]:
        # skip case to sb2
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
    instance,
    instance_service,
    caluma_admin_user,
    caluma_workflow_config_be,
    use_fallback,
    circulation,
    docx_decision_factory,
):
    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        user=caluma_admin_user,
    )
    instance.case = case
    instance.save()

    docx_decision_factory(decision=DECISIONS_BEWILLIGT, instance=instance)

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
        "publication",
        "audit",
        "init-circulation",
        "circulation",
        "start-decision",
        "decision",
    ]:
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


@pytest.mark.parametrize(
    "bewilligungspflichtig_hidden,expect_copy", [("true", True), ("false", False)]
)
def test_copy_tank_installation(
    db,
    instance,
    caluma_admin_user,
    caluma_workflow_config_be,
    docx_decision_factory,
    question_factory,
    form_question_factory,
    bewilligungspflichtig_hidden,
    expect_copy,
):
    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        user=caluma_admin_user,
    )
    instance.case = case
    instance.save()

    docx_decision_factory(decision=DECISIONS_BEWILLIGT, instance=instance)

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
        "init-circulation",
        "circulation",
        "start-decision",
        "decision",
        "sb1",
    ]:
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


@pytest.mark.freeze_time("2020-08-11")
@pytest.mark.parametrize("application_name", ["kt_bern", "kt_schwyz"])
@pytest.mark.parametrize("notify_completed", [True, False])
def test_notify_completed_work_item(
    db,
    caluma_admin_user,
    service_factory,
    user_factory,
    instance,
    work_item_factory,
    mailoutbox,
    snapshot,
    application_name,
    application_settings,
    notify_completed,
):
    excluded = set()

    if application_name == "kt_bern":
        application_settings["IS_MULTILINGUAL"] = True
        application_settings["HAS_EBAU_NUMBER"] = True

        services = service_factory.create_batch(6)

        for serv in services[:3]:
            serv.notification = False
            serv.save()
            excluded.add(serv.email)

    if application_name == "kt_schwyz":
        application_settings["HAS_GESUCHSNUMMER"] = True
        services = service_factory.create_batch(2)
        instance.identifier = "72-21-001"
        instance.save()
        fake = faker.Faker()
        for i, serv in enumerate(services):
            emails = [fake.email() for _ in range(3)]
            serv.email = ",".join(emails)

            if i == 0:
                serv.notification = False
                excluded = set(emails)

            serv.save()

    work_item = work_item_factory(
        status="ready",
        controlling_groups=[str(service.pk) for service in services],
        child_case=None,
        deadline=timezone.now(),
        meta={"notify-completed": notify_completed},
    )

    work_item.case.meta = {
        **work_item.case.meta,
        "ebau-number": "2020-01",
    }
    work_item.case.save()

    instance.pk = 1
    instance.case = work_item.case
    instance.save()

    caluma_admin_user.group = str(services[0].pk)

    workflow_api.complete_work_item(work_item, user=caluma_admin_user)

    if not notify_completed:
        assert len(mailoutbox) == 0
    else:
        assert len(mailoutbox) == 3
        assert not excluded.intersection(set(mail.to[0] for mail in mailoutbox))
        snapshot.assert_match(
            [(mail.subject, mail.body, mail.to, mail.cc) for mail in mailoutbox]
        )


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
    "role__name,instance__user", [("Municipality", LazyFixture("admin_user"))]
)
def test_complete_case(
    caluma_admin_user,
    admin_client,
    instance_service,
    circulation,
    activation_factory,
    caluma_workflow_config_be,
):
    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        user=caluma_admin_user,
    )
    circulation.instance.case = case
    circulation.instance.save()

    for task_id in ["submit", "ebau-number", "init-circulation"]:
        workflow_api.skip_work_item(
            case.work_items.get(task_id=task_id),
            user=caluma_admin_user,
            context={"circulation-id": circulation.pk},
        )

    circulation_work_item = case.work_items.get(
        **{"task_id": "circulation", "meta__circulation-id": circulation.pk}
    )

    activation = activation_factory(circulation=circulation)

    admin_client.patch(reverse("circulation-sync", args=[circulation.pk]))

    circulation_work_item.refresh_from_db()
    activation_work_item = circulation_work_item.child_case.work_items.get(
        **{"task_id": "activation", "meta__activation-id": activation.pk}
    )

    workflow_api.complete_work_item(activation_work_item, caluma_admin_user)

    circulation_work_item.child_case.refresh_from_db()
    assert (
        circulation_work_item.child_case.status
        == caluma_workflow_models.Case.STATUS_COMPLETED
    )


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
        (
            "circulation",
            {},
            {"circulation-id": 123},
            {
                "not-viewed": True,
                "notify-deadline": True,
                "notify-completed": False,
                "circulation-id": 123,
            },
        ),
        (
            "activation",
            {},
            {"activation-id": 123},
            {
                "not-viewed": True,
                "notify-deadline": True,
                "notify-completed": False,
                "activation-id": 123,
            },
        ),
        (
            "activation",
            {},
            {},
            {"not-viewed": True, "notify-deadline": True, "notify-completed": False},
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
    application_settings["CALUMA"] = {
        "CIRCULATION_TASK": "circulation",
        "ACTIVATION_TASKS": ["activation"],
    }

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
    activation,
    service_factory,
    docx_decision_factory,
    work_item_factory,
    instance_state_factory,
    workflow,
    decision,
    decision_type,
    expected_instance_state,
    expected_text,
    multilang,
    use_instance_service,
):
    docx_decision_factory(
        decision=decision, decision_type=decision_type, instance=be_instance
    )
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

    work_item = work_item_factory(case=be_instance.case)

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
    [
        ("start-decision", "coordination", "Zirkulation abgeschlossen"),
        ("skip-circulation", "coordination", "Zirkulation übersprungen"),
        ("reopen-circulation", "circulation", "Zirkulation wiedereröffnet"),
        ("complete", "finished", "Baugesuchsverfahren abgeschlossen"),
    ],
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
