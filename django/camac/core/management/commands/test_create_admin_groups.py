import os

import pytest
from django.core.management import call_command


@pytest.mark.parametrize(
    "service_name,service_group_name,admin_role_name,lead_role_name",
    [
        (
            "Swisscom AG",
            "Fachstelle",
            "Administration Fachstelle",
            "Leitung Fachstelle",
        ),
        (
            "Leitbehörde Bern",
            "Leitbehörde Gemeinde",
            "Administration Leitbehörde",
            "Leitung Leitbehörde",
        ),
        (
            "Baukontrolle Bern",
            "Baukontrolle",
            "Administration Baukontrolle",
            "Leitung Baukontrolle",
        ),
        (
            "Regierungsstatthalteramt Bern-Mittelland",
            "Leitbehörde RSTA",
            "Administration Leitbehörde",
            "Leitung Leitbehörde",
        ),
    ],
)
def test_create_admin_groups(
    db,
    service_name,
    service_group_name,
    admin_role_name,
    lead_role_name,
    service_factory,
    user_group_factory,
    role_factory,
    multilang,
):
    service = service_factory(
        trans__name=service_name, service_group__trans__name=service_group_name
    )
    admin_role = role_factory(trans__name=admin_role_name)
    lead_role = role_factory(trans__name=lead_role_name)
    user_group = user_group_factory(group__service=service, group__role=lead_role)

    call_command("create_admin_groups", "--exec", stdout=open(os.devnull, "w"))

    new_group = service.groups.get(role=admin_role)

    assert user_group.user.groups.filter(pk=new_group.pk).exists()
    assert new_group.get_name() == f"Administration {service_name}"
