import os

import pytest
from django.core.management import call_command


@pytest.mark.parametrize("exec", [True, False])
def test_migrate_service(db, exec, service_factory, instance_service_factory):

    instance_service = instance_service_factory()
    service = instance_service.service
    target = service_factory()

    args = ["--source", instance_service.service.pk, "--target", target.pk]
    if exec:
        args.append("--exec")

    call_command("migrate_service", *args, stdout=open(os.devnull, "w"))
    instance_service.refresh_from_db()

    if exec:
        assert not instance_service.service == service
        assert instance_service.service == target
    else:
        assert instance_service.service == service
