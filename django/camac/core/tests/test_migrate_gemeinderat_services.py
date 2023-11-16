from django.core.management import call_command

from camac.user.models import Group, Service


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

    services_extern = []
    services_intern = []
    service_groups_extern = []
    service_groups_intern = []
    groups_extern = []
    groups_intern = []
    for municipality in ["Altdorf", "Andermatt"]:
        services_extern.append(
            service_factory(name=f"Gemeinderat {municipality} externe Pendenz")
        )
        services_intern.append(
            service_factory(name=f"Gemeinderat {municipality} interne Pendenz")
        )
        service_groups_extern.append(
            service_group_factory(name=f"Gemeinderat {municipality} externe Pendenzen")
        )
        service_groups_intern.append(
            service_group_factory(name=f"Gemeinderat {municipality} interne Pendenzen")
        )
        groups_extern.append(
            group_factory(name=f"Gemeinderat {municipality} externe Pendenz")
        )
        groups_intern.append(
            group_factory(name=f"Gemeinderat {municipality} interne Pendenz")
        )

    # test user 1 is in two internal groups
    user_group = user_group_factory(group=groups_intern[0])
    user_group_factory(group=groups_intern[1], user=user_group.user)
    # test user 1 is in internal and external group
    user_group_2 = user_group_factory(group=groups_intern[0])
    user_group_factory(group=groups_extern[0], user=user_group_2.user)
    activation = activation_factory(
        circulation=circulation_factory(), service=services_intern[0]
    )
    attachment = attachment_factory(service_id=services_intern[0].pk)

    call_command("migrate_gemeinderaete")

    for obj in (
        services_extern
        + service_groups_extern
        + groups_extern
        + [user_group, activation, attachment]
    ):
        obj.refresh_from_db()

    for service in Service.objects.filter(pk__in=[s.pk for s in services_intern]):
        assert service.disabled
    for group in Group.objects.filter(pk__in=[g.pk for g in groups_intern]):
        assert group.disabled

    assert services_extern[0].name == "Gemeinderat Altdorf Pendenzen"
    assert services_extern[1].name == "Gemeinderat Andermatt Pendenzen"

    assert service_groups_extern[0].name == "Gemeinderat Altdorf Pendenzen"
    assert groups_extern[0].name == "Gemeinderat Altdorf Pendenzen"

    assert sorted(
        list(user_group.user.groups.values_list("group_id", flat=True))
    ) == sorted([g.pk for g in groups_extern])
    assert sorted(
        list(user_group_2.user.groups.values_list("group_id", flat=True))
    ) == sorted([groups_extern[0].pk])

    assert activation.service_id == services_extern[0].pk
    assert attachment.service_id == services_extern[0].pk
