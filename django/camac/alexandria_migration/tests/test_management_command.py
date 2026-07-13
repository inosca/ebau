"""
Tests for the migrate_to_alexandria management command.

These tests focus on coverage for the command's handle method,
the reset subcommand, and edge cases like missing eligible instances.
"""

from contextlib import nullcontext as no_exception
from io import StringIO
from uuid import uuid4

import pytest
from alexandria.core.models import Document, File
from django.core.management import call_command

from camac.alexandria_migration.management.commands.migrate_to_alexandria import Command
from camac.alexandria_migration.models import MigrationLog, MigrationRun
from camac.instance.models import Instance, InstanceAlexandriaDocument


@pytest.mark.django_db(transaction=True)
def test_reset(
    instance,
    alexandria_document_factory,
    alexandria_file_factory,
    alexandria_mark_factory,
    # parametrization
    user_factory,
):
    """Test the reset subcommand executes and clears data."""
    stdout = StringIO()

    user = user_factory()

    # Create some data to be deleted using factories.
    # We use unique slugs to avoid conflicts between parametrizations, as the reset
    # command does not clear categories or marks.
    doc = alexandria_document_factory(
        created_by_user=user,
        created_by_group=user.get_default_group(),
    )
    # Some document factories might create an initial file.
    # We create another one to be sure we have at least one and to test parametrization.
    alexandria_file_factory(
        document=doc,
        created_by_user=user,
        created_by_group=user.get_default_group(),
    )
    mark = alexandria_mark_factory(pk=str(uuid4()))
    doc.marks.add(mark)

    run = MigrationRun.objects.create(command="create_documents")
    MigrationLog.objects.create(
        run=run,
        type=MigrationLog.Type.INSTANCE_DOCUMENTS_CREATED,
        instance_id=instance.pk,
    )
    InstanceAlexandriaDocument.objects.create(instance_id=instance.pk, document=doc)

    # Verify data exists before reset
    assert Document.objects.count() == 1
    assert File.objects.count() >= 1
    assert MigrationRun.objects.count() == 1

    call_command("migrate_to_alexandria", "reset", stdout=stdout)

    output = stdout.getvalue()
    assert "Resetting old alexandria data..." in output
    assert "Alexandria data successfully resetted" in output

    # Verify data is removed
    assert Document.objects.count() == 0
    assert File.objects.count() == 0
    assert MigrationRun.objects.count() == 0
    assert MigrationLog.objects.count() == 0
    assert InstanceAlexandriaDocument.objects.count() == 0


@pytest.mark.django_db
def test_no_eligible_instances():
    """
    Test subcommands when no eligible instances are found.

    We don't create any Instance models here because it's easier and faster.
    If no models exist, nothing will be found regardless of any filtering applied
    (e.g., --from, --to, --limit), which correctly triggers the "no eligible instances"
    warning and cleans up the MigrationRun object.
    """

    # Each subcommand should output an error message and delete the MigrationRun
    subcommands = [
        "create_documents",
        "duplicate_documents",
        "fix_communication_links",
        "annotate",
    ]

    for cmd in subcommands:
        # fixtures
        stdout = StringIO()
        call_command("migrate_to_alexandria", cmd, stdout=stdout)
        output = stdout.getvalue()
        assert "There are no eligible instances" in output
        # Verify MigrationRun is deleted (automatically via self.run.delete() in finally)
        assert MigrationRun.objects.count() == 0


@pytest.mark.django_db(transaction=True)
def test_filter_limit(instance_factory):
    """Test the --limit, --from, and --to arguments in filter_instances."""
    # fixtures
    instances = instance_factory.create_batch(5)
    # Ensure they are sorted by PK as the command does
    pks = sorted([i.pk for i in instances])

    cmd = Command()
    queryset = Instance.objects.all()

    # Case: Limit 3
    filtered = cmd.filter_instances(
        queryset,
        {"limit": 3},  # parametrization
    )
    assert list(filtered) == pks[:3]

    # Case: No limit
    filtered = cmd.filter_instances(
        queryset,
        {},  # parametrization
    )
    assert list(filtered) == pks

    # Case: --from
    filtered = cmd.filter_instances(
        queryset,
        {"from": pks[2]},  # parametrization
    )
    assert list(filtered) == pks[2:]

    # Case: --to
    filtered = cmd.filter_instances(
        queryset,
        {"to": pks[2]},  # parametrization
    )
    assert list(filtered) == pks[:3]

    # Case: --from and --to
    filtered = cmd.filter_instances(
        queryset,
        {"from": pks[1], "to": pks[3]},  # parametrization
    )
    assert list(filtered) == pks[1:4]


expect_exc = pytest.raises(Exception, match="Unexpected Error")


@pytest.mark.parametrize(
    ("event", "expect_exc", "resulting_status"),
    [
        (Exception("Unexpected Error"), expect_exc, MigrationRun.Status.FAILED),
        (KeyboardInterrupt(), no_exception(), MigrationRun.Status.CANCELED),
    ],
)
@pytest.mark.django_db(transaction=True)
def test_exception_handling(mocker, event, expect_exc, resulting_status):
    """Ensure exceptions cause the right migration run status."""
    # fixtures
    mock = mocker.patch(
        "camac.alexandria_migration.management.commands.migrate_to_alexandria.Command.create_documents",
        side_effect=event,
    )
    mock.__name__ = "create_documents"

    with expect_exc:
        call_command("migrate_to_alexandria", "create_documents")

    run = MigrationRun.objects.last()
    assert run.status == resulting_status
