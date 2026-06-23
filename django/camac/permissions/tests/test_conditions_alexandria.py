import pytest
from caluma.caluma_workflow.models import WorkItem

from camac.alexandria.permissions import AlexandriaPermissionContext
from camac.settings.modules.permissions.alexandria.conditions import HasAdditionalDemand


@pytest.mark.django_db
def test_has_additional_demand_condition(
    additional_demand_settings,
    alexandria_document_factory,
    be_instance,
    caluma_work_item_factory,
    userinfo,
):
    condition = HasAdditionalDemand()
    task_id = additional_demand_settings["FILL_TASK"]

    # Create a completed additional demand and a document that should not grant
    # any permissions
    completed_wi = caluma_work_item_factory(
        task_id=task_id,
        case__family=be_instance.case,
        status=WorkItem.STATUS_COMPLETED,
    )
    completed_doc = alexandria_document_factory(
        metainfo={
            "camac-instance-id": be_instance.pk,
            "caluma-document-id": str(completed_wi.document_id),
        },
    )

    create_context = AlexandriaPermissionContext.from_instance(be_instance)
    completed_doc_context = AlexandriaPermissionContext.from_document(completed_doc)

    assert not condition.apply(userinfo, create_context)
    assert not condition.apply(userinfo, completed_doc_context)

    # Create a ready additional demand and a document that SHOULD grant
    # permissions
    ready_wi = caluma_work_item_factory(
        task_id=task_id,
        case__family=be_instance.case,
        status=WorkItem.STATUS_READY,
    )
    ready_doc = alexandria_document_factory(
        metainfo={
            "camac-instance-id": be_instance.pk,
            "caluma-document-id": str(ready_wi.document_id),
        },
    )

    ready_doc_context = AlexandriaPermissionContext.from_document(ready_doc)

    assert condition.apply(userinfo, create_context)
    assert condition.apply(userinfo, ready_doc_context)

    # But not if the context refers to the completed additional demand
    assert not condition.apply(userinfo, completed_doc_context)
