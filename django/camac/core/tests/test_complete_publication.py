import pytest
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import models as caluma_workflow_models
from django.core.management import call_command
from django.utils.timezone import now


@pytest.fixture
def publication_work_item(db, caluma_publication, caluma_admin_user, case_factory):
    document = caluma_form_models.Document.objects.create(
        form=caluma_form_models.Form.objects.get(pk="publikation")
    )

    document.answers.create(question_id="publikation-startdatum", date=now())
    document.answers.create(question_id="publikation-ablaufdatum", date=now())

    return caluma_workflow_models.WorkItem.objects.create(
        case=case_factory(),
        task=caluma_workflow_models.Task.objects.get(pk="fill-publication"),
        deadline=None,
        status=caluma_workflow_models.WorkItem.STATUS_READY,
        document=document,
    )


@pytest.mark.parametrize(
    "has_ablaufdatum,expected_status",
    [
        (True, caluma_workflow_models.WorkItem.STATUS_COMPLETED),
        (False, caluma_workflow_models.WorkItem.STATUS_READY),
    ],
)
def test_complete_publication(publication_work_item, has_ablaufdatum, expected_status):
    if not has_ablaufdatum:
        publication_work_item.document.answers.filter(
            question_id="publikation-ablaufdatum"
        ).delete()

    call_command("complete_publication")

    publication_work_item.refresh_from_db()

    assert publication_work_item.status == expected_status
