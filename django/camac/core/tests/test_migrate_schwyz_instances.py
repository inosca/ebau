import os

from caluma.caluma_workflow.models import WorkItem
from django.core.management import call_command


def test_migrate_schwyz_instances(
    db,
    settings,
    issue,
    instance_factory,
    form_factory,
    workflow_factory,
    instance_state_factory,
    circulation_factory,
    circulation_state_factory,
    activation_factory,
    instance_responsibility_factory,
):
    settings.APPLICATION_DIR = settings.ROOT_DIR.path("kt_schwyz")
    settings.APPLICATION_NAME = "kt_schwyz"

    # load data including test data
    call_command(
        "camac_load",
        user="test-dummy@adfinis.com",
        stdout=open(os.devnull, "w"),
    )

    for state in [
        "new",
        "subm",
        "comm",
        "circ",
        "redac",
        "nfd",
        "done",
        "denied",
        "arch",
        "del",
        "rejected",
        "stopped",
    ]:
        instance_factory(instance_state=instance_state_factory(name=state))

    instance = instance_factory(instance_state=instance_state_factory(name="circ"))
    circ = circulation_factory(instance=instance)
    activation_factory(
        circulation=circ, circulation_state=circulation_state_factory(name="REVIEW")
    )
    activation_factory(
        circulation=circ, circulation_state=circulation_state_factory(name="OK")
    )
    instance_responsibility_factory(instance=instance)

    call_command("migrate_schwyz_instances")

    assert WorkItem.objects.all().count() == 102
