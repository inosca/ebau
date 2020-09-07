from caluma.caluma_workflow.models import WorkItem
from django.core.management import call_command


def test_migrate_issues(db, issue, task_factory, case_factory):
    task_factory(slug="create-manual-workitems")
    case_factory(meta={"camac-instance-id": issue.instance.pk})
    call_command("migrate_issues")
    assert len(WorkItem.objects.all()) == 1
