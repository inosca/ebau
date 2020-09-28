import os

import pytest
from django.core.management import call_command


@pytest.mark.parametrize("exec", [True, False])
@pytest.mark.parametrize("disable", [True, False])
def test_migrate_service(
    db,
    exec,
    disable,
    service_factory,
    instance_service_factory,
    work_item_factory,
    user_factory,
    group_factory,
):

    instance_service = instance_service_factory()
    source_2 = service_factory()
    service = instance_service.service
    target = service_factory()
    work_item = work_item_factory(
        addressed_groups=[source_2.pk], assigned_users=[user_factory().username]
    )
    controlling_work_item = work_item_factory(controlling_groups=[source_2.pk])

    args = [
        "--source",
        ",".join([str(instance_service.service.pk), str(source_2.pk)]),
        "--target",
        target.pk,
    ]
    if exec:
        args.append("--exec")
    if disable:
        args.append("--disable")

    call_command("migrate_service", *args, stdout=open(os.devnull, "w"))
    instance_service.refresh_from_db()
    work_item.refresh_from_db()
    controlling_work_item.refresh_from_db()
    addressed_groups = [int(i) for i in work_item.addressed_groups]
    controlling_groups = [int(i) for i in controlling_work_item.controlling_groups]

    if exec:
        assert not instance_service.service == service
        assert instance_service.service == target
        assert addressed_groups == [target.pk]
        assert work_item.assigned_users == []
        assert controlling_groups == [target.pk]
    else:
        assert instance_service.service == service
        assert not work_item.addressed_groups == target.pk
        assert not work_item.assigned_users == []
        assert not controlling_work_item.controlling_groups == target.pk
