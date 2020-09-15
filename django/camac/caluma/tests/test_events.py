import faker
import pytest
from caluma.caluma_core.events import send_event
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from caluma.caluma_workflow.events import post_create_work_item
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from pytest_factoryboy import LazyFixture


@pytest.mark.parametrize("expected_value", ["papierdossier-ja", "papierdossier-nein"])
def test_copy_papierdossier(
    db,
    instance,
    instance_service,
    caluma_admin_user,
    caluma_workflow_config_be,
    expected_value,
    circulation,
):
    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )

    case.document.answers.create(question_id="papierdossier", value=expected_value)

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
            .document.answers.get(question_id="papierdossier")
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
):
    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )

    case.document.answers.create(
        question_id="papierdossier", value="papierdossier-nein"
    )

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
    notify_completed,
):
    excluded = set()

    if application_name == "kt_bern":
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
            {"not-viewed": True, "notify-deadline": True, "notify-completed": True},
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
                "notify-completed": True,
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
                "notify-completed": True,
                "activation-id": 123,
            },
        ),
        (
            "activation",
            {},
            {},
            {"not-viewed": True, "notify-deadline": True, "notify-completed": True},
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
