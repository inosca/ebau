import os

import pytest
from caluma.caluma_workflow.models import Case
from django.core.management import call_command

from camac.core.models import WorkflowEntry


@pytest.fixture
def workflow_entry_internal(db, ur_instance, workflow_entry_factory):
    workflow_entry_factory(
        instance=ur_instance,
        workflow_date="2022-01-14 12:49:34+00",
        group=1,
        workflow_item__pk=12,
    )


@pytest.fixture
def workflow_entry_portal(db, ur_instance, workflow_entry_factory):
    workflow_entry_factory(
        instance_id=ur_instance.pk,
        workflow_date="2022-01-15 12:49:34+00",
        group=1,
        workflow_item__pk=10,
    )


def test_migrate_internal_workflow_entries(workflow_entry_internal):
    call_command(
        "migrate_workflow_entries_ur",
        stdout=open(os.devnull, "w"),
    )

    case = Case.objects.first()
    assert case.meta["submit-date"] == "2022-01-14T12:49:34+0000"


def test_migrate_portal_workflow_entries(workflow_entry_portal, ur_instance):
    call_command(
        "migrate_workflow_entries_ur",
        stdout=open(os.devnull, "w"),
    )

    workflow_entry = WorkflowEntry.objects.filter(
        instance=ur_instance, workflow_item=12000000
    )

    case = Case.objects.first()
    assert case.meta["submit-date"] == "2022-01-15T12:49:34+0000"
    assert workflow_entry.first().workflow_item_id == 12000000
