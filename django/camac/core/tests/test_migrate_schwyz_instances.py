import os

from caluma.caluma_workflow.models import Case
from django.core.management import call_command
from django.db.models import Count

from camac.core.models import Circulation
from camac.instance.models import Instance


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
):
    settings.APPLICATION_DIR = settings.ROOT_DIR.path("kt_schwyz")
    settings.APPLICATION_NAME = "kt_schwyz"

    # load data including test data
    call_command(
        "loadconfig",
        caluma=True,
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

    call_command("migrate_schwyz_instances")

    assert (
        Case.objects.all().count()
        == Instance.objects.all().count()
        + Circulation.objects.annotate(activation_count=Count("activations"))
        .filter(activation_count__gt=0)
        .count()
        - 1  # one circulation which has finished
    )
