import pytest
from caluma.caluma_workflow.models import WorkItem
from django.core.management import call_command


@pytest.mark.skip
@pytest.mark.django_db
def test_migrate_issues(issue, caluma_task_factory, caluma_case_factory):
    caluma_task_factory(slug="create-manual-workitems")
    caluma_case_factory(meta={"camac-instance-id": issue.instance.pk})
    call_command("migrate_issues")
    assert len(WorkItem.objects.all()) == 1
