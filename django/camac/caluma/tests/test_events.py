import faker
import pytest
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from django.utils import timezone


@pytest.mark.parametrize("expected_value", ["papierdossier-ja", "papierdossier-nein"])
def test_copy_papierdossier(
    db, instance_factory, caluma_admin_user, caluma_workflow, expected_value
):
    instance = instance_factory()

    case = workflow_api.start_case(
        workflow=caluma_workflow_models.Workflow.objects.get(pk="building-permit"),
        form=caluma_form_models.Form.objects.get(pk="main-form"),
        meta={"camac-instance-id": instance.pk},
        user=caluma_admin_user,
    )

    case.document.answers.create(question_id="papierdossier", value=expected_value)

    # complete submit which creates nfd and ebau-number work items
    workflow_api.complete_work_item(
        work_item=case.work_items.get(task_id="submit"), user=caluma_admin_user
    )

    assert (
        case.work_items.get(task_id="nfd")
        .document.answers.get(question_id="papierdossier")
        .value
        == expected_value
    )

    # complete nfd and ebau-number which creates the sb1 work item
    workflow_api.complete_work_item(
        work_item=case.work_items.get(task_id="ebau-number"), user=caluma_admin_user
    )
    workflow_api.complete_work_item(
        work_item=case.work_items.get(task_id="nfd"), user=caluma_admin_user
    )

    assert (
        case.work_items.get(task_id="sb1")
        .document.answers.get(question_id="papierdossier")
        .value
        == expected_value
    )

    # complete sb1 which creates the sb2 work item
    workflow_api.complete_work_item(
        work_item=case.work_items.get(task_id="sb1"), user=caluma_admin_user
    )

    assert (
        case.work_items.get(task_id="sb2")
        .document.answers.get(question_id="papierdossier")
        .value
        == expected_value
    )


@pytest.mark.parametrize("use_fallback", [True, False])
def test_copy_sb_personalien(
    db, instance_factory, caluma_admin_user, caluma_workflow, use_fallback
):
    instance = instance_factory()

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

    workflow_api.complete_work_item(
        work_item=case.work_items.get(task_id="submit"), user=caluma_admin_user
    )
    workflow_api.complete_work_item(
        work_item=case.work_items.get(task_id="ebau-number"), user=caluma_admin_user
    )
    workflow_api.complete_work_item(
        work_item=case.work_items.get(task_id="nfd"), user=caluma_admin_user
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
