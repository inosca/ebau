from django.core.management import call_command

from camac.user.models import Group, Service, ServiceGroup


def test_migrate_gemeinderat_services(
    db,
    service_factory,
    service_group_factory,
    group_factory,
    user_factory,
    user_group_factory,
    activation_factory,
    circulation_factory,
    attachment_factory,
):

    service_extern = service_factory(name="Gemeinderat Altdorf externe Pendenz")
    service_intern = service_factory(name="Gemeinderat Altdorf interne Pendenz")
    service_group_extern = service_group_factory(
        name="Gemeinderat Altdorf externe Pendenzen"
    )
    service_group_intern = service_group_factory(
        name="Gemeinderat Altdorf interne Pendenzen"
    )
    group_extern = group_factory(name="Gemeinderat Altdorf externe Pendenz")
    group_intern = group_factory(name="Gemeinderat Altdorf interne Pendenz")
    user = user_factory()
    user_group = user_group_factory(group_id=group_intern.pk, user_id=user.pk)
    activation = activation_factory(
        circulation=circulation_factory(), service_id=service_intern.pk
    )
    attachment = attachment_factory(service_id=service_intern.pk)

    call_command("migrate_gemeinderaete")

    service_extern.refresh_from_db()
    service_group_extern.refresh_from_db()
    group_extern.refresh_from_db()
    user_group.refresh_from_db()
    activation.refresh_from_db()
    attachment.refresh_from_db()
    try:
        service_intern.refresh_from_db()
    except Service.DoesNotExist:
        service_intern = None
    try:
        service_group_intern.refresh_from_db()
    except ServiceGroup.DoesNotExist:
        service_group_intern = None
    try:
        group_intern.refresh_from_db()
    except Group.DoesNotExist:
        group_intern = None

    assert service_extern.name == "Gemeinderat Altdorf Pendenzen"
    assert service_group_extern.name == "Gemeinderat Altdorf Pendenzen"
    assert group_extern.name == "Gemeinderat Altdorf Pendenzen"
    assert user_group.group_id == group_extern.pk
    assert activation.service_id == service_extern.pk
    assert attachment.service_id == service_extern.pk
    assert not service_intern
    assert not service_group_intern
    assert not group_intern
    assert user_group.group.name == "Gemeinderat Altdorf Pendenzen"
