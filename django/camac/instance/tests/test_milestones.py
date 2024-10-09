from datetime import datetime

import pytest
from caluma.caluma_workflow.factories import WorkItemFactory
from caluma.caluma_workflow.models import WorkItem
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from camac.constants import kt_uri as uri_constants
from camac.instance.milestones.serializers import (
    UrMilestonesSerializer,
    _check_feedback_answer,
    _get_date_of_downloaded_decision_document,
    _get_decision_work_item_closed_at,
)


@pytest.mark.parametrize(
    "role__name",
    [
        ("Sekretariat der Gemeindebaubehörde"),
    ],
)
@pytest.mark.parametrize(
    "is_paper_answer,complete_check_outcome,open_additional_demands",
    [
        ("is-paper-no", "complete-check-vollstaendigkeitspruefung-complete", False),
        ("is-paper-yes", "complete-check-vollstaendigkeitspruefung-complete", False),
        ("is-paper-no", "complete-check-vollstaendigkeitspruefung-incomplete", True),
        ("is-paper-no", "complete-check-vollstaendigkeitspruefung-incomplete", False),
    ],
)
@pytest.mark.freeze_time("2023-12-31")
@pytest.mark.parametrize("receipt_confirmation_of_decision_documents", [True, False])
@pytest.mark.django_db(
    transaction=True, reset_sequences=True
)  # always reset instance id
def test_milestones_ur(
    db,
    role,
    admin_client,
    ur_instance,
    ur_distribution_settings,
    settings,
    application_settings,
    snapshot,
    answer_factory,
    document_factory,
    publication_entry_factory,
    attachment_factory,
    attachment_download_history_factory,
    workflow_entry_factory,
    workflow_item_factory,
    receipt_confirmation_of_decision_documents,
    set_application_ur,
    is_paper_answer,
    complete_check_outcome,
    open_additional_demands,
):
    answer_factory(
        document=ur_instance.case.document,
        question_id="is-paper",
        value=is_paper_answer,
    )

    submit_task = ur_instance.case.work_items.get(task_id="submit")
    submit_task.closed_at = timezone.make_aware(datetime(2023, 1, 1, 20, 0, 0))
    submit_task.status = WorkItem.STATUS_COMPLETED
    submit_task.save()

    complete_check_work_item = WorkItemFactory(
        task_id="complete-check",
        case=ur_instance.case,
        closed_at=timezone.make_aware(datetime(2023, 1, 1, 20, 0, 0)),
        status=WorkItem.STATUS_COMPLETED,
        document=document_factory(form_id="complete-check"),
    )
    answer_factory(
        document=complete_check_work_item.document,
        question__slug="complete-check-vollstaendigkeitspruefung",
        value=complete_check_outcome,
    )
    WorkItemFactory(
        task_id="check-additional-demand",
        case=ur_instance.case,
        closed_at=timezone.make_aware(datetime(2023, 1, 1, 20, 0, 0)),
        status=WorkItem.STATUS_READY
        if open_additional_demands
        else WorkItem.STATUS_COMPLETED,
    )
    decision_work_item = WorkItemFactory(
        task_id="decision",
        case=ur_instance.case,
        closed_at=timezone.make_aware(datetime(2023, 1, 1, 20, 0, 0)),
        status=WorkItem.STATUS_COMPLETED,
    )
    WorkItemFactory(
        task_id="init-distribution",
        case=ur_instance.case,
        meta={"migrated-at": "2024-9-27"},
        status=WorkItem.STATUS_READY,
        closed_at=timezone.make_aware(datetime(2024, 1, 1, 20, 0, 0)),
    )

    # migrated workflow entry dates
    workflow_entry_factory(
        workflow_item=workflow_item_factory(name="Bau- und Einspracheentscheid"),
        workflow_date=timezone.make_aware(datetime(2024, 1, 1)),
        instance=ur_instance,
    )
    workflow_entry_factory(
        workflow_item=workflow_item_factory(name="Einsprachefrist"),
        workflow_date=timezone.make_aware(datetime(2024, 1, 1)),
        instance=ur_instance,
    )
    workflow_entry_factory(
        workflow_item=workflow_item_factory(
            name="Versand / Stellungnahme - Vorentscheid per Post"
        ),
        workflow_date=timezone.make_aware(datetime(2024, 1, 1)),
        instance=ur_instance,
    )
    workflow_entry_factory(
        workflow_item=workflow_item_factory(
            name="Versand / Stellungnahme - Vorentscheid per Mail"
        ),
        workflow_date=timezone.make_aware(datetime(2024, 1, 1)),
        instance=ur_instance,
    )
    workflow_entry_factory(
        workflow_item=workflow_item_factory(name="Versand Entscheiddokumente per Post"),
        workflow_date=timezone.make_aware(datetime(2024, 1, 1)),
        instance=ur_instance,
    )
    workflow_entry_factory(
        workflow_item=workflow_item_factory(
            name="Versand Entscheiddokumente per Portal"
        ),
        workflow_date=timezone.make_aware(datetime(2024, 1, 1)),
        instance=ur_instance,
    )
    workflow_entry_factory(
        workflow_item=workflow_item_factory(name="Versand Entscheiddokumente per Mail"),
        workflow_date=timezone.make_aware(datetime(2024, 1, 1)),
        instance=ur_instance,
    )
    workflow_entry_factory(
        workflow_item=workflow_item_factory(name="Meldung Baubewilligung an Geometer"),
        workflow_date=timezone.make_aware(datetime(2024, 1, 1)),
        instance=ur_instance,
    )
    workflow_entry_factory(
        workflow_item=workflow_item_factory(name="Weiterleitung an Koord"),
        workflow_date=timezone.make_aware(datetime(2024, 1, 1)),
        instance=ur_instance,
    )
    workflow_entry_factory(
        workflow_item=workflow_item_factory(name="Baubeginn erfolgt"),
        workflow_date=timezone.make_aware(datetime(2024, 1, 1)),
        instance=ur_instance,
    )
    workflow_entry_factory(
        workflow_item=workflow_item_factory(name="Abnahme Schnurgerüst"),
        workflow_date=timezone.make_aware(datetime(2024, 1, 1)),
        instance=ur_instance,
    )
    workflow_entry_factory(
        workflow_item=workflow_item_factory(name="Abnahme Rohbau"),
        workflow_date=timezone.make_aware(datetime(2024, 1, 1)),
        instance=ur_instance,
    )
    workflow_entry_factory(
        workflow_item=workflow_item_factory(name="Bau beendet"),
        workflow_date=timezone.make_aware(datetime(2024, 1, 1)),
        instance=ur_instance,
    )
    workflow_entry_factory(
        workflow_item=workflow_item_factory(name="Endabnahme erfolgt"),
        workflow_date=timezone.make_aware(datetime(2024, 1, 1)),
        instance=ur_instance,
    )
    workflow_entry_factory(
        workflow_item=workflow_item_factory(name="Dossier archiviert"),
        workflow_date=timezone.make_aware(datetime(2024, 1, 1)),
        instance=ur_instance,
    )

    # top level circulation (Gemeinde -> KOOR)
    WorkItemFactory(
        task_id="inquiry",
        case=ur_instance.case,
        created_at=timezone.make_aware(datetime(2023, 1, 1, 20, 0, 0)),
        addressed_groups=[uri_constants.KOOR_BG_SERVICE_ID],
        controlling_groups=[],
        status=WorkItem.STATUS_COMPLETED,
        closed_at=timezone.make_aware(datetime(2023, 1, 1, 20, 0, 0)),
    )

    # Nested KOOR circulation
    WorkItemFactory(
        task_id="inquiry",
        case=ur_instance.case,
        created_at=timezone.make_aware(datetime(2023, 1, 1, 20, 0, 0)),
        controlling_groups=[uri_constants.KOOR_BG_SERVICE_ID],
        status=WorkItem.STATUS_COMPLETED,
        closed_at=timezone.make_aware(datetime(2023, 1, 1, 20, 0, 0)),
    )

    # Forwarding to KOOR
    WorkItemFactory(
        task_id="fill-inquiry",
        case=ur_instance.case,
        created_at=timezone.make_aware(datetime(2024, 8, 30, 20, 0, 0)),
        addressed_groups=[uri_constants.KOOR_BG_SERVICE_ID],
        status=WorkItem.STATUS_READY,
    )

    # Publication
    publication_entry_factory(
        publication_date=timezone.now(),
        instance=ur_instance,
    )

    # Receipt confirmations
    if receipt_confirmation_of_decision_documents:
        answer_factory(
            document=decision_work_item.document,
            question__slug="decision-task-feedback-type",
            value="decision-task-feedback-type-bau-und-einspracheentscheid",
        )
    else:
        answer_factory(
            document=decision_work_item.document,
            question__slug="decision-task-feedback-type",
            value="decision-task-feedback-type-stellungnahme-vorentscheid",
        )

    attachment = attachment_factory(instance=ur_instance, context={"isDecision": True})
    attachment_download_history_factory(attachment=attachment, date_time=timezone.now())

    url = reverse("instance-milestones", args=[ur_instance.pk])
    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.json())


@pytest.mark.freeze_time("2024-08-29")
def test_get_date_of_downloaded_decision_document(
    db,
    attachment_factory,
    attachment_download_history_factory,
    instance_factory,
    case_factory,
):
    instance = instance_factory(case=case_factory())
    attachment = attachment_factory(instance=instance, context={"isDecision": True})
    attachment_download_history_factory(attachment=attachment, date_time=timezone.now())
    assert _get_date_of_downloaded_decision_document(instance) == timezone.now()


def test_check_feedback_answer(
    db, work_item_factory, answer_factory, instance_factory, case_factory
):
    instance = instance_factory(case=case_factory())
    decision_work_item = work_item_factory(task__slug="decision", case=instance.case)
    answer_factory(
        document=decision_work_item.document,
        question__slug="decision-task-feedback-type",
        value="decision-task-feedback-type-bau-und-einspracheentscheid",
    )
    instance._all_work_items = [decision_work_item]
    assert _check_feedback_answer(
        instance, "decision-task-feedback-type-bau-und-einspracheentscheid"
    )
    assert not _check_feedback_answer(instance, "wrong-slug")


@pytest.mark.freeze_time("2024-08-29")
def test_decision_work_item_closed_at(
    db, work_item_factory, case_factory, instance_factory
):
    instance = instance_factory(case=case_factory())
    decision_work_item = work_item_factory(
        task__slug="decision",
        case=instance.case,
        status="completed",
        closed_at=timezone.now(),
    )
    instance._all_work_items = [decision_work_item]
    assert _get_decision_work_item_closed_at(instance) == timezone.now()


@pytest.mark.freeze_time("2024-08-29")
def test_get_publication_date(
    db, publication_entry_factory, instance_factory, case_factory
):
    instance = instance_factory(case=case_factory())
    publication_entry_factory(
        publication_date=timezone.now(),
        instance=instance,
    )
    serializer = UrMilestonesSerializer(instance)
    assert serializer.get_publication_date(instance) == timezone.now()
