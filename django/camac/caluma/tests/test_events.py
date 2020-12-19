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

from camac.constants.kt_bern import DECISIONS_ABGELEHNT, DECISIONS_BEWILLIGT
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
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )

    docx_decision_factory(decision=DECISIONS_BEWILLIGT, instance=instance.pk)

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
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )

    docx_decision_factory(decision=DECISIONS_BEWILLIGT, instance=instance.pk)

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


@pytest.mark.freeze_time("2020-08-11")
@pytest.mark.parametrize("application_name", ["kt_bern", "kt_schwyz"])
@pytest.mark.parametrize("notify_completed", [True, False])
def test_notify_completed_work_item(
    db,
    caluma_admin_user,
    service_factory,
    user_factory,
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
        services = service_factory.create_batch(2)
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
        "camac-instance-id": 1,
        "ebau-number": "2020-01",
    }
    work_item.case.save()

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
        meta={"camac-instance-id": circulation.instance.pk},
    )

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
    "has_addressed_groups,service_exists,expected_users",
    [(False, False, 0), (False, True, 0), (True, False, 0), (True, True, 1)],
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
    service_exists,
    expected_users,
    application_name,
):
    service = None
    addressed_groups = []
    assigned_users = [user_factory().username] if has_assigned_users else []

    if service_exists:
        if application_name == "kt_bern":
            service = responsible_service_factory(
                instance=instance, responsible_user=user
            ).service
        else:
            service = instance_responsibility_factory(
                instance=instance, user=user
            ).service

    if has_addressed_groups:
        addressed_groups = [service.pk] if service else [123]

    work_item = work_item_factory(
        addressed_groups=addressed_groups, assigned_users=assigned_users
    )
    case = work_item.case
    case.meta["camac-instance-id"] = str(instance.pk)
    case.save()

    send_event(
        post_create_work_item,
        sender="test_set_assigned_user",
        work_item=work_item,
        user=caluma_admin_user,
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
    case.meta["camac-instance-id"] = str(instance.pk)
    case.save()

    if process_type == "skip":
        send_event(
            post_skip_work_item,
            sender="post_skip_work_item",
            work_item=work_item,
            user=caluma_admin_user,
        )
    elif process_type == "complete":
        send_event(
            post_complete_work_item,
            sender="post_complete_work_item",
            work_item=work_item,
            user=caluma_admin_user,
        )

    assert (
        HistoryEntryT.objects.filter(history_entry__instance=instance, language="de")
        .first()
        .title
        == expected_text
    )


@pytest.mark.parametrize("role__name", ["Support"])
@pytest.mark.parametrize(
    "workflow,decision,expected_instance_state,expected_text",
    [
        ("building-permit", DECISIONS_BEWILLIGT, "sb1", "Bauentscheid verfügt"),
        ("building-permit", DECISIONS_ABGELEHNT, "finished", "Bauentscheid verfügt"),
        ("migrated", DECISIONS_BEWILLIGT, "finished", "Beurteilung abgeschlossen"),
        (
            "preliminary-clarification",
            DECISIONS_BEWILLIGT,
            "evaluated",
            "Beurteilung abgeschlossen",
        ),
        (
            "internal",
            DECISIONS_BEWILLIGT,
            "finished_internal",
            "Beurteilung abgeschlossen",
        ),
    ],
)
def test_complete_decision(
    db,
    instance,
    caluma_admin_user,
    application_settings,
    mailoutbox,
    group,
    role,
    instance_service_factory,
    notification_template,
    service_factory,
    docx_decision_factory,
    workflow_factory,
    work_item_factory,
    instance_state_factory,
    notification_template_factory,
    workflow,
    decision,
    expected_instance_state,
    expected_text,
    multilang,
):
    docx_decision_factory(decision=decision, instance=instance.pk)
    instance_state_factory(name=expected_instance_state)

    instance_service_factory(
        instance=instance,
        service=service_factory(
            trans__name="Leitbehörde Bern",
            trans__language="de",
            service_group__name="municipality",
        ),
        active=1,
    )

    service_factory(
        trans__name="Baukontrolle Bern",
        trans__language="de",
        service_group__name="construction-control",
    )

    work_item = work_item_factory()
    case = work_item.case

    application_settings["CALUMA"]["DECISION_TASK"] = work_item.task_id
    application_settings["NOTIFICATIONS"] = {
        "DECISION": [
            {
                "template_slug": notification_template.slug,
                "recipient_types": ["applicant"],
            }
        ]
    }

    case.workflow = workflow_factory(slug=workflow)
    case.meta["camac-instance-id"] = str(instance.pk)
    case.save()

    if workflow == "internal":
        work_item_factory(case=case)
        application_settings["CALUMA"]["EBAU_NUMBER_TASK"] = work_item.task_id

    send_event(
        post_complete_work_item,
        sender="post_complete_work_item",
        work_item=work_item,
        user=caluma_admin_user,
        context={"group_id": group.pk},
    )

    instance.refresh_from_db()

    assert instance.instance_state.name == expected_instance_state
    assert len(mailoutbox) == 1
    assert HistoryEntryT.objects.filter(
        history_entry__instance=instance, title=expected_text, language="de"
    ).exists()


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
    db,
    instance,
    caluma_admin_user,
    caluma_config_be,
    group,
    role,
    multilang,
    instance_state_factory,
    work_item_factory,
    task_factory,
    task,
    expected_instance_state,
    expected_history_text,
):
    work_item = work_item_factory(task=task_factory(slug=task))
    instance_state = instance_state_factory(name=expected_instance_state)

    case = work_item.case
    case.meta["camac-instance-id"] = str(instance.pk)
    case.save()

    send_event(
        post_complete_work_item,
        sender="post_complete_work_item",
        work_item=work_item,
        user=caluma_admin_user,
        context={"group_id": group.pk},
    )

    instance.refresh_from_db()

    assert instance.instance_state == instance_state
    assert HistoryEntryT.objects.filter(
        history_entry__instance=instance,
        title=expected_history_text,
        language="de",
    ).exists()
